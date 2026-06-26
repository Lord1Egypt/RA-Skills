#!/usr/bin/env python
"""通过关键词搜索店铺商品 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.search_offer_by_keyword.service import search_offer_by_keyword

COMMAND_NAME = "search_offer_by_keyword"
COMMAND_DESC = "通过关键词搜索店铺商品"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法搜索商品。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--page", type=int, default=1, help="页码，默认 1")
    parser.add_argument("--page_size", type=int, default=10, help="每页数量，默认 10")
    args = parser.parse_args()

    try:
        result = search_offer_by_keyword(args.keyword, args.page, args.page_size)
        print_output(True, "商品搜索成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
