#!/usr/bin/env python3
"""逐日流量趋势数据查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_traffic_trend.service import get_traffic_trend

COMMAND_NAME = "get_traffic_trend"
COMMAND_DESC = "获取逐日流量趋势数据（近7天/30天）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询流量趋势数据。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="逐日流量趋势数据查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--query_date", "-q", required=True,
                        help="查询日期（昨日日期，格式：YYYY-MM-DD）")
    parser.add_argument("--days", "-d", type=int, default=7,
                        choices=[7, 30],
                        help="天数: 7(近7天,默认) / 30(近30天)")
    args = parser.parse_args()

    try:
        result = get_traffic_trend(args.query_date, args.days)
        print_output(True, f"逐日流量趋势查询成功（近{args.days}天）", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
