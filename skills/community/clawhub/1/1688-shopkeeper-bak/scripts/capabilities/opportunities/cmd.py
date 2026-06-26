#!/usr/bin/env python3
"""商机热榜命令 — CLI 入口"""

COMMAND_NAME = "opportunities"
COMMAND_DESC = "商机热榜"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.opportunities.service import fetch_opportunities


def main():
    parser = argparse.ArgumentParser(description="商机热榜")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询商机。\n\n运行: `cli.py configure YOUR_AK`",
                     {"platforms": [], "raw": {}})
        return

    try:
        result = fetch_opportunities()
        print_output(True, result["markdown"], result["data"])
    except Exception as e:
        print_error(e, {"platforms": [], "raw": {}})


if __name__ == "__main__":
    main()
