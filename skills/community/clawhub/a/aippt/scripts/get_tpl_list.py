#!/usr/bin/env python3
"""
这是一个获取PPT模板列表的脚本。
"""

import requests
import argparse

def get_tpl_list(page:int, num:int):
    url = "https://ppt-api.7niuai.com/ppt/tpl/list"

    headers = {
        "Content-Type": "application/json"
    }

    param = {
        "page": page,
        "num": num
    }

    response = requests.post(url, json=param, headers=headers)
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create task')
    parser.add_argument('--page', type=int, default=1, help='page')
    parser.add_argument('--num', type=int, default=10, help='num')
    args = parser.parse_args()  
    get_tpl_list(page=args.page, num=args.num)
