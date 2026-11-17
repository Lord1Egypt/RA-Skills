#!/usr/bin/env python3
"""多店铺绑定列表查询服务

通过 1688 Skills 网关调用 alibaba.1688.newton.shop.list.binds 接口，
获取当前用户绑定的所有店铺及对应 loginId。
"""

from _http import api_post

_API_PATH = "/api/alibaba.1688.newton.shop.list.binds/1.0.0"


def get_bindlist(strict: bool = False, deadline=None) -> list:
    """获取当前用户绑定的所有店铺及 loginId 列表。

    Returns:
        店铺列表，每条包含 companyName、isOwner、loginId 等字段。
        若接口异常或无绑定数据则返回空列表；strict 模式保留接口异常。
    """
    try:
        data = api_post(_API_PATH, {}, timeout=15, _deadline=deadline)
    except Exception:
        if strict:
            raise
        return []

    if not isinstance(data, dict):
        if isinstance(data, list):
            return data
        return []

    bind_data = data.get("data", data)
    if isinstance(bind_data, list):
        return bind_data

    return []
