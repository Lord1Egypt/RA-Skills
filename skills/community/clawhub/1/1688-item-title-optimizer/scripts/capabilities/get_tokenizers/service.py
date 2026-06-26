#!/usr/bin/env python3
"""分词器列表获取服务"""

from _http import api_post
from _const import TOOL_CODE
from _errors import ServiceError


def get_tokenizers() -> dict:
    """
    获取所有可用的分词器列表

    Returns:
        分词器列表，包含每个分词器的 tokenizer 和 desc
    """
    data = api_post(
        f"/api/{TOOL_CODE}/1.0.0",
        {"function": "get_tokenizers"},
        timeout=30,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
