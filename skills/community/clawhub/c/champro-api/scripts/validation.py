"""Local pre-flight for CHAMPRO orders.

Everything here is a rejection CHAMPRO would issue *after* the round trip, and
some of those round trips are expensive: PlaceOrder is not idempotent, has no
dry-run mode on the production host, and answers a partially-valid request by
creating the suborders it liked and reporting errors for the rest. So the
cheapest correct order is one that never leaves the process while it is still
wrong.

Rules implemented, with the documented code each prevents:

| Rule                                              | Code |
| ------------------------------------------------- | ---- |
| SKU exists in the product master's grid            | 08 / E3.1 |
| Quantity is a multiple of MOQ / MOQCustom          | 25 |
| `LeadTime` names one of the master's lead times    | 21 / 22 |
| Proof file is PDF/JPG/JPEG/PNG                     | 02 |
| Custom and stock lines are not mixed in one order  | 07 |
| Warehouse given, or Autowarehouse set              | 11 |
| Recipient name and address are present             | 24 |
| `ShippingMethod` is in the catalog                 | — |
| Collect/third-party method carries a payer account | — |

Each finding is `{severity, code, message, ...}`. `error` blocks submission;
`warning` does not — it is for things CHAMPRO permits but that usually mean
the caller meant something else.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import shipping
from schemas import CUSTOM, PROOF_FILE_EXTENSIONS, STOCK, Order

_REQUIRED_SHIPTO = (
    ("ship_to_first_name", "ShipToFirstName"),
    ("ship_to_last_name", "ShipToLastName"),
    ("address", "Address"),
    ("city", "City"),
    ("state_code", "StateCode"),
    ("zip_code", "ZIPCode"),
)


def _finding(severity: str, code: str | None, message: str, **extra: Any) -> dict[str, Any]:
    return {"severity": severity, "code": code, "message": message, **extra}


def validate_order(
    order: Order,
    *,
    product_info: dict[str, dict[str, Any]] | None = None,
    autowarehouse: bool = False,
) -> list[dict[str, Any]]:
    """Check one order. `product_info` maps product master -> ProductInfo body.

    Without `product_info` the SKU, MOQ and lead-time rules are skipped and
    reported as skipped, rather than silently passing — "not checked" and
    "checked and fine" must not look alike to a caller about to place an order.
    """

    findings: list[dict[str, Any]] = []
    order_type = (order.order_type or "").strip().upper()

    if order_type not in (STOCK, CUSTOM):
        findings.append(
            _finding("error", "19", f"OrderType must be STOCK or CUSTOM, got {order.order_type!r}.")
        )
        return findings

    if not order.items:
        findings.append(_finding("error", "19", "Order has no OrderItems."))

    if not str(order.po or "").strip():
        findings.append(_finding("error", "17", "PO is required; CHAMPRO rejects a blank PO."))

    # -- ship-to (code 24) ---------------------------------------------------
    for attr, wire_name in _REQUIRED_SHIPTO:
        if not str(getattr(order, attr, "") or "").strip():
            findings.append(_finding("error", "24", f"{wire_name} is required."))
    if not str(order.phone or "").strip():
        findings.append(_finding("error", "24", "Phone is required."))
    state = str(order.state_code or "").strip()
    if state and len(state) != 2:
        findings.append(
            _finding(
                "warning",
                "24",
                f"StateCode {state!r} is not a 2-letter code; CHAMPRO validates against UPS.",
            )
        )

    # -- type-specific fields ------------------------------------------------
    if order_type == STOCK:
        findings.extend(_validate_stock(order, autowarehouse=autowarehouse))
    else:
        findings.extend(_validate_custom(order))

    # -- cross-type contamination (code 07) ----------------------------------
    findings.extend(_validate_no_mixing(order, order_type))

    # -- catalog rules (codes 08, 25, 21/22) ---------------------------------
    if product_info is None:
        findings.append(
            _finding(
                "skipped",
                None,
                "SKU / MOQ / lead-time checks skipped: no ProductInfo supplied. "
                "Run `get-product-info` for each product master to enable them.",
            )
        )
    else:
        findings.extend(_validate_against_catalog(order, order_type, product_info))

    return findings


def _validate_stock(order: Order, *, autowarehouse: bool) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    method = str(order.shipping_method or "").strip()
    if not method:
        findings.append(_finding("error", None, "ShippingMethod is required on a STOCK order."))
    else:
        entry = shipping.lookup(method)
        if entry is None:
            findings.append(
                _finding(
                    "error",
                    None,
                    f"ShippingMethod {method!r} is not in CHAMPRO's published list.",
                    suggestions=shipping.suggest(method),
                )
            )
        else:
            # A non-canonical spelling is rewritten (and reported) by
            # `orders._canonicalise_shipping` before this runs, so `method` is
            # already CHAMPRO's own spelling by now.
            if entry.get("billing_type") and not str(
                order.shipping_customer_account or ""
            ).strip():
                findings.append(
                    _finding(
                        "error",
                        None,
                        f"{entry['name']} bills {entry['billing_type']}, so "
                        "ShippingCustomerAccount (the payer's carrier account) is required.",
                    )
                )
            if not entry.get("billing_type") and str(
                order.shipping_customer_account or ""
            ).strip():
                findings.append(
                    _finding(
                        "warning",
                        None,
                        f"ShippingCustomerAccount is set but {entry['name']} is a prepaid "
                        "method; the freight will be billed to your CHAMPRO account.",
                    )
                )

    # -- warehouse (code 11) -------------------------------------------------
    missing = [i.sku for i in order.items if not str(i.warehouse or "").strip()]
    if missing and not autowarehouse:
        findings.append(
            _finding(
                "error",
                "11",
                "No Warehouse on "
                + ", ".join(missing[:5])
                + (" ..." if len(missing) > 5 else "")
                + '. Set a per-item warehouse, or pass autowarehouse:true ("Autowarehouse":"YES").',
            )
        )
    for item in order.items:
        code = str(item.warehouse or "").strip().upper()
        if code and code not in shipping.WAREHOUSE_CODES:
            findings.append(
                _finding(
                    "error",
                    "11",
                    f"{item.sku}: warehouse {code!r} is not one of "
                    f"{sorted(shipping.WAREHOUSE_CODES)}.",
                )
            )
    return findings


def _validate_custom(order: Order) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    if not str(order.lead_time or "").strip():
        findings.append(
            _finding("error", "21", "LeadTime is required on a CUSTOM order (error code 21).")
        )

    url = str(order.proof_file_url or "").strip()
    if not url:
        findings.append(_finding("error", "01", "ProofFileURL is required on a CUSTOM order."))
    else:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            findings.append(
                _finding("error", "01", f"ProofFileURL must be an http(s) URL; got {url!r}.")
            )
        elif not parsed.path.lower().endswith(PROOF_FILE_EXTENSIONS):
            findings.append(
                _finding(
                    "error",
                    "02",
                    "ProofFileURL must end in "
                    + "/".join(e.upper() for e in PROOF_FILE_EXTENSIONS)
                    + f"; got {parsed.path!r}.",
                )
            )
        elif parsed.scheme == "http":
            findings.append(
                _finding(
                    "warning",
                    "01",
                    "ProofFileURL is plain http; CHAMPRO must fetch it server-side "
                    "(error 01 if unreachable).",
                )
            )
    return findings


def _validate_no_mixing(order: Order, order_type: str) -> list[dict[str, Any]]:
    """Code 07: one order is entirely custom or entirely stock."""

    findings: list[dict[str, Any]] = []
    if order_type == STOCK:
        roster = [
            i.sku for i in order.items if i.team_name or i.player_name or i.player_number
        ]
        if roster:
            findings.append(
                _finding(
                    "error",
                    "07",
                    "STOCK lines carry roster fields (TeamName/PlayerName/PlayerNumber) on "
                    + ", ".join(roster[:5])
                    + ". Split those into a CUSTOM order.",
                )
            )
        for attr, name in (("lead_time", "LeadTime"), ("proof_file_url", "ProofFileURL")):
            if str(getattr(order, attr) or "").strip():
                findings.append(
                    _finding("error", "07", f"{name} is a CUSTOM field on a STOCK order.")
                )
    else:
        warehoused = [i.sku for i in order.items if str(i.warehouse or "").strip()]
        if warehoused:
            findings.append(
                _finding(
                    "warning",
                    "07",
                    "Warehouse is set on CUSTOM lines "
                    + ", ".join(warehoused[:5])
                    + "; CHAMPRO assigns the warehouse for custom production, so it is dropped.",
                )
            )
        if str(order.shipping_method or "").strip():
            findings.append(
                _finding(
                    "warning",
                    "07",
                    "ShippingMethod is a STOCK field; a CUSTOM order is routed by LeadTime.",
                )
            )
    return findings


def sku_index(info: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """SKU -> its ProductInfo row, upper-cased."""

    out: dict[str, dict[str, Any]] = {}
    for row in info.get("ProductSKUs") or []:
        sku = str(row.get("SKU") or "").strip().upper()
        if sku:
            out[sku] = row
    return out


def lead_time_names(info: dict[str, Any]) -> list[str]:
    return [
        str(row.get("LeadTimeName") or "").strip()
        for row in info.get("AvailableLeadTimes") or []
        if str(row.get("LeadTimeName") or "").strip()
    ]


def _validate_against_catalog(
    order: Order, order_type: str, product_info: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    # Build a global SKU -> master index across everything the caller fetched.
    index: dict[str, tuple[str, dict[str, Any]]] = {}
    for master, info in product_info.items():
        for sku, row in sku_index(info).items():
            index[sku] = (master, row)

    # -- SKU existence (code 08 / E3.1) --------------------------------------
    quantities: dict[str, int] = {}
    for item in order.items:
        sku = str(item.sku or "").strip().upper()
        if sku not in index:
            findings.append(
                _finding(
                    "error",
                    "08",
                    f"SKU {sku!r} is not in the ProductInfo grid for "
                    + ", ".join(sorted(product_info))
                    + ". Either the SKU is wrong or its product master was not fetched.",
                    sku=sku,
                )
            )
            continue
        master, _row = index[sku]
        quantities[master] = quantities.get(master, 0) + int(item.quantity or 0)
        if int(item.quantity or 0) <= 0:
            findings.append(
                _finding("error", "19", f"{sku}: Quantity must be a positive integer.", sku=sku)
            )

    # -- MOQ increments (code 25) --------------------------------------------
    #
    # The doc words this as increments, not a floor: with MOQCustom 12, a
    # quantity of 18 is rejected even though it exceeds the minimum. The
    # increment applies to the product-master total across the order's lines,
    # which is what makes a roster of 3+3+6 valid at MOQCustom 12 only in
    # aggregate.
    moq_field = "MOQCustom" if order_type == CUSTOM else "MOQ"
    for master, total in quantities.items():
        raw = (product_info.get(master) or {}).get(moq_field)
        try:
            moq = int(raw or 0)
        except (TypeError, ValueError):
            moq = 0
        if moq > 0 and total % moq != 0:
            short = moq - (total % moq)
            findings.append(
                _finding(
                    "error",
                    "25",
                    f"{master}: {moq_field} is {moq}, so the order total must be a multiple "
                    f"of {moq}. Total is {total}; add {short} or drop {total % moq}.",
                    product_master=master,
                    total_quantity=total,
                    moq=moq,
                )
            )

    # -- lead time (codes 21/22) ---------------------------------------------
    if order_type == CUSTOM:
        wanted = str(order.lead_time or "").strip()
        available: list[str] = []
        for master in quantities or product_info:
            available.extend(lead_time_names(product_info.get(master) or {}))
        available = sorted(set(available))
        if wanted and available and wanted.casefold() not in {a.casefold() for a in available}:
            findings.append(
                _finding(
                    "error",
                    "22",
                    f"LeadTime {wanted!r} is not offered for this product. Available: "
                    + ", ".join(available),
                    available_lead_times=available,
                )
            )
    return findings


def blocking(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [f for f in findings if f.get("severity") == "error"]
