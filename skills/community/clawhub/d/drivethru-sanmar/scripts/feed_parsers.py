"""Parsers for SanMar's FTP data files.

Pure functions: text (the file contents) in, typed dataclasses out. No
network, no side effects. Every layout here is transcribed directly from
the SanMar FTP Integration Guide v23.1:

- ``parse_daily_invoice_fixedwidth`` — the fixed-width Daily Invoice file
  (``123456_Invoice_Details-MM-DD-YY.txt``), one line item per row,
  grouped into invoices by invoice number.
- ``parse_edi810`` — the EDI-810 X12 invoice file (best-effort: one
  invoice per ST/SE transaction).
- ``parse_shipment_status`` — the tab-delimited Daily Shipment Status
  (Advance Ship Notification) file, one line item per row.
- ``parse_inventory_feed`` — the pipe-delimited ``sanmar_dip.txt``
  inventory-by-warehouse feed.
"""

from __future__ import annotations

from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    Invoice,
    InvoiceAddress,
    InvoiceLine,
    InventoryFeedRow,
    ShipmentStatusRow,
)


def _f(raw: str | None) -> float | None:
    if raw is None:
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _i(raw: str | None) -> int:
    if raw is None:
        return 0
    raw = raw.strip()
    if not raw:
        return 0
    try:
        return int(float(raw))
    except ValueError:
        return 0


def _iso_date(raw: str) -> str | None:
    """Normalize a yyyymmdd or yyyy-mm-dd date to ISO ``yyyy-mm-dd``."""

    raw = raw.strip()
    if not raw:
        return None
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
    return raw


# ---------------------------------------------------------------------------
# Daily Invoice — fixed-width (SanMar FTP Integration Guide v23.1, p22)
# ---------------------------------------------------------------------------

# (field, start, end) — 1-indexed inclusive character positions.
_INVOICE_FIELDS: list[tuple[str, int, int]] = [
    ("account_number", 1, 10),
    ("account_name", 11, 38),
    ("invoice_number", 39, 47),
    ("invoice_date", 48, 57),
    ("po_number", 58, 72),
    ("order_date", 73, 82),
    ("due_date", 83, 92),
    ("ship_to_name", 93, 132),
    ("ship_to_state", 133, 135),
    ("ship_date", 136, 145),
    ("freight_method", 146, 157),
    ("terms", 158, 169),
    ("unique_key", 170, 179),
    ("style", 180, 189),
    ("color", 190, 203),
    ("description", 204, 253),
    ("size", 254, 257),
    ("pieces", 258, 263),
    ("price", 264, 273),
    ("amount", 274, 283),
    ("sales_tax", 284, 293),
    ("shipping_handling", 294, 303),
    ("total", 304, 313),
    ("invoice_total", 314, 323),
    ("sales_order_number", 324, 332),
]


def parse_daily_invoice_fixedwidth(text: str) -> list[Invoice]:
    """Parse the fixed-width Daily Invoice file into grouped invoices.

    Each row is one line item; rows are grouped into one :class:`Invoice`
    per invoice number. The invoice's ``sub_total`` is computed as the sum
    of its line amounts (merchandise); tax, shipping, and the grand total
    come from the row fields (identical across a given invoice's rows).
    """

    invoices: dict[str, Invoice] = {}
    order: list[str] = []

    for raw_line in text.splitlines():
        # A valid data row extends to at least the Amount column.
        if len(raw_line) < 283 or not raw_line.strip():
            continue
        row = {
            name: raw_line[start - 1 : end].strip()
            for name, start, end in _INVOICE_FIELDS
        }
        invoice_no = row["invoice_number"]
        if not invoice_no:
            continue

        if invoice_no not in invoices:
            order.append(invoice_no)
            invoices[invoice_no] = Invoice(
                invoice_number=invoice_no,
                sales_order_number=row["sales_order_number"] or None,
                po_number=row["po_number"] or None,
                invoice_date=_iso_date(row["invoice_date"]),
                order_date=_iso_date(row["order_date"]),
                due_date=_iso_date(row["due_date"]),
                terms=row["terms"] or None,
                ship_via=row["freight_method"] or None,
                customer_number=row["account_number"] or None,
                sales_tax=_f(row["sales_tax"]),
                shipping_handling=_f(row["shipping_handling"]),
                total_amount=_f(row["invoice_total"]),
                ship_to=InvoiceAddress(
                    name=row["ship_to_name"], state=row["ship_to_state"]
                ),
                remit_to=InvoiceAddress(name=row["account_name"]),
            )
        invoice = invoices[invoice_no]
        invoice.lines.append(
            InvoiceLine(
                style=row["style"],
                color=row["color"],
                size=row["size"],
                description=row["description"],
                quantity=_i(row["pieces"]),
                unit_price=_f(row["price"]),
                amount=_f(row["amount"]),
                unique_key=row["unique_key"] or None,
            )
        )

    # Merchandise sub-total = sum of line extensions.
    for invoice in invoices.values():
        invoice.sub_total = round(
            sum(ln.amount or 0.0 for ln in invoice.lines), 2
        )
    return [invoices[k] for k in order]


