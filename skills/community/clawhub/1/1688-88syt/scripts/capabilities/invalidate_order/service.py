#!/usr/bin/env python3
"""采购单失效服务 — 将采购单标记为失效"""

import json
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    response_code = data.get("responseCode", "-")
    response_msg = data.get("responseMessage", "")

    parts: List[str] = ["## 采购单失效结果"]

    if success:
        parts.append("✅ 采购单已成功标记为失效")
    else:
        parts.append("❌ 采购单失效失败")
        if response_msg:
            parts.append(f"- 错误信息: {response_msg}")

    return "\n\n".join(parts)


def invalidate_order(draft_no: str) -> dict:
    """
    将采购单标记为失效

    Args:
        draft_no: 采购单合同号

    Returns:
        {"success": bool, "markdown": str, "data": dict}

    Raises:
        ValueError: 参数不合法
        SkillError 子类: API 调用失败
    """
    if not draft_no:
        raise ValueError("draft_no 不能为空")

    body = {
        "site": SITE,
        "skillName": SKILL_NAME,
        "skillVersion": SKILL_VERSION,
        "draftNo": draft_no
    }

    model = api_post("/api/SYT_INVALID/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("操作异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
