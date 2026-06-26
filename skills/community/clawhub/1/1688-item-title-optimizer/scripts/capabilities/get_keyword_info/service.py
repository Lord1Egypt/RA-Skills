#!/usr/bin/env python3
"""关键词信息获取服务"""

from _http import api_post
from _const import TOOL_CODE
from _errors import ParamError, ServiceError


def get_keyword_info(
    item_id: int,
    include_expo_words: bool = True,
    include_hot_words: bool = True,
    custom_keywords: str = None,
) -> dict:
    """
    获取标题优化所需的全部关键词数据

    Args:
        item_id: 商品ID
        include_expo_words: 是否包含高曝光词
        include_hot_words: 是否包含类目热搜词
        custom_keywords: 自定义关键词，分号分隔

    Returns:
        关键词信息，包含 hot_words, expo_words, cate_id, cate_name 等
    """
    if not item_id:
        raise ParamError("商品ID（item_id）不能为空")

    body = {
        "function": "get_keyword_info",
        "item_id": item_id,
        "include_expo_words": include_expo_words,
        "include_hot_words": include_hot_words,
    }
    if custom_keywords:
        body["custom_keywords"] = custom_keywords

    data = api_post(
        f"/api/{TOOL_CODE}/1.0.0",
        body,
        timeout=30,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
