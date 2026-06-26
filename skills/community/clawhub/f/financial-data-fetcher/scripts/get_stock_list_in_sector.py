import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取板块成份股')
parser.add_argument('--block_code', type=str, required=True, help='板块代码')
parser.add_argument('--block_type', type=int, default=0, help='板块类型: 0=板块指数代码或名称, 1=自定义板块简称')
parser.add_argument('--list_type', type=int, default=0, choices=[0, 1], help='返回数据类型: 0=只返回代码, 1=返回代码和名称')

args = parser.parse_args()

data = tq.get_stock_list_in_sector(
    block_code=args.block_code,
    block_type=args.block_type,
    list_type=args.list_type
)

print(data)