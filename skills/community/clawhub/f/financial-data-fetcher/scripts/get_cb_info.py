import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取可转债基础信息')
parser.add_argument('--stock_code', type=str, required=True, help='可转债代码')
parser.add_argument('--field_list', type=str, nargs='*', default=[], help='字段筛选列表')

args = parser.parse_args()

data = tq.get_cb_info(
    stock_code=args.stock_code,
    field_list=args.field_list
)

print(data)