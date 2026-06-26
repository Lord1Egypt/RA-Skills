#!/usr/bin/env python
"""店铺维度数据查询服务"""

from _http import api_post
from _errors import ServiceError

def get_shop_data() -> dict:
    """获取店铺维度数据，作为商品评分的对比基准。

    Returns:
        API 响应 data 字段，包含店铺支付金额、支付买家数、在线商品数等
    """
    data = api_post(
        "/api/skill_1688_item_select_get_shop_data/1.0.0",
        {},
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
