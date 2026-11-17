#!/usr/bin/env python3
"""自定义属性新增 CLI入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import JsonArgumentParser, print_output, print_error
from capabilities.customer_attr_add.service import customer_attr_add

COMMAND_NAME = "customer_attr_add"
COMMAND_DESC = "新增一列自定义属性"


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未注入，请检查框架环境变量 ALI_1688_AK 是否已配置", {})
        return 2

    parser = JsonArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--key", required=True, help="字段编码，仅允许 [a-z0-9_]")
    parser.add_argument("--label", required=True, help="字段显示名")
    parser.add_argument("--type", default="string", choices=["string", "number", "date", "boolean"],
                        help="字段类型，默认 string")
    parser.add_argument("--value", help="初始值（可选）")
    args = parser.parse_args()

    try:
        result = customer_attr_add(
            attr_key=args.key,
            attr_label=args.label,
            attr_type=args.type,
            value=args.value,
        )
        print_output(True, f"# ✅ 新增属性成功\n\n属性编码：`{args.key}`\n显示名：{args.label}\n类型：{args.type}", {"data": result})
        return 0
    except Exception as e:
        return print_error(e, {})


if __name__ == "__main__":
    sys.exit(main())
