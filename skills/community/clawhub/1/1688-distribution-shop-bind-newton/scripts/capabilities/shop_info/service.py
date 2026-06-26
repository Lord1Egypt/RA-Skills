#!/usr/bin/env python3
"""店铺和工具信息查询服务

提供两个数据源：
1. distribution_tools_shops — 获取所有 ISV 工具和绑定的店铺（推荐，数据更全）
2. shop_and_tool_info — 获取已绑定的工具和店铺（备选）
"""

import os
import sys
from typing import List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post_tool
from _errors import ServiceError


# ── distribution_tools_shops 接口（推荐） ─────────────────────────────────────

def get_distribution_tools_shops() -> dict:
    """
    获取当前用户所有 ISV 工具和绑定的店铺信息。

    调用 distribution_tools_shops 接口，返回完整的工具和店铺数据，
    包括支持绑店流程的标记（shopBundle/shopBundleAI）。

    Returns:
        包含 isvTools 和 recentlyDistributeShops 的 dict
    """
    inner = api_post_tool(tool_name="distribution_tools_shops", body={})
    data = _extract_biz_data(inner)

    if not isinstance(data, dict):
        return {"isvTools": []}
    return data


def filter_available_isv_tools(isv_tools: list, bindable_only: bool = False,
                               include_expired: bool = True) -> List[dict]:
    """
    过滤 ISV 工具列表。

    注意：默认保留过期工具，因为绑店流程中包含工具订购步骤，
    用户可能需要在绑店过程中完成续订。

    Args:
        isv_tools: 原始 isvTools 列表
        bindable_only: 是否只保留支持绑店流程的工具（shopBundle=True 或 shopBundleAI=True）
        include_expired: 是否保留已过期的工具（默认 True，绑店流程需要）
    """
    filtered = []
    for tool in isv_tools:
        if not include_expired and tool.get("toolExpired", False):
            continue
        if bindable_only:
            if not tool.get("shopBundle", False) and not tool.get("shopBundleAI", False):
                continue
        filtered.append(tool)
    return filtered


def extract_tool_options_from_isv(isv_tools: List[dict]) -> List[dict]:
    """
    从 isvTools 列表中提取所有 appKey + channel 组合，供绑店流程使用。

    isvTools 的 shops 字段直接包含 channel 信息（扁平结构，非嵌套）。

    Returns:
        [{"appKey": "xxx", "appName": "xxx", "channel": "douyin", "channelDesc": "抖音",
          "shopBundle": True, "shopBundleAI": False,
          "shops": [{"shopCode": "xxx", "shopName": "xxx"}]}]
    """
    options = []
    seen_combinations = set()

    for tool in isv_tools:
        app_key = tool.get("appKey", "")
        app_name = tool.get("appName", "")
        shop_bundle = tool.get("shopBundle", False)
        shop_bundle_ai = tool.get("shopBundleAI", False)
        support_channels = tool.get("supportChannel", [])

        # 从 shops 中按 channel 分组
        channel_shops = {}
        for shop in tool.get("shops", []):
            channel_code = shop.get("channel", "")
            if not channel_code:
                continue
            if channel_code not in channel_shops:
                channel_shops[channel_code] = {
                    "channelDesc": shop.get("channelDesc", channel_code),
                    "shops": [],
                }
            channel_shops[channel_code]["shops"].append({
                "shopCode": shop.get("shopCode", ""),
                "shopName": shop.get("shopName", ""),
            })

        # 为有店铺的渠道生成选项
        for channel_code, channel_info in channel_shops.items():
            combo_key = f"{app_key}_{channel_code}"
            if combo_key in seen_combinations:
                continue
            seen_combinations.add(combo_key)
            options.append({
                "appKey": app_key,
                "appName": app_name,
                "channel": channel_code,
                "channelDesc": channel_info["channelDesc"],
                "shopBundle": shop_bundle,
                "shopBundleAI": shop_bundle_ai,
                "shops": channel_info["shops"],
            })

        # 对于支持但尚无店铺的渠道，也生成选项（用于绑店）
        for channel_code in support_channels:
            combo_key = f"{app_key}_{channel_code}"
            if combo_key in seen_combinations:
                continue
            seen_combinations.add(combo_key)
            options.append({
                "appKey": app_key,
                "appName": app_name,
                "channel": channel_code,
                "channelDesc": channel_code,
                "shopBundle": shop_bundle,
                "shopBundleAI": shop_bundle_ai,
                "shops": [],
            })

    return options


