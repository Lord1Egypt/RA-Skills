#!/usr/bin/env python3
"""账号查询命令 — CLI 入口"""

COMMAND_NAME = "account"
COMMAND_DESC = "查询账号信息"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.account.service import query_account


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询账号信息。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    try:
        result = query_account()
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
