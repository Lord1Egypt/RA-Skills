import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

# 解析命令行参数
parser = argparse.ArgumentParser(description='获取K线行情数据')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='证券代码列表，如: 688318.SH')
parser.add_argument('--period', type=str, default='1d',
                    choices=['1m', '5m', '15m', '30m', '1h', '1d', '1w', '1mon', '1q', '1y', 'tick'],
                    help='周期')
parser.add_argument('--start_time', type=str, default='', help='起始时间，格式如: 20251220')
parser.add_argument('--end_time', type=str, default='', help='结束时间，格式如: 20251220')
parser.add_argument('--count', type=int, default=-1, help='返回数据个数')
parser.add_argument('--dividend_type', type=str, default='none',
                    choices=['none', 'front', 'back'],
                    help='复权类型: none(不复权), front(前复权), back(后复权)')
parser.add_argument('--fill_data', type=bool, default=True, help='是否向后填充空缺数据')
parser.add_argument('--field_list', type=str, nargs='*', default=[], help='字段筛选列表')

args = parser.parse_args()

# 获取K线行情数据
data = tq.get_market_data(
    field_list=args.field_list,
    stock_list=args.stock_list,
    start_time=args.start_time,
    end_time=args.end_time,
    count=args.count,
    dividend_type=args.dividend_type,
    period=args.period,
    fill_data=args.fill_data
)
# 直接打印返回的数据到控制台
print(data)
