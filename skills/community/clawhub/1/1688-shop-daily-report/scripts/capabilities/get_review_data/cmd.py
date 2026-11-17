#!/usr/bin/env python3
"""获取商品评价数据 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_review_data.service import get_review_data

COMMAND_NAME = "get_review_data"
COMMAND_DESC = "获取商品评价数据（好评/中评/差评分类统计 + 好差评原因收集）"


def _to_yyyymmdd(date_str: str) -> str:
    """YYYY-MM-DD → yyyyMMdd"""
    return date_str.replace("-", "")


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--query_date", required=True, help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="目标店铺的 loginId（可选）")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询评价数据。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    date_yyyymmdd = _to_yyyymmdd(args.query_date)

    try:
        result = get_review_data(
            start_date=date_yyyymmdd,
            end_date=date_yyyymmdd,
            login_id=args.NEWTON_SHOP_LOGIN_ID,
        )
        print_output(True, "商品评价数据查询成功", result)
    except Exception as exc:
        print_error(exc, {})


if __name__ == "__main__":
    main()
