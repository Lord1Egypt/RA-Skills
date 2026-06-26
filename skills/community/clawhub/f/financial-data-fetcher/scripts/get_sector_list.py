import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取A股板块代码列表')
parser.add_argument('--list_type', type=int, default=0, choices=[0, 1], help='返回数据类型: 0=只返回代码, 1=返回代码和名称')

args = parser.parse_args()

data = tq.get_sector_list(list_type=args.list_type)

print(data)