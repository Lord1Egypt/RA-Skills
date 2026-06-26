#!/usr/bin/env python3
"""确认收货命令 — CLI 入口"""

COMMAND_NAME = "confirm-receipt"
COMMAND_DESC = "买家确认收货"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.confirm_receipt.service import confirm_receipt


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法确认收货。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="买家确认收货")
    parser.add_argument("--draft-no", required=True, help="采购单号")
    args = parser.parse_args()

    try:
        result = confirm_receipt(draft_no=args.draft_no)
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
