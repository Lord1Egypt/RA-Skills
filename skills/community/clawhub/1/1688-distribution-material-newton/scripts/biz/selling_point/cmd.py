#!/usr/bin/env python3
"""卖点生成 — CLI 入口"""

COMMAND_NAME = "selling_point"
COMMAND_DESC = "卖点生成"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from biz.selling_point.service import generate_selling_point


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法生成卖点。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="卖点生成")
    parser.add_argument("--offer_id", "-o", required=True, help="1688 商品 ID")
    parser.add_argument("--prompt", "-p", required=True, help="用户提文（原封不动传入）")
    args = parser.parse_args()

    try:
        result = generate_selling_point(args.offer_id, args.prompt)
        points = result.get("points_result", "")

        md = f"卖点生成完成！\n\n**商品卖点：**\n{points}"
        print_output(True, md, {
            "points_result": points,
        })
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
