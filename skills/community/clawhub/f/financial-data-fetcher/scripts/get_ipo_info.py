import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取新股申购信息')
parser.add_argument('--ipo_type', type=int, default=0, choices=[0, 1, 2], help='0=新股申购信息, 1=新发债信息, 2=新股和新发债信息')
parser.add_argument('--ipo_date', type=int, default=0, choices=[0, 1], help='0=只获取今天信息, 1=获取今天及以后信息')

args = parser.parse_args()

data = tq.get_ipo_info(
    ipo_type=args.ipo_type,
    ipo_date=args.ipo_date
)

print(data)