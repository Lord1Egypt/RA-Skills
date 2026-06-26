#!/usr/bin/env python3
"""趋势洞察 — 服务层"""

import json
from _http import api_post
from _errors import ParamError, ServiceError


def fetch_trend(query: str, timeout: int = 25) -> dict:
    """
    查询趋势（使用 AK 签名）

    Returns:
        {"markdown": str, "data": dict, "query_used": str}
    """
    if not query:
        raise ParamError("query 不能为空")

    body = {"code": "offer_hot", "bizParams": {"query": query}}
    model = api_post("/1688claw/skill/workflow", body, timeout=timeout)

    biz_data = (model or {}).get("bizData")
    if biz_data is None:
        raise ServiceError("趋势接口返回为空")

    if isinstance(biz_data, str):
        markdown = biz_data
    else:
        markdown = "```json\n" + json.dumps(biz_data, ensure_ascii=False, indent=2) + "\n```"

    prefix = f"关键词：{query}\n\n"
    return {"markdown": prefix + markdown, "data": biz_data, "query_used": query}
