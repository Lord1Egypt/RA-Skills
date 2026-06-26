#!/usr/bin/env python3
"""采购数字人 CLI 入口 — 解析用户采购需求并发起采购任务"""

COMMAND_NAME = "procurement"
COMMAND_DESC = "采购数字人：解析采购需求并创建采购任务"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_raw
from _output import make_output, print_output, print_error
from capabilities.procurement.service import create_procurement_task


def main():
    if not get_ak_raw():
        print_output(make_output(
            success=False,
            markdown="❌ AK 未配置，无法创建采购任务。\n\n运行: `cli.py configure YOUR_AK`",
            data={"data": {}},
        ))
        return

    parser = argparse.ArgumentParser(description="采购数字人 — 创建采购任务")
    parser.add_argument("--offerName", "-n", required=True,
                        help="商品名称，如：衣服、螺丝")
    parser.add_argument("--count", "-c", required=True,
                        help="采购数量（纯数字，不含单位），如：10")
    parser.add_argument("--demand", "-d", required=True,
                        help="采购需求描述，如：价格便宜、要求包邮")
    args = parser.parse_args()

    try:
        result = create_procurement_task(args.offerName, args.count, args.demand)
        markdown = (
            f"✅ 采购任务已创建\n\n"
            f"- **商品名称**: {args.offerName}\n"
            f"- **采购数量**: {args.count}\n"
            f"- **采购需求**: {args.demand}"
        )
        print_output(make_output(
            success=True,
            markdown=markdown,
            data={"data": result},
        ))
    except Exception as error:
        print_error(error, {"data": {}})


if __name__ == "__main__":
    main()
