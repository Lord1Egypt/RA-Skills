import argparse

from lib.tqcenter import tq

tq.initialize(__file__)

data = tq.get_user_sector()

print(data)