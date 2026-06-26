#!/usr/bin/env python3
"""商家异常商品列表查询 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.get_abnormal_offers.service import get_abnormal_offers

COMMAND_NAME = "get_abnormal_offers"
COMMAND_DESC = "查询商家需重点关注的异常商品列表（支付下跌、访客下跌等）"


def _parse_args():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument(
        "--date_type",
        default="RECENT_7",
        help="日期类型：RECENT_7（近7天，默认）、RECENT_30（近30天）",
    )
    parser.add_argument(
        "--device",
        default="ALL",
        help="设备筛选：ALL（全部，默认）、PC、APP",
    )
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        items = get_abnormal_offers(date_type=args.date_type, device=args.device)
        print_output(True, "异常商品列表查询成功", {"count": len(items), "items": items})
    except SystemExit:
        raise
    except Exception as e:
        print_error(e, {"count": 0, "items": []})


if __name__ == "__main__":
    main()
