#!/usr/bin/env python3
"""确认收货服务 — 买家确认收货"""

import json
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    if not success:
        code = data.get("responseCode", "-")
        msg = data.get("responseMessage", "未知错误")
        return f"错误代码: {code}\n错误信息: {msg}"

    draft_no = data.get("draftNo", "-")

    parts: List[str] = ["## 确认收货结果"]
    if success:
        parts.append(f"✅ 确认收货成功")
    else:
        parts.append(f"❌ 确认收货失败")
    if draft_no:
        parts.append(f"- 采购单号: {draft_no}")

    return "\n\n".join(parts)


def confirm_receipt(draft_no: str) -> dict:
    """
    买家确认收货

    Args:
        draft_no: 采购单号

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

    model = api_post("/api/SYT_CONFIRM/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("操作异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
