#!/usr/bin/env python3
"""标题 LLM 深度重写服务"""

from _http import api_post
from _const import TOOL_CODE
from _errors import ParamError, ServiceError


def optimize_title_llm(item_id: int, preference: str = None) -> dict:
    """
    基于 LLM 的智能标题重写（方式B）

    Args:
        item_id: 商品ID
        preference: 用户偏好（可选），如 "加入'防潮'单词"

    Returns:
        优化结果，包含 old_title, new_title, new_title_words, other_words
    """
    if not item_id:
        raise ParamError("商品ID（item_id）不能为空")

    body = {
        "function": "optimize_title_llm",
        "item_id": item_id,
    }
    if preference:
        body["preference"] = preference

    data = api_post(
        f"/api/{TOOL_CODE}/1.0.0",
        body,
        timeout=60,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
