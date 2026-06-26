import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='取消订阅更新')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')

args = parser.parse_args()

data = tq.unsubscribe_hq(stock_list=args.stock_list)

print(data)