"""Agent-facing SanMar tools.

Each function here is a deterministic callable that other Knoxville
agents invoke. Inputs are typed, outputs are JSON-serializable dicts,
and errors are normalized via :class:`SanMarError` subclasses.

Read-only tools are clearly distinguished from side-effecting tools
(``sanmar_create_purchase_order``, ``sanmar_cancel_order``). The two
write tools require ``confirm=True`` and otherwise return a dry-run
preview without contacting SanMar.

Each LLM-facing function accepts BOTH typed credential dataclasses
(``credentials``, ``ftp_credentials``) AND plain-string kwargs
(``customer_number``, ``username``, ``password``, ``environment``,
``ftp_password``). The plain-string form is what the role's BOOT.md /
SOUL.md instruct the agent to pass on every call; the typed form is
preserved for direct Python callers (tests, sibling skills). When both
are provided, the typed dataclass wins.
"""

from __future__ import annotations

import logging
from collections import namedtuple
from typing import Any

from feed_parsers import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    parse_daily_invoice_fixedwidth,
    parse_edi810,
    parse_inventory_feed,
    parse_shipment_status,
)
from ftp_resolver import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    SanMarFTPConfigError,
    SanMarFTPError,
    lookup_mainframe_color,
)
from pdf_parser import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    PDFParseError,
    parse_purchase_order_pdf,
    to_purchase_order_draft,
)
from sanmar_client import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    SanMarAPIError,
    SanMarClient,
    SanMarConfigError,
    SanMarError,
    credentials_from_env,
)
from sanmar_ftp import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    DEFAULT_OUTBOUND_DIR,
    PDD_DIR,
    SanMarFTP,
)
from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    CancelResult,
    CartValidationResult,
    InventoryFeedResult,
    InventoryLevelsResult,
    InventoryResult,
    InvoiceResult,
    MainframeColorResolution,
    OrderStatusResult,
    ParsedPurchaseOrder,
    PricingLine,
    PricingResult,
    ProductSearchResult,
    PurchaseOrderDraft,
    PurchaseOrderLine,
    PurchaseOrderResult,
    ReturnLineRequest,
    SanMarCredentials,
    SanMarFTPCredentials,
    SanMarPortalCredentials,
    ShipTo,
    ShipmentStatusResult,
    TrackingResult,
    to_dict,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _client(credentials: SanMarCredentials | None) -> SanMarClient:
    if credentials is None:
        credentials = credentials_from_env()
    return SanMarClient(credentials=credentials)


