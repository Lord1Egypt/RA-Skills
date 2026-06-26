#!/usr/bin/env python3
"""客户地域分布查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.seller_customer_business_province.service import get_customer_business_province

COMMAND_NAME = "seller_customer_business_province"
COMMAND_DESC = "获取客户地域分布数据"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询客户地域分布。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="客户地域分布查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        choices=["RECENT_7", "RECENT_30"],
                        help="日期类型: RECENT_7(近7天,默认) / RECENT_30(近30天)")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码,默认1")
    parser.add_argument("--page_size", "-s", type=int, default=50, help="每页数量,默认50")
    parser.add_argument("--no_translate", action="store_true",
                        help="关闭地域名称翻译（默认开启）")
    args = parser.parse_args()

    try:
        result = get_customer_business_province(
            date_type=args.date_type,
            page=args.page,
            page_size=args.page_size,
            is_translate=not args.no_translate,
        )
        print_output(True, "客户地域分布查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
