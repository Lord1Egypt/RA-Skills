"""Product master info: the SKU grid, MOQs and the lead-time catalog.

This is the gap PromoStandards leaves widest for CHAMPRO. Their PPC 1.0.0
service returns quantity price breaks, FOB points and decoration charges, but
carries no minimum-order quantity and no lead-time catalog at all — and both
are hard requirements for placing a CHAMPRO order (MOQ increments are error 25,
an unknown lead time is error 22).

`ProductInfo` is also the only place the *sellable SKU grid* appears with its
configuration/fabric/color/size decomposition, which is what turns "youth large
in active cloth" into `JSBJ8YACL`.
"""

from __future__ import annotations

from typing import Any

from client import ChamproClient
from errors import ChamproValidationError


def _norm(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def normalise_product_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Canonical shape for one product master.

    CHAMPRO returns `Color` as an empty string for most apparel (color lives
    inside the SKU suffix rather than as its own attribute), and `null` for the
    SKU list when the request failed. Empty string becomes `None` so "no colour
    dimension" is not mistaken for a colour named "".
    """

    skus = []
    for row in payload.get("ProductSKUs") or []:
        skus.append(
            {
                "sku": _norm(row.get("SKU")),
                "configuration": _norm(row.get("Configuration")),
                "fabric": _norm(row.get("Fabric")),
                "color": _norm(row.get("Color")),
                "size": _norm(row.get("Size")),
            }
        )

    lead_times = []
    for row in payload.get("AvailableLeadTimes") or []:
        lead_times.append(
            {
                "name": _norm(row.get("LeadTimeName")),
                # Days and charge arrive as strings; keep the parsed value but
                # never coerce an unparseable one to 0 — "unknown lead time"
                # and "ships today" are not the same answer.
                "days": _int_or_none(row.get("LeadTime")),
                "charge": _float_or_none(row.get("LeadTimeCharge")),
            }
        )

    return {
        "product_master": _norm(payload.get("ProductMaster")),
        "moq_stock": _int_or_none(payload.get("MOQ")) or 0,
        "moq_custom": _int_or_none(payload.get("MOQCustom")) or 0,
        "sku_count": len(skus),
        "skus": skus,
        "lead_times": lead_times,
        "configurations": sorted({s["configuration"] for s in skus if s["configuration"]}),
        "fabrics": sorted({s["fabric"] for s in skus if s["fabric"]}),
        "sizes": sorted({s["size"] for s in skus if s["size"]}),
        "colors": sorted({s["color"] for s in skus if s["color"]}),
    }


def _int_or_none(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def get_product_info(
    product_master: str | None = None,
    product_masters: list[str] | None = None,
    *,
    raw: bool = False,
    **credentials: Any,
) -> dict[str, Any]:
    """Fetch one or several product masters.

    Multiple masters is the common case before an order: the MOQ rule is
    per-master, so a cart spanning two products needs both.
    """

    masters = [m for m in ([product_master] if product_master else []) + (product_masters or []) if m]
    if not masters:
        raise ChamproValidationError("Pass `product_master` or a `product_masters` list.")

    client = _client(credentials)
    products: dict[str, Any] = {}
    for master in masters:
        payload = client.product_info(master)
        products[master.strip().upper()] = payload if raw else normalise_product_info(payload)
    return {"products": products, "product_masters": sorted(products)}


def find_skus(
    product_master: str | None = None,
    *,
    size: str | None = None,
    configuration: str | None = None,
    fabric: str | None = None,
    color: str | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Filter a master's SKU grid by the attributes an order line is described in.

    Matching is case-insensitive and exact per supplied attribute; omitted
    attributes do not filter. Returns every match rather than guessing one,
    because a size that appears in three fabrics is a question for the caller,
    not something to pick from silently.
    """

    if not str(product_master or "").strip():
        raise ChamproValidationError("`product_master` is required (e.g. \"JSBJ8\").")

    info = normalise_product_info(_client(credentials).product_info(product_master))
    wanted = {
        "size": size,
        "configuration": configuration,
        "fabric": fabric,
        "color": color,
    }
    wanted = {k: str(v).strip().casefold() for k, v in wanted.items() if v}

    matches = [
        row
        for row in info["skus"]
        if all((row.get(k) or "").casefold() == v for k, v in wanted.items())
    ]
    return {
        "product_master": info["product_master"],
        "filters": {k: v for k, v in wanted.items()},
        "match_count": len(matches),
        "matches": matches,
        "ambiguous": len(matches) > 1,
        "available": {
            "configurations": info["configurations"],
            "fabrics": info["fabrics"],
            "sizes": info["sizes"],
            "colors": info["colors"],
        },
    }


def get_lead_times(product_master: str | None = None, **credentials: Any) -> dict[str, Any]:
    """Lead times a CUSTOM order for this master may name, with their surcharges."""

    if not str(product_master or "").strip():
        raise ChamproValidationError("`product_master` is required (e.g. \"JSBJ8\").")

    info = normalise_product_info(_client(credentials).product_info(product_master))
    return {
        "product_master": info["product_master"],
        "moq_custom": info["moq_custom"],
        "lead_times": info["lead_times"],
        "names": [lt["name"] for lt in info["lead_times"] if lt["name"]],
    }


def _client(credentials: dict[str, Any]) -> ChamproClient:
    return ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base"),
    )
