#!/usr/bin/env python3
"""采购单详情服务 — 查询采购单详情、格式化"""

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


def _format_role(role: str) -> str:
    """将角色转换为中文"""
    role_map = {
        "BUYER": "买家",
        "SELLER": "卖家"
    }
    return role_map.get(role, role)


def _format_type(type_str: str) -> str:
    """将类型转换为中文"""
    type_map = {
        "PERSONAL": "个人",
        "COMPANY": "企业"
    }
    return type_map.get(type_str, type_str)


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    if not success:
        code = data.get("responseCode", "-")
        msg = data.get("responseMessage", "未知错误")
        return f"错误代码: {code}\n错误信息: {msg}"

    contract = data.get("contract", {})

    if not contract:
        return "未找到采购单详情。"

    draft_no = contract.get("draftNo", "-")
    status = _format_status(contract.get("status", "-"))
    drafter_role = _format_role(contract.get("drafterRole", "-"))
    drafter_type = _format_type(contract.get("drafterType", "-"))
    buyer_type = _format_type(contract.get("buyerType", "-"))
    seller_type = _format_type(contract.get("sellerType", "-"))
    buyer_name = contract.get("buyerName", "-")
    seller_name = contract.get("sellerName", "-")
    amount = contract.get("amount")

    parts: List[str] = [f"## 采购单详情"]
    parts.append(f"- 单号: {draft_no}")
    parts.append(f"- 状态: {status}")
    parts.append(f"- 起草方: {drafter_role} ({drafter_type})")
    parts.append(f"- 买家: {buyer_name} ({buyer_type})")
    parts.append(f"- 卖家: {seller_name} ({seller_type})")
    if amount is not None:
        parts.append(f"- 金额: {amount} 元")

    return "\n\n".join(parts)


def query_contract_detail(draft_no: str) -> dict:
    """
    查询采购单详情

    Args:
        draft_no: 采购单号（交易单号，88SYT 开头）

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

    model = api_post("/api/SYT_QUERY_CONTRACT/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("查询异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
