"""Step4: query and normalize Amazon category attributes from Dianxiaobao."""
from __future__ import annotations

import os
import re
import sys
from collections.abc import Iterable
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import DEFAULT_MARKETPLACE_ID, DXB_BASE, dump, env, post


ATTRIBUTE_GROUPS = (
    ("attributesList", "PRODUCT_PROPERTY"),
    ("tradeAttributeList", "TRADE_ATTRIBUTE"),
    ("packageAttributeList", "PACKAGE_ATTRIBUTE"),
    ("safetyAndComplianceContentList", "SAFETY_AND_COMPLIANCE"),
)

REQUIRED_MODE_HARD = "hard"
REQUIRED_MODE_EVALUATED = "evaluated"
REQUIRED_MODE_CONDITIONAL = "conditional"
REQUIRED_MODE_ALL = "all"
REQUIRED_MODE_DEFAULT = REQUIRED_MODE_EVALUATED
VALID_REQUIRED_MODES = {REQUIRED_MODE_HARD, REQUIRED_MODE_EVALUATED, REQUIRED_MODE_CONDITIONAL, REQUIRED_MODE_ALL}


def _as_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _pick_language_node(data: dict, language: str = "en") -> dict:
    inner = _as_dict(data.get("data") or data)
    if language in inner and isinstance(inner[language], dict):
        return inner[language]
    for fallback in ("en", "cn"):
        if fallback in inner and isinstance(inner[fallback], dict):
            return inner[fallback]
    return inner


def _schema_groups(node: dict) -> dict[str, tuple[str, dict]]:
    groups: dict[str, tuple[str, dict]] = {}
    for group_name, attr_type in ATTRIBUTE_GROUPS:
        for attr_id, schema in _as_dict(node.get(group_name)).items():
            if isinstance(schema, dict):
                groups[attr_id] = (attr_type, schema)
    return groups


def _nested_required_fields(schema: dict) -> list[str]:
    fields: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            required = value.get("required")
            if isinstance(required, list):
                fields.update(str(item) for item in required if isinstance(item, str))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(schema.get("items") or schema)
    return sorted(fields)


def _enum_values(schema: dict) -> list[str]:
    values: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            enum = value.get("enum")
            if isinstance(enum, list):
                values.update(str(item) for item in enum if isinstance(item, (str, int, float)))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(schema)
    return sorted(values)


