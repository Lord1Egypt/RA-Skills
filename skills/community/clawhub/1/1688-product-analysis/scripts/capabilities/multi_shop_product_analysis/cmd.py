#!/usr/bin/env python3
"""多店铺商品诊断汇总 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.multi_shop_product_analysis.service import run_multi_shop_product_analysis

COMMAND_NAME = "multi_shop_product_analysis"
COMMAND_DESC = "批量查询多店铺异常商品汇总（支持指定店铺）"


def _parse_args():
    parser = argparse.ArgumentParser(
        prog=f"cli.py {COMMAND_NAME}",
        description=COMMAND_DESC,
    )
    parser.add_argument(
        '--shop_name', type=str, default=None,
        help='指定店铺名称（模糊匹配），不传则查询所有绑定店铺',
    )
    parser.add_argument(
        '--date_type', type=str, default='RECENT_7',
        help='日期类型：RECENT_7（默认）、RECENT_30',
    )
    parser.add_argument(
        '--device', type=str, default='ALL',
        help='设备筛选：ALL（默认）、PC、APP',
    )
    parser.add_argument(
        '--max_total_rows', type=int, default=20,
        help='多店汇总后全局硬封顶行数（超出则按跌幅绝对值排序后从尾部裁掉，最大不超过20）',
    )
    parser.add_argument(
        '--no-lite',
        action='store_false',
        dest='lite',
        help='关闭 lite 裁剪模式（默认开启 lite，删除 valueMap 中非映射 key 和 cycleCqc 子字段以减少 payload 体积）',
    )
    return parser.parse_args()


def main():
    try:
        args = _parse_args()
        result = run_multi_shop_product_analysis(
            shop_name=args.shop_name,
            date_type=args.date_type,
            device=args.device,
            max_total_rows=args.max_total_rows,
            lite=args.lite,
        )
        print_output(True, "多店铺异常商品查询成功", result)
    except SystemExit:
        raise
    except Exception as e:
        print_error(e, {"shops": []})


if __name__ == "__main__":
    main()
