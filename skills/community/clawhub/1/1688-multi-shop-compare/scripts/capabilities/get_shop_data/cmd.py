#!/usr/bin/env python3
"""单店铺全量经营数据采集 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.get_shop_data.service import get_shop_data

COMMAND_NAME = "get_shop_data"
COMMAND_DESC = "获取单个店铺的全量经营数据（需传入该店铺的 AK）"

def main():
    parser = argparse.ArgumentParser(description="获取单个店铺的全量经营数据（商家身份由传入的 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--ak", "-a", required=True,
                        help="目标店铺的原始 AK（从 get_bindlist 获取）")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        choices=["RECENT_7", "RECENT_30"],
                        help="日期类型: RECENT_7(近7天,默认) / RECENT_30(近30天)")
    args = parser.parse_args()

    try:
        result = get_shop_data(args.ak, args.date_type)
        print_output(True, f"店铺全量经营数据采集成功（{args.date_type}）", {
            "data": result,
            "date_type": args.date_type,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