# ---------------------------------------------------------------------------
# EDI-810 X12 invoice (SanMar FTP Integration Guide v23.1, p24) — best effort
# ---------------------------------------------------------------------------


def _split_desc(desc: str) -> tuple[str, str, str]:
    """Split an EDI item description like "K420 - Athletic Gold - S" into
    (style, color, size). Falls back gracefully on unexpected formats."""

    parts = [p.strip() for p in desc.split(" - ")]
    if len(parts) >= 3:
        return parts[0], " - ".join(parts[1:-1]), parts[-1]
    if len(parts) == 2:
        return parts[0], parts[1], ""
    return desc.strip(), "", ""


def parse_edi810(text: str) -> list[Invoice]:
    """Best-effort parse of an EDI-810 (X12 004010) invoice file.

    Splits on the ``~`` segment terminator and ``*`` element separator
    (SanMar's 810 uses these). Each ST/SE transaction becomes one
    :class:`Invoice`. Reliably extracted: invoice number/date (BIG),
    line items (IT1: qty, unit price, unique key, description → style/
    color/size), grand total (TDS, implied 2-decimals), and tax (TXI).
    The customer PO number is read from a REF*PO/REF*CO segment or BIG04
    when present, else left ``None``.
    """

    segments = [s.strip() for s in text.replace("\n", "").split("~") if s.strip()]
    invoices: list[Invoice] = []
    current: Invoice | None = None

    for seg in segments:
        elems = seg.split("*")
        tag = elems[0].upper()

        if tag == "ST" and len(elems) > 1 and elems[1] == "810":
            current = Invoice()
            invoices.append(current)
        elif current is None:
            continue
        elif tag == "BIG":
            # BIG01 invoice date, BIG02 invoice number, BIG03 po date, BIG04 po number
            if len(elems) > 1 and elems[1]:
                current.invoice_date = _iso_date(elems[1])
            if len(elems) > 2 and elems[2]:
                current.invoice_number = elems[2]
            if len(elems) > 3 and elems[3]:
                current.order_date = _iso_date(elems[3])
            if len(elems) > 4 and elems[4] and current.po_number is None:
                current.po_number = elems[4]
        elif tag == "REF" and len(elems) > 2 and elems[1].upper() in ("PO", "CO", "IV"):
            if elems[1].upper() in ("PO", "CO") and current.po_number is None:
                current.po_number = elems[2] or None
        elif tag == "IT1":
            qty = _i(elems[2]) if len(elems) > 2 else 0
            unit_price = _f(elems[4]) if len(elems) > 4 else None
            unique_key = elems[7] if len(elems) > 7 else ""
            desc = elems[9] if len(elems) > 9 else ""
            style, color, size = _split_desc(desc)
            current.lines.append(
                InvoiceLine(
                    style=style,
                    color=color,
                    size=size,
                    description=desc,
                    quantity=qty,
                    unit_price=unit_price,
                    amount=round((unit_price or 0.0) * qty, 2) if unit_price else None,
                    unique_key=unique_key or None,
                )
            )
        elif tag == "PID" and len(elems) > 4 and elems[4] and current.lines:
            # Free-form product description enriches the last line item.
            if not current.lines[-1].description:
                current.lines[-1].description = elems[4]
        elif tag == "TDS" and len(elems) > 1:
            # TDS amounts carry implied 2 decimal places.
            cents = _f(elems[1])
            current.total_amount = round(cents / 100.0, 2) if cents is not None else None
        elif tag == "TXI" and len(elems) > 2:
            current.sales_tax = _f(elems[2])
        elif tag == "SAC" and "shipping" in seg.lower():
            # SAC05 holds the charge amount in implied 2-decimal cents.
            if len(elems) > 5:
                amt = _f(elems[5])
                current.shipping_handling = (
                    round(amt / 100.0, 2) if amt is not None else None
                )

    for inv in invoices:
        inv.sub_total = round(sum(ln.amount or 0.0 for ln in inv.lines), 2)
    return invoices


