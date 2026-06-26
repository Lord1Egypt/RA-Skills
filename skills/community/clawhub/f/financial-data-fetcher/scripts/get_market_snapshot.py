import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取快照数据')
parser.add_argument('--stock_code', type=str, required=True, help='证券代码')
parser.add_argument('--field_list', type=str, nargs='*', default=[], help='字段筛选列表')

args = parser.parse_args()

data = tq.get_market_snapshot(
    stock_code=args.stock_code,
    field_list=args.field_list
)

print(data)