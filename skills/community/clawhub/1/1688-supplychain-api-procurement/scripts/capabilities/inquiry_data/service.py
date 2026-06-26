# -*- coding: utf-8 -*-
"""
询盘数据查询能力实现

流程：
1. 使用之前搜索的 instanceId
2. 调用 DigitalHumanInstanceData 接口
3. 传递 apiFunction=instanceData, subScene=newton_api, itemStage=inquiry
4. 返回最新的询盘数据，提取 inquirySummary
"""

import time
from typing import Dict, Any, List

from _http import api_post
from _errors import ServiceError
from settings import settings


def fetch_inquiry_data(instance_id: str) -> Dict[str, Any]:
    """
    查询最新询盘数据

    Args:
        instance_id: 之前搜索的 instanceId

    Returns:
        {
            "instance_id": str,
            "elapsed_seconds": float,
            "stage": str,         # "recall" / "inquiry"
            "status": str,        # "running" / "finish" / "invalid"
            "total_items": int,
            "inquired_items": [...],  # 有 inquirySummary 的商品
            "raw": dict,              # 完整原始响应
        }
    """
    if not instance_id or not instance_id.strip():
        raise ServiceError("instance_id 不能为空，请先执行 inquiry")

    instance_id = instance_id.strip()

    body = {
        "instance_id": instance_id,
        "apiFunction": "instanceData",
        "subScene": "newton_api",
        "itemStage": "inquiry",
    }

    start_time = time.time()

    resp = api_post(
        path=settings.INSTANCE_DATA_PATH,
        body=body,
        timeout=settings.TOOL_TIMEOUT,
    )

    elapsed = time.time() - start_time

    # 解析响应层级：resp.data.result / resp.data.stage / resp.data.status
    inner = resp.get("data", {})
    stage = inner.get("stage", "")
    status = inner.get("status", "")
    result = inner.get("result", [])

    # 提取有 inquirySummary 的商品
    inquired_items = []
    for item in result:
        summary = item.get("inquirySummary")
        if summary:
            inquired_items.append({
                "itemId": item.get("itemId", ""),
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "skuName": item.get("skuName", ""),
                "inquirySummary": summary,
            })

    return {
        "instance_id": instance_id,
        "elapsed_seconds": round(elapsed, 1),
        "stage": stage,
        "status": status,
        "total_items": len(result),
        "inquired_items": inquired_items,
        "raw": resp,
    }
