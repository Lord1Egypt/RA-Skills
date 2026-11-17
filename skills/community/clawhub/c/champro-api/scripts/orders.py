"""Placing CHAMPRO orders, and the guards around doing so.

PromoStandards PO 1.0.0 *is* published by CHAMPRO, so why order here instead?
Three reasons, and the first is decisive:

1. **CHAMPRO registers no test endpoint for PO 1.0.0.** The `promostandards`
   skill refuses `send-po` outright rather than falling back to production, so
   there is no way to rehearse an order through that path. The REST API has a
   real sandbox host, `/api/OrderSandBox/PlaceOrder`.
2. **Custom orders carry roster data** — per-line TeamName/PlayerName/
   PlayerNumber, a TeamColor and a proof file — that PO 1.0.0 has nowhere to
   put.
3. **Warehouse routing and split shipments** are first-class here: a stock
   order is answered with suborders, one per fulfilling warehouse, each with
   its own order number to track.

Three properties of PlaceOrder shape everything below:

* **It is not idempotent and there is no cancel.** Resending a request that may
  have landed duplicates the order. Every ambiguous failure therefore escalates
  rather than retries.
* **Partial success is normal.** CHAMPRO's own documented example rejects two
  SKUs for inventory and still cuts two suborders. `RequestErrors` present does
  *not* mean nothing happened; only `SubOrders` tells you what exists.
* **Sandbox is a different URL, not a flag.** See `client.place_order`.
"""

from __future__ import annotations

from typing import Any

import validation
from catalog import get_product_info
from client import ChamproClient
from errors import ChamproAPIError, ChamproPartialOrderError, ChamproValidationError
from schemas import CUSTOM, STOCK, Order
from shipping import lookup as lookup_shipping_method


def _client(credentials: dict[str, Any]) -> ChamproClient:
    return ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base"),
    )


def _coerce_orders(orders: Any, order: Any) -> list[Order]:
    raw = list(orders or [])
    if order:
        raw.append(order)
    if not raw:
        raise ChamproValidationError("Pass `order` (one object) or `orders` (a list).")
    return [Order.from_dict(o) if isinstance(o, dict) else o for o in raw]


def _canonicalise_shipping(orders: list[Order]) -> list[dict[str, Any]]:
    """Send CHAMPRO's own spelling of a method, not the caller's.

    Returns one finding per rewrite. The rewrite happens *before* validation
    so the envelope carries the canonical spelling, which is why the notice has
    to be produced here — by the time the rules run, the original is gone.
    """

    notes: list[dict[str, Any]] = []
    for index, order in enumerate(orders):
        original = order.shipping_method
        if not original:
            continue
        entry = lookup_shipping_method(original)
        if entry and entry["name"] != original:
            order.shipping_method = entry["name"]
            notes.append(
                {
                    "severity": "warning",
                    "code": None,
                    "order_index": index,
                    "message": (
                        f"ShippingMethod {original!r} will be sent as {entry['name']!r}."
                    ),
                }
            )
    return notes


def build_envelope(orders: list[Order], *, autowarehouse: bool = False) -> dict[str, Any]:
    body: dict[str, Any] = {"Orders": [o.to_payload() for o in orders]}
    if autowarehouse:
        body["Autowarehouse"] = "YES"
    return body


def _fetch_product_info(
    orders: list[Order], product_masters: list[str] | None, credentials: dict[str, Any]
) -> dict[str, dict[str, Any]] | None:
    """Load the ProductInfo needed for the SKU/MOQ/lead-time rules.

    Masters cannot be derived from SKUs (`JSBJ8` -> `JSBJ8GACL` and
    `JSBJ8WWP14XL` share no fixed suffix length), so the caller names them. With
    none named the catalog rules are reported as *skipped*, never as passed.
    """

    masters = [m.strip().upper() for m in (product_masters or []) if str(m).strip()]
    if not masters:
        return None
    return get_product_info(product_masters=masters, **credentials)["products"]


