"""Tool functions for the adidas Click skill.

Thin adapters between the CLI (stdin JSON) and the browser driver. They coerce
the incoming JSON into the typed request models, resolve credentials (inline or
``ADIDAS_CLICK_*`` env), call the driver, and return a plain dict.
"""

from __future__ import annotations

import re
from typing import Any

from adidas_client import AdidasClickCredentials, credentials_from_env
from schemas import OrderLine, OrderRequest, ShipTo, to_dict


# ---------------------------------------------------------------------------
# Coercion
# ---------------------------------------------------------------------------


def _coerce_ship_to(value: Any) -> ShipTo | None:
    if value is None:
        return None
    if isinstance(value, ShipTo):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to ShipTo")
    return ShipTo(
        name=value["name"],
        address1=value["address1"],
        city=value["city"],
        state=value["state"],
        zip=value["zip"],
        address2=value.get("address2", ""),
        country=value.get("country", "US"),
        attention=value.get("attention", ""),
        phone=value.get("phone", ""),
        email=value.get("email", ""),
    )


def _coerce_line(value: Any) -> OrderLine:
    if isinstance(value, OrderLine):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to OrderLine")
    return OrderLine(
        style=value["style"],
        size=value["size"],
        quantity=int(value["quantity"]),
        color=value.get("color", ""),
    )


def _coerce_request(value: Any) -> OrderRequest:
    if isinstance(value, OrderRequest):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to OrderRequest")
    return OrderRequest(
        po_number=value["po_number"],
        lines=[_coerce_line(ln) for ln in value.get("lines", [])],
        new_cart=bool(value.get("new_cart", True)),
        ship_to=_coerce_ship_to(value.get("ship_to")),
        delivery_location_id=value.get("delivery_location_id"),
        ship_method=value.get("ship_method"),
        requested_ship_date=value.get("requested_ship_date"),
        notes=value.get("notes"),
        spread_delivery=bool(value.get("spread_delivery", False)),
        on_insufficient_stock=value.get("on_insufficient_stock", "pause"),
        on_missing_product=value.get("on_missing_product", "pause"),
    )


def _coerce_check_line(value: Any) -> OrderLine:
    """Like :func:`_coerce_line`, but tolerant of check-only omissions.

    A check does not need a quantity to read inventory, and a blank ``size``
    means "every size of this style", so ``size`` and ``quantity`` are optional
    (``quantity`` defaults to 1 so a pricing check still adds a priceable line).
    """

    if isinstance(value, OrderLine):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to OrderLine")
    return OrderLine(
        style=value["style"],
        size=value.get("size", "") or "",
        quantity=int(value.get("quantity", 1) or 1),
        color=value.get("color", ""),
    )


def _coerce_check_request(value: Any) -> OrderRequest:
    """Coerce a check payload into an :class:`OrderRequest`.

    ``po_number`` is optional (the check generates a DO-NOT-BUY marker when it
    is absent), and lines use the tolerant :func:`_coerce_check_line`.
    """

    if isinstance(value, OrderRequest):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to OrderRequest")
    return OrderRequest(
        po_number=value.get("po_number") or "",
        lines=[_coerce_check_line(ln) for ln in value.get("lines", [])],
        new_cart=True,
        ship_to=_coerce_ship_to(value.get("ship_to")),
        delivery_location_id=value.get("delivery_location_id"),
        ship_method=value.get("ship_method"),
        requested_ship_date=value.get("requested_ship_date"),
        notes=value.get("notes"),
        spread_delivery=bool(value.get("spread_delivery", False)),
        on_insufficient_stock=value.get("on_insufficient_stock", "pause"),
        on_missing_product=value.get("on_missing_product", "pause"),
    )


def _coerce_po_list(value: Any) -> list[str]:
    """Coerce a PO argument into a list of PO number strings.

    Accepts a list of strings (or of ``{"po_number"/"po"/"name": ...}`` dicts, so
    a caller can pass rows straight from its own order data), or a single string
    holding one or more POs separated by commas / whitespace.
    """

    if value is None:
        return []
    if isinstance(value, str):
        return [part for part in re.split(r"[,\s]+", value.strip()) if part]
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        for item in value:
            if isinstance(item, dict):
                item = item.get("po_number") or item.get("po") or item.get("name")
            if item is None:
                continue
            out.extend(_coerce_po_list(item) if isinstance(item, str) else [str(item)])
        return out
    return [str(value)]


