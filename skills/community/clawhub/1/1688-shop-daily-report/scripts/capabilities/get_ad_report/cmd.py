#!/usr/bin/env python3
"""获取广告投放日报数据 CLI 入口"""

import argparse
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_ad_report.service import get_ad_report

COMMAND_NAME = "get_ad_report"
COMMAND_DESC = "获取广告投放日报数据（消耗、曝光、点击、CTR、CPC、询盘、成交、ROI + 日环比 + Top计划）"


def _to_yyyymmdd(date_str: str) -> str:
    """YYYY-MM-DD → yyyyMMdd"""
    return date_str.replace("-", "")


def _calc_prev_date(date_str: str) -> str:
    """计算前一天日期 YYYY-MM-DD"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    prev = date_obj - timedelta(days=1)
    return prev.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--query_date", required=True, help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="目标店铺的 loginId（可选）")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询广告数据。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    prev_date = _calc_prev_date(args.query_date)

    try:
        result = get_ad_report(
            query_date=_to_yyyymmdd(args.query_date),
            prev_date=_to_yyyymmdd(prev_date),
            login_id=args.NEWTON_SHOP_LOGIN_ID,
        )
        print_output(True, "广告投放数据查询成功", result)
    except Exception as exc:
        print_error(exc, {})


if __name__ == "__main__":
    main()
