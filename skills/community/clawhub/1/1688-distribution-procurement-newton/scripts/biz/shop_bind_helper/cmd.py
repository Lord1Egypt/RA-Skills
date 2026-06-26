#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""店铺绑定助手命令 - 店铺信息查询

复用 1688-distribution 的 shop_info 能力
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.shop_bind_helper.service import (
    get_shop_and_tool_info,
    filter_available_tools,
    format_shop_list,
    get_app_keys,
)


def query():
    """
    查询绑定的店铺和工具信息

    从 1688-distribution/scripts/biz/shop_info 复制

    用法：
        python3 scripts/cli.py shop_bind_helper query
    """
    try:
        # 获取店铺信息
        result = get_shop_and_tool_info()
        tool_list = result.get("toolList", [])

        # 过滤可用店铺
        available_tools = filter_available_tools(tool_list)

        # 格式化输出
        markdown = format_shop_list(available_tools)

        print_output(True, markdown, {
            "toolList": available_tools,
            "totalTools": len(tool_list),
            "availableTools": len(available_tools)
        })
    except Exception as e:
        print_error(e)


def app_keys():
    """
    查询绑定的店铺对应的 ISV AppKey 信息

    用于后续 ISV Token 获取和 ISV 技能调用。

    用法：
        python3 scripts/cli.py shop_bind_helper app_keys
    """
    try:
        result = get_shop_and_tool_info()
        tool_list = result.get("toolList", [])
        available_tools = filter_available_tools(tool_list)
        app_keys_info = get_app_keys(available_tools)

        if not app_keys_info:
            print_output(True, "当前没有可用的 ISV AppKey 信息。", {"appKeys": []})
            return

        lines = ["ISV AppKey 信息：\n"]
        for i, info in enumerate(app_keys_info, 1):
            lines.append(f"{i}. {info['app_name']}（AppKey: {info['app_key']}）")
            lines.append(f"   渠道：{info['channel_desc']} · {info['shop_name']}（{info['shop_code']}）")
        lines.append("")
        lines.append("💡 使用示例：")
        lines.append(f"   python3 scripts/cli.py isv_token fetch --app_key={app_keys_info[0]['app_key']}")

        print_output(True, "\n".join(lines), {"appKeys": app_keys_info})
    except Exception as e:
        print_error(e)
