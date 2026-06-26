#!/usr/bin/env python3
"""创建采购单服务 — 创建采购单、格式化"""

import json
from typing import List, Optional, Dict, Any
from decimal import Decimal, ROUND_HALF_UP

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
    contract_status = data.get("contractCurrentStatus", "-")

    parts: List[str] = ["## 创建采购单结果"]
    parts.append(f"- 创建状态: {'成功' if success else '失败'}")
    if draft_no:
        parts.append(f"- 采购单号: {draft_no}")
    if contract_status:
        parts.append(f"- 当前状态: {contract_status}")

    return "\n\n".join(parts)


def create_purchase_order(
    draft_role: str,
    counterparty_name: str,
    purchase_items: List[Dict[str, Any]]
) -> dict:
    """
    创建采购单

    Args:
        draft_role: 起草方角色，BUYER 或 SELLER
        counterparty_name: 对方 1688 会员登录名
        purchase_items: 采购清单，每项包含 productName, quantity, unitPrice, productSpec(可选)

    Returns:
        {"success": bool, "markdown": str, "data": dict}

    Raises:
        ValueError: 参数不合法
        SkillError 子类: API 调用失败
    """
    if draft_role not in ("BUYER", "SELLER"):
        raise ValueError("draft_role 必须是 BUYER 或 SELLER")

    if not counterparty_name:
        raise ValueError("counterparty_name 不能为空")

    if not purchase_items or len(purchase_items) == 0:
        raise ValueError("purchase_items 不能为空")

    # 处理对方登录名（移除空格）
    counterparty_name = counterparty_name.replace(" ", "")

    # 构建采购单项列表
    item_list = []
    total_amount = Decimal("0")

    for idx, item in enumerate(purchase_items):
        product_name = item.get("productName", "").strip()
        quantity = item.get("quantity")
        unit_price = item.get("unitPrice")
        product_spec = item.get("productSpec", "").strip()

        if not product_name:
            raise ValueError(f"第 {idx + 1} 项商品名称不能为空")

        try:
            qty = int(quantity)
            if qty < 1:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"第 {idx + 1} 项商品数量必须是大于等于 1 的整数")

        try:
            price = Decimal(str(unit_price))
            if price < Decimal("0.001"):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"第 {idx + 1} 项商品单价必须是大于等于 0.001 的数字")

        # 计算小计
        subtotal = (Decimal(str(qty)) * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        item_dict = {
            "productName": product_name,
            "quantity": qty,
            "unitPrice": str(price),
            "subtotal": str(subtotal),
            "class": "com.alibaba.fin.agent.skill.tools.provider.syt.dto.PurchaseItemDTO"
        }
        if product_spec:
            item_dict["productSpec"] = product_spec

        item_list.append(item_dict)
        total_amount += subtotal

    # 校验总金额
    if total_amount < Decimal("0.01"):
        raise ValueError("采购单总金额不能低于 0.01 元，请调整商品数量或单价")

    body = {
        "site": SITE,
        "skillName": SKILL_NAME,
        "skillVersion": SKILL_VERSION,
        "draftRole": draft_role,
        "contractType": "PURCHASE_ORDER",
        "counterpartyOrigin": "LOGIN_ID_1688_MATCH",
        "counterpartyName": counterparty_name,
        "purchaseItemList": item_list
    }

    model = api_post("/api/SYT_DRAFT/1.0.0", body, timeout=10)
    if not isinstance(model, dict):
        raise ServiceError("创建异常，请稍后重试")

    markdown = _build_markdown(model)
    return {"success": model.get("success"), "markdown": markdown, "data": model}
