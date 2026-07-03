"""Playwright-driven SanMar *portal* automation (browser surface).

Some SanMar customer-portal actions are not exposed by any SOAP/PromoStandards
web service — notably **processing a return**. This module drives the
sanmar.com portal with Playwright to fill those gaps.

The portal login is **separate** from the SOAP web-services credentials
(:class:`SanMarCredentials`). Supply portal creds via
``SANMAR_PORTAL_USERNAME`` / ``SANMAR_PORTAL_PASSWORD`` (or inline kwargs),
modeled as :class:`SanMarPortalCredentials`.

Selectors and the page flow were reverse-engineered from the live portal; see
``references/returns_flow_notes.md`` for the captured HTML and step map.

Playwright is an **optional** dependency, imported lazily — the skill loads
fine without it; only :func:`process_return` needs it (plus a browser binary,
installed via ``python -m playwright install chromium``).

Scope note: the flow up to (but not including) the final
**Continue → review → confirm** submission is implemented. The final submit is
gated behind :data:`FINAL_SUBMIT_IMPLEMENTED` and is intentionally a stub until
the review/success pages are captured from a real return. With ``confirm`` false
the driver fills and validates the form and returns a ``dry_run`` preview without
filing anything.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any

from sanmar_client import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    SanMarAPIError,
    SanMarConfigError,
    SanMarTransportError,
)
from schemas import (  # noqa: E402  (sibling module)
    ReturnLineFill,
    ReturnLineRequest,
    ReturnOrderLine,
    ReturnResult,
    SanMarPortalCredentials,
)

if TYPE_CHECKING:  # pragma: no cover — typing only
    from playwright.sync_api import Page

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Valid return reasons (the <option> values on the reason <select>).
VALID_REASONS = {
    "SAMPLES",
    "UNWANTED",
    "ORDER_INCORRECT",
    "INCORRECT_PRODUCT",
    "DEFECTIVE_DAMAGED",
}

# Reasons that reveal a sub-row requiring free-text details + a
# replacement yes/no choice.
REASONS_REQUIRING_DETAILS = {"ORDER_INCORRECT", "INCORRECT_PRODUCT", "DEFECTIVE_DAMAGED"}

# Reasons whose detail fields live under the ``incorrect-*`` id group
# (vs. the ``defective-*`` group). DEFECTIVE_DAMAGED uses ``defective-*``.
_INCORRECT_GROUP = {"ORDER_INCORRECT", "INCORRECT_PRODUCT"}

# Flip to True once the review → submit → confirmation flow is captured and
# ``_complete_submission`` is implemented.
FINAL_SUBMIT_IMPLEMENTED = False

_DEFAULT_TIMEOUT_MS = 30_000


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def portal_credentials_from_env() -> SanMarPortalCredentials:
    """Load portal credentials from ``SANMAR_PORTAL_*`` env vars.

    Raises :class:`SanMarConfigError` (the agent's cue to ask the user) when
    username or password is missing.
    """

    username = os.getenv("SANMAR_PORTAL_USERNAME", "").strip()
    password = os.getenv("SANMAR_PORTAL_PASSWORD", "").strip()
    base_url = (
        os.getenv("SANMAR_PORTAL_BASE_URL", "").strip() or "https://www.sanmar.com"
    )

    missing = [
        name
        for name, value in (("portal_username", username), ("portal_password", password))
        if not value
    ]
    if missing:
        raise SanMarConfigError(
            "SanMar portal credentials were not provided. Ask the user for "
            + ", ".join(missing)
            + " and supply them via SANMAR_PORTAL_USERNAME / "
            "SANMAR_PORTAL_PASSWORD (separate from the web-services login) or "
            "as portal_username / portal_password in the tool's stdin JSON."
        )
    return SanMarPortalCredentials(
        username=username, password=password, base_url=base_url
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def _clean(value: str | None) -> str:
    return " ".join((value or "").split())


def _to_int(value: str | None) -> int | None:
    digits = "".join(ch for ch in (value or "") if ch.isdigit())
    return int(digits) if digits else None


def _validate_request(lines: list[ReturnLineRequest]) -> None:
    if not lines:
        raise SanMarConfigError("at least one return line is required")
    for ln in lines:
        if not (ln.style and ln.color and ln.size):
            raise SanMarConfigError("each return line needs style, color, and size")
        reason = (ln.reason or "").strip().upper()
        if reason not in VALID_REASONS:
            raise SanMarConfigError(
                f"invalid reason {ln.reason!r} for {ln.style}/{ln.color}/{ln.size}; "
                f"valid reasons: {', '.join(sorted(VALID_REASONS))}"
            )
        if reason in REASONS_REQUIRING_DETAILS:
            if not ln.details:
                raise SanMarConfigError(
                    f"reason {reason} requires 'details' for "
                    f"{ln.style}/{ln.color}/{ln.size}"
                )
            if ln.replacement is None:
                raise SanMarConfigError(
                    f"reason {reason} requires 'replacement' (true/false) for "
                    f"{ln.style}/{ln.color}/{ln.size}"
                )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


class SanMarReturnsDriver:
    """Drives the sanmar.com portal to fill a return for one sales order."""

    def __init__(self, page: "Page", base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    # -- auth -------------------------------------------------------------

    def login(self, credentials: SanMarPortalCredentials) -> None:
        """Log in via the homepage header form (Spring Security)."""

        self.page.goto(self.base_url + "/", wait_until="domcontentloaded")
        try:
            self.page.fill("#login-header-form #username", credentials.username)
            self.page.fill("#login-header-form #password", credentials.password)
            self.page.click(
                "#login-header-form button.btn-primary-df[type=submit]"
            )
        except Exception as exc:  # noqa: BLE001 — surface as transport
            raise SanMarTransportError(f"Could not submit the portal login form: {exc}")
        # Login reloads the homepage (no redirect). Confirm by reaching an
        # authenticated page; a bounce back to a login form means bad creds.
        self.page.wait_for_load_state("networkidle")
        if not self._is_logged_in():
            raise SanMarConfigError(
                "SanMar portal login failed — check SANMAR_PORTAL_USERNAME / "
                "SANMAR_PORTAL_PASSWORD. (The portal login is separate from the "
                "web-services credentials.)"
            )

    def _is_logged_in(self) -> bool:
        # Logged-out chrome carries the `.logged-out` header class; logged-in
        # state drops it. Fall back to confirming order-history is reachable.
        try:
            if self.page.locator(".top-header.logged-out").count() == 0:
                return True
        except Exception:  # noqa: BLE001
            pass
        self.page.goto(
            self.base_url + "/mysanmar/order-history", wait_until="domcontentloaded"
        )
        return self.page.locator("#sales-order-table").count() > 0

    # -- order resolution -------------------------------------------------

    def resolve_po_to_sales_order(self, po_number: str) -> str:
        """Map a PO number to its unique sales-order (SO-…) number.

        PO numbers are not unique in order history, so this raises when a PO
        maps to zero or multiple orders, listing the candidate SO numbers.
        """

        orders = self._collect_orders()
        matches = [
            so for (po, so) in orders if _norm(po) == _norm(po_number)
        ]
        unique = sorted(set(matches))
        if not unique:
            raise SanMarAPIError(
                f"No order found for PO {po_number!r} in the order-history "
                "window (Previous 30 days). Pass the SanMar order number "
                "(order_number='SO-…') directly if it is older."
            )
        if len(unique) > 1:
            raise SanMarAPIError(
                f"PO {po_number!r} maps to multiple orders: {', '.join(unique)}. "
                "Re-run with order_number set to the specific SO-… number."
            )
        return unique[0]

    def _collect_orders(self) -> list[tuple[str, str]]:
        """Return (po_number, sales_order_number) for every order row.

        Bumps the page size to 250 and pages through to cover the full
        30-day window.
        """

        self.page.goto(
            self.base_url + "/mysanmar/order-history", wait_until="domcontentloaded"
        )
        self.page.wait_for_selector("#sales-order-table", timeout=_DEFAULT_TIMEOUT_MS)
        try:
            self.page.select_option("select.items-per-page", "250")
            self.page.wait_for_load_state("networkidle")
        except Exception:  # noqa: BLE001 — selector optional; continue paginating
            pass

        seen: list[tuple[str, str]] = []
        while True:
            rows = self.page.locator("#sales-order-table tbody tr.orders-separator")
            for i in range(rows.count()):
                row = rows.nth(i)
                po = _clean(row.locator("td.col-purchase-order span").first.text_content())
                so = _clean(row.locator("td.col-order-number strong").first.text_content())
                if so:
                    seen.append((po, so))
            nxt = self.page.locator("[data-testid=next-page-button]")
            if nxt.count() == 0 or not nxt.first.is_enabled():
                break
            nxt.first.click()
            self.page.wait_for_load_state("networkidle")
        return seen

    # -- initiate page ----------------------------------------------------

    def open_initiate(self, sales_order_number: str) -> tuple[str, str | None]:
        """Navigate to the initiate-return page; returns (po, order_date)."""

        url = (
            f"{self.base_url}/mysanmar/returns/initiate"
            f"?salesOrderNumber={sales_order_number}"
        )
        self.page.goto(url, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(
                "table.table-initiate-returns tbody tr.order-history-details-items",
                timeout=_DEFAULT_TIMEOUT_MS,
            )
        except Exception as exc:  # noqa: BLE001
            raise SanMarAPIError(
                f"Could not open a return for {sales_order_number}. The order may "
                "not be eligible (returns are available 30 days from purchase, "
                "after shipping) or the order number is wrong."
            ) from exc
        po = _clean(
            self.page.locator("#table-history-summary td.column-po").first.text_content()
        )
        order_date = _clean(
            self.page.locator(
                "#table-history-summary td.column-ordered"
            ).first.text_content()
        )
        return po, (order_date or None)

    def read_lines(self) -> list[ReturnOrderLine]:
        """Parse the returnable line rows on the initiate page."""

        rows = self.page.locator(
            "table.table-initiate-returns tbody tr.order-history-details-items"
        )
        out: list[ReturnOrderLine] = []
        for i in range(rows.count()):
            row = rows.nth(i)
            checkbox_id = row.locator("input[id^=select-item-]").first.get_attribute("id")
            row_index = _to_int(checkbox_id) if checkbox_id else i
            out.append(
                ReturnOrderLine(
                    row_index=row_index if row_index is not None else i,
                    style=_clean(row.locator("td.column-style .style-number").first.text_content()),
                    color=_clean(row.locator("td.column-color .name").first.text_content()),
                    size=_clean(
                        row.locator("td.column-size.d-none.d-lg-table-cell").first.text_content()
                    )
                    or _clean(row.locator("td.column-size").first.text_content()),
                    description=_clean(
                        row.locator("td.column-description span").last.text_content()
                    )
                    or None,
                    warehouse=_clean(
                        row.locator("td.column-warehouse span").last.text_content()
                    )
                    or None,
                    pieces=_to_int(row.locator("td.column-pieces").first.text_content()),
                    price=_clean(row.locator("td.column-price").first.text_content()) or None,
                    amount=_clean(row.locator("td.column-amount span").first.text_content())
                    or None,
                )
            )
        return out

    def match_lines(
        self, requested: list[ReturnLineRequest], available: list[ReturnOrderLine]
    ) -> list[ReturnLineFill]:
        """Match each requested line to exactly one page row by SKU."""

        fills: list[ReturnLineFill] = []
        used: set[int] = set()
        for req in requested:
            reason = req.reason.strip().upper()
            candidates = [
                row
                for row in available
                if _norm(row.style) == _norm(req.style)
                and _norm(row.color) == _norm(req.color)
                and _norm(row.size) == _norm(req.size)
                and row.row_index not in used
            ]
            if not candidates:
                raise SanMarAPIError(
                    f"No returnable line matched {req.style}/{req.color}/{req.size}. "
                    "Available: "
                    + "; ".join(
                        f"{r.style}/{r.color}/{r.size}" for r in available
                    )
                )
            if len(candidates) > 1:
                raise SanMarAPIError(
                    f"{req.style}/{req.color}/{req.size} matched multiple lines on "
                    "this order; the portal return flow cannot disambiguate "
                    "identical SKUs automatically."
                )
            row = candidates[0]
            used.add(row.row_index)
            qty = req.quantity if req.quantity is not None else (row.pieces or 1)
            if row.pieces is not None and qty > row.pieces:
                raise SanMarAPIError(
                    f"Return quantity {qty} for {req.style}/{req.color}/{req.size} "
                    f"exceeds the {row.pieces} originally shipped."
                )
            fills.append(
                ReturnLineFill(
                    style=row.style,
                    color=row.color,
                    size=row.size,
                    quantity=qty,
                    reason=reason,
                    row_index=row.row_index,
                    details=req.details,
                    replacement=req.replacement,
                    image_path=req.image_path,
                )
            )
        return fills

    def fill_line(self, fill: ReturnLineFill) -> None:
        """Select a row, set quantity + reason, and any reason-specific fields."""

        n = fill.row_index
        row = self.page.locator(f"tr.order-history-details-items:has(#select-item-{n})")

        self.page.check(f"#select-item-{n}")
        # Quantity + reason inputs unhide only after the item is checked.
        qty_input = row.locator("td.column-quantity input[type=number]")
        qty_input.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        qty_input.fill(str(fill.quantity))

        row.locator("td.column-select-reason select").select_option(fill.reason)

        if fill.reason in REASONS_REQUIRING_DETAILS:
            self._fill_reason_details(n, fill)

    def _fill_reason_details(self, n: int, fill: ReturnLineFill) -> None:
        group = "incorrect" if fill.reason in _INCORRECT_GROUP else "defective"
        details = self.page.locator(f"#{group}-details-{n}")
        details.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        details.fill(fill.details or "")
        choice = "yes" if fill.replacement else "no"
        self.page.check(f"#{group}-replacement-{choice}-{n}")
        if (
            fill.reason == "DEFECTIVE_DAMAGED"
            and fill.image_path
            and os.path.isfile(fill.image_path)
        ):
            self.page.locator(f"#file{n}").set_input_files(fill.image_path)

    def read_summary(self) -> dict[str, str | None]:
        """Best-effort read of the estimated credit / restock summary."""

        out: dict[str, str | None] = {
            "merchandise": None,
            "restock": None,
            "credit": None,
        }
        labels = {
            "Total Merchandise Amount": "merchandise",
            "Estimated Restock Fee": "restock",
            "Estimated Credit": "credit",
        }
        try:
            rows = self.page.locator(".shipping-payment-summary table tr")
            for i in range(rows.count()):
                row = rows.nth(i)
                start = _clean(row.locator("td.column-start").first.text_content())
                amount = _clean(row.locator("td.column-end .amount").first.text_content())
                for label, key in labels.items():
                    if label.lower() in start.lower():
                        out[key] = amount
        except Exception:  # noqa: BLE001 — summary is informational
            pass
        return out

    def continue_enabled(self) -> bool:
        try:
            btn = self.page.get_by_role("button", name="Continue")
            return btn.count() > 0 and btn.first.is_enabled()
        except Exception:  # noqa: BLE001
            return False

    def screenshot(self, path: str) -> None:
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not capture screenshot at %s: %s", path, exc)

    def complete_submission(self) -> str:  # pragma: no cover — stub
        """Click Continue → review → confirm and return the RMA number.

        TODO: implement once the review/submit/confirmation pages are captured
        from a real return (see ``references/returns_flow_notes.md`` Step 5).
        """

        raise NotImplementedError


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def process_return(
    *,
    order_number: str | None,
    po_number: str | None,
    lines: list[ReturnLineRequest],
    credentials: SanMarPortalCredentials,
    confirm: bool = False,
    screenshot_path: str | None = None,
    headless: bool = True,
) -> ReturnResult:
    """Fill (and optionally file) a SanMar portal return for one order.

    Resolves the order (``order_number`` wins; otherwise ``po_number`` is
    mapped to a unique SO), opens the initiate page, matches each requested
    line to a row, and fills quantity + reason + reason-specific fields.

    With ``confirm`` false (default) it stops before submitting and returns a
    ``dry_run`` preview. With ``confirm`` true it currently returns
    ``not_implemented`` (the final submit flow is not yet captured) unless
    :data:`FINAL_SUBMIT_IMPLEMENTED` is set.
    """

    _validate_request(lines)
    if not order_number and not po_number:
        raise SanMarConfigError("either order_number (SO-…) or po_number is required")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise SanMarConfigError(
            "playwright is required for the portal return flow. Install it with "
            "`pip install playwright` and then `python -m playwright install chromium`."
        ) from exc

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=headless)
        except Exception as exc:  # noqa: BLE001
            raise SanMarConfigError(
                "Could not launch a Chromium browser for Playwright. Run "
                "`python -m playwright install chromium`. "
                f"(underlying error: {exc})"
            ) from exc
        context = browser.new_context()
        context.set_default_timeout(_DEFAULT_TIMEOUT_MS)
        page = context.new_page()
        driver = SanMarReturnsDriver(page, credentials.base_url)
        try:
            driver.login(credentials)

            sales_order = order_number
            if not sales_order:
                sales_order = driver.resolve_po_to_sales_order(po_number or "")

            po, order_date = driver.open_initiate(sales_order)
            available = driver.read_lines()
            fills = driver.match_lines(lines, available)
            for fill in fills:
                driver.fill_line(fill)

            summary = driver.read_summary()
            if screenshot_path:
                driver.screenshot(screenshot_path)

            if not driver.continue_enabled():
                raise SanMarAPIError(
                    "The return form was filled but the Continue button did not "
                    "enable — SanMar may have rejected a field (check quantities, "
                    "reasons, and required details)."
                )

            base = ReturnResult(
                order_number=sales_order,
                po_number=po or po_number,
                order_date=order_date,
                eligible_lines=available,
                return_lines=fills,
                estimated_merchandise_amount=summary.get("merchandise"),
                estimated_restock_fee=summary.get("restock"),
                estimated_credit=summary.get("credit"),
                screenshot_path=screenshot_path,
                status="dry_run",
            )

            if not confirm:
                base.message = (
                    "Dry run — the return form was filled and validated but NOT "
                    "submitted. Re-run with confirm=true to file it."
                )
                return base

            if not FINAL_SUBMIT_IMPLEMENTED:
                base.status = "not_implemented"
                base.message = (
                    "confirm=true was requested, but the final "
                    "Continue → review → confirm submission is not yet "
                    "implemented (pending capture from a real return). The form "
                    "was filled and validated; nothing was submitted."
                )
                return base

            base.rma_number = driver.complete_submission()
            base.status = "submitted"
            base.message = "Return submitted."
            return base
        except (SanMarConfigError, SanMarAPIError, SanMarTransportError):
            raise
        except Exception as exc:  # noqa: BLE001 — normalize unexpected failures
            raise SanMarTransportError(
                f"Unexpected failure during the portal return flow: {exc}"
            ) from exc
        finally:
            context.close()
            browser.close()
