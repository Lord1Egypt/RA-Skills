#!/usr/bin/env python3
"""头部老客户明细查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.seller_customer_detail.service import get_top_old_customers

COMMAND_NAME = "seller_customer_detail"
COMMAND_DESC = "获取头部老客户明细（高价值客户稳定性分析）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询头部老客户。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="头部老客户明细查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--date_type", "-d", default="RECENT_7",
                        choices=["RECENT_7", "RECENT_30"],
                        help="日期类型: RECENT_7(近7天,默认) / RECENT_30(近30天)")
    parser.add_argument("--buyer_type", "-b", default="头部老客户",
                        help="买家类型，默认: 头部老客户")
    parser.add_argument("--order_by", "-o", default="payAmount",
                        choices=["payAmount", "payAmtAll", "lastPayDate", "payParentOrderNum"],
                        help="排序字段，默认: payAmount(本周期支付金额)")
    parser.add_argument("--order", default="desc", choices=["desc", "asc"],
                        help="排序方向: desc(降序,默认) / asc(升序)")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码,默认1")
    parser.add_argument("--page_size", "-s", type=int, default=50, help="每页数量,默认50")
    args = parser.parse_args()

    try:
        result = get_top_old_customers(
            date_type=args.date_type,
            buyer_type=args.buyer_type,
            order_by=args.order_by,
            order=args.order,
            page=args.page,
            page_size=args.page_size,
        )
        print_output(True, "头部老客户查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