def _resolve_credentials(
    username: str | None, password: str | None, base_url: str | None
) -> AdidasClickCredentials:
    if username or password:
        # Inline creds take precedence; fall back to env for base_url only.
        return AdidasClickCredentials(
            username=username or "",
            password=password or "",
            base_url=base_url or _env_base_url(),
        )
    return credentials_from_env()


def _env_base_url() -> str:
    import os

    from adidas_client import DEFAULT_BASE_URL

    return os.getenv("ADIDAS_CLICK_BASE_URL", "").strip() or DEFAULT_BASE_URL


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


def adidas_create_purchase_order(
    *,
    purchase_order: dict | None = None,
    confirm: bool = False,
    screenshot_path: str | None = None,
    headless: bool = False,
    username: str | None = None,
    password: str | None = None,
    base_url: str | None = None,
    # Convenience: allow the PO fields at the top level too.
    po_number: str | None = None,
    lines: list | None = None,
    ship_to: dict | None = None,
    delivery_location_id: str | None = None,
    ship_method: str | None = None,
    requested_ship_date: str | None = None,
    notes: str | None = None,
    spread_delivery: bool = False,
    on_insufficient_stock: str = "pause",
    on_missing_product: str = "pause",
    new_cart: bool = True,
) -> dict[str, Any]:
    """Place an adidas Click B2B purchase order via browser automation. **WRITE.**

    Accepts the order either nested under ``purchase_order`` or as top-level
    fields (``po_number``, ``lines``, ``ship_to``, ...). Each line is
    ``{style, color, size, quantity}``; ``ship_to`` is
    ``{name, address1, city, state, zip, address2?, country?, ...}``.

    Credentials come from ``ADIDAS_CLICK_USERNAME`` / ``ADIDAS_CLICK_PASSWORD``
    (or inline ``username`` / ``password``).

    - ``confirm`` false (default): fills and validates the cart/checkout and
      returns a ``dry_run`` preview. Nothing is placed. Pass ``screenshot_path``
      to capture the filled page for review.
    - ``confirm`` true: places the order.

    ``on_insufficient_stock`` (``pause`` | ``order`` | ``skip``, default
    ``pause``) controls out-of-stock lines: ``pause`` places nothing and returns
    ``status="needs_confirmation"`` with an ``out_of_stock`` list so the agent
    can confirm with the user; ``order`` orders them anyway (delayed delivery);
    ``skip`` removes them and orders the rest. See SKILL.md "Out-of-stock
    handling".

    ``on_missing_product`` (``pause`` | ``skip`` | ``error``, default ``pause``)
    controls styles adidas has no product listing for (a wrong article number,
    or one this account is not offered): ``pause`` places nothing and returns
    ``status="needs_confirmation"`` with a ``missing_products`` list so the agent
    can take the choice back to the user; ``skip`` drops those lines and orders
    the rest; ``error`` fails the run. See SKILL.md "Missing / unlisted product
    handling".
    """

    from adidas_browser import create_purchase_order as _create  # lazy: optional dep

    payload = purchase_order or {
        "po_number": po_number,
        "lines": lines or [],
        "new_cart": new_cart,
        "ship_to": ship_to,
        "delivery_location_id": delivery_location_id,
        "ship_method": ship_method,
        "requested_ship_date": requested_ship_date,
        "notes": notes,
        "spread_delivery": spread_delivery,
        "on_insufficient_stock": on_insufficient_stock,
        "on_missing_product": on_missing_product,
    }
    request = _coerce_request(payload)
    credentials = _resolve_credentials(username, password, base_url)

    result = _create(
        request=request,
        credentials=credentials,
        confirm=confirm,
        screenshot_path=screenshot_path,
        headless=headless,
    )
    return to_dict(result)


