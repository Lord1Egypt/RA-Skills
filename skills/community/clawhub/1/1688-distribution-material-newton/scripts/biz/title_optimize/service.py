#!/usr/bin/env python3
"""标题优化 — service"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post, parse_data_field
from _errors import ServiceError
from biz.const import API_TITLE_OPTIMIZE, DEFAULT_USER_ID


def optimize_title(offer_id: str, prompt: str) -> dict:
    """
    标题优化

    Args:
        offer_id: 1688 商品 ID
        prompt:   用户提文（原封不动传入）

    Returns:
        {"title_result": "优化后的标题"}
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "offer_id": str(offer_id),
        "prompt": prompt,
    }

    result = api_post(API_TITLE_OPTIMIZE, body)
    # result 格式: {"data": {"title_result": "..."}, "__success__": true}
    if isinstance(result, dict):
        data = result.get("data", {})
        if isinstance(data, dict):
            return {
                "title_result": data.get("title_result", ""),
            }
        # 如果 data 已经是解析后的 dict
        if "title_result" in result:
            return {"title_result": result.get("title_result", "")}

    raise ServiceError(f"标题优化返回格式异常：{result}")
