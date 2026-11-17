#!/usr/bin/env python3
"""多店铺绑定关系查询服务（从 1688-shop-bind-newton 移植）"""

from _http import api_post
from _errors import ServiceError


def get_bindlist() -> dict:
    """获取当前用户的多店铺绑定关系列表

    Returns:
        API 响应 data 字段，包含绑定店铺数组
        每个元素包含：companyName, isOwner, loginId, userId
    """
    data = api_post("/api/alibaba.1688.newton.shop.list.binds/1.0.0", {})

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
