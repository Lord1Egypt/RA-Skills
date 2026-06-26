import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='下载特定数据文件')
parser.add_argument('--stock_code', type=str, required=True, help='证券代码')
parser.add_argument('--down_time', type=str, default='', help='指定日期')
parser.add_argument('--down_type', type=int, required=True, choices=[1, 2, 3, 4], help='1=10大股东数据, 2=ETF申赎清单, 3=最近舆情信息, 4=股票综合信息')

args = parser.parse_args()

data = tq.download_file(
    stock_code=args.stock_code,
    down_time=args.down_time,
    down_type=args.down_type
)

print(data)