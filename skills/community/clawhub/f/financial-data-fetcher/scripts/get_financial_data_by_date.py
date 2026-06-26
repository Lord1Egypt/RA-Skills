import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取指定日期专业财务数据')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')
parser.add_argument('--field_list', type=str, nargs='+', required=True, help='字段筛选列表')
parser.add_argument('--year', type=int, default=0, help='指定年份')
parser.add_argument('--mmdd', type=int, default=0, help='指定月日')

args = parser.parse_args()

data = tq.get_financial_data_by_date(
    stock_list=args.stock_list,
    field_list=args.field_list,
    year=args.year,
    mmdd=args.mmdd
)

print(data)