def adidas_check_inventory_pricing(
    *,
    check: str = "both",
    lines: list | None = None,
    request: dict | None = None,
    po_number: str | None = None,
    screenshot_path: str | None = None,
    headless: bool = False,
    username: str | None = None,
    password: str | None = None,
    base_url: str | None = None,
    ship_to: dict | None = None,
    delivery_location_id: str | None = None,
    ship_method: str | None = None,
    spread_delivery: bool = False,
    on_insufficient_stock: str = "pause",
    on_missing_product: str = "pause",
) -> dict[str, Any]:
    """Check adidas Click **inventory and/or wholesale pricing** — never orders.

    ``check`` selects the mode:

    - ``inventory`` — read each line's live stock level. **No cart is created**
      (add-to-cart is not needed to read inventory). A line with a blank ``size``
      reports every size of that style.
    - ``pricing`` — fill a **throwaway cart**, go all the way to the priced
      checkout screen (the only place wholesale net pricing is shown), read it,
      then **delete the cart**.
    - ``both`` (default) — pricing plus the inventory read while filling the cart.

    Lines are ``{style, size?, quantity?}`` (``quantity`` defaults to 1; needed
    for a pricing line total). The throwaway cart / Customer PO is named with a
    "DO NOT BUY {random}" marker so a leftover from a crash is obviously safe —
    override it with ``po_number`` (≤18 chars). Nothing is ever purchased.

    A style adidas has no listing for never aborts the check: it comes back as a
    ``not_found`` line plus a ``missing_products`` entry, and with
    ``on_missing_product`` at ``pause`` (default) the result's status is
    ``needs_confirmation`` so the agent escalates it to the user. ``skip``
    downgrades that to a warning; ``error`` fails the check.

    Credentials come from ``ADIDAS_CLICK_USERNAME`` / ``ADIDAS_CLICK_PASSWORD``
    (or inline ``username`` / ``password``).
    """

    from adidas_browser import check_inventory_pricing as _check  # lazy: optional dep

    payload = request or {
        "po_number": po_number,
        "lines": lines or [],
        "ship_to": ship_to,
        "delivery_location_id": delivery_location_id,
        "ship_method": ship_method,
        "spread_delivery": spread_delivery,
        "on_insufficient_stock": on_insufficient_stock,
        "on_missing_product": on_missing_product,
    }
    check_request = _coerce_check_request(payload)
    credentials = _resolve_credentials(username, password, base_url)

    result = _check(
        request=check_request,
        credentials=credentials,
        check=check,
        screenshot_path=screenshot_path,
        headless=headless,
    )
    return to_dict(result)


def adidas_get_order_tracking(
    *,
    po_numbers: list | str | None = None,
    po_number: str | None = None,
    pos: list | str | None = None,
    screenshot_path: str | None = None,
    headless: bool = False,
    username: str | None = None,
    password: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Get carrier **tracking numbers** for one or more PO numbers. **READ-ONLY.**

    Searches the adidas Click order book for each PO in turn (a PO commonly maps
    to several adidas orders), opens every matching order, and reads its
    Delivery Tracking table (delivery note, ship date, carrier, tracking
    number + link). An order with no Delivery Tracking link has not shipped: its
    **expected** ship dates are read from the order's article rows instead and
    are flagged as expected everywhere they appear.

    POs may be passed as ``po_numbers`` (a list, or a comma/whitespace-separated
    string), as ``pos``, or as a single ``po_number``. Nothing is written — no
    cart is created and no order is modified.

    The result carries per-PO / per-order detail plus ``table``, a ready-to-
    render Markdown table of every tracking number with the expected-ship-date
    rows annotated. A PO the order book returns nothing for comes back
    ``status="not_found"`` (and flips the result to ``needs_confirmation``) so
    the agent can confirm the number with the user; the other POs still run.

    Credentials come from ``ADIDAS_CLICK_USERNAME`` / ``ADIDAS_CLICK_PASSWORD``
    (or inline ``username`` / ``password``).
    """

    from adidas_browser import get_order_tracking as _tracking  # lazy: optional dep

    requested = _coerce_po_list(po_numbers) or _coerce_po_list(pos) or _coerce_po_list(
        po_number
    )
    credentials = _resolve_credentials(username, password, base_url)

    result = _tracking(
        po_numbers=requested,
        credentials=credentials,
        screenshot_path=screenshot_path,
        headless=headless,
    )
    return to_dict(result)
