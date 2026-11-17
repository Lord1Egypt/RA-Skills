"""Typed request/response models for the adidas Click skill.

Plain dataclasses — no external deps — so the skill runs in any Python 3.11+
process. Conversion to JSON uses :func:`to_dict` (``dataclasses.asdict``).

The order request mirrors what the adidas Click B2B checkout collects: product
lines (style / color / size / quantity) plus a purchase-order number and a
ship-to address. Optional order-level fields (ship method, requested date,
notes) are captured as the real form is reverse-engineered.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Order request (agent input)
# ---------------------------------------------------------------------------


@dataclass
class OrderLine:
    """One product line on an adidas Click order.

    ``style`` is the adidas article number, which on adidas Click **already
    encodes the color** (e.g. ``JW4306`` = "M FLEECE CREW BLACK"), so ``color``
    is optional/informational — no separate color selection is needed. ``size``
    is the portal-facing size label (e.g. ``M``, ``XL``, ``10``); the driver
    resolves it to adidas's numeric size code from the product page.
    """

    style: str
    size: str
    quantity: int
    color: str = ""


@dataclass
class ShipTo:
    """Destination address for an adidas Click order.

    Field set is a superset of what most B2B checkouts collect; unused fields
    are pruned once the real ship-to form is captured.
    """

    name: str
    address1: str
    city: str
    state: str
    zip: str
    address2: str = ""
    country: str = "US"
    attention: str = ""
    phone: str = ""
    email: str = ""


@dataclass
class OrderRequest:
    """A purchase order to place on adidas Click (agent input).

    ``ship_to`` may be omitted when the order ships to a saved/default account
    address; the driver validates that against the captured checkout flow.
    Optional order-level fields are populated as the flow is reverse-engineered.
    """

    po_number: str
    lines: list[OrderLine]
    # Create a fresh cart (named with the PO) at the start of the run and make
    # it active, so the order never lands in a shared/existing cart. Default on.
    new_cart: bool = True
    # Delivery location precedence at checkout:
    #   delivery_location_id (pick a saved location by its number)
    #   > ship_to (add a one-time / dropship location)
    #   > default (leave the cart's preset location).
    ship_to: ShipTo | None = None
    delivery_location_id: str | None = None
    ship_method: str | None = None
    requested_ship_date: str | None = None  # ISO date, if the portal supports it
    notes: str | None = None
    # When a requested size quantity exceeds current availability, adidas offers
    # to "spread" it over future delivery dates. False (default) declines the
    # spread (single delivery); True accepts it.
    spread_delivery: bool = False
    # What to do when a line's full quantity is NOT available:
    #   "pause" (default) — place nothing and return status="needs_confirmation"
    #     with the out-of-stock lines, so the agent confirms with the user.
    #   "order" — order it anyway, accepting delayed delivery (spread).
    #   "skip"  — remove the out-of-stock line(s) and order the rest.
    # (Substitution is handled by the agent re-running with edited lines.)
    on_insufficient_stock: str = "pause"
    # What to do when adidas has no product page for a requested style (a wrong
    # article number, or one this account is simply not offered):
    #   "pause" (default) — place nothing and return status="needs_confirmation"
    #     with the missing styles, so the agent escalates to the user instead of
    #     failing the run.
    #   "skip"  — drop the missing style's line(s) and order the rest.
    #   "error" — raise (the pre-0.7 behaviour): the run fails outright.
    on_missing_product: str = "pause"


# ---------------------------------------------------------------------------
# Order result (driver output)
# ---------------------------------------------------------------------------


@dataclass
class OrderLineResult:
    """Per-line outcome as matched/configured on the portal."""

    style: str
    color: str
    size: str
    quantity: int
    unit_price: str | None = None
    line_total: str | None = None
    available: str | None = None  # availability text the portal shows, if any
    # When adidas restocks a size that is out of stock / short, as the portal
    # shows it ("Nov 8, 2026") and in ISO ("2026-11-08"). Both None when the
    # line is in stock, when the size is flatly unavailable (never restocked),
    # or when the portal posted no date.
    restock_date: str | None = None
    restock_date_iso: str | None = None
    note: str | None = None


@dataclass
class OrderResult:
    """Outcome of an adidas Click order attempt.

    ``status``:
    - ``needs_confirmation`` — the order needs a human decision before it can
      be placed. **Nothing was ordered.** Either one or more lines are not fully
      in stock (``on_insufficient_stock`` was ``pause`` — see ``out_of_stock``)
      or adidas has no product page for a requested style
      (``on_missing_product`` was ``pause`` — see ``missing_products``). Re-run
      with an explicit policy, or with corrected/edited lines.
    - ``dry_run`` — the cart/checkout was filled and validated but **not**
      submitted (``confirm`` was false). No order was placed.
    - ``not_implemented`` — ``confirm`` was true but the final
      review/submit/confirmation step has not been reverse-engineered yet;
      nothing past the filled form was clicked.
    - ``submitted`` — an order was placed (``confirmation_number`` populated).
    - ``error`` — see ``message``.
    """

    status: str
    po_number: str
    lines: list[OrderLineResult] = field(default_factory=list)
    # Populated when status == "needs_confirmation": the lines whose full
    # quantity is not available:
    # [{style, size, requested, available, status, restock_date,
    #   restock_date_iso}, ...] — the restock date is when adidas brings the
    # size back (None on an "unavailable" size, or when none was posted).
    out_of_stock: list[dict] = field(default_factory=list)
    # Styles adidas served no product page for (wrong article number, or not
    # offered to this account), one entry per style:
    # [{style, sizes, requested, reason, detail}, ...]. ``reason`` is
    # "not_found" (the portal said so) or "unresolved" (the product page never
    # rendered a size table — treat the style as unconfirmed, not proven absent).
    missing_products: list[dict] = field(default_factory=list)
    total_quantity: int | None = None
    order_subtotal: str | None = None
    order_total: str | None = None
    confirmation_number: str | None = None
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    screenshot_path: str | None = None
    surface: str = "adidas_click"
    operation: str = "create_purchase_order"


# ---------------------------------------------------------------------------
# Inventory / pricing check (agent input + driver output)
# ---------------------------------------------------------------------------


@dataclass
class CheckLineResult:
    """One line's outcome from an inventory / pricing check.

    A check reuses the ordering flow's product navigation but **never places an
    order**: for a pricing check the cart is filled, priced at checkout, read,
    and then deleted. Inventory fields come straight off the product page; price
    fields require the checkout "Calc. Net Price" step.
    """

    style: str
    size: str
    color: str = ""
    requested_quantity: int | None = None
    # Raw inventory indicator the size tile shows ("300+", "160", "0"); None if
    # unread. ``available_count`` is the parsed integer, or None when the tile is
    # unbounded/unknown ("300+", blank).
    available: str | None = None
    available_count: int | None = None
    # Availability classification: "in_stock" | "backorder" | "unavailable" |
    # "not_found". ("backorder" = orderable but 0/low with a restock date;
    # "unavailable" = the portal's "X" cell, which can never be ordered;
    # "not_found" = adidas served no product page for the style at all, so
    # nothing about it — stock or price — could be read.)
    status: str | None = None
    in_stock: bool | None = None
    # When adidas restocks this size, as shown ("Nov 8, 2026") and in ISO
    # ("2026-11-08"). Populated for a ``backorder`` line; None when the size is
    # in stock, is flatly ``unavailable`` (never restocked), or the portal
    # posted no date — in which case ``note`` says so rather than implying a
    # date exists.
    restock_date: str | None = None
    restock_date_iso: str | None = None
    # Wholesale (net) pricing — populated only for a pricing/both check that
    # reached the priced checkout page.
    unit_price: str | None = None
    line_total: str | None = None
    note: str | None = None


@dataclass
class CheckResult:
    """Outcome of an adidas Click inventory / pricing check.

    ``status``:
    - ``checked`` — the requested inventory and/or pricing was retrieved. For a
      pricing/both check the cart was created, priced, read, and then deleted.
    - ``needs_confirmation`` — the check ran and every resolvable line was
      reported, but adidas served no product page for one or more styles (see
      ``missing_products``) and ``on_missing_product`` was ``pause``. The
      results that *are* present are complete and usable; the caller should take
      the missing styles back to the user.
    - ``error`` — see ``message``.

    ``check`` echoes the requested mode (``inventory`` | ``pricing`` | ``both``).
    ``po_number`` is the "DO NOT BUY" marker used to name the throwaway cart /
    Customer PO on a pricing check (None on an inventory-only check, which never
    touches a cart).
    """

    status: str
    check: str
    po_number: str | None = None
    lines: list[CheckLineResult] = field(default_factory=list)
    # Styles adidas served no product page for, same shape as on OrderResult:
    # [{style, sizes, requested, reason, detail}, ...].
    missing_products: list[dict] = field(default_factory=list)
    total_quantity: int | None = None
    order_total: str | None = None
    # True/False once a pricing check tried to remove its throwaway cart; None
    # when no cart was created (inventory-only).
    cart_deleted: bool | None = None
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    screenshot_path: str | None = None
    surface: str = "adidas_click"
    operation: str = "check_inventory_pricing"


# ---------------------------------------------------------------------------
# Delivery tracking (agent input + driver output)
# ---------------------------------------------------------------------------


@dataclass
class TrackingShipment:
    """One shipped delivery on an adidas Click order.

    Read from the order's Delivery Tracking page — one entry per row of the
    delivery table (an order can ship in several deliveries, and one delivery
    note can carry more than one parcel/tracking number).

    ``carrier`` is adidas's raw carrier code as shown ("UPSN"); ``carrier_name``
    is the human carrier derived from the tracking URL's host (UPS, FedEx, ...)
    or None when the host is unrecognized. The delivery note's PDF download link
    is deliberately **not** captured — its URL embeds a bearer access token.
    """

    delivery_note: str | None = None
    ship_date: str | None = None
    carrier: str | None = None
    carrier_name: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None


@dataclass
class TrackingOrder:
    """One adidas order found for a purchase-order number.

    ``status``:
    - ``shipped`` — the order has a Delivery Tracking page; ``shipments`` holds
      its carrier/tracking rows.
    - ``not_shipped`` — no Delivery Tracking link on the order, so nothing has
      shipped yet. ``expected_ship_dates`` holds the per-article expected ship
      dates read from the order's expanded article rows, and
      ``expected_ship_date`` is the earliest of them (as displayed).
    - ``unreadable`` — the order page could not be opened or parsed; see
      ``note``. Nothing about this order is known.
    """

    order_number: str
    po_number: str = ""
    order_type: str | None = None
    status: str = "unreadable"
    shipments: list[TrackingShipment] = field(default_factory=list)
    # [{"article": str | None, "dates": [str, ...]}, ...] — expected (not
    # actual) ship dates, only populated for an order that has not shipped.
    expected_ship_dates: list[dict] = field(default_factory=list)
    expected_ship_date: str | None = None
    note: str | None = None


@dataclass
class TrackingPO:
    """All adidas orders found for one requested PO number.

    ``status``:
    - ``shipped`` — every order for this PO has shipment tracking.
    - ``partial`` — some orders have shipped, others have not.
    - ``not_shipped`` — orders exist but none has shipped yet.
    - ``unreadable`` — orders exist but none of their pages could be read, so
      whether they shipped is unknown (see each order's ``note``).
    - ``not_found`` — the order-book search returned no order carrying this PO.

    ``partial`` also covers a mix that includes an unreadable order — an order
    whose page did not load is never counted as "not shipped".
    """

    po_number: str
    status: str = "not_found"
    orders: list[TrackingOrder] = field(default_factory=list)
    order_count: int = 0
    shipment_count: int = 0
    note: str | None = None


@dataclass
class TrackingResult:
    """Outcome of an adidas Click delivery-tracking lookup (read-only).

    ``status``:
    - ``checked`` — every requested PO resolved to at least one order.
    - ``needs_confirmation`` — the lookup is **incomplete**: one or more POs
      returned no orders at all (see ``not_found_pos``), and/or an order's page
      could not be read (that order's ``status`` is ``unreadable`` and the run's
      ``warnings`` say which). Everything that *was* read is complete and
      usable; the gaps should be taken back to the user (or retried).
    - ``error`` — see ``message``.

    ``table`` is a ready-to-render Markdown table of every PO / order /
    tracking number, with unshipped lines annotated as expected ship dates.
    """

    status: str
    pos: list[TrackingPO] = field(default_factory=list)
    not_found_pos: list[str] = field(default_factory=list)
    total_orders: int = 0
    total_shipments: int = 0
    table: str = ""
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    screenshot_path: str | None = None
    surface: str = "adidas_click"
    operation: str = "get_order_tracking"


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------


def to_dict(obj: Any) -> Any:
    """Convert dataclass trees to plain JSON-serializable dicts."""

    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj
