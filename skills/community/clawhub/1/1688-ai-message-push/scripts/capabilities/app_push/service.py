#!/usr/bin/env python3
"""APP 系统通知服务"""

from _http import api_post
from _errors import ServiceError


def send_app_push(text: str) -> dict:
    """发送 APP 系统通知

    Args:
        text: 通知内容（纯文本）

    Returns:
        API 响应 data 字段
    """
    data = api_post("/api/skill_ai_app_push/1.0.0", {
        "text": text,
        "needTimeLimit": False,
    })

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
