#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""店铺和工具信息查询服务"""

import os
import sys
from typing import List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._http import api_post
from scripts._sys._errors import ServiceError


def get_shop_and_tool_info() -> dict:
    """
    查询当前 AK 绑定用户的分销工具和店铺信息。

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


def filter_available_tools(tool_list: list) -> List[dict]:
    """
    过滤掉已过期的工具和店铺。

    移除 toolExpired=True 的工具，以及 channelAuthExpired=True 的店铺。

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
