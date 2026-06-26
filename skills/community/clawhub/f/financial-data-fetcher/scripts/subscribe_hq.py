import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='订阅行情')
parser.add_argument('--stock_list', type=str, nargs='+', required=True, help='订阅的证券代码')
# callback参数需要传入Python函数，这里暂时不处理

args = parser.parse_args()

# 注意: subscribe_hq需要传入回调函数，这里演示仅获取返回结果
data = tq.subscribe_hq(stock_list=args.stock_list)

print(data)