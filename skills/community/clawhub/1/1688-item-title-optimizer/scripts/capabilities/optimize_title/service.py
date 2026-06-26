#!/usr/bin/env python3
"""标题热词优化服务（规则版）"""

from _http import api_post
from _const import TOOL_CODE
from _errors import ParamError, ServiceError


def optimize_title(item_id: int) -> dict:
    """
    基于规则和统计的标题优化（方式A）

    Args:
        item_id: 商品ID

    Returns:
        优化结果，包含 old_title, new_title, optimize_reason, new_title_words, other_words
    """
    if not item_id:
        raise ParamError("商品ID（item_id）不能为空")

    data = api_post(
        f"/api/{TOOL_CODE}/1.0.0",
        {
            "function": "optimize_title",
            "item_id": item_id,
        },
        timeout=30,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
