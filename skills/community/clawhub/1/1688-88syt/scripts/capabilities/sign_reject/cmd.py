#!/usr/bin/env python3
"""拒绝签约命令 — CLI 入口"""

COMMAND_NAME = "sign-reject"
COMMAND_DESC = "拒绝签署采购单"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.sign_reject.service import sign_reject


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法拒绝签约。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    parser = argparse.ArgumentParser(description="拒绝签署采购单")
    parser.add_argument("--draft-no", required=True, help="采购单合同号")
    args = parser.parse_args()

    try:
        result = sign_reject(draft_no=args.draft_no)
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
