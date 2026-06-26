"""Step6: build Dianxiaobao Amazon listing payload."""
from __future__ import annotations

import json
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts.common import DEFAULT_LANGUAGE_TAG, DEFAULT_MARKETPLACE_ID, dump, env, first_present

DEFAULT_INVENTORY_QUANTITY = "1"


def _strip_chinese(value: str) -> str:
    value = re.sub(r"[\u4e00-\u9fff]+", " ", value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _safe_title(title: str) -> str:
    cleaned = _strip_chinese(title)
    return cleaned[:180] or "1688 sourced product"


def _price(value: str | int | float | Decimal, multiplier: Decimal = Decimal("1.00")) -> str:
    amount = Decimal(str(value or "0")) * multiplier
    offset = env("AMAZON_PRICE_OFFSET")
    if offset:
        amount += Decimal(str(offset))
    return str(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _json_string(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = env(name)
    if not raw:
        return default
    return raw.lower() in {"1", "true", "yes", "y"}


def _env_int(name: str, default: int) -> int:
    raw = env(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _inventory_quantity() -> str:
    raw = env("AMAZON_INVENTORY_QUANTITY", DEFAULT_INVENTORY_QUANTITY)
    try:
        quantity = int(str(raw).strip())
    except ValueError as exc:
        raise ValueError(f"AMAZON_INVENTORY_QUANTITY must be a positive integer, got {raw!r}") from exc
    if quantity < 1:
        raise ValueError(f"AMAZON_INVENTORY_QUANTITY must be >= 1, got {quantity}")
    return str(quantity)


def _json_env(name: str, default) -> str:
    raw = env(name)
    if not raw:
        return _json_string(default)
    try:
        json.loads(raw)
    except json.JSONDecodeError:
        return _json_string(raw)
    return raw


def _named_value(prefix: str, *, default_name: str = "", default_value: str = "") -> dict:
    return {
        "id": env(f"{prefix}_ID"),
        "name": env(f"{prefix}_NAME", default_name),
        "value": env(f"{prefix}_VALUE", default_value),
    }


def _listing_marker() -> str:
    marker = env("AMAZON_LISTING_MARKER")
    marker = re.sub(r"[^A-Za-z0-9._-]+", "-", marker).strip("-")
    return marker[:32]


def _title_with_marker(title: str, marker: str) -> str:
    if not marker:
        return title
    suffix = f" {marker}"
    if title.endswith(suffix):
        return title
    return f"{title[:180 - len(suffix)]}{suffix}"


def _seller_sku(raw: str, idx: int, seen: set[str]) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]+", "-", raw or f"SKU-{idx + 1}").strip("-") or f"SKU-{idx + 1}"
    marker = _listing_marker()
    if marker:
        base = f"{base}-{marker}"
    sku = base
    if sku in seen:
        sku = f"{base}-{idx + 1}"
    seen.add(sku)
    return sku


NO_LANGUAGE_TAG_ATTRS = {
    "chain_length",
    "cpsia_cautionary_statement",
    "fulfillment_availability",
    "item_display_weight",
    "item_length_width",
    "item_package_dimensions",
    "item_package_weight",
    "item_weight",
    "jewelry_material_categorization",
    "list_price",
    "part_number",
    "variation_theme",
}

HARD_REQUIRED_CAT_PROP_IDS = {
    "cpsia_cautionary_statement",
    "jewelry_material_categorization",
    "list_price",
    "number_of_items",
    "stones",
}

CONDITIONAL_CAT_PROP_FALLBACKS = {
    "clasp_type",
    "color",
    "department",
    "fulfillment_availability",
    "gem_type",
    "item_package_dimensions",
    "item_package_weight",
    "material",
    "part_number",
    "size",
    "style",
    "variation_theme",
}

VARIATION_NAME_ALIASES = {
    "colour": "color",
    "applicable_model": "compatible_phone_models",
    "applicable_models": "compatible_phone_models",
    "compatible_model": "compatible_phone_models",
    "compatible_models": "compatible_phone_models",
    "phone_model": "compatible_phone_models",
    "phone_models": "compatible_phone_models",
}


def _amazon_attr_entry(key: str, value, marketplace_id: str, language_tag: str, currency: str) -> dict:
    if isinstance(value, dict):
        entry = dict(value)
        entry.setdefault("marketplace_id", marketplace_id)
        return entry
    entry = {"marketplace_id": marketplace_id, "value": value}
    if isinstance(value, str) and key not in NO_LANGUAGE_TAG_ATTRS:
        entry["language_tag"] = language_tag
    if key == "list_price" or isinstance(value, (int, float, Decimal)):
        entry["currency"] = currency
    return entry


def _is_present(value) -> bool:
    if isinstance(value, str) and value.strip().upper() == "NONE":
        return False
    return value not in (None, "", [], {})


def _include_conditional_attrs() -> bool:
    if _env_bool("AMAZON_INCLUDE_CONDITIONAL_ATTRS", False):
        return True
    return env("AMAZON_REQUIRED_ATTR_MODE", "evaluated").lower() in {"evaluated", "conditional", "all"}


def _ascii_or(value: str, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = _strip_chinese(str(value))
    return cleaned if cleaned else fallback


def _normalize_common_value(key: str, value: str) -> str:
    replacements = {
        "彩色": "Multicolor",
        "锆石": "Cubic Zirconia",
        "串珠链": "Beaded Chain",
        "Fashion": "fashion",
        "Fine": "fine",
        "No Warning Applicable": "no_warning_applicable",
    }
    if value in replacements:
        return replacements[value]
    if key in {"color"}:
        return _ascii_or(value, "Multicolor")
    if key in {"gem_type"}:
        return _ascii_or(value, "Cubic Zirconia")
    if key in {"chain_type"}:
        return _ascii_or(value, "Beaded Chain")
    if key in {"department"}:
        return _ascii_or(value, "Women's")
    if key in {"material"}:
        return _ascii_or(value, "Metal")
    if key in {"style"}:
        return _ascii_or(value, "Fashion")
    if key in {"part_number"}:
        return _ascii_or(value, env("AMAZON_PART_NUMBER", "DMS-00422"))
    return value


def _number_from_text(value, default: str | int | float | Decimal = "0") -> float:
    numbers = re.findall(r"\d+(?:\.\d+)?", str(value or ""))
    if len(numbers) >= 2:
        amount = (Decimal(numbers[0]) + Decimal(numbers[1])) / Decimal("2")
    elif numbers:
        amount = Decimal(numbers[0])
    else:
        amount = Decimal(str(default or "0"))
    return float(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _unit_from_text(raw_value, default: str, aliases: dict[str, str]) -> str:
    text = str(raw_value or "").lower()
    for needle, unit in aliases.items():
        if needle in text:
            return unit
    return default


def _dimension_unit_from_text(raw_value, default: str) -> str:
    return _unit_from_text(
        raw_value,
        default,
        {
            "centimeter": "centimeters",
            "cm": "centimeters",
            "inch": "inches",
            "inches": "inches",
            "feet": "feet",
            "foot": "feet",
            "meter": "meters",
            "millimeter": "millimeters",
            "mm": "millimeters",
            "yard": "yards",
        },
    )


def _list_price_value(raw_value, sku_prices: list[dict]) -> float:
    override = env("AMAZON_LIST_PRICE")
    if override:
        return _number_from_text(override)
    max_sku_price = max((Decimal(str(row.get("price") or "0")) for row in sku_prices), default=Decimal("0"))
    multiplier = Decimal(env("AMAZON_LIST_PRICE_MULTIPLIER", "1.25") or "1.25")
    fallback = (max_sku_price * multiplier).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    raw_amount = Decimal(str(_number_from_text(raw_value))) if _is_present(raw_value) else Decimal("0")
    amount = max(raw_amount, fallback)
    return float(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _list_price_cat_prop(raw_value, sku_prices: list[dict], marketplace_id: str, currency: str) -> list[dict]:
    return [
        {
            "marketplace_id": marketplace_id,
            "currency": currency,
            "value": _list_price_value(raw_value, sku_prices),
        }
    ]


def _package_dimensions_cat_prop(raw_value, marketplace_id: str) -> list[dict]:
    values = re.findall(r"\d+(?:\.\d+)?", str(raw_value or ""))
    length = _number_from_text(values[0] if len(values) > 0 else "", env("AMAZON_PACKAGE_LENGTH", "10"))
    width = _number_from_text(values[1] if len(values) > 1 else "", env("AMAZON_PACKAGE_WIDTH", "10"))
    height = _number_from_text(values[2] if len(values) > 2 else "", env("AMAZON_PACKAGE_HEIGHT", "10"))
    unit = _dimension_unit_from_text(raw_value, env("AMAZON_DIMENSION_UNIT", "centimeters"))
    return [
        {
            "marketplace_id": marketplace_id,
            "length": {"unit": unit, "value": length},
            "width": {"unit": unit, "value": width},
            "height": {"unit": unit, "value": height},
        }
    ]


def _item_length_width_cat_prop(raw_value, marketplace_id: str) -> list[dict]:
    values = re.findall(r"\d+(?:\.\d+)?", str(raw_value or ""))
    length = _number_from_text(values[0] if len(values) > 0 else "", env("AMAZON_ITEM_LENGTH", "6"))
    width = _number_from_text(values[1] if len(values) > 1 else "", env("AMAZON_ITEM_WIDTH", "3"))
    unit = _dimension_unit_from_text(raw_value, env("AMAZON_ITEM_DIMENSION_UNIT", "inches"))
    return [
        {
            "marketplace_id": marketplace_id,
            "length": {"unit": unit, "value": length},
            "width": {"unit": unit, "value": width},
        }
    ]


def _package_weight_cat_prop(raw_value, marketplace_id: str, offer_info: dict) -> list[dict]:
    default_weight = offer_info.get("weightKg") or env("AMAZON_DEFAULT_WEIGHT", "0.03")
    unit = _unit_from_text(
        raw_value,
        env("AMAZON_WEIGHT_UNIT", "kilograms"),
        {
            "pound": "pounds",
            "lb": "pounds",
            "ounce": "ounces",
            "oz": "ounces",
            "kilogram": "kilograms",
            "kg": "kilograms",
            "gram": "grams",
            "g": "grams",
            "milligram": "milligrams",
            "mg": "milligrams",
        },
    )
    return [
        {
            "marketplace_id": marketplace_id,
            "unit": unit,
            "value": _number_from_text(raw_value, default_weight),
        }
    ]


def _fulfillment_availability_cat_prop(raw_value) -> list[dict]:
    text = str(raw_value or "").strip().upper()
    channel = env("AMAZON_FULFILLMENT_CHANNEL_CODE")
    if not channel:
        if text in {"FBA", "AMAZON_NA"} or "AMAZON" in text:
            channel = "AMAZON_NA"
        else:
            channel = "DEFAULT"
    entry = {"fulfillment_channel_code": channel}
    handle_time = env("AMAZON_HANDLE_TIME")
    if handle_time:
        entry["lead_time_to_ship_max_days"] = _env_int("AMAZON_HANDLE_TIME", 3)
    quantity = _inventory_quantity()
    entry["quantity"] = int(quantity)
    return [entry]


def _measurement_cat_prop(
    key: str,
    raw_value,
    marketplace_id: str,
    offer_info: dict,
) -> list[dict] | None:
    if key == "chain_length":
        return [
            {
                "marketplace_id": marketplace_id,
                "unit": env("AMAZON_CHAIN_LENGTH_UNIT", "centimeters"),
                "decimal_value": _number_from_text(raw_value, env("AMAZON_CHAIN_LENGTH", "45")),
            }
        ]
    if key in {"item_display_weight", "item_weight"}:
        default_weight = offer_info.get("weightKg") or env("AMAZON_DEFAULT_WEIGHT", "0.03")
        return [
            {
                "marketplace_id": marketplace_id,
                "unit": env("AMAZON_WEIGHT_UNIT", "kilograms"),
                "value": _number_from_text(raw_value, default_weight),
            }
        ]
    return None


def _stones_cat_prop(raw_value, marketplace_id: str, language_tag: str) -> list[dict]:
    stone_type = _normalize_common_value("gem_type", str(raw_value or "")) if raw_value else "Cubic Zirconia"
    return [
        {
            "marketplace_id": marketplace_id,
            "id": 1,
            "type": {"language_tag": language_tag, "value": stone_type or "Cubic Zirconia"},
            "creation_method": {"language_tag": language_tag, "value": env("AMAZON_STONE_CREATION_METHOD", "Lab-Created")},
            "treatment_method": {"language_tag": language_tag, "value": env("AMAZON_STONE_TREATMENT_METHOD", "Not Treated")},
            "number_of_stones": _env_int("AMAZON_NUMBER_OF_STONES", 1),
        }
    ]


def _fallback_cat_prop(
    offer_info: dict,
    sku_prices: list[dict],
    marketplace_id: str,
    language_tag: str,
    currency: str,
    variation_theme: str = "",
) -> dict:
    max_price = max((Decimal(str(row.get("price") or "0")) for row in sku_prices), default=Decimal("0"))
    list_price = (max_price * Decimal("1.25")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    default_part_number = env("AMAZON_PART_NUMBER") or str(
        first_present(
            offer_info.get("cargoNumber"),
            sku_prices[0].get("skuCode") if sku_prices else "",
            offer_info.get("offerId"),
            default="DMS-00422",
        )
    )
    fallback = {
        "list_price": _list_price_cat_prop(list_price, sku_prices, marketplace_id, currency),
        "cpsia_cautionary_statement": [{"marketplace_id": marketplace_id, "value": "no_warning_applicable"}],
        "jewelry_material_categorization": [{"marketplace_id": marketplace_id, "value": "fashion"}],
        "number_of_items": [{"marketplace_id": marketplace_id, "value": "1"}],
        "stones": _stones_cat_prop("Cubic Zirconia", marketplace_id, language_tag),
    }
    if _include_conditional_attrs():
        conditional_fallback = {
            "clasp_type": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Lobster Claw"}],
            "color": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Multicolor"}],
            "department": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Women's"}],
            "fulfillment_availability": _fulfillment_availability_cat_prop("FBM"),
            "gem_type": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Cubic Zirconia"}],
            "item_package_dimensions": _package_dimensions_cat_prop("", marketplace_id),
            "item_package_weight": _package_weight_cat_prop("", marketplace_id, offer_info),
            "material": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Metal"}],
            "part_number": [{"marketplace_id": marketplace_id, "value": default_part_number}],
            "size": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "One Size"}],
            "style": [{"marketplace_id": marketplace_id, "language_tag": language_tag, "value": "Fashion"}],
        }
        selected_variation_theme = variation_theme or env("AMAZON_VARIATION_THEME")
        if selected_variation_theme:
            conditional_fallback["variation_theme"] = [{"marketplace_id": marketplace_id, "name": selected_variation_theme}]
        fallback.update(
            {
                key: value
                for key, value in conditional_fallback.items()
                if key in CONDITIONAL_CAT_PROP_FALLBACKS
            }
        )
    return fallback


def _common_cat_prop(
    pv_result: dict,
    marketplace_id: str,
    language_tag: str,
    currency: str,
    offer_info: dict,
    sku_prices: list[dict],
    variation_theme: str = "",
) -> dict:
    cat_prop = {}
    include_conditional_attrs = _include_conditional_attrs()
    for pv in pv_result.get("commonPvList", []):
        key = pv.get("attributeId") or pv.get("attributeName")
        if not key:
            continue
        key = str(key)
        if not include_conditional_attrs and key not in HARD_REQUIRED_CAT_PROP_IDS:
            continue
        raw_value = first_present(
            pv.get("value"),
            pv.get("valueName"),
            pv.get("valueId"),
            default="",
        )
        if not _is_present(raw_value):
            continue
        if key == "list_price":
            cat_prop[key] = _list_price_cat_prop(raw_value, sku_prices, marketplace_id, currency)
            continue
        if key == "item_package_dimensions":
            cat_prop[key] = _package_dimensions_cat_prop(raw_value, marketplace_id)
            continue
        if key == "item_length_width":
            cat_prop[key] = _item_length_width_cat_prop(raw_value, marketplace_id)
            continue
        if key == "item_package_weight":
            cat_prop[key] = _package_weight_cat_prop(raw_value, marketplace_id, offer_info)
            continue
        if key == "fulfillment_availability":
            cat_prop[key] = _fulfillment_availability_cat_prop(raw_value)
            continue
        if key == "stones":
            cat_prop[key] = _stones_cat_prop(raw_value, marketplace_id, language_tag)
            continue
        if key == "variation_theme":
            selected_variation_theme = variation_theme or _variation_theme_from_text(raw_value)
            if selected_variation_theme:
                cat_prop[key] = [{"marketplace_id": marketplace_id, "name": selected_variation_theme}]
            continue
        measurement_value = _measurement_cat_prop(str(key), raw_value, marketplace_id, offer_info)
        if measurement_value is not None:
            cat_prop[key] = measurement_value
            continue
        value = _normalize_common_value(key, raw_value) if isinstance(raw_value, str) else raw_value
        if isinstance(value, list):
            cat_prop[key] = value
        else:
            cat_prop[key] = [_amazon_attr_entry(key, value, marketplace_id, language_tag, currency)]
    for key, value in _fallback_cat_prop(
        offer_info,
        sku_prices,
        marketplace_id,
        language_tag,
        currency,
        variation_theme,
    ).items():
        if key not in cat_prop:
            cat_prop[key] = value
    return cat_prop


def _safe_variation_name(name: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_]+", "_", _strip_chinese(name).lower()).strip("_") or "style"
    return VARIATION_NAME_ALIASES.get(safe_name, safe_name)


def _variation_theme_from_names(names: list[str]) -> str:
    return "/".join(name.upper() for name in names if name)


def _variation_theme_from_text(value) -> str:
    theme = re.sub(r"[^A-Za-z0-9/]+", "_", str(value or "").strip().upper()).strip("_")
    theme = re.sub(r"_*/_*", "/", theme)
    return theme


def _select_variation_theme(selected_names: list[str]) -> str:
    inferred_theme = _variation_theme_from_names(selected_names[:2])
    configured_theme = env("AMAZON_VARIATION_THEME")
    if configured_theme:
        configured_theme = configured_theme.strip()
        if configured_theme.upper() == "STYLE" and inferred_theme and "style" not in selected_names:
            return inferred_theme
        return configured_theme
    return inferred_theme


def _sku_spec_and_prices(offer_info: dict, pv_result: dict, price_multiplier: Decimal) -> tuple[dict, list[dict]]:
    sku_pv_index = {
        str(item.get("skuId")): item.get("pvList", [])
        for item in pv_result.get("skuPvList", [])
        if item.get("skuId") is not None
    }
    variation_names: list[str] = []
    variation_values: dict[str, list[str]] = {}
    sku_prices = []
    seen_skus: set[str] = set()
    sku_rows = offer_info.get("skuList") or [
        {
            "skuId": "",
            "price": offer_info.get("minPrice", "0"),
            "cargoNumber": str(offer_info.get("offerId") or ""),
            "stock": 0,
            "specs": [],
            "image": "",
        }
    ]
    multi_sku = len(sku_rows) > 1
    condition_type = [
        {
            "value": env("AMAZON_CONDITION_TYPE_VALUE", "new_new"),
            "name": env("AMAZON_CONDITION_TYPE_NAME", "New"),
        }
    ]

    for idx, sku in enumerate(sku_rows):
        sku_id = str(sku.get("skuId", ""))
        pv_list = sku_pv_index.get(sku_id, [])
        specs = sku.get("specs", [])
        attr_pairs = []
        if not multi_sku:
            attr_pairs = []
        elif pv_list:
            attr_pairs = [
                (
                    pv.get("attributeName") or pv.get("attributeId") or "variation",
                    pv.get("valueName") or pv.get("valueId") or "Option",
                )
                for pv in pv_list
            ]
        elif specs:
            translated_values = [str(spec.get("valueTrans") or spec.get("value") or "") for spec in specs]
            use_style = any(value.lower() in {"necklace", "bracelet", "ring", "earrings"} for value in translated_values)
            if use_style:
                attr_pairs = [("style", spec.get("valueTrans") or spec.get("value") or "Option") for spec in specs]
            else:
                attr_pairs = [
                    (spec.get("nameTrans") or spec.get("name") or "variation", spec.get("valueTrans") or spec.get("value") or "Option")
                    for spec in specs
                ]
        else:
            attr_pairs = [("style", f"Style {idx + 1}")]

        sku_entry = {
            "price": _price(sku.get("price", "0"), price_multiplier),
            "discountedPrice": env("AMAZON_DISCOUNTED_PRICE"),
            "skuCode": _seller_sku(sku.get("cargoNumber", ""), idx, seen_skus),
            "externalProductIDType": env("AMAZON_EXTERNAL_PRODUCT_ID_TYPE", "GTIN"),
            "externalProductID": env("AMAZON_EXTERNAL_PRODUCT_ID"),
            "currency": "",
            "inventory": _inventory_quantity(),
            "conditionNote": env("AMAZON_CONDITION_NOTE"),
            "discountedStartTime": env("AMAZON_DISCOUNTED_START_TIME"),
            "discountedEndTime": env("AMAZON_DISCOUNTED_END_TIME"),
            "mainImg": [sku["image"]] if sku.get("image") else [],
            "imageList": [sku["image"]] if sku.get("image") else [],
            "swatchImage": sku.get("image", ""),
            "conditionType": condition_type,
            "attrTypes": [],
            "skuGroup": env("AMAZON_SKU_GROUP"),
            "goodsType": "local",
        }
        sku_attr_types: list[str] = []

        for name, value in attr_pairs:
            safe_name = _safe_variation_name(name)
            safe_value = _strip_chinese(value) or f"Option {idx + 1}"
            sku_entry[safe_name] = safe_value
            sku_entry[f"skuId{safe_name}"] = {
                "attrId": safe_name,
                "attrName": safe_name,
                "valueId": safe_value,
                "valueName": safe_value,
            }
            if safe_name not in variation_names:
                variation_names.append(safe_name)
            if safe_name not in sku_attr_types:
                sku_attr_types.append(safe_name)
            variation_values.setdefault(safe_name, [])
            if safe_value not in variation_values[safe_name]:
                variation_values[safe_name].append(safe_value)

        sku_entry["attrTypes"] = sku_attr_types or [""]
        sku_prices.append(sku_entry)

    if multi_sku:
        varying_names = [name for name in variation_names if len(variation_values.get(name, [])) > 1]
        selected_names = (varying_names or variation_names)[:2]
        variation_theme = _select_variation_theme(selected_names)
        for sku_entry in sku_prices:
            for name in variation_names:
                if name not in selected_names:
                    sku_entry.pop(name, None)
                    sku_entry.pop(f"skuId{name}", None)
            sku_entry["attrTypes"] = selected_names or [""]
    else:
        variation_theme = ""
    sku_speci = {"variation_theme": variation_theme}
    if multi_sku:
        sku_speci.update({name: variation_values.get(name, []) for name in selected_names})
    return sku_speci, sku_prices


def _safety_and_compliance(marketplace_id: str) -> dict:
    return {
        "country_of_origin": [
            {"marketplace_id": marketplace_id, "value": env("AMAZON_COUNTRY_OF_ORIGIN", "CN")}
        ],
        "batteries_required": [
            {"marketplace_id": marketplace_id, "value": _env_bool("AMAZON_BATTERIES_REQUIRED", False)}
        ],
        "supplier_declared_dg_hz_regulation": [
            {"marketplace_id": marketplace_id, "value": env("AMAZON_DG_HZ_REGULATION", "not_applicable")}
        ],
    }


def _pack_info(offer_info: dict) -> dict:
    return {
        "channelCode": env("AMAZON_CHANNEL_CODE", "FBM"),
        "handleTime": env("AMAZON_HANDLE_TIME", "3"),
        "weight": _json_string(
            {
                "value": str(offer_info.get("weightKg") or env("AMAZON_DEFAULT_WEIGHT", "0.1")),
                "unit": env("AMAZON_WEIGHT_UNIT", "kilograms"),
            }
        ),
        "length": _json_string(
            {"value": env("AMAZON_PACKAGE_LENGTH", "10"), "unit": env("AMAZON_DIMENSION_UNIT", "centimeters")}
        ),
        "width": _json_string(
            {"value": env("AMAZON_PACKAGE_WIDTH", "10"), "unit": env("AMAZON_DIMENSION_UNIT", "centimeters")}
        ),
        "height": _json_string(
            {"value": env("AMAZON_PACKAGE_HEIGHT", "10"), "unit": env("AMAZON_DIMENSION_UNIT", "centimeters")}
        ),
        "pricingRule": _json_string(_named_value("AMAZON_PRICING_RULE", default_name="Competitive Price Rule by Amazon")),
        "shippingModel": _json_string(_named_value("AMAZON_SHIPPING_MODEL", default_name="Migrated Template")),
        "masterPackLayersPerPalletQuantity": env("AMAZON_MASTER_PACK_LAYERS_PER_PALLET_QUANTITY", "1"),
        "masterPacksPerLayerQuantity": env("AMAZON_MASTER_PACKS_PER_LAYER_QUANTITY", "1"),
    }


def _other_info() -> dict:
    return {
        "complianceMediaShow": _env_int("AMAZON_COMPLIANCE_MEDIA_SHOW", 1),
        "searchKeywords": env("AMAZON_SEARCH_KEYWORDS", "1688 sourced product"),
        "complianceMedia": _json_env("AMAZON_COMPLIANCE_MEDIA", []),
        "responsiblePartyEmail": env("AMAZON_RESPONSIBLE_PARTY_EMAIL"),
        "manufacturerEmail": env("AMAZON_MANUFACTURER_EMAIL"),
    }


def build_amazon_product(
    offer_info: dict,
    category: dict,
    pv_result: dict,
    *,
    store_name: str = "",
    marketplace_id: str | None = None,
    language_tag: str | None = None,
    brand_name: str | None = None,
    manufacturer: str | None = None,
    price_multiplier: str = "1.00",
) -> dict:
    marketplace_id = marketplace_id or env("AMAZON_MARKETPLACE_ID", DEFAULT_MARKETPLACE_ID)
    language_tag = language_tag or env("AMAZON_LANGUAGE_TAG", DEFAULT_LANGUAGE_TAG)
    brand_name = brand_name or env("AMAZON_BRAND_NAME", "Generic")
    manufacturer = manufacturer or env("AMAZON_MANUFACTURER", brand_name)
    currency = env("AMAZON_CURRENCY", "USD")
    listing_marker = _listing_marker()
    title = _title_with_marker(_safe_title(offer_info.get("subject", "")), listing_marker)
    product_type = category.get("productType") or category.get("categoryName") or "PRODUCT"
    full_category_id = category.get("fullCategoryId") or category.get("categoryId") or ""
    main_images = offer_info.get("mainImages", [])[:9]
    detail_images = offer_info.get("detailImages", []) or main_images
    descriptions = [_strip_chinese(item) for item in pv_result.get("descriptions", []) if _strip_chinese(item)]
    bullet_points = descriptions[:5] or [title]
    sku_speci, sku_prices = _sku_spec_and_prices(offer_info, pv_result, Decimal(price_multiplier))
    product_sku_type = 1 if len(sku_prices) > 1 else 0
    single_seller_sku = sku_prices[0].get("skuCode", "") if product_sku_type == 0 and sku_prices else ""
    parent_sku = single_seller_sku or f"PARENT-{offer_info.get('offerId') or '1688'}"
    upc_exempt_default = 0 if product_sku_type else 1
    upc_exempt = _env_int("AMAZON_UPC_EXEMPT", upc_exempt_default)
    cat_prop = _common_cat_prop(
        pv_result,
        marketplace_id,
        language_tag,
        currency,
        offer_info,
        sku_prices,
        sku_speci.get("variation_theme", ""),
    )
    if product_sku_type == 0:
        # Dianxiaobao no-SKU examples use parentSku as the seller SKU carrier;
        # sending variation attributes or a child skuCode causes Amazon sku
        # validation errors for single-SKU listings.
        cat_prop.pop("variation_theme", None)
        cat_prop.pop("style", None)
        if sku_prices:
            sku_prices[0]["skuCode"] = ""

    return {
        "storeName": store_name,
        "site": marketplace_id,
        "languageTag": language_tag,
        "categoryId": category.get("categoryId", ""),
        "fullCategoryId": full_category_id,
        "ptType": product_type,
        "subject": title,
        "productSkuType": product_sku_type,
        "upcExempt": upc_exempt,
        "brandName": brand_name,
        "manufacturer": manufacturer,
        "cateInfo": {"fullCateName": category.get("fullCategoryName") or category.get("categoryName", "")},
        "baseInfo": {"parentSku": parent_sku, "scImages": _json_string(main_images)},
        "attrInfo": {"catProp": _json_string(cat_prop)},
        "skuInfo": {"skuSpeci": _json_string(sku_speci)},
        "tradeInfo": {"skuAndPrice": _json_string(sku_prices)},
        "safetyAndCompliance": _safety_and_compliance(marketplace_id),
        "packInfo": _pack_info(offer_info),
        "detailInfo": {
            "webDetail": "".join(f'<img src="{url}" width="890">' for url in detail_images[:20]),
            "bulletPoint": _json_string(bullet_points),
        },
        "otherInfo": _other_info(),
    }


def offer_for_build(offer_info: dict, image_processing: dict | None = None) -> dict:
    if not image_processing:
        return offer_info
    processed_offer = image_processing.get("offer")
    if isinstance(processed_offer, dict):
        return processed_offer
    processed_url = image_processing.get("processedImageUrl")
    if not processed_url:
        return offer_info
    updated_offer = dict(offer_info)
    main_images = list(updated_offer.get("mainImages") or [])
    if main_images:
        main_images[0] = processed_url
    else:
        main_images = [processed_url]
    updated_offer["mainImages"] = main_images
    return updated_offer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_product.py <session_dir> OR <offerJson> <cpvJson> <categoryJson>", file=sys.stderr)
        sys.exit(1)
    if os.path.isdir(sys.argv[1]):
        from scripts.common import read_session, write_session

        session_dir = sys.argv[1]
        offer = read_session(session_dir, "query_offer.json", required_keys=["subject", "mainImages", "skuList"])
        try:
            image_processing = read_session(session_dir, "image_processing.json")
        except FileNotFoundError:
            image_processing = {}
        offer = offer_for_build(offer, image_processing)
        cpv = read_session(session_dir, "map_pv_attrs.json")
        category_data = read_session(session_dir, "map_category.json", required_keys=["categoryId"])
        user = read_session(session_dir, "query_user_info.json", required_keys=["storeName"])
        run_input = read_session(session_dir, "input.json")
        multiplier = env("AMAZON_PRICE_MULTIPLIER", "1.00")
        for idx, arg in enumerate(sys.argv):
            if arg == "--price-multiplier" and idx + 1 < len(sys.argv):
                multiplier = sys.argv[idx + 1]
            if arg == "--inventory-quantity" and idx + 1 < len(sys.argv):
                os.environ["AMAZON_INVENTORY_QUANTITY"] = sys.argv[idx + 1]
        product = build_amazon_product(
            offer,
            category_data,
            cpv,
            store_name=user["storeName"],
            marketplace_id=run_input.get("marketplace_id") or DEFAULT_MARKETPLACE_ID,
            price_multiplier=multiplier,
        )
        write_session(session_dir, "build_product.json", product)
        print(dump(product))
    else:
        if len(sys.argv) < 4:
            print("Usage: python scripts/build_product.py <offerJson> <cpvJson> <categoryJson>", file=sys.stderr)
            sys.exit(1)
        with open(sys.argv[1]) as f:
            offer = json.load(f)
        with open(sys.argv[2]) as f:
            cpv = json.load(f)
        with open(sys.argv[3]) as f:
            category_data = json.load(f)
        for idx, arg in enumerate(sys.argv):
            if arg == "--inventory-quantity" and idx + 1 < len(sys.argv):
                os.environ["AMAZON_INVENTORY_QUANTITY"] = sys.argv[idx + 1]
        print(dump(build_amazon_product(offer, category_data, cpv)))
