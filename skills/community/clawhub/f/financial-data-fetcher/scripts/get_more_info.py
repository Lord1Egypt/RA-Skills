import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取股票更多信息')
parser.add_argument('--stock_code', type=str, required=True, help='股票代码')
parser.add_argument('--field_list', type=str, nargs='*', default=[], help='字段筛选列表')

args = parser.parse_args()

data = tq.get_more_info(
    stock_code=args.stock_code,
    field_list=args.field_list
)

print(data)