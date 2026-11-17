"""Per-warehouse inventory — the service CHAMPRO does not publish over PromoStandards.

CHAMPRO's PromoStandards registry entry lists PRODUCT, PPC, PO, MED and Company
Data. There is **no INV endpoint at any version**, so the `promostandards`
skill correctly reports inventory as unsupported for this supplier. The REST
`Inventory` endpoint is the only stock source CHAMPRO offers, and it is richer
than PromoStandards INV 1.2.1 would have been: named warehouses (IL, CA, DR)
plus a `MORE_EXPECTED_ON` restock date.

Warehouse matters for ordering, not just for reporting: a STOCK order line
carries its own `Warehouse`, and picking one that cannot cover the quantity
returns "Not enough Inventory" for that line while the rest of the order still
places. `plan_warehouses` does the allocation up front instead.
"""

from __future__ import annotations

from typing import Any

from client import ChamproClient
from errors import ChamproValidationError
from shipping import WAREHOUSE_CODES

# Batch size for the Inventory POST. The endpoint takes an unbounded list, but
# CHAMPRO reports per-SKU failures in a flat `ErrorMessages` array with no
# index, so smaller batches keep an unknown-SKU error attributable.
DEFAULT_BATCH = 50


def _int_or_none(value: Any) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def normalise_inventory(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in payload.get("Inventory") or []:
        warehouses = {}
        for wh in row.get("Warehouses") or []:
            code = str(wh.get("WarehouseLocation") or "").strip().upper()
            if code:
                # A quantity that will not parse stays None. "Unreadable" and
                # "zero on hand" drive opposite decisions.
                warehouses[code] = _int_or_none(wh.get("Quantity"))
        known = [q for q in warehouses.values() if q is not None]
        rows.append(
            {
                "sku": str(row.get("SKU") or "").strip().upper() or None,
                "item_id": str(row.get("ItemID") or "").strip() or None,
                "more_expected_on": str(row.get("MORE_EXPECTED_ON") or "").strip() or None,
                "warehouses": warehouses,
                "total": sum(known) if known else (0 if warehouses else None),
                "has_unreadable_quantity": any(q is None for q in warehouses.values()),
            }
        )
    return rows


def check_inventory(
    skus: list[str] | None = None,
    sku: str | None = None,
    *,
    batch_size: int = DEFAULT_BATCH,
    **credentials: Any,
) -> dict[str, Any]:
    """Stock by warehouse for a list of SKUs.

    SKUs CHAMPRO could not resolve come back in `errors` (as `E3.1: <SKU> - SKU
    does not Exist.`) and are also listed in `missing`, because a SKU that is
    simply absent from `Inventory` looks identical to one with no stock.
    """

    wanted = [str(s).strip().upper() for s in (skus or []) + ([sku] if sku else []) if str(s).strip()]
    if not wanted:
        raise ChamproValidationError("Pass `sku` or a non-empty `skus` list.")

    client = _client(credentials)
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for start in range(0, len(wanted), max(1, int(batch_size))):
        batch = wanted[start : start + max(1, int(batch_size))]
        payload = client.inventory(batch)
        rows.extend(normalise_inventory(payload))
        errors.extend(str(e) for e in (payload.get("ErrorMessages") or []) if e)

    returned = {r["sku"] for r in rows if r["sku"]}
    return {
        "requested": wanted,
        "inventory": rows,
        "missing": [s for s in wanted if s not in returned],
        "errors": errors,
        "warehouses": sorted(WAREHOUSE_CODES),
    }


def plan_warehouses(
    lines: list[dict[str, Any]] | None = None,
    *,
    prefer: list[str] | None = None,
    **credentials: Any,
) -> dict[str, Any]:
    """Assign each STOCK line a warehouse that can actually cover it.

    `lines` is `[{sku, quantity}]`. For each line the first preferred warehouse
    holding the full quantity wins; a line no single warehouse can cover is
    reported as `split` with the per-warehouse availability, and one nothing can
    cover as `short`.

    **Whole lines only.** CHAMPRO takes one `Warehouse` per order line, so
    covering a line from two warehouses means emitting two lines — which is a
    decision about the order, not an allocation detail, so it is surfaced rather
    than performed. `Autowarehouse: "YES"` hands the same problem to CHAMPRO;
    this exists for when the caller needs to know the answer before committing.
    """

    lines = lines or []
    if not lines:
        raise ChamproValidationError("Pass a non-empty `lines` list of {sku, quantity}.")

    order = [w.strip().upper() for w in (prefer or ["IL", "CA", "DR"]) if w.strip()]
    unknown = [w for w in order if w not in WAREHOUSE_CODES]
    if unknown:
        raise ChamproValidationError(
            f"Unknown warehouse(s) {unknown} in `prefer`; valid: {sorted(WAREHOUSE_CODES)}"
        )

    wanted = [str(line.get("sku") or "").strip().upper() for line in lines]
    stock = {
        row["sku"]: row
        for row in check_inventory(skus=[s for s in wanted if s], **credentials)["inventory"]
    }

    assignments: list[dict[str, Any]] = []
    for line in lines:
        sku = str(line.get("sku") or "").strip().upper()
        quantity = int(line.get("quantity") or 0)
        row = stock.get(sku)
        if row is None:
            assignments.append(
                {
                    "sku": sku,
                    "quantity": quantity,
                    "warehouse": None,
                    "status": "unknown_sku",
                    "available": {},
                }
            )
            continue

        available = row["warehouses"]
        chosen = next(
            (w for w in order if (available.get(w) or 0) >= quantity and quantity > 0), None
        )
        if chosen:
            status = "ok"
        elif sum(q for q in available.values() if q) >= quantity:
            status = "split"
        else:
            status = "short"
        assignments.append(
            {
                "sku": sku,
                "quantity": quantity,
                "warehouse": chosen,
                "status": status,
                "available": available,
                "more_expected_on": row["more_expected_on"],
            }
        )

    unresolved = [a for a in assignments if a["status"] != "ok"]
    return {
        "preference": order,
        "assignments": assignments,
        "all_assigned": not unresolved,
        "unresolved": unresolved,
        "order_items": [
            {"sku": a["sku"], "quantity": a["quantity"], "warehouse": a["warehouse"]}
            for a in assignments
            if a["status"] == "ok"
        ],
    }


def _client(credentials: dict[str, Any]) -> ChamproClient:
    return ChamproClient(
        api_customer_key=credentials.get("api_customer_key"),
        cb_customer_key=credentials.get("cb_customer_key"),
        api_base=credentials.get("api_base"),
        cb_base=credentials.get("cb_base"),
    )
