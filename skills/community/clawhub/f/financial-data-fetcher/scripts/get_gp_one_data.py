import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取股票的单个财务数据')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')
parser.add_argument('--field_list', type=str, nargs='+', required=True, help='字段筛选列表')

args = parser.parse_args()

data = tq.get_gp_one_data(
    stock_list=args.stock_list,
    field_list=args.field_list
)

print(data)