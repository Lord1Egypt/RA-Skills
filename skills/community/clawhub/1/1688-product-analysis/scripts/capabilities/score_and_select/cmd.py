#!/usr/bin/env python3
"""商品评分与圈选 CLI 入口"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.score_and_select.service import score_and_select

COMMAND_NAME = "score_and_select"
COMMAND_DESC = "商品评分与圈选（需通过 --shop_total 传入店铺数据 JSON）"


def main():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--strategy", choices=["comprehensive", "sales", "all"],
                        default="comprehensive",
                        help="查询策略: comprehensive(综合排序,默认) / sales(按销售额) / all(全部商品)")
    parser.add_argument("--limit", type=int, default=100,
                        help="获取商品数量上限，默认100")
    parser.add_argument("--top_n", type=int, default=10,
                        help="输出排名前N的商品，默认10")
    parser.add_argument("--shop_total", required=True,
                        help="店铺维度数据 JSON 字符串（由 get_shop_data 命令获取）")
    args = parser.parse_args()

    try:
        shop_total = json.loads(args.shop_total)
    except json.JSONDecodeError as e:
        print_output(False, f"❌ shop_total JSON 解析错误: {e}", {"data": {}})
        return

    try:
        result = score_and_select(shop_total, args.strategy, args.limit, args.top_n)
        print_output(True, "商品评分与圈选成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
