#!/usr/bin/env python3
"""标题优化 — CLI 入口"""

COMMAND_NAME = "title_optimize"
COMMAND_DESC = "标题优化"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from biz.title_optimize.service import optimize_title


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法进行标题优化。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="标题优化")
    parser.add_argument("--offer_id", "-o", required=True, help="1688 商品 ID")
    parser.add_argument("--prompt", "-p", required=True, help="用户提文（原封不动传入）")
    args = parser.parse_args()

    try:
        result = optimize_title(args.offer_id, args.prompt)
        title = result.get("title_result", "")

        md = f"标题优化完成！\n\n**优化后标题：**\n{title}"
        print_output(True, md, {
            "title_result": title,
        })
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
