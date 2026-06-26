#!/usr/bin/env python3
"""卖点生成 — service"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post, parse_data_field
from _errors import ServiceError
from biz.const import API_SELLING_POINT, DEFAULT_USER_ID


def generate_selling_point(offer_id: str, prompt: str) -> dict:
    """
    生成商品卖点

    Args:
        offer_id: 1688 商品 ID
        prompt:   用户提文（原封不动传入）

    Returns:
        {"points_result": "生成的卖点"}
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "offer_id": str(offer_id),
        "prompt": prompt,
    }

    result = api_post(API_SELLING_POINT, body)
    # result 格式: {"data": {"points_result": "..."}, "__success__": true}
    if isinstance(result, dict):
        data = result.get("data", {})
        if isinstance(data, dict):
            return {
                "points_result": data.get("points_result", ""),
            }
        # 如果 data 已经是解析后的 dict
        if "points_result" in result:
            return {"points_result": result.get("points_result", "")}

    raise ServiceError(f"卖点生成返回格式异常：{result}")
