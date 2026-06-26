#!/usr/bin/env python3
"""获取商品主图信息 — service"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post, parse_data_field
from _errors import ServiceError
from biz.const import API_IMAGE_INFO, DEFAULT_USER_ID


def get_image_info(offer_id: str) -> dict:
    """
    获取商品主图信息

    Args:
        offer_id: 1688 商品 ID

    Returns:
        {
            "main_image_urls": ["url1", "url2", ...],
            "white_image_url": "url"
        }
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "offer_id": str(offer_id),
    }

    result = api_post(API_IMAGE_INFO, body)
    # result 格式: {"data": {"main_image_urls": [...], "white_image_url": "..."}, "__success__": true}
    if isinstance(result, dict):
        data = result.get("data", {})
        if isinstance(data, dict) and ("main_image_urls" in data or "white_image_url" in data):
            return {
                "main_image_urls": data.get("main_image_urls", []),
                "white_image_url": data.get("white_image_url", ""),
            }
        # 兜底：result 本身就有
        if "main_image_urls" in result:
            return {
                "main_image_urls": result.get("main_image_urls", []),
                "white_image_url": result.get("white_image_url", ""),
            }

    raise ServiceError(f"获取商品主图返回格式异常：{result}")
