#!/usr/bin/env python3
"""拒绝签约服务 — 拒绝签署采购单"""

import json
from typing import List, Optional, Dict, Any

from _http import api_post
from _errors import ServiceError
from _const import SKILL_NAME, SKILL_VERSION, SITE


def _format_status(status: str) -> str:
    """将签约状态转换为中文"""
    status_map = {
        "SIGN_INIT": "签署初始化",
        "AUTHING": "核身中",
        "SIGNING": "签署中",
        "SIGN_SUCCESS": "签署成功",
        "SIGN_FAIL": "签署失败",
        "SIGN_EXPIRED": "签署过期"
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

    response_code = data.get("responseCode", "-")
    draft_no = data.get("draftNo", "-")
    contract_status = data.get("contractCurrentStatus", "-")

    parts: List[str] = ["## 拒绝签约结果"]

    if success:
        parts.append("✅ 拒绝签约成功")
    else:
        parts.append("❌ 拒绝签约失败")

    if draft_no:
        parts.append(f"- 采购单号: {draft_no}")
    if contract_status:
        parts.append(f"- 合同当前状态: {_format_status(contract_status)}")

    return "\n\n".join(parts)


def sign_reject(draft_no: str) -> dict:
    """
    拒绝签署采购单

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

    model = api_post("/api/SYT_SIGN_REJECT/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("操作异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
