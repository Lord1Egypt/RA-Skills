#!/usr/bin/env python3
"""1688招商活动商品信息及建议价查询服务"""

from _http import api_post
from _errors import ServiceError


def query_enroll_offer(activity_id: int, item_id: int) -> dict:
    """
    查询商品信息和建议提报价

    Args:
        activity_id: 活动Id
        item_id: 商品Id

    Returns:
        包含 itemId, title, price, suggestPrice, skuList 的字典
    """
    body = {
        "activityId": activity_id,
        "itemId": item_id,
    }

    result = api_post("/api/1688_enroll_offer_query/1.0.0", body)

    if not isinstance(result, dict):
        raise ServiceError("格式异常，请稍后重试")
    return result
