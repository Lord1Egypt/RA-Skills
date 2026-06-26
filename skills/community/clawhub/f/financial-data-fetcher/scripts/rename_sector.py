import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='重命名自定义板块')
parser.add_argument('--block_code', type=str, required=True, help='自定义板块简称')
parser.add_argument('--block_name', type=str, required=True, help='重命名后的自定义板块名称')

args = parser.parse_args()

data = tq.rename_sector(
    block_code=args.block_code,
    block_name=args.block_name
)

print(data)