#!/usr/bin/env python3
"""采购单汇总查询命令 — CLI 入口"""

COMMAND_NAME = "contract-summary"
COMMAND_DESC = "查询采购单汇总信息"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.contract_summary.service import query_contract_summary


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询采购单汇总。\n\n运行: `cli.py configure YOUR_AK`",
                     {})
        return

    try:
        result = query_contract_summary()
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
