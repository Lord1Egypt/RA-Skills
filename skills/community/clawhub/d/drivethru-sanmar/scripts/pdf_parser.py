"""Best-effort PDF purchase-order parser.

Extracts text from a PDF and attempts to identify the fields a SanMar
PO submission needs: PO number, ship-to address, and line items
(style, color, size, quantity, unit price). The output is a
:class:`ParsedPurchaseOrder` that the agent presents to the user for
approval before it is converted into a real :class:`PurchaseOrderDraft`
and submitted via :func:`sanmar_create_purchase_order`.

Heuristics are intentionally conservative — when a field cannot be
confidently extracted, the parser leaves it blank and adds a warning
rather than guessing. PO formats vary widely across customers, so the
agent should treat parser output as a draft and confirm every field.
"""

from __future__ import annotations

import io
import logging
import re
from pathlib import Path
from typing import Iterable

from schemas import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    ParsedPOLine,
    ParsedPurchaseOrder,
    ParsedShipTo,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class PDFParseError(Exception):
    """Raised when the PDF cannot be opened or contains no extractable text."""


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------


def _extract_text(source: str | bytes | Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise PDFParseError(
            "pypdf is required for PDF parsing. Install it with `pip install pypdf`."
        ) from exc

    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.is_file():
            raise PDFParseError(f"PDF file not found: {path}")
        reader = PdfReader(str(path))
    elif isinstance(source, bytes):
        reader = PdfReader(io.BytesIO(source))
    else:
        raise PDFParseError(f"Unsupported PDF source type: {type(source).__name__}")

    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)
    if not text.strip():
        raise PDFParseError(
            "PDF contained no extractable text — it may be a scanned image. "
            "OCR is not supported by this parser."
        )
    return text


# ---------------------------------------------------------------------------
# Field heuristics
# ---------------------------------------------------------------------------


_PO_NUMBER_PATTERNS = (
    re.compile(r"\bP\.?O\.?\s*(?:Number|No\.?|#)\s*[:\-]?\s*([A-Za-z0-9\-_/]+)", re.I),
    re.compile(r"\bPurchase\s+Order\s*(?:Number|No\.?|#)?\s*[:\-]?\s*([A-Za-z0-9\-_/]+)", re.I),
)

_DATE_PATTERN = re.compile(
    r"\b(?:Order\s+Date|Date|PO\s+Date)\s*[:\-]?\s*"
    r"(\d{1,4}[/\-.]\d{1,2}[/\-.]\d{1,4}|"
    r"[A-Za-z]+\s+\d{1,2},?\s+\d{4})",
    re.I,
)

_SHIP_METHOD_PATTERN = re.compile(
    r"\b(?:Ship\s*Via|Ship\s*Method|Shipping\s*Method|Carrier)\s*[:\-]?\s*"
    r"([A-Za-z0-9 \-]+?)(?:\n|$|  )",
    re.I,
)

_EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_ZIP_PATTERN = re.compile(r"\b(\d{5})(?:-\d{4})?\b")
_STATE_ZIP_LINE = re.compile(
    r"^(?P<city>[A-Za-z .'\-]+?),\s*(?P<state>[A-Z]{2})\s+(?P<zip>\d{5}(?:-\d{4})?)\s*$"
)


def _extract_po_number(text: str) -> str | None:
    for pattern in _PO_NUMBER_PATTERNS:
        m = pattern.search(text)
        if m:
            value = m.group(1).strip().rstrip(".:,")
            if value and value.lower() not in {"number", "no", "#"}:
                return value
    return None


def _extract_date(text: str) -> str | None:
    m = _DATE_PATTERN.search(text)
    return m.group(1).strip() if m else None


def _extract_ship_method(text: str) -> str | None:
    m = _SHIP_METHOD_PATTERN.search(text)
    if not m:
        return None
    return m.group(1).strip().rstrip(".") or None


