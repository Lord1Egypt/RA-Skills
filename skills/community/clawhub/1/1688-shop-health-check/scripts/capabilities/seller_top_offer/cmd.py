#!/usr/bin/env python3
"""优秀商品榜单查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.seller_top_offer.service import get_top_offer, DEFAULT_INDEX_CODE

COMMAND_NAME = "seller_top_offer"
COMMAND_DESC = "获取优秀商品榜单（成交/流量/拉新/复购）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询优秀商品榜单。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="优秀商品榜单查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.add_argument("--order_by", "-o", default="payAmt",
                        choices=["payAmt", "uv", "payNewByrCnt", "itemMultiByrCnt"],
                        help="排序字段: payAmt(成交,默认) / uv(流量) / payNewByrCnt(拉新) / itemMultiByrCnt(复购)")
    parser.add_argument("--range_type", "-r", default="RECENT_7",
                        choices=["RECENT_7", "RECENT_30"],
                        help="时间范围: RECENT_7(近7天,默认) / RECENT_30(近30天)")
    parser.add_argument("--device", "-v", default="ALL",
                        choices=["ALL", "PC", "WIRELESS"],
                        help="设备类型: ALL(全部,默认) / PC / WIRELESS(无线)")
    parser.add_argument("--order", default="desc", choices=["desc", "asc"],
                        help="排序方向: desc(降序,默认) / asc(升序)")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码,默认1")
    parser.add_argument("--page_size", "-s", type=int, default=50, help="每页数量,默认50")
    parser.add_argument("--index_code", default=DEFAULT_INDEX_CODE,
                        help="返回指标列（逗号分隔）")
    args = parser.parse_args()

    try:
        result = get_top_offer(
            order_by=args.order_by,
            range_type=args.range_type,
            device=args.device,
            order=args.order,
            page=args.page,
            page_size=args.page_size,
            index_code=args.index_code,
        )
        print_output(True, f"优秀商品榜单（{args.order_by}）查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
