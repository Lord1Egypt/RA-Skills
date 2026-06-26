# -*- coding: utf-8 -*-
"""
模拟对话能力实现

接口：testChat（path: api/cowboy_test_chat/1.0.0）
入参：{query}（sellerUserId 由网关根据 AK 自动注入，不需主动传递）
出参：AiSellerCcResult<AiChatResponse>，双层 data 包装：
  外层 resp.data = 内层 AiChatResponse { timeCost, status, instanceId, data: [...] }
  内层 data[] 每项：{ thought, actionType, message, images }
  actionType 取值：answer（直接回答）/ ask（反问商家）/ human（转人工）

instanceId 属于系统内部 ID，不向商家展示，仅在 data 里返回供后续追溯。
"""

import time
from typing import Any, Dict, List

from _errors import ServiceError
from _http import api_post
from settings import settings


_ACTION_TYPE_LABEL = {
    "answer": "直接回答",
    "ask": "反问商家",
    "human": "转人工",
}

# Step 5 模拟对话卡 conversations[].answer 文案映射规则：
#   answer → A = message 原文（接待助手实际回答内容）
#   human  → A = "转人工"（兑底文案，不暴露 message）
#   ask    → A = "询问买家"（兑底文案，不暴露 message）
_DERIVED_ANSWER_OVERRIDE = {
    "human": "转人工",
    "ask": "询问买家",
}


def derive_answer(action_type: str, message: str) -> str:
    """按 actionType 三类映射出 Step 5 模拟对话卡 conversations[].answer 的最终文案"""
    if action_type in _DERIVED_ANSWER_OVERRIDE:
        return _DERIVED_ANSWER_OVERRIDE[action_type]
    return message or ""


def test_chat(query: str) -> Dict[str, Any]:
    """
    调用测试聊天接口，模拟买家询问后接待助手的回复

    Args:
        query: 模拟买家提问内容

    Returns:
        {
          "query": "...",
          "elapsed_seconds": 1.2,
          "time_cost_ms": "1200",
          "status": "success",
          "instance_id": "inst_001",
          "replies": [
              {"thought": "...", "action_type": "answer",
               "action_label": "直接回答", "message": "...", "images": []},
              ...
          ]
        }
    """
    start_time = time.time()

    body = {"query": query}

    resp = api_post(
        path=settings.TEST_CHAT_PATH,
        body=body,
        timeout=settings.API_TIMEOUT,
    )

    if not resp.get("success"):
        err = resp.get("errorMsg") or resp.get("message") or resp
        raise ServiceError("模拟对话失败：{}".format(err))

    # 网关可能双层 Result 包装，逐层剚到 AiChatResponse
    # 可能结构：
    #   单层 Result：resp.data = AiChatResponse { timeCost, status, instanceId, data: [...] }
    #   双层 Result：resp.data = Result2 { success, data: AiChatResponse {...} }
    inner = resp.get("data")
    if not isinstance(inner, dict):
        raise ServiceError("响应结构异常：data 字段不是对象（实际类型 {}）".format(type(inner).__name__))

    # 双层 Result 检测：inner 本身带 success 字段且 data 是 dict，说明还是个 Result 壳
    if "success" in inner and isinstance(inner.get("data"), dict):
        if not inner.get("success"):
            err = inner.get("errorMsg") or inner.get("message") or inner
            raise ServiceError("模拟对话失败：{}".format(err))
        inner = inner.get("data") or {}
        if not isinstance(inner, dict):
            raise ServiceError("响应结构异常：内层 AiChatResponse 不是对象")

    raw_replies = inner.get("data")
    # 单条 dict 返回时包成 list
    if isinstance(raw_replies, dict):
        raw_replies = [raw_replies]
    if raw_replies is None:
        raw_replies = []
    if not isinstance(raw_replies, list):
        raise ServiceError(
            "响应结构异常：AiChatResponse.data 不是列表（实际类型 {}，其它 keys={}）".format(
                type(raw_replies).__name__, list(inner.keys())
            )
        )

    replies: List[Dict[str, Any]] = []
    for item in raw_replies:
        if not isinstance(item, dict):
            continue
        action_type = item.get("actionType") or ""
        message = item.get("message") or ""
        replies.append({
            "thought": item.get("thought") or "",
            "action_type": action_type,
            "action_label": _ACTION_TYPE_LABEL.get(action_type, action_type or "未知"),
            "message": message,
            "derived_answer": derive_answer(action_type, message),
            "images": item.get("images") or [],
        })

    return {
        "query": query,
        "elapsed_seconds": round(time.time() - start_time, 1),
        "time_cost_ms": inner.get("timeCost") or "",
        "status": inner.get("status") or "",
        "instance_id": inner.get("instanceId") or "",
        "replies": replies,
    }


def format_chat_markdown(result: Dict[str, Any]) -> str:
    """将模拟对话结果格式化为 Markdown（不展示 instanceId 等系统内部 ID）"""
    query = result.get("query", "")
    replies = result.get("replies", [])
    time_cost = result.get("time_cost_ms", "")
    status = result.get("status", "")

    lines = ["## 模拟对话试答\n"]
    lines.append("**买家提问**：{}\n".format(query))

    meta_parts = []
    if status:
        meta_parts.append("状态 `{}`".format(status))
    if time_cost:
        meta_parts.append("耗时 `{} ms`".format(time_cost))
    if meta_parts:
        lines.append("> {}\n".format(" · ".join(meta_parts)))

    if not replies:
        lines.append("接待助手未给出回复。")
        return "\n".join(lines)

    for idx, r in enumerate(replies, 1):
        lines.append("### 回复 {} - {}\n".format(idx, r["action_label"]))
        if r["thought"]:
            lines.append("- **思考**：{}".format(r["thought"]))
        lines.append("- **拟答**：{}".format(r["derived_answer"]))
        if r["action_type"] == "answer" and r["images"]:
            lines.append("- **图片**：{} 张".format(len(r["images"])))
        lines.append("")

    return "\n".join(lines)
