import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取分红配送数据')
parser.add_argument('--stock_code', type=str, required=True, help='证券代码')
parser.add_argument('--start_time', type=str, default='', help='起始时间')
parser.add_argument('--end_time', type=str, default='', help='结束时间')

args = parser.parse_args()

data = tq.get_divid_factors(
    stock_code=args.stock_code,
    start_time=args.start_time,
    end_time=args.end_time
)

print(data)