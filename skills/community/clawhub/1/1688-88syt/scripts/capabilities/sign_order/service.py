#!/usr/bin/env python3
"""采购单签署服务 — 确认/签署采购单"""

import json
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _format_status(status: str) -> str:
    """将状态码转换为中文"""
    status_map = {
        "DRAFT": "起草中",
        "DATA_SUPPLYING": "起草中",
        "SIGNING": "确认中",
        "SIGN_REJECT": "已拒绝",
        "PAYING": "待支付",
        "PAID": "已支付",
        "SHIPPED": "已发货",
        "COMPLETED": "已完成",
        "CANCELLED": "已取消",
        "INVALID": "已失效"
    }
    return status_map.get(status, status)


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    if not success:
        code = data.get("responseCode", "-")
        msg = data.get("responseMessage", "未知错误")
        return f"错误代码: {code}\n错误信息: {msg}"

    draft_no = data.get("draftNo", "-")
    contract_status = data.get("contractCurrentStatus", "-")

    parts: List[str] = ["## 采购单签署结果"]
    if success:
        parts.append("✅ 采购单签署成功")
    else:
        parts.append("❌ 采购单签署失败")
    if draft_no:
        parts.append(f"- 采购单号: {draft_no}")
    if contract_status:
        parts.append(f"- 当前状态: {_format_status(contract_status)}")

    return "\n\n".join(parts)


def sign_order(draft_no: str) -> dict:
    """
    签署/确认采购单

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

    model = api_post("/api/SYT_SIGN/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("操作异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
