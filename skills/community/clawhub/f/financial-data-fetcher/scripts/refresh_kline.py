import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='刷新历史K线缓存')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')
parser.add_argument('--period', type=str, required=True,
                    choices=['1d', '1m', '5m'],
                    help='周期: 1d=日线, 1m=一分钟线, 5m=五分钟线')

args = parser.parse_args()

data = tq.refresh_kline(
    stock_list=args.stock_list,
    period=args.period
)

print(data)