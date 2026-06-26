#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""店铺绑定助手 - 绑店状态查询、绑店引导、店铺信息查询

从 1688-distribution 复制获取绑店关系的能力
"""

import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError



def get_shop_and_tool_info() -> Dict:
    """
    查询当前 AK 绑定用户的分销工具和店铺信息

    从 1688-distribution/scripts/biz/shop_info/service.py 复制

    :return: 包含 toolList（工具和店铺列表）的 dict
    """
    inner = api_post(tool_name="shop_and_tool_info", body={})

    # success 在 inner 层
    if inner.get("success") is False:
        raise ServiceError("查询店铺信息失败，请检查 AK 是否正确或稍后重试。")

    # toolList 在 inner.data 层
    data = inner.get("data", {})
    if not isinstance(data, dict):
        return {"toolList": []}
    if not data.get("toolList"):
        return {"toolList": []}
    return data


def filter_available_tools(tool_list: List[Dict]) -> List[Dict]:
    """
    过滤掉已过期的工具和店铺

    从 1688-distribution/scripts/biz/shop_info/service.py 复制

    移除 toolExpired=True 的工具，以及 channelAuthExpired=True 的店铺

    :param tool_list: 原始 toolList
    :return: 过滤后的 toolList
    """
    filtered_tools = []
    for tool in tool_list:
        if tool.get("toolExpired", False):
            continue
        filtered_channels = []
        for channel in tool.get("channelList", []):
            filtered_shops = [
                shop for shop in channel.get("shopList", [])
                if not shop.get("channelAuthExpired", False)
            ]
            if filtered_shops:
                filtered_channel = {**channel, "shopList": filtered_shops}
                filtered_channels.append(filtered_channel)
        if filtered_channels:
            filtered_tool = {**tool, "channelList": filtered_channels}
            filtered_tools.append(filtered_tool)
    return filtered_tools


def get_app_keys(tool_list: List[Dict]) -> List[Dict]:
    """
    从 toolList 中提取所有可用的 appKey 信息

    用于 ISV 技能发现和 Token 获取。

    :param tool_list: 过滤后的 toolList
    :return: [{"app_key": "...", "app_name": "...", "channel": "...", "shop_code": "...", "shop_name": "..."}]
    """
    result = []
    for tool in tool_list:
        app_key = tool.get("appKey", "")
        if not app_key:
            continue
        for channel in tool.get("channelList", []):
            for shop in channel.get("shopList", []):
                result.append({
                    "app_key": app_key,
                    "app_name": tool.get("appName", ""),
                    "channel": channel.get("channel", ""),
                    "channel_desc": channel.get("channelDesc", ""),
                    "shop_code": shop.get("shopCode", ""),
                    "shop_name": shop.get("shopName", ""),
                })
    return result


def format_shop_list(tool_list: List[Dict]) -> str:
    """
    将 toolList 格式化为可读的 Markdown 文本

    从 1688-distribution/scripts/biz/shop_info/cmd.py 复制

    :param tool_list: 工具列表
    :return: Markdown 格式的店铺列表
    """
    if not tool_list:
        return "当前没有绑定任何店铺。"

    lines = ["您当前绑定的店铺如下：\n"]
    for tool in tool_list:
        app_name = tool.get("appName", "未知工具")
        lines.append(f"**【{app_name}】**")
        for channel in tool.get("channelList", []):
            channel_desc = channel.get("channelDesc", channel.get("channel", "未知渠道"))
            for shop in channel.get("shopList", []):
                shop_name = shop.get("shopName", "未知店铺")
                shop_code = shop.get("shopCode", "")
                lines.append(f"  - {channel_desc} · {shop_name}（店铺编码：{shop_code}）")
        lines.append("")
    return "\n".join(lines)
