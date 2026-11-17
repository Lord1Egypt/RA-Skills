#!/usr/bin/env python3
"""获取店铺维度数据 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.get_shop_data.service import get_shop_data

COMMAND_NAME = "get_shop_data"
COMMAND_DESC = "获取店铺维度数据（支付金额、买家数等）"


def main():
    try:
        result = get_shop_data()
        print_output(True, "店铺数据查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