def _iter_then_blocks(value: Any) -> Iterable[dict]:
    if isinstance(value, dict):
        then_block = value.get("then")
        if isinstance(then_block, dict):
            yield then_block
        for child in value.values():
            yield from _iter_then_blocks(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_then_blocks(child)


def _iter_then_rules(value: Any, path: str = "allOfObj") -> Iterable[tuple[str, dict]]:
    if isinstance(value, dict):
        if isinstance(value.get("then"), dict):
            yield path, value
        for key, child in value.items():
            yield from _iter_then_rules(child, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_then_rules(child, f"{path}[{index}]")


def _normalize_required_mode(mode: str | None) -> str:
    normalized = (mode or REQUIRED_MODE_DEFAULT).lower().strip()
    if normalized not in VALID_REQUIRED_MODES:
        raise ValueError(f"Unsupported Amazon required mode: {mode}. Expected one of {sorted(VALID_REQUIRED_MODES)}")
    return normalized


def _matches_schema(value: Any, schema: Any) -> bool:
    """Evaluate the JSON-schema subset used by Amazon allOfObj.if blocks."""
    if not isinstance(schema, dict):
        return True

    if "allOf" in schema and not all(_matches_schema(value, child) for child in _as_list(schema.get("allOf"))):
        return False
    if "anyOf" in schema and not any(_matches_schema(value, child) for child in _as_list(schema.get("anyOf"))):
        return False
    if "oneOf" in schema and sum(1 for child in _as_list(schema.get("oneOf")) if _matches_schema(value, child)) != 1:
        return False
    if "not" in schema and _matches_schema(value, schema.get("not")):
        return False

    required = schema.get("required")
    if isinstance(required, list):
        if not isinstance(value, dict):
            return False
        for key in required:
            if key not in value:
                return False

    properties = schema.get("properties")
    if isinstance(properties, dict):
        if not isinstance(value, dict):
            return False
        for key, child_schema in properties.items():
            if key in value and not _matches_schema(value[key], child_schema):
                return False

    contains = schema.get("contains")
    if isinstance(contains, dict):
        if not isinstance(value, list):
            return False
        if not any(_matches_schema(item, contains) for item in value):
            return False

    items = schema.get("items")
    if isinstance(items, dict) and isinstance(value, list):
        if not all(_matches_schema(item, items) for item in value):
            return False

    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        return False

    const = schema.get("const")
    if "const" in schema and value != const:
        return False

    return True


def _normalize_condition_contexts(condition_contexts: list[dict] | dict | None) -> list[dict]:
    if condition_contexts is None:
        return []
    if isinstance(condition_contexts, dict):
        return [condition_contexts]
    return [context for context in condition_contexts if isinstance(context, dict)]


def _condition_matches(if_schema: Any, condition_contexts: list[dict]) -> bool:
    if if_schema is None:
        return True
    return any(_matches_schema(context, if_schema) for context in condition_contexts)


def _context_with_variation(variation_theme: str) -> dict:
    context: dict[str, Any] = {}
    if variation_theme:
        context["variation_theme"] = [{"name": variation_theme}]
    return context


VARIATION_NAME_ALIASES = {
    "colour": "color",
    "applicable_model": "compatible_phone_models",
    "applicable_models": "compatible_phone_models",
    "compatible_model": "compatible_phone_models",
    "compatible_models": "compatible_phone_models",
    "phone_model": "compatible_phone_models",
    "phone_models": "compatible_phone_models",
}


def _safe_variation_name(name: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_]+", "_", str(name or "").lower()).strip("_") or "style"
    return VARIATION_NAME_ALIASES.get(safe_name, safe_name)


def _variation_theme_from_names(names: list[str]) -> str:
    return "/".join(name.upper() for name in names if name)


def _infer_variation_theme_from_offer(offer_info: dict) -> str:
    sku_rows = offer_info.get("skuList") if isinstance(offer_info.get("skuList"), list) else []
    if len(sku_rows) <= 1:
        return ""
    variation_names: list[str] = []
    variation_values: dict[str, set[str]] = {}
    for sku in sku_rows:
        specs = sku.get("specs", []) if isinstance(sku, dict) else []
        for spec in specs:
            name = _safe_variation_name(spec.get("nameTrans") or spec.get("name") or "variation")
            value = str(spec.get("valueTrans") or spec.get("value") or "").strip()
            if name not in variation_names:
                variation_names.append(name)
            variation_values.setdefault(name, set()).add(value)
    varying_names = [name for name in variation_names if len(variation_values.get(name, set())) > 1]
    selected_names = varying_names or variation_names[:2]
    return _variation_theme_from_names(selected_names[:2])


def _select_condition_variation_theme(offer_info: dict, variation_theme: str | None) -> str:
    if variation_theme is not None:
        return variation_theme
    inferred_theme = _infer_variation_theme_from_offer(offer_info)
    configured_theme = env("AMAZON_VARIATION_THEME")
    if configured_theme:
        configured_theme = configured_theme.strip()
        if configured_theme.upper() == "STYLE" and inferred_theme and inferred_theme != "STYLE":
            return inferred_theme
        return configured_theme
    return inferred_theme


def build_amazon_condition_contexts(
    offer_info: dict | None = None,
    *,
    variation_theme: str | None = None,
    parent_sku: str | None = None,
) -> list[dict]:
    """Build listing contexts used to evaluate Amazon conditional required rules."""
    offer_info = offer_info or {}
    variation_theme = _select_condition_variation_theme(offer_info, variation_theme)
    sku_rows = offer_info.get("skuList") if isinstance(offer_info.get("skuList"), list) else []
    parent_sku = parent_sku or f"PARENT-{offer_info.get('offerId') or '1688'}"

    contexts = [_context_with_variation(variation_theme)]
    if len(sku_rows) <= 1:
        return contexts

    parent_context = _context_with_variation(variation_theme)
    parent_context["parentage_level"] = [{"value": "parent"}]
    contexts.append(parent_context)

    for _sku in sku_rows:
        child_context = _context_with_variation(variation_theme)
        child_context["parentage_level"] = [{"value": "child"}]
        child_context["child_parent_sku_relationship"] = [{"parent_sku": parent_sku}]
        contexts.append(child_context)

    return contexts


def _required_level(sources: set[str]) -> str:
    if any(source.endswith(".required") and not source.startswith("allOfObj.") for source in sources):
        return REQUIRED_MODE_HARD
    if any(source.startswith("allOfObj") and source.endswith(".then.required") for source in sources):
        return REQUIRED_MODE_CONDITIONAL
    return "conditional_property"


def _required_attribute_ids(
    node: dict,
    known_attrs: set[str],
    required_mode: str = REQUIRED_MODE_DEFAULT,
    condition_contexts: list[dict] | dict | None = None,
) -> dict[str, set[str]]:
    required_mode = _normalize_required_mode(required_mode)
    condition_contexts = _normalize_condition_contexts(condition_contexts)
    required: dict[str, set[str]] = {}

    for group_name, _ in ATTRIBUTE_GROUPS:
        for attr_id, schema in _as_dict(node.get(group_name)).items():
            if isinstance(schema, dict) and schema.get("required") is True:
                required.setdefault(attr_id, set()).add(f"{group_name}.required")

    if required_mode == REQUIRED_MODE_HARD:
        return required

    if required_mode == REQUIRED_MODE_EVALUATED:
        for path, rule in _iter_then_rules(node.get("allOfObj") or []):
            if not _condition_matches(rule.get("if"), condition_contexts):
                continue
            then_block = _as_dict(rule.get("then"))
            for attr_id in then_block.get("required") or []:
                if attr_id in known_attrs:
                    required.setdefault(attr_id, set()).add(f"{path}.then.required")
        return required

    for then_block in _iter_then_blocks(node.get("allOfObj") or []):
        for attr_id in then_block.get("required") or []:
            if attr_id in known_attrs:
                required.setdefault(attr_id, set()).add("allOfObj.then.required")
        if required_mode != REQUIRED_MODE_ALL:
            continue
        for attr_id in _as_dict(then_block.get("properties")).keys():
            if attr_id in known_attrs:
                required.setdefault(attr_id, set()).add("allOfObj.then.properties")

    return required


def _attribute_entry(attr_id: str, attr_type: str, schema: dict, sources: set[str]) -> dict:
    title = schema.get("title") or schema.get("name") or attr_id
    entry = {
        "attributeId": attr_id,
        "attributeName": title,
        "name": attr_id,
        "title": title,
        "type": attr_type,
        "required": True,
        "is_required": True,
        "requiredLevel": _required_level(sources),
        "sources": sorted(sources),
        "description": schema.get("description", ""),
        "examples": schema.get("examples", []),
        "selectors": schema.get("selectors", []),
        "valueType": schema.get("type", ""),
        "requiredSubFields": _nested_required_fields(schema),
        "enumValues": _enum_values(schema),
        "schema": schema,
    }
    return entry


def compact_required_attrs(attrs: list[dict]) -> list[dict]:
    """Build the lighter requiredPv payload passed to the CPV mapping API."""
    compact_attrs = []
    for attr in attrs:
        compact_attrs.append(
            {
                "attributeId": attr.get("attributeId"),
                "attributeName": attr.get("attributeName"),
                "name": attr.get("name"),
                "title": attr.get("title"),
                "type": attr.get("type"),
                "required": True,
                "is_required": True,
                "requiredLevel": attr.get("requiredLevel", REQUIRED_MODE_HARD),
                "description": attr.get("description", ""),
                "examples": attr.get("examples", []),
                "selectors": attr.get("selectors", []),
                "valueType": attr.get("valueType", ""),
                "requiredSubFields": attr.get("requiredSubFields", []),
                "sources": attr.get("sources", []),
            }
        )
    return compact_attrs


def parse_amazon_schema(
    data: dict,
    language: str = "en",
    required_mode: str = REQUIRED_MODE_DEFAULT,
    condition_contexts: list[dict] | dict | None = None,
) -> dict:
    """Normalize Dianxiaobao's Amazon schema response.

    Amazon returns JSON-schema-like nodes under data.<lang>.*.  This parser keeps
    the original field schema and extracts the minimum required attributes for
    the current listing context. By default it evaluates conditional allOf/then
    rules; hard mode is kept only for explicit 11-field diagnostics.
    """
    required_mode = _normalize_required_mode(required_mode)
    if required_mode == REQUIRED_MODE_EVALUATED and condition_contexts is None:
        condition_contexts = build_amazon_condition_contexts()
    condition_contexts = _normalize_condition_contexts(condition_contexts)
    node = _pick_language_node(data, language)
    groups = _schema_groups(node)
    required_ids = _required_attribute_ids(node, set(groups.keys()), required_mode, condition_contexts)
    required_attrs = [
        _attribute_entry(attr_id, groups[attr_id][0], groups[attr_id][1], sources)
        for attr_id, sources in sorted(required_ids.items())
        if attr_id in groups
    ]
    variation_theme = _as_dict(_as_dict(node.get("tradeAttributeList")).get("variation_theme"))
    return {
        "language": language if language in _as_dict(data.get("data") or data) else node.get("languageTagStr", language),
        "requiredMode": required_mode,
        "conditionContextCount": len(condition_contexts),
        "marketplaceId": node.get("marketplaceIdStr", ""),
        "attributes": {attr_id: schema for attr_id, (_, schema) in groups.items()},
        "requiredAttrs": required_attrs,
        "variationThemes": _enum_values(variation_theme),
        "raw": data,
    }


def get_amazon_attrs(
    encrypted_code: str,
    store_name: str,
    product_type: str,
    marketplace_id: str | None = None,
    required_mode: str | None = None,
    condition_contexts: list[dict] | dict | None = None,
) -> list[dict]:
    marketplace_id = marketplace_id or env("AMAZON_MARKETPLACE_ID", DEFAULT_MARKETPLACE_ID)
    required_mode = required_mode or env("AMAZON_REQUIRED_ATTR_MODE", REQUIRED_MODE_DEFAULT)
    payload = {
        "userCode": encrypted_code,
        "storeName": store_name,
        "marketplaceId": marketplace_id,
        "productType": product_type,
        "ptName": "amazon",
    }
    data = post(f"{DXB_BASE}/api-goods/aboutProduct/getAttrInfoByCateIdToOut", payload, timeout=90)
    parsed = parse_amazon_schema(data, required_mode=required_mode, condition_contexts=condition_contexts)
    return compact_required_attrs(parsed["requiredAttrs"])


if __name__ == "__main__":
    if len(sys.argv) >= 2 and os.path.isdir(sys.argv[1]):
        from scripts.common import read_session, write_session

        session_dir = sys.argv[1]
        user = read_session(session_dir, "query_user_info.json", required_keys=["encryptedCode", "storeName"])
        category = read_session(session_dir, "map_category.json", required_keys=["productType"])
        offer = read_session(session_dir, "query_offer.json")
        run_input = read_session(session_dir, "input.json")
        mode = sys.argv[2] if len(sys.argv) >= 3 else None
        condition_contexts = build_amazon_condition_contexts(offer)
        required_attrs = get_amazon_attrs(
            user["encryptedCode"],
            user["storeName"],
            category["productType"],
            run_input.get("marketplace_id") or DEFAULT_MARKETPLACE_ID,
            required_mode=mode,
            condition_contexts=condition_contexts,
        )
        result = {
            "requiredMode": mode or env("AMAZON_REQUIRED_ATTR_MODE", REQUIRED_MODE_DEFAULT),
            "conditionContexts": condition_contexts,
            "requiredAttrs": required_attrs,
        }
        write_session(session_dir, "map_amazon_attrs.json", result)
        print(dump(result))
    elif len(sys.argv) < 4:
        print(
            "Usage: python scripts/map_amazon_attrs.py <session_dir> OR <encryptedCode> <storeName> <productType> [evaluated|hard|conditional|all]",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        mode = sys.argv[4] if len(sys.argv) >= 5 else None
        print(dump(get_amazon_attrs(sys.argv[1], sys.argv[2], sys.argv[3], required_mode=mode)))
