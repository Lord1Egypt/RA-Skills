import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='添加自定义板块成份股')
parser.add_argument('--block_code', type=str, required=True, help='自定义板块简称')
parser.add_argument('--stocks', type=str, nargs='+', required=True, help='添加的自选股列表')
parser.add_argument('--show', type=bool, default=False, help='客户端是否切换至对应板块界面')

args = parser.parse_args()

data = tq.send_user_block(
    block_code=args.block_code,
    stocks=args.stocks,
    show=args.show
)

print(data)