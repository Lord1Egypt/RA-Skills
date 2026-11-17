"""发票销售方与税额勾稽风险检查。"""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Mapping, Optional

ORGANIZATION_NAME_MARKERS = (
    "公司",
    "集团",
    "有限责任",
    "股份",
    "厂",
    "店",
    "商行",
    "经营部",
    "服务部",
    "中心",
    "工作室",
    "事务所",
    "合作社",
    "协会",
    "研究院",
    "研究所",
    "学校",
    "医院",
    "银行",
    "局",
    "馆",
    "站",
)
SERVICE_ITEM_MARKERS = (
    "服务",
    "维修",
    "维护",
    "安装",
    "调试",
    "咨询",
    "设计",
    "开发",
    "租赁",
    "检测",
    "培训",
)
EQUIPMENT_ITEM_MARKERS = (
    "设备",
    "电脑",
    "计算机",
    "主机",
    "显示器",
    "打印机",
    "服务器",
    "硬件",
    "电子产品",
    "办公用品",
    "配件",
    "零部件",
    "仪器",
    "器材",
)
TAX_TOLERANCE = Decimal("0.02")


def _normalize(value: Any) -> str:
    normalized = unicodedata.normalize("NFKC", str(value or ""))
    return "".join(
        character
        for character in normalized
        if not character.isspace() and unicodedata.category(character) != "Cf"
    )


def _seller_name_is_individual(value: Any) -> bool:
    normalized = _normalize(value)
    if not normalized or any(marker in normalized for marker in ORGANIZATION_NAME_MARKERS):
        return False
    if normalized.startswith("个人"):
        return True
    return re.fullmatch(r"[\u3400-\u9fff]{2,4}", normalized) is not None


def _decimal_amount(value: Any) -> Optional[Decimal]:
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    if not text or "*" in text:
        return None
    cleaned = text.replace(",", "").replace("￥", "").replace("¥", "")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _tax_rate(value: Any) -> Optional[Decimal]:
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    if not text or "*" in text or text in {"免税", "不征税", "零税率"}:
        return None
    is_percent = text.endswith("%")
    if is_percent:
        text = text[:-1].strip()
    try:
        rate = Decimal(text)
    except InvalidOperation:
        return None
    if is_percent or rate > 1:
        rate /= Decimal("100")
    return rate if rate >= 0 else None


def _equipment_projects(invoice: Mapping[str, Any]) -> list[str]:
    project_names = []
    items = invoice.get("items") or []
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, Mapping):
                continue
            name = str(item.get("name") or "").strip()
            normalized = _normalize(name)
            if not normalized:
                continue
            is_service = any(marker in normalized for marker in SERVICE_ITEM_MARKERS)
            is_equipment = any(marker in normalized for marker in EQUIPMENT_ITEM_MARKERS)
            if is_equipment and not is_service:
                project_names.append(name)
    if not project_names and invoice.get("expense_category") == "设备":
        project_names.append("设备类项目")
    return list(dict.fromkeys(project_names))


def invoice_risk_reasons(invoice: Mapping[str, Any]) -> list[str]:
    """检查个人销售设备和税额勾稽风险；无风险时返回空列表。"""

    reasons: list[str] = []
    seller_name = str(invoice.get("seller_name") or "").strip()
    equipment_projects = _equipment_projects(invoice)
    if _seller_name_is_individual(seller_name) and equipment_projects:
        reasons.append(
            f"销售方“{seller_name}”疑似个人，但项目“{'、'.join(equipment_projects)}”"
            "属于设备类；个人销售方仅允许服务类项目"
        )

    invoice_tax_raw = invoice.get("tax_amount")
    invoice_tax_text = unicodedata.normalize(
        "NFKC", str(invoice_tax_raw or "")
    ).strip()
    invoice_tax = _decimal_amount(invoice_tax_raw)
    if "*" in invoice_tax_text:
        reasons.append("整票税额显示为“***”，无法核验税率与税额")
    elif invoice_tax is None:
        reasons.append("整票税额缺失或无法识别，无法核验税率与税额")
    elif invoice_tax == 0:
        reasons.append("整票税额为0，存在税务风险")

    items = invoice.get("items") or []
    parsed_item_taxes: list[Decimal] = []
    all_item_taxes_parsed = bool(items)
    if isinstance(items, list):
        for index, item in enumerate(items, start=1):
            if not isinstance(item, Mapping):
                all_item_taxes_parsed = False
                continue
            name = str(item.get("name") or f"第{index}项").strip()
            amount = _decimal_amount(item.get("amount"))
            rate = _tax_rate(item.get("tax_rate"))
            item_tax_text = unicodedata.normalize(
                "NFKC", str(item.get("tax_amount") or "")
            ).strip()
            item_tax = _decimal_amount(item.get("tax_amount"))
            if "*" in item_tax_text:
                reasons.append(f"项目“{name}”税额显示为“***”，无法核验")
                all_item_taxes_parsed = False
                continue
            if item_tax is None:
                reasons.append(f"项目“{name}”税额缺失或无法识别")
                all_item_taxes_parsed = False
                continue
            parsed_item_taxes.append(item_tax)
            if item_tax == 0:
                reasons.append(f"项目“{name}”税额为0，存在税务风险")
            if amount is None or rate is None:
                reasons.append(f"项目“{name}”缺少有效的不含税金额或税率，无法核验税额")
                continue
            expected_tax = (amount * rate).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if abs(expected_tax - item_tax) > TAX_TOLERANCE:
                reasons.append(
                    f"项目“{name}”税率与税额不对应："
                    f"不含税金额{amount} × 税率{item.get('tax_rate')} "
                    f"应约为{expected_tax}，票面税额为{item_tax}"
                )

    if (
        invoice_tax is not None
        and invoice_tax != 0
        and all_item_taxes_parsed
        and parsed_item_taxes
    ):
        item_tax_total = sum(parsed_item_taxes, Decimal("0"))
        if abs(item_tax_total - invoice_tax) > TAX_TOLERANCE:
            reasons.append(
                f"明细税额合计{item_tax_total}与整票税额{invoice_tax}不一致"
            )
    return list(dict.fromkeys(reasons))
