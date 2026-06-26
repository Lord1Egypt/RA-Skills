#!/usr/bin/env python3
"""商机推荐查询 CLI 入口"""

COMMAND_NAME = "1688_opp_recommend"
COMMAND_DESC = "查询商机推荐列表"

import importlib
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_raw
from _output import make_output, print_output, print_error

_service = importlib.import_module("capabilities.1688_opp_recommend.service")
query_opportunities = _service.query_opportunities

def main():
    if not get_ak_raw():
        print_output(make_output(
            success=False,
            markdown="❌ AK 未配置，无法查询商机推荐。",
            data={"data": {}},
        ))
        return

    parser = argparse.ArgumentParser(description="商机推荐查询")
    parser.add_argument("--pageNo", "-p", type=int, default=1, help="页码，从1开始，默认1")
    parser.add_argument("--pageSize", "-s", type=int, default=20, help="每页条数，默认20")
    parser.add_argument("--keyword", "-k", type=str, default="", help="按商机标题搜索的关键词")
    parser.add_argument("--categoryId", "-c", type=str, default="", help="一级类目ID或中文名称")
    args = parser.parse_args()

    try:
        result = query_opportunities(args.pageNo, args.pageSize, args.keyword, args.categoryId)
        print_output(make_output(success=True, data=result))
    except Exception as exc:
        print_error(exc, {"data": {}})

if __name__ == "__main__":
    main()