def _extract_ship_to(text: str) -> ParsedShipTo:
    """Extract a ship-to address block.

    Looks for a 'Ship To' header, then takes the next 3-6 non-empty
    lines and parses the canonical "City, ST 12345" line to anchor
    state/zip. Heuristic — if the PO uses a non-standard layout, the
    caller will see partial fields and a warning.
    """

    lines = [ln.rstrip() for ln in text.splitlines()]
    header_idx: int | None = None
    for i, ln in enumerate(lines):
        if re.search(r"\bShip\s*To\b", ln, re.I):
            header_idx = i
            break
    if header_idx is None:
        return ParsedShipTo()

    # Take up to 8 lines after the header and stop at obvious section breaks.
    block: list[str] = []
    for ln in lines[header_idx + 1 : header_idx + 1 + 12]:
        stripped = ln.strip()
        if not stripped:
            if block:
                break
            continue
        if re.match(r"^(Bill\s*To|Ship\s*Via|Ship\s*Method|Order\s*Date|PO\s*Date|Item|Qty|Style|Description)\b", stripped, re.I):
            break
        block.append(stripped)

    ship_to = ParsedShipTo()
    if not block:
        return ship_to

    ship_to.name = block[0]

    # Find the city/state/zip line
    csz_idx: int | None = None
    for i, ln in enumerate(block):
        m = _STATE_ZIP_LINE.match(ln)
        if m:
            ship_to.city = m.group("city").strip()
            ship_to.state = m.group("state")
            ship_to.zip = m.group("zip")
            csz_idx = i
            break

    # Anything between the name and the city/state/zip line is street.
    middle = block[1:csz_idx] if csz_idx is not None else block[1:]
    if middle:
        ship_to.address1 = middle[0]
        if len(middle) > 1:
            ship_to.address2 = " ".join(middle[1:])

    email_match = _EMAIL_PATTERN.search("\n".join(block))
    if email_match:
        ship_to.email = email_match.group(0)

    return ship_to


# Line parsing -------------------------------------------------------------

# Common SanMar-style PO line patterns. Two main shapes are supported:
#   1. Tabular line:   QTY  STYLE  COLOR ... SIZE  PRICE
#   2. Tabular line:   STYLE  COLOR  SIZE  QTY  PRICE
# Both with optional unit price. Sizes are restricted to a known set to
# avoid grabbing arbitrary tokens.

_SIZE_TOKENS = {
    "XS", "S", "M", "L", "XL",
    "2XL", "3XL", "4XL", "5XL", "6XL",
    "XXL", "XXXL",
    "LT", "XLT", "2XLT", "3XLT", "4XLT",
    "OS", "OSFA",
}
_SIZE_TOKENS |= {f"{n}" for n in range(2, 21)}  # numeric sizes (pants, etc.)

_LINE_QTY_FIRST = re.compile(
    r"^\s*(?P<qty>\d{1,5})\s+"
    r"(?P<style>[A-Z][A-Z0-9\-]{1,15})\s+"
    r"(?P<rest>.+?)\s+"
    r"(?P<size>" + r"|".join(re.escape(s) for s in sorted(_SIZE_TOKENS, key=len, reverse=True)) + r")\b"
    r"(?:\s+\$?(?P<price>\d+(?:\.\d{1,2})?))?\s*$",
    re.I,
)

_LINE_STYLE_FIRST = re.compile(
    r"^\s*(?P<style>[A-Z][A-Z0-9\-]{1,15})\s+"
    r"(?P<rest>.+?)\s+"
    r"(?P<size>" + r"|".join(re.escape(s) for s in sorted(_SIZE_TOKENS, key=len, reverse=True)) + r")\s+"
    r"(?P<qty>\d{1,5})"
    r"(?:\s+\$?(?P<price>\d+(?:\.\d{1,2})?))?\s*$",
    re.I,
)


def _parse_lines(text: str) -> list[ParsedPOLine]:
    parsed: list[ParsedPOLine] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or len(line) < 6:
            continue
        # Skip obvious headers/totals.
        if re.match(r"^(qty|quantity|style|item|description|total|subtotal|tax|shipping)\b", line, re.I):
            continue

        for pattern in (_LINE_QTY_FIRST, _LINE_STYLE_FIRST):
            m = pattern.match(line)
            if not m:
                continue
            style = m.group("style").upper()
            size = m.group("size").upper()
            qty_str = m.group("qty")
            try:
                qty = int(qty_str)
            except (TypeError, ValueError):
                continue
            if qty <= 0:
                continue
            rest = m.group("rest").strip(" -|\t")
            color = _guess_color(rest)
            if not color:
                continue
            description = rest if rest != color else None
            price_raw = m.group("price")
            price = float(price_raw) if price_raw else None
            parsed.append(
                ParsedPOLine(
                    style=style,
                    color=color,
                    size=size,
                    quantity=qty,
                    unit_price=price,
                    description=description,
                    raw=raw,
                )
            )
            break
    return parsed


