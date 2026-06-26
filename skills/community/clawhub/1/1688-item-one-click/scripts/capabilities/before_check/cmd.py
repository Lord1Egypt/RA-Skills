#!/usr/bin/env python
"""执行前检查 CLI 入口"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.before_check.service import before_check

COMMAND_NAME = "before_check"
COMMAND_DESC = "执行前检查（判断是否可执行、是否需签署协议）"

def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument('--item_id', type=str, required=True, help='商品ID')
    parser.add_argument('--spi_code', type=str, required=True, help='操作码（如 spi_hsf_automatic_title）')
    parser.add_argument('--spi_params', type=str, required=True, help='操作参数（JSON字符串）')
    args = parser.parse_args()

    try:
        spi_params = json.loads(args.spi_params)
    except json.JSONDecodeError as e:
        print_error(ValueError(f"spi_params 不是合法的 JSON：{e}"))
        return

    try:
        result = before_check(args.item_id, args.spi_code, spi_params)
        msg_info = result.get("msgInfo", "") or result.get("message", "")
        has_agreement = "data" in result and isinstance(result.get("data"), str) and "协议" in result.get("data", "")

        if has_agreement:
            agreement_info = result.get("data", "")
            confirm_msg = result.get("message", "让用户确认协议后可以继续执行")
            markdown = f"📋 需要签署协议\n\n{agreement_info}\n\n{confirm_msg}"
            print_output(True, markdown, result)
        elif "不可执行" in msg_info:
            print_output(False, f"❌ {msg_info}", result)
        else:
            print_output(True, f"✅ 检查通过，{msg_info}", result)
    except Exception as e:
        print_error(e)

if __name__ == "__main__":
    main()
