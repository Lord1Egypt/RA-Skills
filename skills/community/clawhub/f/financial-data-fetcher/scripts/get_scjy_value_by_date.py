import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取指定日期市场交易数据')
parser.add_argument('--field_list', type=str, nargs='+', required=True, help='字段筛选列表')
parser.add_argument('--year', type=int, default=0, help='指定年份')
parser.add_argument('--mmdd', type=int, default=0, help='指定月日')

args = parser.parse_args()

data = tq.get_scjy_value_by_date(
    field_list=args.field_list,
    year=args.year,
    mmdd=args.mmdd
)

print(data)