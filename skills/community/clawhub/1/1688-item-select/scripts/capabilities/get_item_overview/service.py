#!/usr/bin/env python
"""商品概览统计查询服务"""

from _http import api_post
from _errors import ServiceError

def get_item_overview() -> dict:
    """获取商品总体概况统计，了解数据规模以决定后续查询策略。

    Returns:
        API 响应 data 字段，包含商品总数、有销售商品数、总销售额等
    """
    data = api_post(
        "/api/skill_1688_item_select_get_item_overview/1.0.0",
        {},
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
