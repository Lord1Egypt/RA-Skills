import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取股本数据')
parser.add_argument('--stock_code', type=str, required=True, help='股票代码')
parser.add_argument('--date_list', type=str, nargs='+', required=True, help='日期数组')
parser.add_argument('--count', type=int, required=True, help='日期有效个数')

args = parser.parse_args()

data = tq.get_gb_info(
    stock_code=args.stock_code,
    date_list=args.date_list,
    count=args.count
)

print(data)