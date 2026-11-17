#!/usr/bin/env python3
"""微信通知服务"""

from _http import api_post
from _errors import ServiceError


def send_wx_push(text: str) -> dict:
    """发送微信通知消息

    Args:
        text: 微信通知内容（纯文本）

    Returns:
        API 响应 data 字段
    """
    data = api_post("/api/skill_wx_push/1.0.0", {"text": text})

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")
    return data
