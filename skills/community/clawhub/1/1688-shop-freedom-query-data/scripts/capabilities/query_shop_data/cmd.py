#!/usr/bin/env python3
"""商家数据查询 CLI 入口"""

import os
import sys
import json
import argparse
from urllib.parse import unquote

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.query_shop_data.service import query_shop_data

COMMAND_NAME = "query_shop_data"
COMMAND_DESC = "查询商家经营数据（需提供 dataSource、apiPath、params）"


def _url_decode_params(obj):
    """递归对 dict/list 中所有字符串值做 URL decode"""
    if isinstance(obj, str):
        return unquote(obj)
    if isinstance(obj, dict):
        return {k: _url_decode_params(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_url_decode_params(item) for item in obj]
    return obj


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置。\n\n请运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="商家数据查询")
    parser.add_argument("--data_source", "-s", required=True,
                        help="数据源标识，如 SYCM、ITEM")
    parser.add_argument("--api_path", "-a", required=True,
                        help="接口路径，如 portal/core/overview")
    parser.add_argument("--params", "-p", required=True,
                        help='业务参数 JSON，如 \'{"dataType":"RECENT_7","device":"ALL"}\'')
    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError as e:
        print_output(False, f"❌ params JSON 解析失败：{e}", {"data": {}})
        return

    # 对所有字符串类型的入参强制 URL decode
    data_source = unquote(args.data_source)
    api_path = unquote(args.api_path)
    params = _url_decode_params(params)

    try:
        result = query_shop_data(data_source, api_path, params)
        print_output(True, "数据查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
