#!/usr/bin/env python
"""执行操作 CLI 入口"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.execute.service import execute_action

COMMAND_NAME = "execute"
COMMAND_DESC = "执行操作（修改标题/主图）"

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
        result = execute_action(args.item_id, args.spi_code, spi_params)
        msg_info = result.get("msgInfo", "")
        is_success = result.get("success", False)

        if is_success:
            print_output(True, f"✅ {msg_info}", result)
        else:
            print_output(False, f"❌ {msg_info}", result)
    except Exception as e:
        print_error(e)

if __name__ == "__main__":
    main()
