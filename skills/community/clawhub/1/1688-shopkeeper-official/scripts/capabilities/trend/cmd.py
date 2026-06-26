#!/usr/bin/env python3
"""趋势洞察命令 — CLI 入口"""

COMMAND_NAME = "trend"
COMMAND_DESC = "趋势洞察"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.trend.service import fetch_trend


def main():
    parser = argparse.ArgumentParser(description="趋势洞察")
    parser.add_argument("--query", "-q", required=True, help="关键词（类目/品类/品牌，尽量宽泛）")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询趋势。\n\n运行: `cli.py configure YOUR_AK`",
                     {"query_used": args.query, "raw": {}})
        return

    try:
        result = fetch_trend(query=args.query)
        print_output(True, result["markdown"], {
            "query_used": result.get("query_used"),
            "raw": result.get("data"),
        })
    except Exception as e:
        print_error(e, {"query_used": args.query, "raw": {}})


if __name__ == "__main__":
    main()
