import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

parser = argparse.ArgumentParser(description='获取订阅列表')
args = parser.parse_args()

data = tq.get_subscribe_hq_stock_list()

print(data)