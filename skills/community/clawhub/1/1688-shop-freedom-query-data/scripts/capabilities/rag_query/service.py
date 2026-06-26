#!/usr/bin/env python3
"""RAG 接口语义检索服务"""

from _http import api_post
from _errors import ServiceError


def rag_query_api_info(query: str) -> list:
    """
    调用 1688_rag_query_api_info，语义检索接口文档。
    userId 由网关根据 AK 签名自动注入，脚本无需传递。

    Args:
        query: 自然语言查询描述

    Returns:
        匹配的接口文档列表 [{"score": "0.93", "content": "..."}]
    """
    if not query or not query.strip():
        raise ValueError("query 不能为空")

    data = api_post("/api/1688_rag_query_api_info/1.0.0", {
        "query": query
    })

    # data 可能是 list 或 dict（含 data 字段）
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("data", data)

    raise ServiceError("RAG 接口返回格式异常")
