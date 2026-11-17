#!/usr/bin/env python3
"""商品状态检查 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_product_status.service import get_product_status

COMMAND_NAME = "alibaba.1688.get.product.status"
COMMAND_DESC = "商品状态检查"


def main():
    parser = argparse.ArgumentParser(description="商品状态检查")
    parser.add_argument("--query_date", required=True, help="诊断日期，格式 YYYY-MM-DD")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="可选，目标店铺的 loginId，用于多店铺查询")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置。\n\n请运行: `cli.py configure YOUR_AK`", {"data": {}})
        return

    try:
        login_id = getattr(args, 'NEWTON_SHOP_LOGIN_ID', None)
        result = get_product_status(args.query_date, login_id=login_id)
        print_output(result.get("success", False), result.get("msgInfo", ""), result.get("data", {}))
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
