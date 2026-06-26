#!/usr/bin/env python3
"""采购单列表服务 — 查询采购单列表、格式化"""

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


def _build_markdown(data: Dict[str, Any]) -> str:
    if not data:
        return "未返回数据。"

    success = data.get("success")
    if not success:
        return f"错误代码: {data.get('responseCode')}\n错误信息: {data.get('responseMessage')}"

    total_count = data.get("totalCount", 0)
    data_list = data.get("dataList", [])

    parts: List[str] = [f"## 采购单列表（共 {total_count} 条）"]

    if not data_list:
        parts.append("暂无采购单数据。")
        return "\n\n".join(parts)

    for item in data_list:
        draft_no = item.get("draftNo", "-")
        status = _format_status(item.get("status", "-"))
        drafter_role = _format_role(item.get("drafterRole", "-"))
        seller_name = item.get("sellerName", "-")
        buyer_name = item.get("buyerName", "-")
        amount = item.get("amount")

        parts.append(f"### 单号: {draft_no}")
        parts.append(f"- 状态: {status}")
        parts.append(f"- 起草方: {drafter_role}")
        parts.append(f"- 卖家: {seller_name}")
        parts.append(f"- 买家: {buyer_name}")
        if amount is not None:
            parts.append(f"- 金额: {amount} 元")

    return "\n\n".join(parts)


def query_contract_list(contract_role: str, page_index: int = 1, page_size: int = 10) -> dict:
    """
    查询采购单列表

    Args:
        contract_role: 角色，BUYER 或 SELLER
        page_index: 页码，默认 1
        page_size: 每页条数，默认 10

    Returns:
        {"success": bool, "markdown": str, "data": dict}

    Raises:
        ValueError: 参数不合法
        SkillError 子类: API 调用失败
    """
    if contract_role not in ("BUYER", "SELLER"):
        raise ValueError("contract_role 必须是 BUYER 或 SELLER")

    body = {
        "site": SITE,
        "skillName": SKILL_NAME,
        "skillVersion": SKILL_VERSION,
        "contractType": "PURCHASE_ORDER",
        "contractRole": contract_role,
        "pageSize": page_size,
        "pageIndex": page_index
    }

    model = api_post("/api/SYT_PAGE_QUERY_CONTRACT/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("查询异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
