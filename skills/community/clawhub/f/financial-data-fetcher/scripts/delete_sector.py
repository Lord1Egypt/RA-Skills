import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='删除自定义板块')
parser.add_argument('--block_code', type=str, required=True, help='自定义板块简称')

args = parser.parse_args()

data = tq.delete_sector(block_code=args.block_code)

print(data)