# ---------------------------------------------------------------------------
# Daily Shipment Status / ASN — tab-delimited (FTP Guide v23.1, p21)
# ---------------------------------------------------------------------------

# Column order A..AB per the guide.
_SHIPMENT_COLUMNS = [
    "customer_po",
    "sales_order_number",
    "ship_from",
    "ship_date",
    "ship_to_name",
    "attention",
    "ship_to_address1",
    "ship_to_address2",
    "ship_to_city",
    "ship_to_state",
    "ship_to_zip",
    "ship_to_country",
    "sub_total",
    "freight",
    "handling_fee",
    "invoice_total",
    "tracking_number",
    "total_cases",
    "ship_via",
    "box_number",
    "style",
    "description",
    "color",
    "size",
    "quantity",
    "inventory_key",
    "size_index",
    "lpn",
]
_SHIPMENT_FLOAT = {"sub_total", "freight", "handling_fee", "invoice_total"}
_SHIPMENT_INT = {"total_cases", "quantity"}


def parse_shipment_status(text: str) -> list[ShipmentStatusRow]:
    """Parse the tab-delimited Daily Shipment Status (ASN) file."""

    rows: list[ShipmentStatusRow] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        cells = raw_line.split("\t")
        # Skip a header row if present.
        if cells and cells[0].strip().upper() in ("CUSTOMER PO", "CUSTOMER_PO"):
            continue
        values: dict[str, object] = {}
        for idx, name in enumerate(_SHIPMENT_COLUMNS):
            cell = cells[idx].strip() if idx < len(cells) else ""
            if name in _SHIPMENT_FLOAT:
                values[name] = _f(cell)
            elif name in _SHIPMENT_INT:
                values[name] = _i(cell)
            else:
                values[name] = cell
        rows.append(ShipmentStatusRow(**values))  # type: ignore[arg-type]
    return rows


# ---------------------------------------------------------------------------
# Inventory feed — sanmar_dip.txt, pipe-delimited (FTP Guide v23.1, p15)
# ---------------------------------------------------------------------------


def parse_inventory_feed(
    text: str, *, style_filter: str | None = None
) -> list[InventoryFeedRow]:
    """Parse the pipe-delimited ``sanmar_dip.txt`` inventory-by-warehouse
    feed. Pass ``style_filter`` to keep only rows for one style
    (Catalog_No, case-insensitive)."""

    wanted = style_filter.strip().lower() if style_filter else None
    rows: list[InventoryFeedRow] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        cols = raw_line.split("|")
        if len(cols) < 7:
            continue
        # Skip a header row if present.
        if cols[0].strip().lower() in ("inventory_key", "inventorykey"):
            continue
        style = cols[2].strip()
        if wanted and style.lower() != wanted:
            continue
        rows.append(
            InventoryFeedRow(
                inventory_key=cols[0].strip(),
                size_index=cols[1].strip(),
                style=style,
                color=cols[3].strip(),
                size=cols[4].strip(),
                warehouse_no=cols[5].strip(),
                quantity=_i(cols[6]),
                piece_price=_f(cols[8]) if len(cols) > 8 else None,
                case_price=_f(cols[10]) if len(cols) > 10 else None,
                case_size=(_i(cols[11]) or None) if len(cols) > 11 else None,
                unique_key=cols[17].strip() if len(cols) > 17 else "",
            )
        )
    return rows
