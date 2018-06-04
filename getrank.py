import sys
from pymongo import MongoClient
import pandas as pd

def get_rank(user_id):
    db = MongoClient().shiyanlou
    contests = db.contests
    data = pd.DataFrame(list(contests.find()))

    if user_id in list(data['user_id']):
        group_data = data.groupby(['user_id'])['score', 'submit_time'].sum()
        rank_data = group_data.sort_values(['submit_time']).sort_values(['score'], ascending=False)
        reindex_data = rank_data.reset_index()
        reindex_data['rank'] = reindex_data.index + 1
        user_data = reindex_data[user_id == reindex_data['user_id']]
        rank = int(user_data['rank'].values)
        score = int(user_data['score'].values)
        submit_time = int(user_data['submit_time'].values)
    else:
        print('NOTFOUND')
        exit()

    return rank, score, submit_time


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Parameter Error')
        sys.exit(1)

    user_id = sys.argv[1]

    userdata = get_rank(int(user_id))
    print(userdata)
