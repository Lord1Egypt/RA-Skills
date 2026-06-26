import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取板块交易数据')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')
parser.add_argument('--field_list', type=str, nargs='+', required=True, help='字段筛选列表')
parser.add_argument('--start_time', type=str, default='', help='起始时间')
parser.add_argument('--end_time', type=str, default='', help='结束时间')

args = parser.parse_args()

data = tq.get_bkjy_value(
    stock_list=args.stock_list,
    field_list=args.field_list,
    start_time=args.start_time,
    end_time=args.end_time
)

print(data)