#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""关联货源助手 - 替换下游商品关联的1688商品（可到SKU维度）

可被独立使用，也可被 supply_chain_helper 在自动换供流程中调用
"""

import os
import sys
from typing import Dict, List, Optional

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts.biz.isv_skill_helper.service import (
    discover_isv_skill,
    discover_skill_by_name,
    call_isv_link_supply,
)
from scripts.biz.isv_token.service import fetch_isv_token
from scripts.biz.shop_bind_helper.service import (
    get_shop_and_tool_info,
    filter_available_tools,
    get_app_keys,
)


def link_supply(
    downstream_item_id: str,
    downstream_sku_id: str = None,
    offer_id: str = None,
    sku_id: str = None,
    isv_app_key: str = None,
    platform: str = None,
) -> Dict:
    """
    关联货源 - 将下游商品与1688商品建立关联关系

    通过 ISV 技能执行关联，必须提供 isv_app_key 和 platform。

    :param downstream_item_id: 下游商品ID（必填）
    :param downstream_sku_id: 下游SKU ID（可选，支持SKU维度关联）
    :param offer_id: 1688商品ID（可选）
    :param sku_id: 1688 SKU ID（可选）
    :param isv_app_key: ISV AppKey（必填）
    :param platform: 平台类型（必填，如 taobao/douyin）
    :return: 关联结果
    """
    if not isv_app_key or not platform:
        return {
            "success": False,
            "error": "关联货源需要提供 isv_app_key 和 platform",
        }

    return _link_supply_via_isv(
        downstream_item_id=downstream_item_id,
        downstream_sku_id=downstream_sku_id,
        offer_id=offer_id,
        sku_id=sku_id,
        isv_app_key=isv_app_key,
        platform=platform,
    )


def _link_supply_via_isv(
    downstream_item_id: str,
    downstream_sku_id: str = None,
    offer_id: str = None,
    sku_id: str = None,
    isv_app_key: str = None,
    platform: str = None,
) -> Dict:
    """
    通过 ISV 技能执行关联货源（ISV 模式内部实现）
    """
    # Step 1: 发现 ISV 技能
    isv_result = discover_isv_skill(isv_app_key)
    if not isv_result.get("found"):
        isv_result = discover_skill_by_name("fx-procurement-9018264")
    if not isv_result.get("found"):
        return {
            "success": False,
            "error": f"未找到对应的 ISV 技能（AppKey: {isv_app_key}）",
        }

    skill_path = isv_result["skill_path"]

    # Step 2: 获取 ISV Token
    try:
        token = fetch_isv_token(isv_app_key)
    except Exception as e:
        return {"success": False, "error": f"获取 ISV Token 失败: {e}"}

    # Step 3: 获取店铺信息
    try:
        shop_info = get_shop_and_tool_info()
        available_tools = filter_available_tools(shop_info.get("toolList", []))
        app_keys_info = get_app_keys(available_tools)

        matched_shops = [
            info
            for info in app_keys_info
            if info["app_key"] == isv_app_key
            and info["channel"].lower() == platform.lower()
        ]

        if not matched_shops:
            return {
                "success": False,
                "error": f"未找到平台 {platform} 下 AppKey {isv_app_key} 的绑定店铺",
            }

        shop = matched_shops[0]
        shop_id = shop["shop_code"]
        shop_nick = shop["shop_name"]
    except Exception as e:
        return {"success": False, "error": f"获取店铺信息失败: {e}"}

    # Step 4: 构造 source_offer_url
    if not offer_id:
        return {"success": False, "error": "ISV 方式关联货源需要提供 offer_id"}

    source_offer_url = f"https://detail.1688.com/offer/{offer_id}.html"

    # Step 5: 调用 ISV 技能执行关联
    try:
        link_result = call_isv_link_supply(
            skill_path=skill_path,
            token=token,
            shop_id=shop_id,
            shop_nick=shop_nick,
            local_item_id=downstream_item_id,
            source_offer_url=source_offer_url,
            purchase_account="",
            platform=platform,
        )
        if not link_result.get("success") and "error" not in link_result:
            link_result["error"] = link_result.get("markdown") or "ISV 关联货源失败"
        return link_result
    except Exception as e:
        return {"success": False, "error": f"ISV 关联货源失败: {e}"}


def batch_link_supply(links: List[Dict]) -> Dict:
    """
    批量关联货源

    :param links: 关联配置列表，每个元素包含 downstream_item_id, downstream_sku_id, offer_id, sku_id 等
    :return: 批量关联结果
    """
    results = []
    success_count = 0
    failed_count = 0

    for link in links:
        try:
            result = link_supply(
                downstream_item_id=link.get("downstream_item_id"),
                downstream_sku_id=link.get("downstream_sku_id"),
                offer_id=link.get("offer_id"),
                sku_id=link.get("sku_id"),
                isv_app_key=link.get("isv_app_key"),
                platform=link.get("platform"),
            )
            results.append({
                "downstream_item_id": link.get("downstream_item_id"),
                "success": True,
                "data": result
            })
            success_count += 1
        except Exception as e:
            results.append({
                "downstream_item_id": link.get("downstream_item_id"),
                "success": False,
                "error": str(e)
            })
            failed_count += 1

    return {
        "success": True,
        "data": {
            "total": len(links),
            "success": success_count,
            "failed": failed_count,
            "results": results
        }
    }
