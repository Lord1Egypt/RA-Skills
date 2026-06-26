#!/usr/bin/env python3
"""多店铺绑定关系查询服务"""

from _http import api_post
from _errors import ServiceError

def get_bindlist() -> dict:
    """获取当前用户的多店铺绑定关系及 AK

    Returns:
        API 响应 data 字段，包含店铺列表
        每个元素包含：companyName, isOwner, ak
    """
    data = api_post("/api/newton_shop_list_binds/1.0.0", {})

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
