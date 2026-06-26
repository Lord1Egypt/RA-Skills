#!/usr/bin/env python3
"""采购单列表查询命令 — CLI 入口"""

COMMAND_NAME = "contract-list"
COMMAND_DESC = "查询采购单列表"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.contract_list.service import query_contract_list


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询采购单列表。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="查询采购单列表")
    parser.add_argument("--role", required=True, choices=["BUYER", "SELLER"],
                        help="角色: BUYER(买家) 或 SELLER(卖家)")
    parser.add_argument("--page", type=int, default=1, help="页码，默认 1")
    parser.add_argument("--size", type=int, default=10, help="每页条数，默认 10")
    args = parser.parse_args()

    try:
        result = query_contract_list(
            contract_role=args.role,
            page_index=args.page,
            page_size=args.size
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
