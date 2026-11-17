#!/usr/bin/env python3
"""
这是用于根据用户Markdown内容获取一个PPT下载链接的脚本。
"""

import os
import requests
import argparse

def generate_by_content(access_token:str, tpl_id:str, content:str):
    url = "https://ppt-api.7niuai.com/openclaw/generate_ppt_by_content"

    headers = {
        "token": access_token,
        "Content-Type": "application/json"
    }

    param = {
        "tpl_id": tpl_id,
        "markdown_content": content
    }

    response = requests.post(url, json=param, headers=headers)
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create task')
    parser.add_argument('--tpl_id', type=str, default='', help='tpl_id')
    parser.add_argument('--markdown_content', type=str, default='', help='markdown_content')
    args = parser.parse_args()

    access_token = os.getenv("AIPPT_ACCESS_TOKEN")
    if not access_token:
        print("Error: AIPPT_ACCESS_TOKEN must be set in environment.")
        exit(1)

    generate_by_content(access_token=access_token, tpl_id=args.tpl_id, content=args.markdown_content)