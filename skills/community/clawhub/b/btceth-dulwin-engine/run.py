#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DualWin Alpha Engine Skill
"""

import requests
import time

# 配置
API_URL = "http://43.156.132.183:30080/api/analysis"

def get_data():
    t = int(time.time())
    resp = requests.get(f"{API_URL}?t={t}", timeout=30)
    return resp.json()

def main():
    data = get_data()
    
    if data.get('success'):
        print(data.get('output', ''))
    else:
        print("Error:", data.get('error', 'Unknown error'))

if __name__ == "__main__":
    main()
