from __future__ import annotations

from typing import Any


TEMPLATE_NAMES: dict[str, str] = {
    "common": "通用业务蓝图模板",
    "retail": "零售行业模板",
    "finance": "金融行业模板",
    "manufacturing": "制造行业模板",
    "cross-border-ecommerce": "跨境电商 know-how 模板",
}


def resolve_template_name(template_id: str | None) -> str:
    if not template_id:
        return "未指定模板"
    normalized = template_id.strip()
    if not normalized:
        return "未指定模板"
    return TEMPLATE_NAMES.get(normalized, normalized)


def blueprint_template_name(meta: dict[str, Any]) -> str:
    template_name = meta.get("templateName")
    if isinstance(template_name, str) and template_name.strip():
        return template_name

    template_id = meta.get("templateId") or meta.get("industry")
    if isinstance(template_id, str):
        return resolve_template_name(template_id)
    return "未指定模板"
