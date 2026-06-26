# -*- coding: utf-8 -*-
"""
DigitalHumanMainAgent 请求构建共享模块

提供会话ID获取和请求体构建，供 inquiry 能力共用。
"""

import json
import os
import uuid


def get_session_id() -> str:
    """获取会话ID：优先从 NEWTON_SESSION_ID 环境变量获取，拿不到则随机生成"""
    session_id = os.environ.get("NEWTON_SESSION_ID", "").strip()
    if not session_id:
        session_id = uuid.uuid4().hex
    return session_id


def build_tool_body(
    content_obj: dict,
    instance_id: str,
    type_name: str,
) -> str:
    """
    构建 DigitalHumanMainAgent 的请求体 JSON 字符串

    content 字段需要双重转义：先 JSON 序列化，再将 " 替换为 \\"，
    使得最终 body JSON 中 content 值包含 \\" 字面量。

    Args:
        content_obj: 请求内容对象（sessionId 等字段由调用方按需放入）
        instance_id: requestId（即 instanceId）
        type_name: 请求类型（"start" / "itemSelectResume"）

    Returns:
        序列化后的 JSON 字符串，可直接作为 api_post 的 raw_body
    """
    content_json = json.dumps(content_obj, ensure_ascii=False, separators=(",", ":"))
    content_escaped = content_json.replace('"', '\\"')

    tool_body = {
        "requestId": instance_id,
        "content": content_escaped,
        "type": type_name,
    }
    return json.dumps(tool_body, ensure_ascii=False, separators=(",", ":"))
