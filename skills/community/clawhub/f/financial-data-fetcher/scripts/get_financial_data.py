import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取专业财务数据')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表')
parser.add_argument('--field_list', type=str, nargs='+', required=True, help='字段筛选列表')
parser.add_argument('--start_time', type=str, default='', help='起始时间，格式: 20250101')
parser.add_argument('--end_time', type=str, default='', help='结束时间，格式: 20250101')
parser.add_argument('--report_type', type=str, default='announce_time',
                    choices=['announce_time', 'tag_time'],
                    help='按截止日期还是公告日期筛选')

args = parser.parse_args()

data = tq.get_financial_data(
    stock_list=args.stock_list,
    field_list=args.field_list,
    start_time=args.start_time,
    end_time=args.end_time,
    report_type=args.report_type
)

print(data)
