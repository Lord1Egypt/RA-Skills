import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取交易日列表')
parser.add_argument('--market', type=str, default='SH', help='市场代码')
parser.add_argument('--start_time', type=str, default='', help='起始日期')
parser.add_argument('--end_time', type=str, default='', help='结束日期')
parser.add_argument('--count', type=int, default=-1, help='返回最近的count个交易日')

args = parser.parse_args()

data = tq.get_trading_dates(
    market=args.market,
    start_time=args.start_time,
    end_time=args.end_time,
    count=args.count
)

print(data)