# ── shop_and_tool_info 接口（备选） ───────────────────────────────────────────

def get_shop_and_tool_info() -> dict:
    """
    查询当前 AK 绑定用户的分销工具和店铺信息（旧接口，备选）。

    Returns:
        包含 toolList（工具和店铺列表）的 dict
    """
    inner = api_post_tool(tool_name="shop_and_tool_info", body={})
    data = _extract_biz_data(inner)

    if not isinstance(data, dict):
        return {"toolList": []}
    if not data.get("toolList"):
        return {"toolList": []}
    return data


def filter_available_tools(tool_list: list) -> List[dict]:
    """
    过滤掉已过期的工具和店铺（shop_and_tool_info 格式）。

    三级过滤：
    - 工具级：移除 toolExpired=True 的工具
    - 渠道级：移除所有店铺都过期的渠道
    - 店铺级：移除 channelAuthExpired=True 的店铺
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


def extract_tool_channel_options(available_tools: List[dict]) -> List[dict]:
    """
    从 shop_and_tool_info 格式的工具列表中提取 appKey + channel 组合。
    """
    options = []
    for tool in available_tools:
        app_key = tool.get("appKey", "")
        app_name = tool.get("appName", "")
        for channel in tool.get("channelList", []):
            channel_code = channel.get("channel", "")
            channel_desc = channel.get("channelDesc", channel_code)
            shops = [
                {"shopCode": s.get("shopCode", ""), "shopName": s.get("shopName", "")}
                for s in channel.get("shopList", [])
            ]
            options.append({
                "appKey": app_key,
                "appName": app_name,
                "channel": channel_code,
                "channelDesc": channel_desc,
                "shops": shops,
            })
    return options


# ── 统一入口 ──────────────────────────────────────────────────────────────────

def get_all_tools_and_shops() -> dict:
    """
    统一入口：优先使用 distribution_tools_shops，失败时回退到 shop_and_tool_info。

    Returns:
        {
            "source": "distribution_tools_shops" | "shop_and_tool_info" | "none",
            "isvTools": [...],       # distribution_tools_shops 格式
            "toolList": [...],       # shop_and_tool_info 格式（回退时）
            "options": [...],        # 统一的 appKey+channel 选项列表
        }
    """
    # 优先尝试 distribution_tools_shops
    try:
        data = get_distribution_tools_shops()
        isv_tools = data.get("isvTools", [])
        if isv_tools:
            available = filter_available_isv_tools(isv_tools)
            options = extract_tool_options_from_isv(available)
            return {
                "source": "distribution_tools_shops",
                "isvTools": available,
                "toolList": [],
                "options": options,
                "recentlyDistributeShops": data.get("recentlyDistributeShops"),
            }
    except Exception:
        pass

    # 回退到 shop_and_tool_info
    try:
        data = get_shop_and_tool_info()
        tool_list = data.get("toolList", [])
        available = filter_available_tools(tool_list)
        options = extract_tool_channel_options(available)
        return {
            "source": "shop_and_tool_info",
            "isvTools": [],
            "toolList": available,
            "options": options,
        }
    except Exception:
        pass

    return {"source": "none", "isvTools": [], "toolList": [], "options": []}


# ── 内部工具函数 ──────────────────────────────────────────────────────────────

def _extract_biz_data(inner: dict) -> dict:
    """从 API 返回的 inner 结构中提取业务数据，兼容多层嵌套。"""
    if not isinstance(inner, dict):
        return {}

    data = inner.get("data", {})

    # 处理双层嵌套：data.data
    if isinstance(data, dict):
        if data.get("success") is False:
            msg = data.get("bizMsg") or data.get("message") or "查询失败"
            raise ServiceError(str(msg))
        if "data" in data and isinstance(data["data"], dict):
            return data["data"]

    return data if isinstance(data, dict) else {}
