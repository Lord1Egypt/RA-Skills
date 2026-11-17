#!/usr/bin/env python3
"""店铺健康检查聚合工具 CLI 入口

单命令 + --code：order_risk（订单履约）/ shop_punish（合规扣分）/ feedback（买家评价）。
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.shop_health_check.service import get_shop_health_check, VALID_CODES

COMMAND_NAME = "shop_health_check"
COMMAND_DESC = "店铺健康检查（订单履约/合规扣分/买家评价）"


def main():
    parser = argparse.ArgumentParser(description="店铺健康检查（订单履约/合规扣分/买家评价）")
    parser.add_argument("--code", required=True, choices=list(VALID_CODES),
                        help="模块 code：order_risk（订单履约）/ shop_punish（合规扣分）/ feedback（买家评价）")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", default=None, help="可选，目标店铺的 loginId，用于多店铺查询")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置。\n\n请运行: `cli.py configure YOUR_AK`", {"data": {}})
        return

    try:
        login_id = getattr(args, 'NEWTON_SHOP_LOGIN_ID', None)
        result = get_shop_health_check(args.code, login_id=login_id)
        print_output(result.get("success", False), result.get("message", ""), result.get("data", {}))
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
