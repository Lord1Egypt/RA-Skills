#!/usr/bin/env python3
"""采购单失效命令 — CLI 入口"""

COMMAND_NAME = "invalidate-order"
COMMAND_DESC = "将采购单标记为失效"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.invalidate_order.service import invalidate_order


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法失效采购单。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="将采购单标记为失效")
    parser.add_argument("--draft-no", required=True, help="采购单合同号")
    args = parser.parse_args()

    try:
        result = invalidate_order(draft_no=args.draft_no)
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
