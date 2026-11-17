#!/usr/bin/env python3
"""同款选品、竞品分析 V2 诊断的 CLI 入口。"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_error, print_output
from capabilities.get_same_offer_competition.service import get_same_offer_competition

COMMAND_NAME = "get_same_offer_competition"
COMMAND_DESC = "按商品ID选择同款标杆，并使用竞品分析 V2 做综合对标"


def _parse_args():
    parser = argparse.ArgumentParser(prog=f"cli.py {COMMAND_NAME}", description=COMMAND_DESC)
    parser.add_argument("--offer_id", required=True, help="1688 商品 ID")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="店铺登录 ID，指定查询的店铺")
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        result = get_same_offer_competition(args.offer_id, args.NEWTON_SHOP_LOGIN_ID)
        print_output(True, "竞品 V2 综合对标查询成功", result)
    except SystemExit:
        raise
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
