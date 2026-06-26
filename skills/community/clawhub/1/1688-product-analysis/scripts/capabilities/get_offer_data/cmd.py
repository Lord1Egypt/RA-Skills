#!/usr/bin/env python3
"""商品综合数据查询 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.get_offer_data.service import get_offer_data

COMMAND_NAME = "get_offer_data"
COMMAND_DESC = "获取商品综合数据（基础/表现/货盘/搜推问题/购买因素/异常/广告/热搜词/热品）"


def _parse_args():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--offer_id", required=True, help="1688 商品 ID")
    parser.add_argument(
        "--modules",
        default="all",
        help=(
            "要获取的数据模块，逗号分隔。可选值: profile,performance,huopan,"
            "search_issues,purchase_factors,sycm_anomaly,ad_analysis,hotwords,hot_items,all"
        ),
    )
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        result = get_offer_data(offer_id=args.offer_id, modules=args.modules)
        print_output(True, "商品综合数据查询成功", {"data": result})
    except SystemExit:
        # argparse 自身的 -h / 参数错误已经写过 stderr，这里直接抛回
        raise
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
