#!/usr/bin/env python3
"""获取指定日期的流量数据 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_traffic_data.service import get_traffic_data

COMMAND_NAME = "get_traffic_data"
COMMAND_DESC = "获取指定日期的流量数据（PV、UV、UVCTR、跳出率等）"

def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--query_date", required=True, help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", required=False, default=None,
                        help="可选，目标店铺的 loginId，用于多店铺场景")
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询流量数据。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    login_id = getattr(args, 'NEWTON_SHOP_LOGIN_ID', None)

    try:
        result = get_traffic_data(args.query_date, login_id=login_id)
        print_output(True, "流量数据查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