def _build_creds_if_needed(
    credentials: SanMarCredentials | None,
    ftp_credentials: SanMarFTPCredentials | None,
    *,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> tuple[SanMarCredentials | None, SanMarFTPCredentials | None]:
    """Translate plain-string kwargs into typed credential dataclasses.

    Each LLM-facing tool wrapper accepts plain string kwargs that match
    what the role's BOOT.md / SOUL.md tell the agent to pass on every
    call. This helper builds the typed credential objects when they
    aren't already supplied. Internal Python callers that prefer the
    typed form pass ``credentials=`` / ``ftp_credentials=`` directly —
    those win over the plain strings when both are present.

    SanMarFTPCredentials uses the SanMar customer number as its
    ``username`` and the FTP password (separate from the web-services
    password) as its ``password``.
    """

    if credentials is None and (customer_number or username or password):
        credentials = SanMarCredentials(
            customer_number=customer_number or "",
            username=username or "",
            password=password or "",
            environment=environment,
        )
    if ftp_credentials is None and (customer_number or ftp_password):
        ftp_credentials = SanMarFTPCredentials(
            username=customer_number or "",
            password=ftp_password or "",
        )
    return credentials, ftp_credentials


def _invoice_result_to_dict(result: InvoiceResult) -> dict[str, Any]:
    """Serialize an InvoiceResult, attaching the normalized ``common``
    invoice shape to every invoice for the payables workflow."""

    payload = to_dict(result)
    for native, invoice in zip(payload.get("invoices", []), result.invoices):
        native["common"] = invoice.to_common()
    return payload


_FileContent = namedtuple("_FileContent", ["text", "source"])


def _looks_like_dir(remote_path: str) -> bool:
    if remote_path.endswith("/"):
        return True
    base = remote_path.rstrip("/").rsplit("/", 1)[-1]
    return "." not in base  # a basename with no extension → treat as a directory


def _load_file_content(
    *,
    path: str | None,
    text: str | None,
    remote_path: str | None,
    default_dir: str,
    default_glob: str,
    customer_number: str | None,
    ftp_password: str | None,
    ftp_credentials: SanMarFTPCredentials | None,
) -> "_FileContent":
    """Resolve file contents from inline text, a local path, or SFTP.

    For the SFTP path, an exact ``remote_path`` (one that looks like a
    file) is read directly; a directory or an omitted path selects the
    newest file matching ``default_glob``.
    """

    if text is not None:
        return _FileContent(text=text, source="inline")
    if path:
        try:
            with open(path, "rb") as handle:
                raw = handle.read()
        except OSError as exc:
            raise ValueError(f"could not read file {path!r}: {exc}") from exc
        return _FileContent(text=raw.decode("utf-8-sig", errors="replace"), source=path)

    _, ftp_credentials = _build_creds_if_needed(
        None, ftp_credentials, customer_number=customer_number, ftp_password=ftp_password
    )
    with SanMarFTP(ftp_credentials) as ftp:
        target = remote_path
        if not target or _looks_like_dir(target):
            directory = target or default_dir
            found = ftp.find_latest(directory, default_glob)
            if not found:
                raise SanMarFTPError(
                    f"no file matching {default_glob!r} found in {directory!r}"
                )
            target = found
        return _FileContent(text=ftp.read_text(target), source=target)


def _coerce_pricing_line(value: Any) -> PricingLine:
    if isinstance(value, PricingLine):
        return value
    if isinstance(value, dict):
        return PricingLine(
            style=value["style"], color=value["color"], size=value["size"]
        )
    raise TypeError(f"Cannot coerce {value!r} to PricingLine")


def _coerce_po_draft(value: Any) -> PurchaseOrderDraft:
    if isinstance(value, PurchaseOrderDraft):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to PurchaseOrderDraft")

    ship_to_raw = value.get("ship_to")
    if isinstance(ship_to_raw, ShipTo):
        ship_to = ship_to_raw
    elif isinstance(ship_to_raw, dict):
        ship_to = ShipTo(**ship_to_raw)
    else:
        raise ValueError("purchase_order.ship_to is required")

    lines_raw = value.get("lines") or []
    lines: list[PurchaseOrderLine] = []
    for ln in lines_raw:
        if isinstance(ln, PurchaseOrderLine):
            lines.append(ln)
        elif isinstance(ln, dict):
            lines.append(PurchaseOrderLine(**ln))
        else:
            raise TypeError(f"Cannot coerce PO line {ln!r}")

    if not lines:
        raise ValueError("purchase_order.lines must contain at least one line")

    return PurchaseOrderDraft(
        po_number=value["po_number"], ship_to=ship_to, lines=lines
    )


# ---------------------------------------------------------------------------
# Read-only tools
# ---------------------------------------------------------------------------


def sanmar_search_products(
    style: str,
    color: str | None = None,
    size: str | None = None,
    *,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Catalog discovery for a SanMar style.

    Wraps ``getProductInfoByStyleColorSize``. Returns title, weight,
    primary image, and the full set of color/size variants found.
    Read-only.
    """

    if not style:
        raise SanMarConfigError("style is required")
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: ProductSearchResult = client.search_products(style=style, color=color, size=size)
    return to_dict(result)


def _resolve_mainframe_color_or_none(
    style: str,
    color: str,
    size: str | None,
    ftp_credentials: SanMarFTPCredentials | None,
) -> str | None:
    """Try the SDL FTP fallback. Returns the mainframe color or ``None``."""

    try:
        resolution = lookup_mainframe_color(
            style=style,
            color=color,
            size=size,
            credentials=ftp_credentials,
        )
    except (SanMarFTPError, SanMarFTPConfigError) as exc:
        logger.warning(
            "SDL fallback unavailable for style=%s color=%s: %s", style, color, exc
        )
        return None
    if resolution.status == "matched" and resolution.matches:
        return resolution.matches[0].mainframe_color
    return None


def sanmar_check_inventory(
    style: str,
    color: str,
    size: str,
    *,
    credentials: SanMarCredentials | None = None,
    ftp_credentials: SanMarFTPCredentials | None = None,
    auto_resolve_color: bool = True,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Live inventory for a single style/color/size at SanMar warehouses.

    SanMar's inventory endpoint queries against the *mainframe* color
    code, not the marketing color name. If the initial request fails
    with a SanMar API error or returns no warehouses, and
    ``auto_resolve_color`` is ``True`` (default), this tool will fetch
    ``SanMarPDD/SanMar_SDL_N.csv`` from SanMar's SFTP server, resolve
    the marketing color to the mainframe color for the given
    style/size, and retry once. Read-only.
    """

    if not (style and color and size):
        raise SanMarConfigError("style, color, and size are all required")
    credentials, ftp_credentials = _build_creds_if_needed(
        credentials, ftp_credentials,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)

    try:
        result: InventoryResult = client.get_inventory(style=style, color=color, size=size)
    except SanMarAPIError:
        if not auto_resolve_color:
            raise
        mainframe = _resolve_mainframe_color_or_none(style, color, size, ftp_credentials)
        if not mainframe or mainframe == color:
            raise
        logger.info(
            "Retrying inventory query with mainframe color %s (was %s)", mainframe, color
        )
        result = client.get_inventory(style=style, color=mainframe, size=size)
        result.color = mainframe
        return to_dict(result)

    if (
        auto_resolve_color
        and not result.warehouse_quantities
        and not result.total_available
    ):
        mainframe = _resolve_mainframe_color_or_none(style, color, size, ftp_credentials)
        if mainframe and mainframe != color:
            logger.info(
                "Empty inventory for color=%s; retrying with mainframe %s",
                color,
                mainframe,
            )
            retry = client.get_inventory(style=style, color=mainframe, size=size)
            if retry.warehouse_quantities or retry.total_available:
                return to_dict(retry)
    return to_dict(result)


def sanmar_get_pricing(
    lines: list[Any],
    *,
    credentials: SanMarCredentials | None = None,
    ftp_credentials: SanMarFTPCredentials | None = None,
    auto_resolve_color: bool = True,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Customer-specific (`myPrice`) and tier pricing for one or more lines.

    Each line is ``{style, color, size}``. The response also includes
    ``inventory_key`` and ``size_index`` per line — pass those into
    :func:`sanmar_create_purchase_order` to enrich PO submit lines.

    SanMar's pricing endpoint queries against the mainframe color
    code. When ``auto_resolve_color`` is ``True`` (default) and the
    response is missing some lines (a common signal that the marketing
    color name was used), the tool fetches the SDL CSV over SFTP,
    resolves each missing line's mainframe color, and retries once
    with the resolved values. Read-only.
    """

    coerced = [_coerce_pricing_line(ln) for ln in lines]
    if not coerced:
        raise SanMarConfigError("at least one pricing line is required")
    credentials, ftp_credentials = _build_creds_if_needed(
        credentials, ftp_credentials,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)

    try:
        result: PricingResult = client.get_pricing(lines=coerced)
    except SanMarAPIError:
        if not auto_resolve_color:
            raise
        resolved = _resolve_pricing_lines(coerced, ftp_credentials)
        if resolved == coerced:
            raise
        result = client.get_pricing(lines=resolved)
        return to_dict(result)

    if auto_resolve_color and len(result.items) < len(coerced):
        returned_keys = {(_n(it.style), _n(it.color), _n(it.size)) for it in result.items}
        missing = [
            ln
            for ln in coerced
            if (_n(ln.style), _n(ln.color), _n(ln.size)) not in returned_keys
        ]
        if missing:
            resolved_missing = _resolve_pricing_lines(missing, ftp_credentials)
            if resolved_missing != missing:
                retry = client.get_pricing(lines=resolved_missing)
                result.items.extend(retry.items)
    return to_dict(result)


def _n(value: str | None) -> str:
    return (value or "").strip().lower()


def _resolve_pricing_lines(
    lines: list[PricingLine],
    ftp_credentials: SanMarFTPCredentials | None,
) -> list[PricingLine]:
    out: list[PricingLine] = []
    for ln in lines:
        mainframe = _resolve_mainframe_color_or_none(
            ln.style, ln.color, ln.size, ftp_credentials
        )
        if mainframe and mainframe != ln.color:
            out.append(PricingLine(style=ln.style, color=mainframe, size=ln.size))
        else:
            out.append(ln)
    return out


def sanmar_validate_cart(
    purchase_order: Any,
    *,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Pre-submit validation for a draft PO.

    Wraps ``getPreSubmitInfo`` — surfaces per-line inventory and
    validation errors without committing the order. Always safe to
    call. Read-only.
    """

    draft = _coerce_po_draft(purchase_order)
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: CartValidationResult = client.pre_submit_po(draft)
    return to_dict(result)


def sanmar_check_order_status(
    po_number: str,
    *,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Look up SanMar's sales-order number and shipment progress for a PO.

    Wraps the PromoStandards ``GetOrderShipmentNotificationRequest``.
    Read-only.
    """

    if not po_number:
        raise SanMarConfigError("po_number is required")
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: OrderStatusResult = client.get_order_status(po_number=po_number)
    return to_dict(result)


def sanmar_get_tracking(
    po_number: str | None = None,
    *,
    sales_order_number: str | None = None,
    shipment_date: str | None = None,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Tracking + shipment detail for a SanMar order (PromoStandards OSN).

    Query by ``po_number`` (default), ``sales_order_number`` (SanMar's
    ``SO-…`` number), or ``shipment_date`` (UTC, e.g.
    ``2024-01-12T00:00:00Z``; 7-day max window). Returns one package per
    shipment with ``{tracking_number, carrier, shipment_method,
    ship_date, sales_order_number, ship_from_*, ship_to_*, items[]}``.
    Read-only.
    """

    if not (po_number or sales_order_number or shipment_date):
        raise SanMarConfigError(
            "one of po_number, sales_order_number, or shipment_date is required"
        )
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: TrackingResult = client.get_tracking(
        po_number=po_number,
        sales_order_number=sales_order_number,
        shipment_date=shipment_date,
    )
    return to_dict(result)


# ---------------------------------------------------------------------------
# Inventory levels (PromoStandards v2.0.0 — per-warehouse)
# ---------------------------------------------------------------------------


def sanmar_get_inventory_levels(
    style: str,
    *,
    part_ids: Any = None,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Named per-warehouse availability for a style (PromoStandards
    ``getInventoryLevels`` v2.0.0).

    Returns ``{style, parts: [{part_id, color, size, total_available,
    warehouses: [{warehouse_id, warehouse_name, quantity}]}]}``. Pass
    ``part_ids`` (a list of SanMar unique keys) to limit the response to
    specific color/size variants. Read-only.
    """

    if not style:
        raise SanMarConfigError("style is required")
    if part_ids is not None and not isinstance(part_ids, list):
        part_ids = [part_ids]
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: InventoryLevelsResult = client.get_inventory_levels(
        style=style, part_ids=[str(p) for p in part_ids] if part_ids else None
    )
    return to_dict(result)


# ---------------------------------------------------------------------------
# Invoicing (SanMar Standard InvoicePort + FTP daily invoice file)
# ---------------------------------------------------------------------------


def sanmar_get_invoices(
    *,
    po_number: str | None = None,
    invoice_number: str | None = None,
    order_date: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    unpaid: bool = False,
    headers_only: bool = False,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Retrieve SanMar invoices via the ``InvoicePort`` web service.

    Pick exactly one query:
    - ``po_number`` — invoices for a customer PO (the payables match key).
    - ``invoice_number`` — a single invoice by number.
    - ``order_date`` — invoices for an order date (``yyyy-mm-dd``).
    - ``start_date`` + ``end_date`` — invoice date range (≤ 3 months).
    - ``unpaid: true`` — all open (unpaid) invoices.

    Each returned invoice carries the SanMar-native header/lines **and** a
    ``common`` block — the cross-vendor invoice shape consumed by
    ``drivethru-payable-matching``. ``headers_only`` skips line items
    where the query type supports it. Read-only.

    Note: SanMar invoices once/day after 9 p.m. PT; an order is only
    invoiced after it ships. Pull invoice data a day after the order date.
    """

    if po_number:
        query_type, value = "purchase_order", po_number
    elif invoice_number:
        query_type, value = "invoice_number", invoice_number
    elif order_date:
        query_type, value = "order_date", order_date
    elif start_date or end_date:
        query_type, value = "invoice_date_range", None
    elif unpaid:
        query_type, value = "unpaid", None
    else:
        raise SanMarConfigError(
            "provide one of: po_number, invoice_number, order_date, "
            "start_date+end_date, or unpaid=true"
        )

    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)
    result: InvoiceResult = client.get_invoices(
        query_type=query_type,
        value=value,
        start_date=start_date,
        end_date=end_date,
        headers_only=headers_only,
    )
    return _invoice_result_to_dict(result)


def sanmar_parse_invoice_file(
    *,
    path: str | None = None,
    text: str | None = None,
    remote_path: str | None = None,
    edi: bool = False,
    customer_number: str | None = None,
    ftp_password: str | None = None,
    ftp_credentials: SanMarFTPCredentials | None = None,
) -> dict[str, Any]:
    """Parse a SanMar FTP Daily Invoice file into normalized invoices.

    Supply the file one of three ways: ``text`` (raw contents), ``path``
    (a local file), or ``remote_path`` (fetched over SFTP; if the value is
    a directory or omitted, the newest ``*Invoice_Details*`` file in the
    account's outbound folder is used). Set ``edi: true`` for the EDI-810
    format; otherwise the fixed-width Daily Invoice layout is assumed.

    Returns the same shape as ``get-invoices`` (native + ``common`` per
    invoice) so it feeds the payables workflow identically. Read-only.
    """

    content = _load_file_content(
        path=path,
        text=text,
        remote_path=remote_path,
        default_dir=DEFAULT_OUTBOUND_DIR,
        default_glob="*Invoice_Details*.txt",
        customer_number=customer_number,
        ftp_password=ftp_password,
        ftp_credentials=ftp_credentials,
    )
    invoices = parse_edi810(content.text) if edi else parse_daily_invoice_fixedwidth(
        content.text
    )
    result = InvoiceResult(
        query_type="file",
        query_value=content.source,
        count=len(invoices),
        invoices=invoices,
        source_file=content.source,
        surface="sanmar_ftp",
        operation="edi810" if edi else "daily_invoice_file",
    )
    return _invoice_result_to_dict(result)


# ---------------------------------------------------------------------------
# Shipment status + inventory feed (FTP files)
# ---------------------------------------------------------------------------


def sanmar_get_shipment_status(
    *,
    path: str | None = None,
    text: str | None = None,
    remote_path: str | None = None,
    po_number: str | None = None,
    customer_number: str | None = None,
    ftp_password: str | None = None,
    ftp_credentials: SanMarFTPCredentials | None = None,
) -> dict[str, Any]:
    """Parse the FTP Daily Shipment Status (Advance Ship Notification) file.

    Each row is a shipped line item carrying the tracking number, ship
    date/from, per-line costs, and box/LPN detail. Supply ``text``,
    ``path``, or ``remote_path`` (a directory or omission fetches the
    newest ``*Status.txt`` from the outbound folder). Filter to one
    ``po_number`` to see just that order's shipment lines. Read-only.
    """

    content = _load_file_content(
        path=path,
        text=text,
        remote_path=remote_path,
        default_dir=DEFAULT_OUTBOUND_DIR,
        default_glob="*Status.txt",
        customer_number=customer_number,
        ftp_password=ftp_password,
        ftp_credentials=ftp_credentials,
    )
    rows = parse_shipment_status(content.text)
    if po_number:
        rows = [r for r in rows if r.customer_po == po_number]
    result = ShipmentStatusResult(
        rows=rows, count=len(rows), source_file=content.source
    )
    return to_dict(result)


def sanmar_get_inventory_feed(
    *,
    style: str | None = None,
    path: str | None = None,
    text: str | None = None,
    remote_path: str | None = None,
    customer_number: str | None = None,
    ftp_password: str | None = None,
    ftp_credentials: SanMarFTPCredentials | None = None,
) -> dict[str, Any]:
    """Parse the pipe-delimited ``sanmar_dip.txt`` inventory-by-warehouse
    feed (updated hourly on SanMar's SFTP).

    Supply ``text``, ``path``, or ``remote_path`` (omitted →
    ``/SanMarPDD/sanmar_dip.txt``). Pass ``style`` to keep only that
    catalog number's rows — strongly recommended, as the full feed is
    large. Bulk companion to the real-time ``get-inventory-levels`` SOAP
    call. Read-only.
    """

    content = _load_file_content(
        path=path,
        text=text,
        remote_path=remote_path or f"{PDD_DIR}/sanmar_dip.txt",
        default_dir=PDD_DIR,
        default_glob="sanmar_dip.txt",
        customer_number=customer_number,
        ftp_password=ftp_password,
        ftp_credentials=ftp_credentials,
    )
    rows = parse_inventory_feed(content.text, style_filter=style)
    result = InventoryFeedResult(
        style=style, rows=rows, count=len(rows), source_file=content.source
    )
    return to_dict(result)


# ---------------------------------------------------------------------------
# Write tools (high risk)
# ---------------------------------------------------------------------------


def sanmar_create_purchase_order(
    purchase_order: Any,
    *,
    confirm: bool = False,
    credentials: SanMarCredentials | None = None,
    customer_number: str | None = None,
    username: str | None = None,
    password: str | None = None,
    environment: str = "production",
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Submit a SanMar PO. **HIGH-RISK external write.**

    Behavior:

    - If ``confirm`` is False (default), returns a dry-run preview with
      the SOAP envelope that *would* be sent. No network call to the
      submit endpoint happens.
    - If ``confirm`` is True, transmits the order via ``submitPO``.

    Callers should normally:

    1. Call :func:`sanmar_get_pricing` to obtain ``inventory_key`` and
       ``size_index`` per line and populate them on the draft.
    2. Call :func:`sanmar_validate_cart` and only proceed if ``ok``.
    3. Call this function with ``confirm=True``.
    """

    draft = _coerce_po_draft(purchase_order)
    credentials, _ = _build_creds_if_needed(
        credentials, None,
        customer_number=customer_number, username=username, password=password,
        environment=environment, ftp_password=ftp_password,
    )
    client = _client(credentials)

    if not confirm:
        preview = client.build_po_envelope(draft, pre_submit=False)
        return to_dict(
            PurchaseOrderResult(
                status="dry_run",
                po_number=draft.po_number,
                sanmar_reference=None,
                raw_payload=preview.decode("utf-8"),
                raw_response=None,
            )
        )

    result: PurchaseOrderResult = client.submit_po(draft)
    return to_dict(result)


def sanmar_cancel_order(
    po_number: str,
    reason: str | None = None,
    *,
    confirm: bool = False,
    credentials: SanMarCredentials | None = None,  # noqa: ARG001 — interface stable
    customer_number: str | None = None,  # noqa: ARG001 — interface stable
    username: str | None = None,  # noqa: ARG001 — interface stable
    password: str | None = None,  # noqa: ARG001 — interface stable
    environment: str = "production",  # noqa: ARG001 — interface stable
    ftp_password: str | None = None,  # noqa: ARG001 — interface stable
) -> dict[str, Any]:
    """Cancel a SanMar PO. **HIGH-RISK external write — STUB.**

    The reference SanMar SOAP web services and the PromoStandards
    bindings used by this skill do not expose a cancel operation.
    Cancellations today must be performed via SanMar customer service
    or the SanMar account portal.

    The tool surface is reserved so future vendor support can drop in
    without changing callers. Currently always returns a structured
    ``not_implemented`` response.
    """

    if not po_number:
        raise SanMarConfigError("po_number is required")
    return to_dict(
        CancelResult(
            status="not_implemented",
            po_number=po_number,
            message=(
                "SanMar's published web services and PromoStandards "
                "bindings do not currently expose a cancel endpoint. "
                "Cancel via SanMar customer service or the SanMar "
                "account portal. (confirm={confirm}, reason={reason!r})"
            ).format(confirm=confirm, reason=reason),
        )
    )


def _coerce_return_line(value: Any) -> ReturnLineRequest:
    if isinstance(value, ReturnLineRequest):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"Cannot coerce {value!r} to ReturnLineRequest")
    return ReturnLineRequest(
        style=value["style"],
        color=value["color"],
        size=value["size"],
        reason=value["reason"],
        quantity=value.get("quantity"),
        details=value.get("details"),
        replacement=value.get("replacement"),
        image_path=value.get("image_path"),
    )


def sanmar_process_return(
    lines: list[Any],
    *,
    order_number: str | None = None,
    po_number: str | None = None,
    confirm: bool = False,
    screenshot_path: str | None = None,
    headless: bool = True,
    portal_credentials: SanMarPortalCredentials | None = None,
    portal_username: str | None = None,
    portal_password: str | None = None,
    portal_base_url: str | None = None,
) -> dict[str, Any]:
    """Process a SanMar **portal** return via browser automation. **WRITE.**

    Returns are not exposed by any SanMar web service, so this drives the
    sanmar.com customer portal with Playwright. The portal login is separate
    from the SOAP web-services credentials: supply ``portal_username`` /
    ``portal_password`` (or the ``SANMAR_PORTAL_USERNAME`` /
    ``SANMAR_PORTAL_PASSWORD`` env vars).

    Identify the order with ``order_number`` (the SanMar ``SO-…`` number,
    preferred — it is unique) or ``po_number`` (resolved against order
    history; errors if the PO maps to more than one order). Each line is
    ``{style, color, size, reason, quantity?, details?, replacement?,
    image_path?}`` where ``reason`` is one of ``SAMPLES``, ``UNWANTED``,
    ``ORDER_INCORRECT``, ``INCORRECT_PRODUCT``, ``DEFECTIVE_DAMAGED``;
    ``details`` + ``replacement`` are required for the latter three.

    Behavior:

    - ``confirm`` false (default): fills and validates the return form and
      returns a ``dry_run`` preview (matched lines + estimated credit). Nothing
      is filed. Pass ``screenshot_path`` to capture the filled page for review.
    - ``confirm`` true: currently returns ``not_implemented`` — the final
      review/submit/confirmation step has not been reverse-engineered yet.
    """

    from sanmar_browser import process_return as _process_return  # lazy: optional dep

    coerced = [_coerce_return_line(ln) for ln in lines]
    if portal_credentials is None:
        if portal_username or portal_password:
            portal_credentials = SanMarPortalCredentials(
                username=portal_username or "",
                password=portal_password or "",
                base_url=portal_base_url or "https://www.sanmar.com",
            )
        else:
            from sanmar_browser import portal_credentials_from_env

            portal_credentials = portal_credentials_from_env()

    result = _process_return(
        order_number=order_number,
        po_number=po_number,
        lines=coerced,
        credentials=portal_credentials,
        confirm=confirm,
        screenshot_path=screenshot_path,
        headless=headless,
    )
    return to_dict(result)


# ---------------------------------------------------------------------------
# PDF + FTP utility tools
# ---------------------------------------------------------------------------


def sanmar_parse_po_pdf(
    pdf_path: str | None = None,
    *,
    pdf_bytes: bytes | None = None,
) -> dict[str, Any]:
    """Extract a draft purchase order from a PDF.

    Accepts either ``pdf_path`` (filesystem path) or ``pdf_bytes``
    (raw PDF content). Returns a :class:`ParsedPurchaseOrder` dict
    that the agent should present to the user for approval before
    converting it into a draft and submitting via
    :func:`sanmar_create_purchase_order`.

    The parser uses heuristics, not structured extraction. Fields it
    cannot confidently identify are left blank and listed in
    ``warnings``. Read-only.
    """

    if pdf_path is None and pdf_bytes is None:
        raise SanMarConfigError("either pdf_path or pdf_bytes is required")
    if pdf_path is not None and pdf_bytes is not None:
        raise SanMarConfigError("pass exactly one of pdf_path or pdf_bytes")
    source: str | bytes = pdf_bytes if pdf_bytes is not None else pdf_path  # type: ignore[assignment]
    parsed: ParsedPurchaseOrder = parse_purchase_order_pdf(source)
    payload = to_dict(parsed)
    # Drop the raw text from the default response — it's large; the
    # caller can re-parse if needed. Keep it accessible via
    # parse_purchase_order_pdf() directly.
    payload.pop("raw_text", None)
    payload["draft_for_submit"] = (
        to_purchase_order_draft(parsed) if parsed.po_number and parsed.lines else None
    )
    return payload


def sanmar_lookup_mainframe_color(
    style: str,
    color: str,
    size: str | None = None,
    *,
    ftp_credentials: SanMarFTPCredentials | None = None,
    force_refresh: bool = False,
    customer_number: str | None = None,
    ftp_password: str | None = None,
) -> dict[str, Any]:
    """Resolve a marketing color name to SanMar's mainframe color code.

    SanMar's web-service inventory and pricing endpoints query against
    the *mainframe* color, not the marketing ``COLOR_NAME``. This tool
    downloads ``SanMarPDD/SanMar_SDL_N.csv`` from SanMar's SFTP server
    (``ftp.sanmar.com:2200`` over SFTP), caches it locally for 24h,
    and returns the matching ``SANMAR_MAINFRAME_COLOR`` for the given
    ``style`` plus marketing ``color`` (and optional ``size``).

    Returns a :class:`MainframeColorResolution` with status:

    - ``matched``: exactly one mainframe color found.
    - ``ambiguous``: multiple matches — agent should ask the user
      which color they meant.
    - ``not_found``: nothing matched.

    Read-only. Requires FTP credentials (env: ``SANMAR_FTP_PASSWORD``
    plus customer-number username).
    """

    if not style:
        raise SanMarConfigError("style is required")
    if not color:
        raise SanMarConfigError("color is required")
    _, ftp_credentials = _build_creds_if_needed(
        None, ftp_credentials,
        customer_number=customer_number, ftp_password=ftp_password,
    )
    try:
        result: MainframeColorResolution = lookup_mainframe_color(
            style=style,
            color=color,
            size=size,
            credentials=ftp_credentials,
            force_refresh=force_refresh,
        )
    except SanMarFTPConfigError as exc:
        raise SanMarConfigError(str(exc)) from exc
    return to_dict(result)


# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------


__all__ = [
    "PDFParseError",
    "SanMarError",
    "SanMarFTPError",
    "sanmar_search_products",
    "sanmar_check_inventory",
    "sanmar_get_inventory_levels",
    "sanmar_get_inventory_feed",
    "sanmar_get_pricing",
    "sanmar_validate_cart",
    "sanmar_create_purchase_order",
    "sanmar_check_order_status",
    "sanmar_get_tracking",
    "sanmar_get_shipment_status",
    "sanmar_get_invoices",
    "sanmar_parse_invoice_file",
    "sanmar_cancel_order",
    "sanmar_process_return",
    "sanmar_parse_po_pdf",
    "sanmar_lookup_mainframe_color",
]