def validate_orders(
    order: dict[str, Any] | None = None,
    orders: list[dict[str, Any]] | None = None,
    *,
    autowarehouse: bool = False,
    product_masters: list[str] | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Run every local rule and report. Sends no order.

    With `product_masters` this makes read-only ProductInfo calls; without it,
    it is fully offline.
    """

    parsed = _coerce_orders(orders, order)
    rewrites = _canonicalise_shipping(parsed)
    info = _fetch_product_info(parsed, product_masters, credentials)

    results = []
    for index, one in enumerate(parsed):
        findings = validation.validate_order(one, product_info=info, autowarehouse=autowarehouse)
        findings.extend(n for n in rewrites if n["order_index"] == index)
        results.append(
            {
                "order_index": index,
                "po": one.po,
                "order_type": one.order_type,
                "line_count": len(one.items),
                "total_quantity": one.total_quantity,
                "findings": findings,
                "blocking": validation.blocking(findings),
            }
        )

    blocking = [f for r in results for f in r["blocking"]]
    return {
        "valid": not blocking,
        "orders": results,
        "blocking_count": len(blocking),
        "catalog_checks": "run" if info is not None else "skipped",
        "envelope": build_envelope(parsed, autowarehouse=autowarehouse),
    }


def preview_order(
    order: dict[str, Any] | None = None,
    orders: list[dict[str, Any]] | None = None,
    *,
    autowarehouse: bool = False,
    product_masters: list[str] | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """The exact JSON that would be POSTed, plus the validation report.

    The API key is *not* included — it is added by the client at send time, so
    a preview can be shown to a user or pasted into a ticket safely.
    """

    report = validate_orders(
        order=order,
        orders=orders,
        autowarehouse=autowarehouse,
        product_masters=product_masters,
        **credentials,
    )
    return {
        "request_body": report["envelope"],
        "note": "APICustomerKey is injected at send time and is deliberately absent here.",
        "sandbox_url": "https://api.champrosports.com/api/OrderSandBox/PlaceOrder",
        "production_url": "https://api.champrosports.com/api/Order/PlaceOrder",
        "validation": report,
    }


def summarise_place_order(payload: dict[str, Any]) -> dict[str, Any]:
    """Classify a PlaceOrder response into placed / failed / partial.

    The only evidence an order exists is a `SubOrderID`. Errors at any level can
    coexist with suborders, so both are reported and the outcome names which
    happened:

    * `placed`  — suborders, no errors.
    * `partial` — suborders **and** errors. Real orders exist; resubmitting the
      whole request duplicates them.
    * `failed`  — errors, no suborders. Nothing was created.
    * `empty`   — neither. Treated as ambiguous, not as success.
    """

    from errors import extract_envelope_errors  # noqa: PLC0415  (avoids a cycle)

    errors = extract_envelope_errors(payload, "PlaceOrder")
    suborders: list[dict[str, Any]] = []
    for index, order in enumerate(payload.get("Orders") or []):
        if not isinstance(order, dict):
            continue
        for sub in order.get("SubOrders") or []:
            if not isinstance(sub, dict) or sub.get("SubOrderID") in (None, "", 0):
                continue
            suborders.append(
                {
                    "order_index": index,
                    "po": order.get("PO"),
                    "suborder_id": sub.get("SubOrderID"),
                    "warehouse": sub.get("Warehouse"),
                    "line_count": len(sub.get("SubOrderItems") or []),
                    "items": [
                        {
                            "sku": item.get("SKU"),
                            "quantity": item.get("Quantity"),
                            "warehouse": item.get("Warehouse"),
                            "cost": item.get("Cost"),
                            "team_name": item.get("TeamName"),
                            "player_name": item.get("PlayerName"),
                            "player_number": item.get("PlayerNumber"),
                        }
                        for item in sub.get("SubOrderItems") or []
                        if isinstance(item, dict)
                    ],
                }
            )

    if suborders and errors:
        outcome = "partial"
    elif suborders:
        outcome = "placed"
    elif errors:
        outcome = "failed"
    else:
        outcome = "empty"

    cost_total = None
    totals = [
        o.get("CostTotal")
        for o in payload.get("Orders") or []
        if isinstance(o, dict) and o.get("CostTotal") is not None
    ]
    if totals:
        try:
            cost_total = sum(float(t) for t in totals)
        except (TypeError, ValueError):
            cost_total = None

    return {
        "outcome": outcome,
        "environment": payload.get("_environment"),
        "endpoint": payload.get("_endpoint"),
        "session_id": payload.get("SessionID"),
        "request_type": payload.get("RequestType"),
        "autowarehouse": payload.get("Autowarehouse"),
        "suborders": suborders,
        "suborder_ids": [s["suborder_id"] for s in suborders],
        "errors": errors,
        "cost_total": cost_total,
        "response": payload,
    }


def place_order(
    order: dict[str, Any] | None = None,
    orders: list[dict[str, Any]] | None = None,
    *,
    confirm: bool = False,
    production: bool = False,
    autowarehouse: bool = False,
    product_masters: list[str] | None = None,
    skip_validation: bool = False,
    **credentials: Any,
) -> dict[str, Any]:
    """Submit one or more orders. **External write.**

    Two independent gates, because they guard different mistakes:

    * `confirm: true` — "send this now". Without it nothing is sent and the
      preview comes back instead, so an exploratory call cannot place an order.
    * `production: true` — "send it to the real host". Without it the sandbox
      URL is used. Default sandbox is deliberate: sandbox orders older than 30
      days are purged by CHAMPRO, so a mistaken sandbox order costs nothing,
      while a mistaken production order is a real garment run.

    A partial result raises `ChamproPartialOrderError` carrying the summary,
    which the CLI surfaces as `escalation_required` (exit 3): some suborders
    exist, so this needs a human deciding what to resubmit — never an automatic
    retry.
    """

    parsed = _coerce_orders(orders, order)
    _canonicalise_shipping(parsed)

    report = validate_orders(
        orders=[o.to_payload() for o in parsed],
        autowarehouse=autowarehouse,
        product_masters=product_masters,
        **credentials,
    )
    if not report["valid"] and not skip_validation:
        return {
            "outcome": "not_sent",
            "reason": "validation_failed",
            "message": (
                f"{report['blocking_count']} blocking finding(s). Fix them, or pass "
                "skip_validation:true to send anyway."
            ),
            "validation": report,
        }

    if not confirm:
        return {
            "outcome": "not_sent",
            "reason": "unconfirmed",
            "message": (
                "Nothing was sent. Pass confirm:true to submit"
                + (
                    " to PRODUCTION (real order, no cancel endpoint)."
                    if production
                    else " to the sandbox."
                )
            ),
            "would_send_to": (
                "production" if production else "sandbox"
            ),
            "request_body": report["envelope"],
            "validation": report,
        }

    client = _client(credentials)
    payload = client.place_order(report["envelope"], production=production)
    summary = summarise_place_order(payload)
    summary["validation"] = report

    if summary["outcome"] == "partial":
        raise ChamproPartialOrderError(
            "PlaceOrder returned suborders AND errors: "
            f"{len(summary['suborders'])} suborder(s) were created "
            f"({', '.join(str(i) for i in summary['suborder_ids'])}) alongside "
            f"{len(summary['errors'])} error(s). Those orders are real. Do not resend this "
            "request — resubmit only the failed lines, as a new order.",
            result=summary,
        )
    if summary["outcome"] == "empty":
        # No suborder ids and no errors. CHAMPRO always says one or the other,
        # so this proves nothing about whether an order was created — which
        # makes it an escalation, not a retry.
        raise ChamproPartialOrderError(
            "PlaceOrder returned neither a SubOrderID nor an error, so whether an order was "
            "created is unknown. Do not resend. Check the CHAMPRO website for an order against "
            f"PO {', '.join(str(o.po) for o in parsed)} before doing anything else.",
            result=summary,
        )
    if summary["outcome"] == "failed":
        raise ChamproAPIError(
            "PlaceOrder created no suborders: "
            + "; ".join(e["message"] for e in summary["errors"]),
            endpoint=summary["endpoint"] or "PlaceOrder",
            errors=summary["errors"],
            response=summary,
        )
    return summary


def split_by_type(
    items: list[dict[str, Any]] | None = None,
    base: dict[str, Any] | None = None,
    **_credentials: Any,
) -> dict[str, Any]:
    """Split a mixed cart into a STOCK order and a CUSTOM order (error 07).

    A line is custom when it carries any roster field; stock otherwise. The
    returned orders inherit `base` (ship-to, PO, etc.) and get a `-S`/`-C`
    suffix on the PO, since two orders cannot share one PO number.
    """

    if not items:
        raise ChamproValidationError("Pass a non-empty `items` list of order lines.")

    base = dict(base or {})
    stock_items, custom_items = [], []
    for item in items or []:
        if any(item.get(k) or item.get(k.title()) for k in ("team_name", "player_name", "player_number")):
            custom_items.append(item)
        else:
            stock_items.append(item)

    po = str(base.get("po") or base.get("PO") or "").strip()
    out: list[dict[str, Any]] = []
    if stock_items:
        out.append({**base, "po": f"{po}-S" if po else po, "order_type": STOCK, "items": stock_items})
    if custom_items:
        out.append({**base, "po": f"{po}-C" if po else po, "order_type": CUSTOM, "items": custom_items})
    return {
        "orders": out,
        "stock_line_count": len(stock_items),
        "custom_line_count": len(custom_items),
        "was_mixed": bool(stock_items and custom_items),
    }
