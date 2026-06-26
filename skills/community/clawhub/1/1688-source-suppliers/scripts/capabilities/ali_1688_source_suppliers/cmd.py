#!/usr/bin/env python3
"""1688供应商查询 CLI入口"""

COMMAND_NAME = "ali_1688_source_suppliers"
COMMAND_DESC = "查询1688供应商信息"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.ali_1688_source_suppliers.service import query_1688_source_suppliers


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询1688供应商信息。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="供应商信息查询")
    parser.add_argument("--query", "-q", required=True, help="供应商名称")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        # argparse 参数缺失时会调用 sys.exit，捕获后返回标准 JSON 格式
        print_output(False,
                     "❌ 参数缺失：query 不能为空。\n\n请提供查询关键字，例如：\n- `cli.py ali_1688_source_suppliers --query \"灯具供应商\"`\n- `cli.py ali_1688_source_suppliers -q \"常州工厂\"`",
                     {"data": {}})
        return

    try:
        result = query_1688_source_suppliers(args.query)
        markdown_output = result.get("markdown", "未找到供应商信息")
        
        print_output(True, markdown_output, result)
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
