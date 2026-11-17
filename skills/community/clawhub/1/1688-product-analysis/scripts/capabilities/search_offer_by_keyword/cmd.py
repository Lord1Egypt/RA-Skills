#!/usr/bin/env python3
"""通过关键词搜索店铺商品 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.search_offer_by_keyword.service import search_offer_by_keyword

COMMAND_NAME = "search_offer_by_keyword"
COMMAND_DESC = "通过关键词搜索店铺商品"


def main():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--keyword", default="", help="搜索关键词（可选，不传则返回店铺商品列表）")
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
