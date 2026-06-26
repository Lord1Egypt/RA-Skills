#!/usr/bin/env python
"""通过关键词搜索店铺商品服务"""

from _http import api_post
from _errors import ServiceError

def search_offer_by_keyword(keyword: str = "", page: int = 1, page_size: int = 10) -> dict:
    """通过关键词搜索店铺商品。

    Args:
        keyword:   搜索关键词（可选）
        page:      页码，默认 1
        page_size: 每页数量，默认 10

    Returns:
        API 响应 data 字段，包含匹配的商品列表
    """
    data = api_post(
        "/api/tool_search_offer_by_keyword/1.0.0",
        {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
        },
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
