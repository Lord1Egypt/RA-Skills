#!/usr/bin/env python3
"""创建采购单命令 — CLI 入口"""

COMMAND_NAME = "create-order"
COMMAND_DESC = "创建采购单"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
import json
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.create_order.service import create_purchase_order


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法创建采购单。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="创建采购单")
    parser.add_argument("--role", required=True, choices=["BUYER", "SELLER"],
                        help="己方角色: BUYER(买家) 或 SELLER(卖家)")
    parser.add_argument("--counterparty", required=True, help="对方 1688 会员登录名")
    parser.add_argument("--items", required=True, help="采购清单 JSON 字符串，如: '[{\"productName\":\"商品\",\"quantity\":10,\"unitPrice\":\"1.00\"}]'")
    args = parser.parse_args()

    try:
        items = json.loads(args.items)
        if not isinstance(items, list):
            raise ValueError("items 必须是数组")
    except json.JSONDecodeError as e:
        print_output(False, f"采购清单 JSON 格式错误: {e}", {})
        return
    except ValueError as e:
        print_output(False, str(e), {})
        return

    try:
        result = create_purchase_order(
            draft_role=args.role,
            counterparty_name=args.counterparty,
            purchase_items=items
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
