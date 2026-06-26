import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='创建自定义板块')
parser.add_argument('--block_code', type=str, required=True, help='自定义板块简称')
parser.add_argument('--block_name', type=str, required=True, help='自定义板块名称')

args = parser.parse_args()

data = tq.create_sector(
    block_code=args.block_code,
    block_name=args.block_name
)

print(data)