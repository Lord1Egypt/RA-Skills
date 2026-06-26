import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='刷新行情缓存')
parser.add_argument('--market', type=str, default='AG',
                    choices=['AG', 'HK', 'US', 'QH', 'QQ', 'NQ', 'ZZ', 'ZS'],
                    help='市场: AG=A股, HK=港股, US=美股, QH=国内期货, QQ=股票期权, NQ=新三板, ZZ=中证和国证指数, ZS=沪深京指数')
parser.add_argument('--force', type=bool, default=False, help='是否强制刷新')

args = parser.parse_args()

data = tq.refresh_cache(
    market=args.market,
    force=args.force
)

print(data)