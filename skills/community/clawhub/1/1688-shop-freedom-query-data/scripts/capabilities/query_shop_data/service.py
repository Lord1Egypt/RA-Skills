#!/usr/bin/env python3
"""商家数据查询服务"""

from _http import api_post
from _errors import ServiceError, ParamError


def query_shop_data(data_source: str, api_path: str, params: dict) -> dict:
    """
    调用 1688_query_shop_data，查询商家经营数据。
    userId 由网关根据 AK 签名自动注入，脚本无需传递。

    Args:
        data_source: 数据源标识（如 SYCM、ITEM）
        api_path: 接口路径（如 portal/core/overview）
        params: 业务参数（如 {"dataType": "RECENT_7", "device": "ALL"}）

    Returns:
        接口返回的数据 dict
    """
    if not data_source:
        raise ParamError("dataSource 不能为空")
    if not api_path:
        raise ParamError("apiPath 不能为空")

    data = api_post("/api/1688_query_shop_data/1.0.0", {
        "dataSource": data_source,
        "apiPath": api_path,
        "params": params or {}
    })

    if not isinstance(data, dict):
        raise ServiceError("数据接口返回格式异常")

    return data