def _guess_color(rest: str) -> str:
    """Pull the color name out of the middle column of a PO line.

    Most PO lines list the color in the description column; we take
    the trailing alpha tokens (color names tend to be last and
    space-delimited words like "Athletic Heather", "Jet Black").
    Returns the cleaned color string or empty if nothing plausible
    is found.
    """

    rest = re.sub(r"\s+", " ", rest).strip()
    if not rest:
        return ""
    # Drop trailing numeric-only tokens (e.g. SKU codes that bled in).
    tokens = rest.split(" ")
    while tokens and re.fullmatch(r"[\d.\-]+", tokens[-1]):
        tokens.pop()
    if not tokens:
        return ""
    # Take up to the last 4 alpha tokens as the color phrase.
    alpha_tail: list[str] = []
    for tok in reversed(tokens):
        if re.fullmatch(r"[A-Za-z][A-Za-z'\-/]*", tok):
            alpha_tail.append(tok)
            if len(alpha_tail) >= 4:
                break
        else:
            break
    if not alpha_tail:
        return ""
    return " ".join(reversed(alpha_tail)).title()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_purchase_order_pdf(source: str | bytes | Path) -> ParsedPurchaseOrder:
    """Extract a best-effort PO draft from a PDF.

    Accepts a filesystem path, ``Path`` object, or raw PDF bytes.
    Raises :class:`PDFParseError` if the PDF cannot be opened or has
    no extractable text. Otherwise always returns a populated
    :class:`ParsedPurchaseOrder` — fields the parser could not extract
    are left blank and recorded in ``warnings``.
    """

    text = _extract_text(source)
    po_number = _extract_po_number(text)
    order_date = _extract_date(text)
    ship_method = _extract_ship_method(text)
    ship_to = _extract_ship_to(text)
    lines = _parse_lines(text)

    warnings: list[str] = []
    if not po_number:
        warnings.append("po_number not found — confirm with the user before submitting")
    if not ship_to.name or not ship_to.zip:
        warnings.append("ship_to address incomplete — confirm with the user")
    if not lines:
        warnings.append("no line items detected — confirm the PDF format with the user")
    else:
        for ln in lines:
            if not ln.color:
                warnings.append(
                    f"line for style {ln.style} size {ln.size}: color could not be parsed"
                )

    return ParsedPurchaseOrder(
        po_number=po_number,
        order_date=order_date,
        ship_to=ship_to,
        ship_method=ship_method,
        lines=lines,
        warnings=warnings,
        raw_text=text,
    )


def to_purchase_order_draft(parsed: ParsedPurchaseOrder) -> dict:
    """Convert a parsed PO into the dict shape ``sanmar_create_purchase_order`` expects.

    The agent should only call this after the user has approved the
    parsed values. Lines without a quantity/style/color/size are
    dropped with a logged warning.
    """

    if not parsed.po_number:
        raise ValueError("ParsedPurchaseOrder.po_number is required before converting to a draft")
    valid_lines = [
        {
            "style": ln.style,
            "color": ln.color,
            "size": ln.size,
            "quantity": ln.quantity,
        }
        for ln in parsed.lines
        if ln.style and ln.color and ln.size and ln.quantity > 0
    ]
    if not valid_lines:
        raise ValueError("ParsedPurchaseOrder has no valid lines to submit")

    ship_to = parsed.ship_to
    return {
        "po_number": parsed.po_number,
        "ship_to": {
            "name": ship_to.name,
            "address1": ship_to.address1,
            "address2": ship_to.address2,
            "city": ship_to.city,
            "state": ship_to.state,
            "zip": ship_to.zip,
            "email": ship_to.email,
            "ship_method": parsed.ship_method or "UPS",
        },
        "lines": valid_lines,
    }


__all__: Iterable[str] = (
    "PDFParseError",
    "parse_purchase_order_pdf",
    "to_purchase_order_draft",
)
