from __future__ import annotations

import copy
import json
import re
from datetime import datetime, timezone, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from .errors import ConfigurationError, MappingError

TOKEN = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")
FULL_TOKEN = re.compile(r"^\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}$")
SHANGHAI_TZ = timezone(timedelta(hours=8))


def load_mapping(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ConfigurationError(
            f"缺少审批字段映射文件：{path}；请复制 config/approval_mapping.example.json"
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"无法读取审批字段映射：{exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("form"), list):
        raise ConfigurationError("字段映射必须是 JSON 对象，并包含 form 数组")
    return value


def _path_get(context: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = context
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            raise MappingError(f"字段映射引用了不存在的值：{dotted_path}")
        current = current[part]
    if current is None or current == "":
        raise MappingError(f"字段映射引用了空值：{dotted_path}")
    return current


def _path_present(context: Mapping[str, Any], dotted_path: str) -> bool:
    try:
        value = _path_get(context, dotted_path)
    except MappingError:
        return False
    return value is not None and value != ""


def _render(value: Any, context: Mapping[str, Any]) -> Any:
    if isinstance(value, dict):
        return {key: _render(child, context) for key, child in value.items()}
    if isinstance(value, list):
        return [_render(child, context) for child in value]
    if not isinstance(value, str):
        return value

    full_match = FULL_TOKEN.match(value)
    if full_match:
        return copy.deepcopy(_path_get(context, full_match.group(1)))

    def replace(match: re.Match[str]) -> str:
        return str(_path_get(context, match.group(1)))

    return TOKEN.sub(replace, value)


def invoice_context(
    invoice: Mapping[str, Any],
    expense_type_options: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """生成审批模板使用的发票字段和派生字段。"""

    result = dict(invoice)
    issue_date = invoice.get("issue_date")
    if issue_date:
        try:
            parsed = datetime.strptime(str(issue_date), "%Y-%m-%d").replace(
                tzinfo=SHANGHAI_TZ
            )
        except ValueError as exc:
            raise MappingError("开票日期不是 YYYY-MM-DD 格式") from exc
        result["issue_date_ms"] = str(int(parsed.timestamp() * 1000))
        result["issue_date_rfc3339"] = parsed.isoformat()

    for key in ("amount_excluding_tax", "tax_amount", "total_amount"):
        value = invoice.get(key)
        if value in (None, ""):
            continue
        try:
            decimal_value = Decimal(str(value))
            cents = (decimal_value * 100).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        except InvalidOperation as exc:
            raise MappingError(f"{key} 不是合法金额：{value}") from exc
        result[f"{key}_cents"] = str(cents)
        if key == "total_amount":
            # 飞书 formula 和 amount 控件需要 JSON 数字，而不是票面金额字符串。
            result["total_amount_number"] = float(decimal_value)

    items = invoice.get("items") or []
    item_summary = "；".join(
        str(item.get("name")) for item in items if item.get("name")
    )
    result["item_summary"] = item_summary
    result["expense_item_content"] = (
        item_summary
        or str(invoice.get("approval_summary") or "").strip()
        or str(invoice.get("seller_name") or "").strip()
        or "发票费用"
    )

    if expense_type_options is not None:
        expense_category = str(invoice.get("expense_category") or "").strip()
        if not expense_category:
            raise MappingError("Codex 未生成报销类型 expense_category")
        option_value = expense_type_options.get(expense_category)
        if option_value in (None, ""):
            raise MappingError(
                f"报销类型“{expense_category}”没有对应的飞书选项 ID"
            )
        result["expense_category_value"] = option_value

    return result


def missing_required_fields(
    invoice: Mapping[str, Any], required_fields: Iterable[str]
) -> List[str]:
    return [
        field
        for field in required_fields
        if field not in invoice or invoice[field] is None or invoice[field] == ""
    ]


def mapping_needs_upload(mapping: Mapping[str, Any], upload_type: str) -> bool:
    token = f"approval_file.{upload_type}_code"
    return token in json.dumps(mapping.get("form", []), ensure_ascii=False)


def render_form(mapping: Mapping[str, Any], context: Mapping[str, Any]) -> List[Any]:
    rendered: List[Any] = []
    for raw_item in mapping["form"]:
        if not isinstance(raw_item, dict):
            raise MappingError("form 中每一项都必须是对象")
        item = copy.deepcopy(raw_item)
        omit_path = item.pop("omit_if_missing", None)
        if omit_path is not None:
            if not isinstance(omit_path, str):
                raise MappingError("omit_if_missing 必须是点分路径字符串")
            if not _path_present(context, omit_path):
                continue
        rendered.append(_render(item, context))
    return rendered
