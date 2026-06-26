#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from 12306_client import Railway12306Client

client = Railway12306Client(headless=False)
client.start()
try:
    if client.login():
        print("✅ 登录成功")
finally:
    client.close()
