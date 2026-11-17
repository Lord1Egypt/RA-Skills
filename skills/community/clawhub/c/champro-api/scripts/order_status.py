"""Order status and package tracking — the other service CHAMPRO omits from PromoStandards.

CHAMPRO publishes no ODRSTAT (Order Status) and no OSN (Order Shipment
Notification) endpoint, so the `promostandards` skill has nothing to call for
"where is my order". The REST `OrderStatus` endpoint answers both questions at
once: a workflow status plus, per shipment, the carrier tracking number and the
SKUs inside that package.

The key that unlocks it is the **SubOrderID**, not the PO. `PlaceOrder` may
answer one order with several suborders (one per fulfilling warehouse), and
each ships and tracks independently — so following an order means following
every suborder id it produced.
"""

from __future__ import annotations

from typing import Any

from client import ChamproClient
from errors import ChamproAPIError, ChamproValidationError


def _text(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def normalise_status(payload: dict[str, Any]) -> dict[str, Any]:
    shipments = []
    for line in payload.get("Lines") or []:
        if not isinstance(line, dict):
            continue
        shipments.append(
            {
                "tracking_number": _text(line.get("TrackingNumber")),
                "carrier": _text(line.get("ShippingCarrier")),
                "service": _text(line.get("ShippingService")),
                "items": [
                    {"sku": _text(sku.get("SKU")), "quantity": sku.get("Quantity")}
                    for sku in line.get("SKUs") or []
                    if isinstance(sku, dict)
                ],
            }
        )

    status = _text(payload.get("Status"))
    return {
        "order_number": payload.get("OrderNumber"),
        "po": _text(payload.get("PO")),
        # CHAMPRO spells this `SalesID` in the response and `SALESID` in the
        # field table; accept either.
        "sales_id": _text(payload.get("SalesID") or payload.get("SALESID")),
        "status": status,
        "shipped": bool(shipments and any(s["tracking_number"] for s in shipments)),
        "shipment_count": len(shipments),
        "shipments": shipments,
        "tracking_numbers": [s["tracking_number"] for s in shipments if s["tracking_number"]],
    }


def get_order_status(
    order_number: str | int | None = None,
    order_numbers: list[str | int] | None = None,
    *,
    raw: bool = False,
    **credentials: Any,
) -> dict[str, Any]:
    """Status for one or more **SubOrderIDs** (not PO numbers).

    Querying several is the normal case: a split shipment produces one suborder
    per warehouse, and asking about only the first reports "shipped" while the
    rest is still in production. A number that errors is reported per-number
    rather than failing the batch, so one bad id does not hide the others.
    """

    wanted = [
        str(n).strip()
        for n in ([order_number] if order_number is not None else []) + list(order_numbers or [])
        if str(n).strip()
    ]
    if not wanted:
        raise ChamproValidationError(
            "Pass `order_number` or `order_numbers` — the SubOrderID(s) returned by PlaceOrder."
        )

    client = _client(credentials)
    results, failures = [], []
    for number in wanted:
        try:
            payload = client.order_status(number)
        except ChamproAPIError as exc:
            failures.append(
                {"order_number": number, "errors": exc.errors, "message": str(exc)}
            )
            continue
        results.append(payload if raw else normalise_status(payload))

    tracking = [t for r in results for t in (r.get("tracking_numbers") or [])] if not raw else []
    return {
        "requested": wanted,
        "orders": results,
        "failures": failures,
        "all_shipped": bool(results) and all(r.get("shipped") for r in results) and not failures,
        "tracking_numbers": tracking,
    }


def track_placed_order(
    place_order_result: dict[str, Any] | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Follow every suborder from a `place-order` result in one call.

    Takes the summary `place-order` returned (or its `suborder_ids`) so the
    caller does not have to dig the ids out of nested suborders and risk
    following only some of them.
    """

    result = place_order_result or {}
    ids = list(result.get("suborder_ids") or [])
    if not ids:
        ids = [
            s.get("suborder_id")
            for s in result.get("suborders") or []
            if s.get("suborder_id") not in (None, "", 0)
        ]
    if not ids:
        raise ChamproValidationError(
            "No suborder ids in `place_order_result`. A PlaceOrder response with no SubOrderID "
            "means no order was created — there is nothing to track."
        )
    return get_order_status(order_numbers=ids, **credentials)


def _client(credentials: dict[str, Any]) -> ChamproClient:
    return ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base"),
    )
