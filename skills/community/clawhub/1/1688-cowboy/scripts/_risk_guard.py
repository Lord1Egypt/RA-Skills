#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险命令二次确认工具 -- 配合 SKILL.md `metadata.risk_command_hooks` 使用

协议参考：钩子_skill_hook_接入协议.md §一 BashRiskCheckHook

用途：
    所有写入 / 状态变更 / 凭证类命令在真正执行前，必须经过商家端侧弹窗显式确认，
    防止 AI 被 prompt 注入或路由错误时跳过 SKILL.md 软约束直接触发后端写入。

两阶段协议：
    Phase 1（首次调用）：脚本输出 <user_confirmation>{message,payload}</user_confirmation>
                       端侧解析后弹窗，由商家点击确认。
    Phase 2（点击确认后）：框架将 payload 写入临时文件，把路径放入环境变量
                       NEWTON_CONFIRM_PAYLOAD，再次执行同一脚本；脚本读取后
                       按 payload 真正执行业务逻辑。

权威值优先：Phase 2 内部所有业务参数都应**只**从 payload 读取，避免命令行参数
           在两阶段之间被任何中间环节篡改。
"""

import json
import os
import sys
from typing import Any, Dict, Optional

_CONFIRM_ENV = "NEWTON_CONFIRM_PAYLOAD"


def get_confirmed_payload() -> Optional[Dict[str, Any]]:
    """读取 Phase 2 注入的 payload。未注入或解析失败返回 None。"""
    payload_file = os.environ.get(_CONFIRM_ENV, "").strip()
    if not payload_file:
        return None
    try:
        with open(payload_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        return None
    return None


def emit_confirmation(
    message: str,
    payload: Dict[str, Any],
    *,
    preview_markdown: str = "",
) -> None:
    """Phase 1：先输出标准 JSON（供 LLM 看到"等待商家确认"），再输出协议
    要求的 <user_confirmation> 标签（端侧弹窗使用）。

    调用方在调用本函数后应**立即返回**，不要继续执行真实业务逻辑。

    Args:
        message: 展示给商家的确认提示（必填）
        payload: Phase 2 真正执行时所需的完整业务参数（必填，必须可 JSON 序列化）
        preview_markdown: 可选，给 LLM 看到的标准 markdown；缺省时复用 message
    """
    if not message:
        raise ValueError("emit_confirmation: message 不能为空")
    if payload is None:
        raise ValueError("emit_confirmation: payload 不能为 None")

    print(json.dumps({
        "success": False,
        "markdown": preview_markdown or "等待商家确认：{}".format(message),
        "data": {"awaiting_confirmation": True},
    }, ensure_ascii=False, indent=2))

    confirm_obj = {"message": message, "payload": payload}
    sys.stdout.write("<user_confirmation>{}</user_confirmation>\n".format(
        json.dumps(confirm_obj, ensure_ascii=False)
    ))
    sys.stdout.flush()
