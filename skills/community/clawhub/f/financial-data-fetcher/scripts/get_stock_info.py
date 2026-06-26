import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取证券基本信息')
parser.add_argument('--stock_code', type=str, required=True, help='证券代码')
parser.add_argument('--field_list', type=str, nargs='*', required=True, help='字段筛选列表，不能为空')

args = parser.parse_args()

data = tq.get_stock_info(
    stock_code=args.stock_code,
    field_list=args.field_list
)

print(data)