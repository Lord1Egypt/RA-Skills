#!/usr/bin/env python3
"""店铺交易核心指标查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.seller_trade_code_index.service import get_trade_code_index

COMMAND_NAME = "seller_trade_code_index"
COMMAND_DESC = "获取店铺交易核心指标（总盘健康判断核心接口）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询店铺交易核心指标。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="店铺交易核心指标查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        choices=["RECENT_7", "RECENT_30"],
                        help="日期类型: RECENT_7(近7天,默认) / RECENT_30(近30天)")
    parser.add_argument("--device", "-v", default="ALL",
                        choices=["ALL", "PC", "WIRELESS"],
                        help="设备类型: ALL(全部,默认) / PC / WIRELESS(无线)")
    args = parser.parse_args()

    try:
        result = get_trade_code_index(args.date_type, args.device)
        print_output(True, "店铺交易核心指标查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
