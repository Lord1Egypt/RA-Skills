import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取跟踪指数的ETF信息')
parser.add_argument('--zs_code', type=str, required=True, help='指数代码')

args = parser.parse_args()

data = tq.get_trackzs_etf_info(zs_code=args.zs_code)

print(data)