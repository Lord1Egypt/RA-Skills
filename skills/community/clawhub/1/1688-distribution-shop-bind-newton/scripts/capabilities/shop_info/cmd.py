#!/usr/bin/env python3
"""
店铺信息查询命令层

提供查询当前用户已绑定店铺和 ISV 工具的能力。
"""

import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from . import service

COMMAND_NAME = "shop_info"
COMMAND_DESC = "查询店铺和 ISV 工具信息"


def _output(success: bool, markdown: str, data: dict = None):
    """统一输出 JSON 响应。"""
    result = {
        "success": success,
        "markdown": markdown,
        "data": data or {},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def format_shops_markdown(data: dict) -> str:
    """格式化店铺信息为 Markdown。"""
    options = data.get("options", [])
    if not options:
        return "暂无已绑定的店铺和工具信息。"

    lines = ["**您的店铺和工具信息：**\n"]

    for opt in options:
        channel_desc = opt.get("channelDesc", opt.get("channel", ""))
        app_name = opt.get("appName", "")
        shops = opt.get("shops", [])

        lines.append(f"**【{channel_desc}】** {app_name}")
        if shops:
            for shop in shops:
                shop_name = shop.get("shopName", "")
                shop_code = shop.get("shopCode", "")
                lines.append(f"  - {shop_name} ({shop_code})")
        else:
            lines.append("  暂无绑定店铺")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"],
                        help="输出格式")

    args = parser.parse_args()

    try:
        data = service.get_all_tools_and_shops()

        if args.format == "json":
            _output(True, "查询成功", data)
        else:
            markdown = format_shops_markdown(data)
            _output(True, markdown, data)

    except Exception as e:
        _output(False, f"查询失败：{e}")


if __name__ == "__main__":
    main()
