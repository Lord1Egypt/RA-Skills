#!/usr/bin/env python3
"""申请退款命令 — CLI 入口"""

COMMAND_NAME = "refund-apply"
COMMAND_DESC = "申请退款"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.refund_apply.service import apply_refund


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法申请退款。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="申请退款")
    parser.add_argument("--draft-no", required=True, help="采购单合同号")
    args = parser.parse_args()

    try:
        result = apply_refund(draft_no=args.draft_no)
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
