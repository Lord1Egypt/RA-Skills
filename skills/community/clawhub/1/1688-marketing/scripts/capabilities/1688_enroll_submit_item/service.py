#!/usr/bin/env python3
"""1688招商活动报名服务"""

from _http import api_post
from _errors import ServiceError


def submit_enroll_item(activity_id: int, item_id: int, fill_form_data_list: list) -> dict:
    """
    提交招商活动报名（报品同时报商）

    Args:
        activity_id: 活动Id
        item_id: 商品Id
        fill_form_data_list: 价格等表单填充数据列表，每项包含:
            - inputKey: 表单key
            - inputValue: 表单值（商品无sku时填此项）
            - inputValueSku: 表单值（商品有sku时填此项，key为skuId，value为对应值）

    Returns:
        包含 success, recordId, message 的字典
    """
    body = {
        "activityId": activity_id,
        "itemId": item_id,
        "fillFormDataList": fill_form_data_list,
    }

    result = api_post("/api/1688_enroll_submit_item/1.0.0", body)

    if not isinstance(result, dict):
        raise ServiceError("格式异常，请稍后重试")
    return result
