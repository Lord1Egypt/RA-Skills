"""Playwright-driven adidas Click B2B ordering automation (browser surface).

adidas Click exposes no public API, so placing a purchase order means driving
the portal with Playwright. This module is being reverse-engineered from real
HTML **one step at a time** — see ``references/order_flow_notes.md`` for the
captured selectors and the step map. Nothing here invents selectors: a step is
only implemented once its HTML has been captured.

Playwright is an **optional** dependency, imported lazily — the skill loads
fine without it; only :func:`create_purchase_order` needs it (plus a browser
binary, installed via ``python -m playwright install chromium``).

Scope note: each page step is gated behind a ``*_IMPLEMENTED`` flag. Until a
step lands, the driver stops early and returns a structured ``not_implemented``
result rather than guessing at selectors. With ``confirm`` false the driver
fills and validates whatever is implemented and returns a ``dry_run`` preview
without placing an order.
"""

from __future__ import annotations

import atexit
import logging
import os
import re
import secrets
import shutil
import string
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import quote, urlparse

from adidas_client import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    AdidasAPIError,
    AdidasClickCredentials,
    AdidasConfigError,
    AdidasTransportError,
    credentials_from_env,
)
from schemas import (  # noqa: E402  (sibling module)
    CheckLineResult,
    CheckResult,
    OrderLine,
    OrderLineResult,
    OrderRequest,
    OrderResult,
    ShipTo,
    TrackingOrder,
    TrackingPO,
    TrackingResult,
    TrackingShipment,
)

if TYPE_CHECKING:  # pragma: no cover — typing only
    from playwright.sync_api import Page

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def _size_lookup_keys(value: str | None) -> list[str]:
    """Candidate size-bar keys for a requested size, most specific first.

    adidas footwear sizes on the size bar are bare integers plus an ``N-`` form
    for the half size *up* (``13-`` == 13.5). Odoo hands sizes as float-strings
    (``"13.0"``, ``"13.5"``), so map those onto the bar's labels; non-numeric
    sizes (apparel: ``XL``) pass through unchanged.
    """
    norm = _norm(value)
    keys = [norm]
    try:
        number = float(norm)
    except ValueError:
        return keys
    whole = int(number)
    frac = number - whole
    if abs(frac) < 1e-9:
        candidate = str(whole)            # 13.0 -> "13"
    elif abs(frac - 0.5) < 1e-9:
        candidate = f"{whole}-"           # 13.5 -> "13-" (half size up)
    else:
        return keys
    if candidate not in keys:
        keys.append(candidate)
    return keys


def _clean(value: str | None) -> str:
    return " ".join((value or "").split())


def _to_int(value: str | None) -> int | None:
    digits = "".join(ch for ch in (value or "") if ch.isdigit())
    return int(digits) if digits else None


def _parse_available(indicator: str | None) -> int | None:
    """Interpret a size tile's inventory indicator as an available count.

    Returns an int for an exact count (``"0"``, ``"160"``), or None when the
    availability is effectively unbounded/unknown (``"300+"``, blank) — in which
    case the line is treated as sufficiently in stock.
    """

    if not indicator:
        return None
    text = indicator.strip()
    if text.endswith("+"):  # e.g. "300+" — at least this many
        return None
    return _to_int(text)


def _iso_date(value: str | None) -> str | None:
    """A portal date ("Nov 8, 2026") as ISO ("2026-11-08"), or None if unparseable.

    Downstream systems (an ERP's expected-date field) want ISO; the raw string
    is kept alongside it so a portal format change degrades to "we still know
    what it said" rather than to nothing.
    """

    parsed = _parse_ship_date(value)
    return parsed.isoformat() if parsed else None


class _OrderPause(Exception):
    """Internal signal: the order needs a human decision before it can be placed.

    Raised when a line isn't fully in stock and ``on_insufficient_stock`` is
    ``pause``, and/or adidas has no product page for a requested style and
    ``on_missing_product`` is ``pause``. Carries both summaries plus a snapshot
    of all requested lines so the entry point can return a
    ``needs_confirmation`` result without ordering anything.
    """

    def __init__(
        self,
        out_of_stock: list[dict],
        lines: list["OrderLineResult"],
        missing_products: list[dict] | None = None,
    ):
        super().__init__("order paused — awaiting confirmation")
        self.out_of_stock = out_of_stock
        self.lines = lines
        self.missing_products = missing_products or []


def _group_by_style(lines: list[OrderLine]) -> dict[str, list[OrderLine]]:
    """Group order lines by article number, preserving first-seen order."""

    grouped: dict[str, list[OrderLine]] = {}
    for line in lines:
        grouped.setdefault(line.style, []).append(line)
    return grouped


# US state / territory 2-letter abbreviation -> the full name adidas Click's
# State dropdown displays. Names must match the dropdown text exactly.
_US_STATE_ABBREV = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
    "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
    # Territories / associated states present in the dropdown.
    "AS": "American Samoa", "GU": "Guam", "PR": "Puerto Rico",
    "VI": "Virgin Islands", "MP": "Northern Mariana Isl", "PW": "Palau",
    "MH": "Marshall Islands", "FM": "Fed. st. Micronesia",
}


# adidas Click Customer PO # allows only letters, numbers, space, and / _ . ? &
# (per the field's own validation message). Anything else (e.g. '-') is rejected.
_PO_ALLOWED_RE = re.compile(r"[^A-Za-z0-9 /_.?&]+")


def _sanitize_po_number(po: str) -> tuple[str, bool]:
    """Replace runs of disallowed characters with '_'. Returns (clean, changed)."""

    clean = _PO_ALLOWED_RE.sub("_", po).strip()
    return clean, clean != po


# A pricing check fills a throwaway cart just to reach the priced checkout page,
# then deletes it — but if a run dies mid-flight, the leftover cart / Customer PO
# must scream "do not buy". The Customer PO field is hard-capped at 18 chars and
# only allows letters, numbers, space, and / _ . ? & (see _PO_ALLOWED_RE), so the
# fuller "AUTOMATED CHECK - DO NOT PURCHASE - …" cannot fit; this is the clearest
# imperative that leaves room for a 5-char random suffix (cart names must be
# unique). Override by passing an explicit ``po_number`` to the check.
_CHECK_PO_PREFIX = "DO NOT BUY"
_CHECK_PO_RANDOM_LEN = 5
# Uppercase letters + digits are all inside the PO charset; drop easily-confused
# glyphs so a human reading the marker off the portal isn't misled.
_CHECK_PO_ALPHABET = "".join(
    c for c in (string.ascii_uppercase + string.digits) if c not in "O0I1L"
)


def _generate_check_po() -> str:
    """Build the "DO NOT BUY {rand5}" marker for a check's throwaway cart / PO.

    Fits the 18-char Customer PO limit and the 25-char cart-name limit, and only
    uses characters the PO field accepts, so it passes through the sanitizer
    unchanged.
    """

    rand = "".join(secrets.choice(_CHECK_PO_ALPHABET) for _ in range(_CHECK_PO_RANDOM_LEN))
    return f"{_CHECK_PO_PREFIX} {rand}"


# Map the internal availability classification (used by the order flow, relative
# to a requested quantity) onto the check's stock-facing vocabulary.
_INVENTORY_STATUS = {
    "ok": "in_stock",
    "short": "backorder",  # orderable but 0/low with a restock date
    "unavailable": "unavailable",  # the portal's "X" cell — never orderable
}


_CURRENCY_RE = re.compile(r"([£$€]?)\s*([\d,]+(?:\.\d+)?)")


def _sum_currency(values: list[str | None]) -> str | None:
    """Sum currency-like strings (e.g. '$35.08'), preserving the symbol.

    Returns None if no value parsed.
    """

    total = 0.0
    symbol = "$"
    found = False
    for value in values:
        match = _CURRENCY_RE.search(value or "")
        if match:
            symbol = match.group(1) or symbol
            total += float(match.group(2).replace(",", ""))
            found = True
    return f"{symbol}{total:,.2f}" if found else None


def _unit_price(line_total: str | None, quantity: int | None) -> str | None:
    """Derive a per-unit price from a line total and quantity, same symbol."""

    if not line_total or not quantity:
        return None
    match = _CURRENCY_RE.search(line_total)
    if not match:
        return None
    symbol = match.group(1) or "$"
    value = float(match.group(2).replace(",", ""))
    return f"{symbol}{value / quantity:,.2f}"


# Debian/Ubuntu package names for Chromium's runtime shared libraries — listed
# in the host-level error so the environment can be fixed.
_CHROMIUM_SYSTEM_PACKAGES = (
    "libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 "
    "libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 "
    "libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2"
)


def _run_playwright(*args: str) -> None:
    """Run ``python -m playwright <args>``, raising on non-zero exit."""

    subprocess.run([sys.executable, "-m", "playwright", *args], check=True)


def _missing_binary(message: str) -> bool:
    return "executable doesn't exist" in message


def _missing_system_libs(message: str) -> bool:
    return (
        "shared librar" in message
        or "libglib" in message
        or "error while loading shared" in message
        or "cannot open shared object" in message
    )


def _launch_chromium(playwright, headless: bool):
    """Launch Chromium, self-healing a missing binary or (best-effort) OS deps.

    The Playwright *package* is a declared dependency, but its Chromium *binary*
    is a separate ~150 MB download that pip/uv doesn't fetch, and the browser
    also needs OS-level shared libraries. There is no OpenClaw install-time hook
    for either, so on the first run we try to install the binary (and, if the
    launch fails on missing shared libraries, the system deps — which needs
    root) and retry. If the host still lacks the libraries, we raise a precise,
    actionable error rather than a raw stack trace.
    """

    try:
        return playwright.chromium.launch(headless=headless, args=_STEALTH_LAUNCH_ARGS)
    except Exception as exc:  # noqa: BLE001
        message = str(exc).lower()
        if not (_missing_binary(message) or _missing_system_libs(message)):
            raise AdidasConfigError(
                f"Could not launch a Chromium browser for Playwright "
                f"(underlying error: {exc})."
            ) from exc

        # Best-effort self-heal: install the binary and/or the OS deps.
        try:
            if _missing_binary(message):
                logger.info("Chromium binary missing — installing it (~150 MB)…")
                _run_playwright("install", "chromium")
            if _missing_system_libs(message):
                logger.info("Chromium system libraries missing — installing deps…")
                _run_playwright("install-deps", "chromium")
        except Exception as install_exc:  # noqa: BLE001 — retry decides the outcome
            logger.warning("Automatic browser install step failed: %s", install_exc)

        try:
            return playwright.chromium.launch(headless=headless, args=_STEALTH_LAUNCH_ARGS)
        except Exception as retry_exc:  # noqa: BLE001
            if _missing_system_libs(str(retry_exc).lower()):
                raise AdidasConfigError(
                    "Chromium is installed but the host is missing the system "
                    "libraries it needs (e.g. libglib-2.0.so.0). This is a host/"
                    "environment issue the skill can't fix without root. Fix it "
                    "one of these ways: (1) run `python -m playwright install-deps "
                    "chromium` (or `playwright install --with-deps chromium`) as "
                    "root on the agent host; (2) have the OpenClaw environment's "
                    "setup script / base image install Chromium's deps — apt "
                    f"packages: {_CHROMIUM_SYSTEM_PACKAGES}. (error: {retry_exc})"
                ) from retry_exc
            raise AdidasConfigError(
                "Could not launch Chromium even after installing it. Run "
                "`python -m playwright install --with-deps chromium` and check the "
                f"host has the required system libraries. (error: {retry_exc})"
            ) from retry_exc


def _stop_process(proc) -> None:
    """Terminate a spawned helper process (best effort)."""
    if not proc or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:  # noqa: BLE001
        proc.kill()


def _headed_needs_virtual_display() -> bool:
    """True only when a headed browser must fall back to an Xvfb virtual display.

    The virtual display is an **X11 (Linux) workaround** for a host with no
    display server — e.g. a headless cloud container. Windows and macOS render a
    headed browser on their native GUI and have no ``DISPLAY`` concept at all, so
    they must **never** try to start Xvfb (doing so wrongly demanded the `xvfb`
    package on Windows). On Linux we still only need it when no display is
    already present — neither an X11 ``DISPLAY`` nor a Wayland session.
    """

    if not sys.platform.startswith("linux"):
        return False  # Windows / macOS: native display, Xvfb is irrelevant.
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _start_virtual_display():
    """Start an Xvfb virtual display for a headed browser on a **Linux** host with
    no X server and point ``$DISPLAY`` at it; return the Xvfb process (register it
    for teardown) or raise ``AdidasConfigError`` if the Xvfb binary is missing.
    Only ever called when :func:`_headed_needs_virtual_display` is true.

    adidas Click's Akamai edge stalls headless Chromium, so the working path is
    a *headed* browser on a virtual display. We spawn ``Xvfb`` directly rather
    than via ``xvfb-run`` so we don't depend on ``xauth`` (minimal images ship
    neither ``xvfb`` nor ``xauth``). ``-displayfd`` lets Xvfb choose a free
    display and report it back once the server is ready — that doubles as a
    readiness signal and avoids display-number collisions across runs.
    """
    xvfb = shutil.which("Xvfb")
    if not xvfb:
        raise AdidasConfigError(
            "Headed mode needs a virtual display, but the Xvfb binary is not "
            "installed. Install it (`apt-get install -y xvfb`) or set "
            "ADIDAS_CLICK_HEADLESS=true to run headless (note: adidas's WAF "
            "stalls headless Chromium)."
        )
    read_fd, write_fd = os.pipe()
    try:
        proc = subprocess.Popen(
            [xvfb, "-displayfd", str(write_fd),
             "-screen", "0", "1440x900x24", "-nolisten", "tcp"],
            pass_fds=(write_fd,),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        os.close(write_fd)
    with os.fdopen(read_fd) as handle:
        display_num = handle.readline().strip()
    if not display_num or proc.poll() is not None:
        _stop_process(proc)
        raise AdidasConfigError(
            "Could not start an Xvfb virtual display for headed Chromium."
        )
    os.environ["DISPLAY"] = f":{display_num}"
    logger.info("Started Xvfb virtual display :%s for headed Chromium", display_num)
    return proc


def _insufficient_stock_message(out_of_stock: list[dict]) -> str:
    """Human-readable summary + the choices for a needs_confirmation result."""

    parts = []
    for s in out_of_stock:
        if s.get("status") == "unavailable":
            parts.append(f"{s['style']} size {s['size']} — not available (cannot be ordered)")
        else:
            restock = (
                f", restocks {s['restock_date']}"
                if s.get("restock_date")
                else ", no restock date posted"
            )
            parts.append(
                f"{s['style']} size {s['size']} — requested {s['requested']}, "
                f"available {s['available'] or 0}{restock}"
            )
    has_unavailable = any(s.get("status") == "unavailable" for s in out_of_stock)
    msg = (
        f"{len(out_of_stock)} line(s) are not fully in stock, so the order was "
        f"NOT placed: {'; '.join(parts)}. Confirm how to proceed, then re-run: "
        "order the backorderable line(s) with delayed delivery "
        "(on_insufficient_stock='order'); remove the out-of-stock line(s) and "
        "order the rest (on_insufficient_stock='skip'); or substitute (edit the "
        "order's lines) and re-run."
    )
    if has_unavailable:
        msg += (
            " NOTE: 'not available' sizes will never be restocked and can only "
            "be removed or substituted — 'order' cannot place them."
        )
    return msg


def _validate_policies(request: OrderRequest) -> tuple[str, str]:
    """Normalize and validate the two "what do I do about it" policies.

    Returns ``(on_insufficient_stock, on_missing_product)`` lowercased. Called
    before the browser launches as well as inside :meth:`add_lines`, so a typo
    fails in milliseconds instead of after a login.
    """

    stock = (request.on_insufficient_stock or "pause").strip().lower()
    if stock not in {"pause", "order", "skip"}:
        raise AdidasConfigError(
            f"on_insufficient_stock must be 'pause', 'order', or 'skip'; "
            f"got {request.on_insufficient_stock!r}."
        )
    missing = (request.on_missing_product or "pause").strip().lower()
    if missing not in {"pause", "skip", "error"}:
        raise AdidasConfigError(
            f"on_missing_product must be 'pause', 'skip', or 'error'; "
            f"got {request.on_missing_product!r}."
        )
    return stock, missing


def _missing_product_message(missing: list[dict], *, ordering: bool = True) -> str:
    """Human-readable summary + the choices when adidas has no such product.

    ``ordering`` false phrases it for a read-only check (which reports whatever
    it *could* read rather than placing nothing).
    """

    parts = []
    for m in missing:
        # "*" is the whole-style inventory request (a check line with no size).
        sizes = (
            ", ".join(s for s in m.get("sizes", []) if s and s != "*") or "all sizes"
        )
        parts.append(f"{m['style']} ({sizes}) — {m.get('detail') or 'no product page'}")
    head = (
        f"adidas Click has no product listing for {len(missing)} requested "
        f"style(s), so the order was NOT placed: "
        if ordering
        else (
            f"adidas Click has no product listing for {len(missing)} requested "
            f"style(s), so they could not be checked: "
        )
    )
    tail = (
        " Ask the user how to proceed, then re-run: correct the article number "
        "(adidas article numbers encode the colorway, e.g. JW4306 — a base "
        "style without the color code will not resolve); drop the style and "
        "proceed with the rest (on_missing_product='skip'); or substitute a "
        "different article."
    )
    note = ""
    if any(m.get("reason") == "unresolved" for m in missing):
        note = (
            " NOTE: at least one style is 'unresolved' — the portal neither "
            "showed the product nor said it was missing (it may be a slow page "
            "or a portal change), so treat it as unconfirmed rather than proven "
            "absent; a retry may resolve it."
        )
    return head + "; ".join(parts) + "." + tail + note


def _resolve_state_name(state: str) -> str:
    """Map a 2-letter US state abbreviation to adidas's full name; pass through
    a value that is already a full name."""

    s = (state or "").strip()
    if len(s) == 2 and s.upper() in _US_STATE_ABBREV:
        return _US_STATE_ABBREV[s.upper()]
    return s


# ---------------------------------------------------------------------------
# Step gates — flip to True as each step's HTML is captured and implemented.
# Mirrors the step map in references/order_flow_notes.md.
# ---------------------------------------------------------------------------

LOGIN_IMPLEMENTED = True            # Step 1 — login
ADD_LINES_IMPLEMENTED = True        # Step 2 — product nav, size map, qty entry
CHECKOUT_IMPLEMENTED = True         # Step 3 — PO number + delivery + shipping
FINAL_SUBMIT_IMPLEMENTED = True     # Step 4 — Next → Calc Net Price → Order Now

_DEFAULT_TIMEOUT_MS = 30_000
# Navigation gets more headroom than ordinary actions: adidas sits behind
# Akamai Bot Manager and the login flow can redirect a few times before the
# authenticated app shell paints.
_NAV_TIMEOUT_MS = 60_000
# Present an ordinary desktop-Chrome fingerprint. adidas Click's Akamai edge
# withholds (stalls to timeout) the HTTP response for clients that look
# automated — a default headless Chromium advertises a "HeadlessChrome" user
# agent and navigator.webdriver=true and gets tarpitted even though the network
# path is fine (a browser-UA curl to the same host returns 200 in <1s).
# Override via ADIDAS_CLICK_USER_AGENT.
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
# Drop the "Chrome is being controlled by automated test software" banner and
# the navigator.webdriver signal at the browser level.
_STEALTH_LAUNCH_ARGS = ["--disable-blink-features=AutomationControlled"]
_LOGIN_PATH = "/login"

# "You're logged in" tell: always-visible elements of the authenticated app
# shell (the login page has none of them). NOTE: the Logout link lives inside a
# collapsed account dropdown, so it is present but hidden — not a reliable
# *visible* tell. These header nav / search controls are always visible.
_LOGGED_IN_MARKER = (
    "#ReorderNavLink, #CartOverviewNavLink, #HeaderSearchButtonButton, "
    "#PersonalNavigationDropdownLabel"
)

# Carts side panel — create a fresh cart per run so shared/existing carts are
# never touched. New Cart opens a name form (the cart name IS the Customer PO /
# personalReference); saving creates it and switches the active cart.
_CARTS_PANEL_BUTTON = "#HeaderCartsTileButton"
_CARTS_LIST = ".o-headerCartsList"  # container of the ag-grid carts list
_CREATE_NEW_CART_BUTTON = "#CreateNewCartButton"
_EDIT_CART_FORM = "form.o-editCartForm"
_EDIT_CART_NAME_INPUT = "form.o-editCartForm input.m-input__field"
_EDIT_CART_SAVE_BUTTON = "#EditCartSaveButton"
_CART_NAME_MAX_LEN = 25  # the cart-name field allows more than the PO field (18)
# Deleting an existing cart with the same PO name (ticking its row checkbox
# reveals the mass-actions trash button; then confirm "Yes").
_DELETE_SELECTED_CARTS_BUTTON = "#DeleteAllCartsButton"
_DELETE_CART_CONFIRM_BUTTON = "#DeleteCartConfirmButton"

# Header search (collapsed by default: click the magnifier to expand, then the
# input appears and the submit button enables once text is entered).
_SEARCH_OPEN_BUTTON = "#HeaderSearchButtonButton"
_SEARCH_INPUT = "#HeaderSearchSearchInput"
_SEARCH_SUBMIT_BUTTON = "#HeaderSearchSubmitButton"

# Product page. adidas article numbers encode the color, so navigating straight
# to the product URL lands on the right color with no color picker.
_PRODUCT_PATH = "/adidas/reorder/product/{style}"
# A style adidas does not offer has no size table to wait for, so the product
# page is polled (rather than blocking on one long wait_for_selector) and gives
# up sooner than the global timeout: an absent product must not burn 30s per
# style before the caller can be told. A real product page renders its size
# table well inside this budget.
_PRODUCT_WAIT_MS = 15_000
_PRODUCT_POLL_MS = 400
# Grace window given to a slow size table after a not-found tell matches, before
# the style is declared missing (see _wait_for_size_table).
_PRODUCT_TELL_GRACE_MS = 2_000
# Positive "no such product" tells, matched against the page's visible text once
# the authenticated shell has painted. The portal's empty-product markup is NOT
# captured (no selector is invented for it), so this is deliberately a text
# match over the wording such pages use, backed by the URL check below. A false
# positive is safe by construction: it can only route the style into the
# missing-product escalation, which places nothing and asks the user.
_PRODUCT_MISSING_TELL_RE = re.compile(
    r"no results|no products? (?:were |was )?found|not found|no such (?:product|article)"
    r"|does(?:n't| not) exist|no longer available|no items? match",
    re.IGNORECASE,
)

# Cart / checkout. /adidas/reorder/cart opens the *active* cart. Quantities that
# overflow availability (when spread is declined) go to a separate, inactive
# cart, so the active cart holds the order we are checking out.
_CART_PATH = "/adidas/reorder/cart"
_CART_HEADER = "#CartModule-CartHeader"
_PO_FIELD = "#CartModule-PersonalReference-InputField input"  # maxlength 18
_PO_MAX_LEN = 18
_DELIVERY_DROPDOWN_LABEL = "#DeliveryAddressOptionsDropdownLabel"
_DELIVERY_DROPDOWN_CONTENT = "#DeliveryAddressOptionsDropdownContent"
_ADD_ONE_TIME_BUTTON = "#DeliveryAddressAddOneTimeShipToButton"
_ONE_TIME_FORM = "#CartModule-DeliveryAddress-OneTimeShipToAddressForm"
_ONE_TIME_SUBMIT = "#DeliveryAddressFormSubmitButton"
_STATE_DROPDOWN_LABEL = "#StateInputFieldDropdownLabel"
_STATE_DROPDOWN_CONTENT = "#StateInputFieldDropdownContent"
_SHIPPING_DROPDOWN_LABEL = "#ShippingMethodsOptionsDropdownLabel"
_SHIPPING_DROPDOWN_CONTENT = "#ShippingMethodsOptionsDropdownContent"
# Shipping-method option codes (stable id suffix #OptionButton{CODE}Button).
_SHIPPING_METHOD_CODES = (
    "DFLT",  # Default
    "FDGP",  # FedEx Ground
    "FDGR",  # FedEx Ground Residential Only
    "FEDE",  # FedEx 2 Day
    "FEDZ",  # FedEx 2 Day Residential Only
    "FED4",  # FedEx 3 Day
    "FESO",  # FedEx Next Business Day
    "FEDN",  # FedEx Next Business Day 10:30
    "FEDY",  # FedEx Next Business Day Residential Only
    "FEDB",  # FedEx Saturday Delivery
)

# Checkout / submit (Step 4).
_CHECKOUT_PATH = "/adidas/reorder/checkout"
_CHECKOUT_NEXT_BUTTON = "#CartModuleCheckoutProgressNPCButton"  # cart -> checkout
# "Calc. Net Price" applies our wholesale discounts and MUST finish before
# ordering — it is slow. In the summary-table header (also per-row). When it
# completes, the button is replaced by a "Done!" message in the header cell.
_CALC_NET_PRICE_BUTTON = "#NPCCartSimulation"
_CALC_DONE_TEXT = "Done!"
_CALC_TIMEOUT_MS = 120_000  # net-price simulation is slow
_ORDER_NOW_BUTTON = "#CartModuleCheckoutProgressBarSubmitOrderButton"
# Order Now auto-redirects to /adidas/reorder/order/{number}/confirmation.
_CONFIRMATION_URL_GLOB = "**/adidas/reorder/order/*/confirmation"
_CONFIRMATION_URL_RE = re.compile(r"/adidas/reorder/order/([^/]+)/confirmation")

# Size table (stable id prefixes; the hashed `*--xxxx` CSS-module classes are
# volatile and deliberately NOT used).
_SIZE_TABLE = "#CartModule-SizeTable"
# The size row scrolls horizontally; off-screen sizes lazy-load when the
# forward/back arrows are clicked (ids carry a dynamic conversion-group number).
_SIZE_NAV_FORWARD = '[id^="CartModuleSizeBarNavigationForward"]'
_SIZE_NAV_BACK = '[id^="CartModuleSizeBarNavigationBack"]'
# Size-label -> numeric-code map lives in the size-bar header cells:
#   #CartModule-SizeBar-SizeTranslation-{group}-{code}  ->  <ins>{label}</ins>
_SIZE_TRANSLATION_PREFIX = "CartModule-SizeBar-SizeTranslation-"
# Per-style, per-size tiles carry the article number + numeric code:
#   quantities cell:  #CartModule-SizeTile-{style}-{code}
#   inventory text:   #CartModule-SizeTile-InventoryIndicator-{style}-{code}
#   material total:   #CartModule-MaterialRow-Summary-TotalQuantity-{style}
#   product name:     #CartModule-TinyProduct-{style}-ProductName

# Availability-date tab (outside the size table). The button text is the
# earliest date on which the product can ship. If it isn't today, the size
# table's inventory numbers refer to *that future date*, not today — so no
# quantity is orderable now regardless of what the tiles show. Must be
# checked first, before reading any size-tile inventory.
_AVAILABLE_DATE_BUTTON = "#DateTabButton"

# Re-stock date. A size tile that will be replenished carries a little calendar
# icon in its top-right corner:
#   #CartModule-SizeTile-RestockIndicator-{style}-{code}
# Its PRESENCE is the "this size gets restocked" tell. The date itself is NOT in
# that markup — the portal renders it only in a hover tooltip ("Re-stock in
# Nov 8, 2026"), so the driver hovers the icon and reads the tooltip that opens.
_SIZE_TILE_RESTOCK_ID = "CartModule-SizeTile-RestockIndicator-{style}-{code}"
# Cheap paths tried before hovering, in case the build exposes the date as an
# attribute somewhere on (or under) the icon.
_RESTOCK_ATTRS = ("title", "aria-label", "data-tooltip", "data-title")
# The tooltip's own markup is NOT captured, so no selector is invented for it:
# after the hover the page text is matched for the portal's wording. Anchored on
# "re-stock" so an unrelated date elsewhere on the page can never be picked up.
_RESTOCK_TOOLTIP_RE = re.compile(
    r"re-?stock(?:ing|s)?\s*(?:in|on|:)?\s*"
    r"([A-Za-z]{3,9}\s+\d{1,2},\s*\d{4})",
    re.IGNORECASE,
)
_RESTOCK_HOVER_SETTLE_MS = 400

# ---------------------------------------------------------------------------
# Order book / delivery tracking (read-only surface)
# ---------------------------------------------------------------------------

# The order book is searched by PO through the URL, so no search-form selectors
# are needed: /adidas/reorder/my/order-book?searchText={po}&page={n}&size={size}
# &filterByRDD=false. Paging is done the same way (bump `page`) rather than
# clicking an un-captured pager.
_ORDER_BOOK_SEARCH_PATH = (
    "/adidas/reorder/my/order-book"
    "?searchText={po}&page={page}&size={size}&filterByRDD=false"
)
_ORDER_BOOK_PAGE_SIZE = 20
_ORDER_BOOK_MAX_PAGES = 10  # 200 orders for one PO is already implausible
# Result rows. Each row's cell holds one <div class="m-orderHeaderData"> whose
# <h2 id="OrderHeaderRow{order}Heading"> text IS the adidas order number; the
# item list below it carries the customer PO and the order type ("Re-Order").
_ORDER_ROW = "div.m-orderHeaderData"
_ORDER_ROW_HEADING = 'h2[id^="OrderHeaderRow"]'
_ORDER_ROW_ID_RE = re.compile(r"OrderHeaderRow(.+?)Heading")
_ORDER_ROW_PO = ".m-orderHeaderData__item span"
_ORDER_ROW_TYPE = ".m-orderHeaderData__item .a-orderType"
# The grid virtualizes rows, so collection scrolls until no new row appears.
_ORDER_BOOK_SCROLL_PASSES = 20
_ORDER_BOOK_WAIT_MS = 20_000
_ORDER_BOOK_POLL_MS = 400

# Order detail. The Delivery Tracking link's captured href
# (/adidas/reorder/my/order-book/{order}/deliveries) gives both paths.
_ORDER_DETAIL_PATH = "/adidas/reorder/my/order-book/{order}"
_DELIVERIES_PATH = "/adidas/reorder/my/order-book/{order}/deliveries"
# Present ONLY when the order has shipments — its absence is the "nothing has
# shipped yet" tell, so a missing link is a result, not an error.
_ORDER_TRACKING_LINK = "#OrderTrackingButtonLink"
# Per-article expected-ship-date rows on an unshipped order: a chevron toggle
# expands the article's week list, whose header shows the expected ship date.
_ARTICLE_WEEK_TOGGLE = ".o-orderDetailArticle__weekToggle button"
_ARTICLE_WEEK_NAME = ".o-orderDetailArticle__weekItemHeaderName"
# Article container: inferred from the BEM block of the two captured elements
# above (both are `o-orderDetailArticle__*`). Only used to group dates per
# article — if it does not match, the dates are still reported order-level.
_ARTICLE_BLOCK = ".o-orderDetailArticle"
_ORDER_DETAIL_WAIT_MS = 20_000
# Grace given to a slow-rendering Delivery Tracking link after the article rows
# have painted, before the order is declared unshipped.
_TRACKING_LINK_GRACE_MS = 2_000

# Delivery Tracking page. One `__item` per delivery row. NOTE: each row also
# holds a delivery-note PDF link whose href embeds a bearer access token — it is
# deliberately NOT read or returned.
_DELIVERY_ITEM = ".o-deliveryTrackingOverview__item"
_DELIVERY_NOTE_LINK = 'a[id^="DownloadPdfCtaLink"]'
_DELIVERY_SHIP_DATE = ".o-deliveryTrackingOverview__shipDate"
_DELIVERY_CARRIER = ".o-deliveryTrackingOverview__carrier"
_DELIVERY_TRACKING_LINK = ".m-trackingNumber__trackingNumber a"
_DELIVERY_WAIT_MS = 20_000
# Carrier names derived from the tracking URL host (adidas shows only a code
# such as "UPSN"; the link it wraps names the actual carrier).
_CARRIER_HOSTS = (
    ("ups.com", "UPS"),
    ("fedex.com", "FedEx"),
    ("usps.com", "USPS"),
    ("dhl.com", "DHL"),
    ("ontrac.com", "OnTrac"),
)
# Expected-ship-date format on the article week header ("Feb 4, 2027").
_SHIP_DATE_FORMATS = ("%b %d, %Y", "%B %d, %Y")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


class AdidasClickDriver:
    """Drives the adidas Click portal to place one purchase order.

    Methods are filled in as each step's HTML is captured. Until then they
    raise :class:`AdidasConfigError` pointing at the flow-notes doc, so a
    premature run fails loudly instead of acting on invented selectors.
    """

    def __init__(self, page: "Page", base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        # Populated from the review page during complete_submission.
        self.order_total: str | None = None
        self.line_net_prices: list[str | None] = []
        # Styles adidas served no product page for, keyed by style so a style
        # visited more than once in a run (e.g. a check that falls back from
        # pricing to an inventory read) is reported once.
        self._missing_by_style: dict[str, dict] = {}

    @property
    def missing_products(self) -> list[dict]:
        """Styles this run could not open a product page for, in request order."""

        return list(self._missing_by_style.values())

    # -- cart management --------------------------------------------------

    def create_new_cart(self, name: str) -> int:
        """Delete any pre-existing cart named ``name``, then create a fresh cart
        named ``name`` and activate it.

        adidas Click allows multiple carts; on a shared account this guarantees
        the run never adds to (or checks out) someone else's cart. Cart names
        must be **unique**, so a same-named leftover (e.g. from an errored prior
        run) is deleted **first**. The active cart cannot be deleted, so if the
        leftover is active, a different cart is activated before deleting it.
        The cart name is the Customer PO (personalReference). Returns the number
        of pre-existing same-named carts deleted.
        """

        self._ensure_carts_panel_open()
        deleted = self._delete_carts_named(name)

        # New Cart control returns once the mass-actions bar clears after a
        # delete (do not toggle the panel button here — that would close it).
        self.page.wait_for_selector(
            _CREATE_NEW_CART_BUTTON, state="visible", timeout=_DEFAULT_TIMEOUT_MS
        )
        self.page.click(_CREATE_NEW_CART_BUTTON)

        name_input = self.page.locator(_EDIT_CART_NAME_INPUT)
        name_input.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        name_input.fill(name[:_CART_NAME_MAX_LEN])
        # Save enables once the name is valid + unique; fail fast + clear if not.
        try:
            self.page.wait_for_selector(
                f"{_EDIT_CART_SAVE_BUTTON}:not([disabled])", timeout=10_000
            )
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(
                f"Could not save the new cart {name!r} — the Save button stayed "
                "disabled (a cart with this name may still exist, or the name is "
                "invalid)."
            ) from exc
        self.page.click(_EDIT_CART_SAVE_BUTTON)
        try:
            self.page.wait_for_selector(
                _EDIT_CART_FORM, state="detached", timeout=_DEFAULT_TIMEOUT_MS
            )
        except Exception:  # noqa: BLE001 — form may just hide; continue
            pass
        self.page.wait_for_load_state("networkidle")
        return deleted

    def _ensure_carts_panel_open(self) -> None:
        """Open the carts side panel if it is not already showing."""

        if self.page.locator(_CREATE_NEW_CART_BUTTON).is_visible():
            return
        self.page.click(_CARTS_PANEL_BUTTON)
        self.page.wait_for_selector(
            _CREATE_NEW_CART_BUTTON, state="visible", timeout=_DEFAULT_TIMEOUT_MS
        )
        self.page.wait_for_load_state("networkidle")  # let the carts grid render

    def _cart_rows(self) -> list[dict]:
        """Snapshot the carts list: row-id, name (title), active flag, toggle id."""

        rows = self.page.locator(f'{_CARTS_LIST} div[role="row"]')
        out: list[dict] = []
        for i in range(rows.count()):
            row = rows.nth(i)
            row_id = row.get_attribute("row-id")
            if not row_id:
                continue
            link = row.locator("a.a-link")
            title = link.first.get_attribute("title") if link.count() else None
            toggle = row.locator('div.a-toggle[id$="ToggleActiveCartToggle"]')
            toggle_id = toggle.first.get_attribute("id") if toggle.count() else None
            out.append(
                {
                    "row_id": row_id,
                    "title": title,
                    "is_active": row.locator(".o-activeBadge").count() > 0,
                    "toggle_id": toggle_id,
                }
            )
        return out

    def _delete_carts_named(self, name: str) -> int:
        """Delete every cart named ``name`` in the (open) panel. Returns the count.

        Matches by name (== Customer PO), so only carts with this exact PO are
        touched. If a same-named cart is the active one, a different cart is
        activated first (the active cart cannot be deleted).
        """

        rows = self._cart_rows()
        old_ids = [r["row_id"] for r in rows if r["title"] == name]
        if not old_ids:
            return 0

        if any(r["is_active"] for r in rows if r["title"] == name):
            others = [
                r for r in rows if r["row_id"] not in set(old_ids) and r["toggle_id"]
            ]
            if not others:
                raise AdidasConfigError(
                    f"The active cart is a leftover named {name!r} and there is "
                    "no other cart to switch to, so it can't be auto-deleted. "
                    "Empty or rename it in the portal, or pass new_cart:false."
                )
            self.page.locator(f'[id="{others[0]["toggle_id"]}"]').click()
            self.page.wait_for_load_state("networkidle")

        return self._delete_cart_rows(old_ids)

    def _delete_cart_rows(self, row_ids: list[str]) -> int:
        """Tick the given (inactive) cart rows and delete them. Returns the count."""

        for row_id in row_ids:
            checkbox = self.page.locator(
                f'div[role="row"][row-id="{row_id}"] input.ag-checkbox-input'
            ).first
            checkbox.check()

        self.page.wait_for_selector(
            _DELETE_SELECTED_CARTS_BUTTON, state="visible", timeout=_DEFAULT_TIMEOUT_MS
        )
        self.page.click(_DELETE_SELECTED_CARTS_BUTTON)
        self.page.wait_for_selector(
            _DELETE_CART_CONFIRM_BUTTON, state="visible", timeout=_DEFAULT_TIMEOUT_MS
        )
        self.page.click(_DELETE_CART_CONFIRM_BUTTON)
        self.page.wait_for_load_state("networkidle")
        return len(row_ids)

    # -- Step 1: auth -----------------------------------------------------

    def login(self, credentials: AdidasClickCredentials) -> None:
        """Log into adidas Click via the standard username/password form.

        The login page (``/login``) posts ``#loginFormDsk`` to ``/login``. We
        fill the visible fields and click the real "Login" button
        (``#send2Dsk``) so any JS validation + CSRF hidden fields come along —
        the "Single Sign On for Sales Managers" path (``#send2SSO``) is a
        separate identity-provider flow we do not use here.
        """

        self.page.goto(self.base_url + _LOGIN_PATH, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector("#loginFormDsk", timeout=_DEFAULT_TIMEOUT_MS)
            self.page.fill("#usernameField", credentials.username)
            self.page.fill("#passwordField", credentials.password)
            # Leave "Remember me" (#form-reminder) unchecked.
            self.page.click("#send2Dsk")
        except Exception as exc:  # noqa: BLE001 — surface as transport
            raise AdidasTransportError(
                f"Could not submit the adidas Click login form: {exc}"
            )
        self.page.wait_for_load_state("networkidle")

        # Bad credentials: the form flips #login-error-alert visible in place
        # (JS, no navigation). An SSO misconfig surfaces on #sso-login-error-alert.
        if self._login_error_visible():
            raise AdidasConfigError(
                "adidas Click login failed — check ADIDAS_CLICK_USERNAME / "
                "ADIDAS_CLICK_PASSWORD. (The 'Single Sign On for Sales Managers' "
                "path is separate and not used by this skill.)"
            )
        # Success tell: a valid login lands on the re-order home and the
        # authenticated header renders. Wait for an always-visible shell control
        # (not the Logout link, which is hidden inside a collapsed dropdown).
        try:
            self.page.wait_for_selector(
                _LOGGED_IN_MARKER, state="visible", timeout=_DEFAULT_TIMEOUT_MS
            )
        except Exception as exc:  # noqa: BLE001
            raise AdidasConfigError(
                "adidas Click login did not complete — the authenticated header "
                "did not appear. The account may require SSO, or an interstitial "
                "is blocking the flow."
            ) from exc

    def _login_error_visible(self) -> bool:
        for selector in ("#login-error-alert", "#sso-login-error-alert"):
            try:
                if self.page.locator(selector).is_visible():
                    return True
            except Exception:  # noqa: BLE001
                continue
        return False

    # -- search -----------------------------------------------------------

    def _search_style(self, style: str) -> None:
        """Open the header search, enter a style number, and submit.

        The header search is collapsed by default — the input is revealed by
        the magnifier button (:data:`_SEARCH_OPEN_BUTTON`). The submit button
        (:data:`_SEARCH_SUBMIT_BUTTON`) is disabled until text is present.
        """

        field = self.page.locator(_SEARCH_INPUT)
        if not field.is_visible():
            self.page.click(_SEARCH_OPEN_BUTTON)
            field.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        field.fill(style)
        self.page.click(_SEARCH_SUBMIT_BUTTON)
        self.page.wait_for_load_state("networkidle")

    # -- Step 2: add product lines ---------------------------------------

    def add_lines(self, request: OrderRequest) -> list["OrderLineResult"]:
        """Enter quantities for each requested {style, size, quantity}.

        First reads availability for every line (opening each product once), then
        applies the ``on_insufficient_stock`` policy for any line whose full
        quantity is not available:

        - ``pause`` (default): raise :class:`_OrderPause` — the entry point
          returns ``needs_confirmation`` and **nothing is ordered**.
        - ``order``: enter it anyway, accepting delayed delivery (spread).
        - ``skip``: do not enter it (removed from the order); order the rest.

        A style adidas serves **no product page** for is handled separately by
        ``on_missing_product``: ``pause`` (default) raises the same
        :class:`_OrderPause` carrying ``missing_products`` so the caller can
        take the choice to the user, ``skip`` drops those lines and orders the
        rest, and ``error`` fails the run outright.

        Lines are grouped by style so each product page is opened once; adidas
        encodes color in the article number, so no color selection is needed.
        """

        policy, missing_policy = _validate_policies(request)

        # "error" restores the pre-0.7 behaviour: a style adidas does not carry
        # aborts the run inside _open_product instead of coming back as a
        # decision for the caller.
        prepared = self._prepare_lines(request, missing_ok=missing_policy != "error")

        missing = [p for p in prepared if p["status"] == "not_found"]
        problems = [
            p for p in prepared if p["status"] not in ("ok", "not_found")
        ]
        if (policy == "pause" and problems) or (missing_policy == "pause" and missing):
            raise _OrderPause(
                out_of_stock=[self._shortfall_dict(p) for p in problems],
                lines=[
                    self._prepared_result(p, note=self._status_note(p))
                    for p in prepared
                ],
                missing_products=self.missing_products if missing else [],
            )

        results: list[OrderLineResult] = []
        current_style: str | None = None
        entered_any = False
        for p in prepared:
            status, style, line, code = p["status"], p["style"], p["line"], p["code"]

            # A style with no product listing has nothing to enter a quantity
            # into. Reaching here means the policy is "skip" (or a pause was
            # already raised above), so drop the line and keep going.
            if status == "not_found":
                results.append(
                    self._prepared_result(p, quantity=0, note=self._status_note(p))
                )
                continue

            # "Not available" sizes can never be ordered (no quantity input) —
            # drop them under every policy, with a clear note. Date-gated
            # products (available date != today) surface the future date so
            # the caller knows when the size can ship.
            if status == "unavailable":
                results.append(
                    self._prepared_result(
                        p, quantity=0, note=self._status_note(p)
                    )
                )
                continue

            if status == "short" and policy == "skip":
                results.append(
                    self._prepared_result(
                        p,
                        quantity=0,
                        note=(
                            f"removed — out of stock (requested {line.quantity}, "
                            f"available {p['indicator'] or 0})"
                        ),
                    )
                )
                continue

            if style != current_style:
                self._open_product(style)
                current_style = style
            spread = request.spread_delivery or (status == "short" and policy == "order")
            committed = self._set_size_quantity(style, code, line.quantity, spread)
            entered_any = True

            note = None
            if status == "short" and policy == "order":
                note = (
                    f"ordered with delayed delivery (requested {line.quantity}, "
                    f"available {p['indicator'] or 0})"
                )
            elif committed is not None and committed != line.quantity:
                note = f"committed {committed} of {line.quantity} requested"
            results.append(
                self._prepared_result(
                    p,
                    quantity=committed if committed is not None else line.quantity,
                    note=note,
                )
            )

        if not entered_any:
            reasons = []
            if any(p["status"] == "not_found" for p in prepared):
                reasons.append(
                    "adidas has no product listing for "
                    + ", ".join(sorted(self._missing_by_style))
                )
            if problems:
                reasons.append("every requested size was out of stock or unavailable")
            raise AdidasConfigError(
                "No lines could be ordered — "
                + ("; ".join(reasons) or "no line resolved to an orderable size")
                + "."
            )
        return results

    def _prepare_lines(
        self, request: OrderRequest, *, missing_ok: bool = True
    ) -> list[dict]:
        """Resolve each line to its size code and classify availability.

        Opens each product once; scrolls the horizontal size row to bring each
        requested size into view (it lazy-loads). Classifies each size as:
        ``ok`` (enough stock), ``short`` (orderable but < requested — e.g. 0 with
        a restock date), ``unavailable`` (the "not available" / X cell, which
        can never be ordered), or ``not_found`` (adidas has no product page for
        the style at all — see :meth:`_open_product`; ``missing_ok`` false raises
        there instead). Raises if a requested size is not offered at all.
        """

        prepared: list[dict] = []
        for style, lines in _group_by_style(request.lines).items():
            if not self._open_product(style, missing_ok=missing_ok):
                # adidas serves no listing for this style: record every one of
                # its lines as not_found and let add_lines apply the policy.
                for line in lines:
                    entry = self._note_missing_line(style, line.size, line.quantity)
                    prepared.append(
                        {
                            "style": style,
                            "line": line,
                            "code": None,
                            "product_name": None,
                            "indicator": None,
                            "available": None,
                            "status": "not_found",
                            "detail": entry["detail"],
                        }
                    )
                continue
            product_name = self._read_product_name(style)
            available_today, available_date = self._product_available_today()
            code_map = self._size_code_map()
            for line in lines:
                code = next(
                    (code_map[key] for key in _size_lookup_keys(line.size)
                     if key in code_map),
                    None,
                )
                if code is None:
                    raise AdidasAPIError(
                        f"Size {line.size!r} is not offered for {style}. "
                        f"Available sizes: {', '.join(sorted(code_map)) or '(none read)'}."
                    )
                if not available_today:
                    prepared.append(
                        {
                            "style": style,
                            "line": line,
                            "code": code,
                            "product_name": product_name,
                            "indicator": None,
                            "available": 0,
                            "status": "unavailable",
                            "available_date": available_date,
                        }
                    )
                    continue
                status, indicator, available, restock = self._classify_size(
                    style, code, line.quantity
                )
                prepared.append(
                    {
                        "style": style,
                        "line": line,
                        "code": code,
                        "product_name": product_name,
                        "indicator": indicator,
                        "available": available,
                        "status": status,
                        "restock_date": restock,
                    }
                )
        return prepared

    def _classify_size(
        self, style: str, code: str, requested: int
    ) -> tuple[str, str | None, int | None, str | None]:
        """Return (status, indicator, available, restock_date) for one size after
        scrolling it into view. status ∈ {"ok", "short", "unavailable"}.

        ``restock_date`` is read **only for a short line** — the case a caller
        has to explain to someone ("out of stock, back Nov 8") — because reading
        it costs a hover per size. A flatly *unavailable* size has no restock
        date by definition: it is never coming back.
        """

        if not self._ensure_size_in_view(style, code):
            return "unavailable", None, None, None
        not_available = self.page.locator(
            f"#CartModule-SizeTile-Status-NotAvailable-{style}-{code}"
        )
        if not_available.count() > 0:
            return "unavailable", None, None, None
        indicator = self._read_inventory(style, code)
        available = _parse_available(indicator)
        if available is not None and available < requested:
            return "short", indicator, available, self._read_restock_date(style, code)
        return "ok", indicator, available, None

    def _read_restock_date(self, style: str, code: str) -> str | None:
        """Return a size's re-stock date as the portal shows it ("Nov 8, 2026").

        The size tile's calendar icon says *that* a size is coming back; the
        date lives only in the tooltip that opens on hover. So: try the cheap
        attribute paths first, then hover the icon and match the portal's
        "Re-stock in …" wording in the text that appears. Returns None when the
        size has no restock icon at all (nothing scheduled) or the tooltip never
        rendered — a missing date is reported as unknown, never guessed.
        """

        icon = self.page.locator(
            "#" + _SIZE_TILE_RESTOCK_ID.format(style=style, code=code)
        ).first
        try:
            if icon.count() == 0:
                return None
        except Exception:  # noqa: BLE001
            return None

        for attr in _RESTOCK_ATTRS:
            for target in (icon, icon.locator("[%s]" % attr).first):
                try:
                    if target.count() == 0:
                        continue
                    match = _RESTOCK_TOOLTIP_RE.search(target.get_attribute(attr) or "")
                except Exception:  # noqa: BLE001
                    continue
                if match:
                    return _clean(match.group(1))

        try:
            icon.scroll_into_view_if_needed(timeout=2_000)
            icon.hover(timeout=5_000)
            self.page.wait_for_timeout(_RESTOCK_HOVER_SETTLE_MS)
            text = self.page.locator("body").inner_text()
        except Exception:  # noqa: BLE001 — a tooltip that won't open is not a failure
            return None
        finally:
            # Close the tooltip so the next size's hover reads its own date and
            # not this one still fading out.
            try:
                self.page.mouse.move(0, 0)
            except Exception:  # noqa: BLE001
                pass
        match = _RESTOCK_TOOLTIP_RE.search(text or "")
        return _clean(match.group(1)) if match else None

    def _ensure_size_in_view(self, style: str, code: str) -> bool:
        """Scroll the horizontal size row until this size's cell is loaded.

        Off-screen sizes lazy-load via the row's forward/back arrows. Resets to
        the leftmost, then scans forward. Returns True if the size's wrapper cell
        (``#CartModule-SizeRow-SizeTile-Wrapper-{style}-{code}``) is present.
        """

        wrapper = f"#CartModule-SizeRow-SizeTile-Wrapper-{style}-{code}"
        if self.page.locator(wrapper).count() > 0:
            return True

        back = self.page.locator(_SIZE_NAV_BACK).first
        forward = self.page.locator(_SIZE_NAV_FORWARD).first
        # Reset to the leftmost sizes.
        for _ in range(20):
            try:
                if back.count() == 0 or not back.is_enabled():
                    break
            except Exception:  # noqa: BLE001
                break
            back.click()
            self.page.wait_for_timeout(200)
            if self.page.locator(wrapper).count() > 0:
                return True
        # Scan forward through the size run.
        for _ in range(20):
            if self.page.locator(wrapper).count() > 0:
                return True
            try:
                if forward.count() == 0 or not forward.is_enabled():
                    break
            except Exception:  # noqa: BLE001
                break
            forward.click()
            self.page.wait_for_timeout(250)
        return self.page.locator(wrapper).count() > 0

    @staticmethod
    def _shortfall_dict(p: dict) -> dict:
        return {
            "style": p["style"],
            "size": p["line"].size,
            "requested": p["line"].quantity,
            "available": p["indicator"],
            "status": p["status"],  # "short" (backorderable) or "unavailable"
            # When adidas restocks the size, as shown and in ISO. None on an
            # "unavailable" size (never restocked) or when no date was posted.
            "restock_date": p.get("restock_date"),
            "restock_date_iso": _iso_date(p.get("restock_date")),
        }

    @staticmethod
    def _status_note(p: dict) -> str | None:
        if p["status"] == "not_found":
            return (
                f"not offered — adidas Click has no product listing for "
                f"{p['style']} ({p.get('detail') or 'no product page'})"
            )
        if p["status"] == "unavailable":
            if p.get("available_date"):
                return (
                    f"not available until {p['available_date']} — "
                    "no inventory available today"
                )
            return "not available — cannot be ordered"
        if p["status"] == "short":
            note = (
                f"out of stock — requested {p['line'].quantity}, "
                f"available {p['indicator'] or 0}"
            )
            return (
                f"{note}; restocks {p['restock_date']}"
                if p.get("restock_date")
                else f"{note}; no restock date posted"
            )
        return None

    @staticmethod
    def _prepared_result(
        p: dict, *, quantity: int | None = None, note: str | None = None
    ) -> "OrderLineResult":
        line = p["line"]
        return OrderLineResult(
            style=p["style"],
            color=line.color or (p["product_name"] or ""),
            size=line.size,
            quantity=quantity if quantity is not None else line.quantity,
            available=p["indicator"],
            restock_date=p.get("restock_date"),
            restock_date_iso=_iso_date(p.get("restock_date")),
            note=note,
        )

    # -- product page -----------------------------------------------------

    def _open_product(self, style: str, *, missing_ok: bool = False) -> bool:
        """Navigate straight to a style's product page and await the size table.

        The size grid sits below the fold and **lazy-renders its per-size tiles
        only when scrolled into view**, so after the table container appears we
        scroll it into view and wait for this style's tiles to attach.

        Returns True once the product is open. When adidas serves no listing for
        the style (a wrong article number, or one this account is not offered),
        ``missing_ok`` decides: True records the style in
        :attr:`missing_products` and returns False so the caller can escalate to
        the user, False raises :class:`AdidasAPIError` as before.
        """

        url = self.base_url + _PRODUCT_PATH.format(style=style)
        self.page.goto(url, wait_until="domcontentloaded")
        if self._wait_for_size_table():
            self._ensure_size_tiles_rendered(style)
            return True

        reason, detail = self._missing_product_reason(style)
        if not missing_ok:
            raise AdidasAPIError(
                f"Could not open the product page for {style!r} — {detail}. "
                "Check the article number (it must include the color, e.g. "
                "JW4306)."
            )
        logger.warning("adidas Click has no product page for %s (%s)", style, detail)
        self._missing_by_style.setdefault(
            style,
            {
                "style": style,
                "sizes": [],
                "requested": 0,
                "reason": reason,
                "detail": detail,
            },
        )
        return False

    def _note_missing_line(self, style: str, size: str, quantity: int | None) -> dict:
        """Attach one requested size to a missing style's summary entry.

        Creates the entry if it somehow isn't there yet, so recording a line can
        never be the thing that fails a run.
        """

        entry = self._missing_by_style.setdefault(
            style,
            {
                "style": style,
                "sizes": [],
                "requested": 0,
                "reason": "unresolved",
                "detail": "no product page could be opened",
            },
        )
        label = size or "*"
        if label not in entry["sizes"]:
            entry["sizes"].append(label)
            entry["requested"] += quantity or 0
        return entry

    def _wait_for_size_table(self) -> bool:
        """Poll for the product's size table, bailing early on a not-found tell.

        A blind ``wait_for_selector`` would spend the full timeout on every
        style adidas does not carry, which is exactly the case the caller most
        needs a fast answer for. So poll instead: return as soon as the table
        attaches, and stop early once the page positively says there is no such
        product.
        """

        deadline = time.monotonic() + _PRODUCT_WAIT_MS / 1000
        while True:
            if self.page.locator(_SIZE_TABLE).count() > 0:
                return True
            if self._missing_product_tell():
                # Confirm before giving up: a stray match (a toast, a background
                # widget, footer copy) must not beat a size table that is merely
                # slow, so give the table one last grace window.
                self.page.wait_for_timeout(_PRODUCT_TELL_GRACE_MS)
                return self.page.locator(_SIZE_TABLE).count() > 0
            if time.monotonic() >= deadline:
                return self.page.locator(_SIZE_TABLE).count() > 0
            self.page.wait_for_timeout(_PRODUCT_POLL_MS)

    def _missing_product_tell(self) -> str | None:
        """Return the page's "no such product" wording, if it is showing one.

        Only trusted once the authenticated shell has painted — before that an
        empty page means "still loading", not "no product". Returns None while
        the page is still coming up or when no tell is present.
        """

        try:
            if self.page.locator(_LOGGED_IN_MARKER).count() == 0:
                return None
            text = self.page.locator("body").first.inner_text()
        except Exception:  # noqa: BLE001 — mid-navigation DOM churn
            return None
        match = _PRODUCT_MISSING_TELL_RE.search(text or "")
        return _clean(match.group(0)) if match else None

    def _missing_product_reason(self, style: str) -> tuple[str, str]:
        """Classify why a product page never produced a size table.

        ``not_found`` — the portal said so, or bounced off the product URL
        entirely: the style is genuinely not offered on this account.
        ``unresolved`` — neither the product nor a not-found tell appeared, so
        the style is *unconfirmed*: it may be a slow page or a portal change,
        and the caller should say so rather than assert the style is missing.
        """

        tell = self._missing_product_tell()
        if tell:
            return "not_found", f"the portal reported {tell!r}"
        try:
            url = self.page.url or ""
        except Exception:  # noqa: BLE001
            url = ""
        if url and "/reorder/product/" not in url.lower():
            return "not_found", f"the portal redirected off the product page (to {url})"
        return (
            "unresolved",
            "the product page never rendered a size table (no confirmation "
            "either way that the style exists)",
        )

    def _ensure_size_tiles_rendered(self, style: str) -> None:
        """Scroll the size grid into view so its per-size tiles render, then wait.

        Tiles (``#CartModule-SizeTile-{style}-{code}``) mount lazily when the
        grid enters the viewport. Scroll it to center; if the tiles still are
        not attached, nudge-scroll down while polling; finally wait explicitly.
        """

        tile_selector = f'[id^="CartModule-SizeTile-{style}-"]'
        if self.page.locator(tile_selector).count() > 0:
            return

        self.page.evaluate(
            "(sel) => { const el = document.querySelector(sel);"
            " if (el) el.scrollIntoView({block: 'center'}); }",
            _SIZE_TABLE,
        )
        try:
            self.page.wait_for_selector(
                tile_selector, state="attached", timeout=8_000
            )
            return
        except Exception:  # noqa: BLE001 — fall back to nudge-scrolling
            pass

        for _ in range(12):
            self.page.mouse.wheel(0, 500)
            self.page.wait_for_timeout(250)
            if self.page.locator(tile_selector).count() > 0:
                return
        self.page.wait_for_selector(
            tile_selector, state="attached", timeout=_DEFAULT_TIMEOUT_MS
        )

    def _read_product_name(self, style: str) -> str | None:
        try:
            name = self.page.locator(
                f"#CartModule-TinyProduct-{style}-ProductName"
            ).first.inner_text()
            return _clean(name) or None
        except Exception:  # noqa: BLE001
            return None

    def _size_code_map(self) -> dict[str, str]:
        """Build a ``{size_label_lower: numeric_code}`` map from the size bar.

        Reads the header translation cells (``…-SizeTranslation-{group}-{code}``
        with the label in an ``<ins>``). Assumes one conversion group per
        product page (true for a single article).
        """

        cells = self.page.locator(f'[id^="{_SIZE_TRANSLATION_PREFIX}"]')
        out: dict[str, str] = {}
        for i in range(cells.count()):
            cell = cells.nth(i)
            cid = cell.get_attribute("id") or ""
            code = cid.rsplit("-", 1)[-1]
            label = _norm(cell.inner_text())
            if code and label:
                out[label] = code
        return out

    def _product_available_today(self) -> tuple[bool, str | None]:
        """Return ``(available_today, raw_date_text)`` from the availability tab.

        The product page shows an availability-date button
        (``#DateTabButton``) outside the size table — its text is the earliest
        date on which the product can ship (e.g. ``"Jul 31, 2026"``). If that
        isn't today, the size-tile inventory numbers refer to that future date
        and nothing is orderable now; the order flow and inventory read both
        gate on this before trusting the size tiles.

        Fail-open: a missing/unparseable date returns ``(True, raw_or_None)``
        with a warning log — a portal shape change should not silently block
        every order. The raw text is returned either way so callers can
        surface it.
        """

        from datetime import date, datetime

        try:
            raw = _clean(
                self.page.locator(_AVAILABLE_DATE_BUTTON).first.inner_text()
            ) or None
        except Exception:  # noqa: BLE001
            raw = None
        if not raw:
            logger.warning(
                "adidas product page: availability date button (%s) missing "
                "or empty — skipping the today check",
                _AVAILABLE_DATE_BUTTON,
            )
            return True, None
        try:
            parsed = datetime.strptime(raw, "%b %d, %Y").date()
        except ValueError:
            logger.warning(
                "adidas product page: could not parse availability date %r "
                "(expected e.g. 'Jul 31, 2026') — skipping the today check",
                raw,
            )
            return True, raw
        return parsed == date.today(), raw

    def _read_inventory(self, style: str, code: str) -> str | None:
        """Return the inventory-indicator text for a size (e.g. '300+', '160', '0')."""

        try:
            text = self.page.locator(
                f"#CartModule-SizeTile-InventoryIndicator-{style}-{code}"
            ).first.inner_text()
            return _clean(text) or None
        except Exception:  # noqa: BLE001
            return None

    def _set_size_quantity(
        self, style: str, code: str, quantity: int, spread_delivery: bool
    ) -> int | None:
        """Enter a quantity into one size tile and return the committed value.

        Clicking the tile opens a shared floating overlay (``#quantityInput``)
        that repositions over the active cell; its field is a react-numeric
        input with no id of its own (``#quantityInput input``). Typing a value
        and pressing Enter commits it — the overlay closes and the ordered
        quantity renders in ``#CartModule-SizeTile-OrderedInDate-{style}-{code}``.
        If the requested quantity exceeds availability, an "Insufficient
        availability" proposal offers to spread it over dates.
        """

        self._ensure_size_in_view(style, code)
        tile = self.page.locator(f"#CartModule-SizeTile-{style}-{code}")
        tile.scroll_into_view_if_needed()
        tile.click()

        overlay = self.page.locator("#quantityInput")
        overlay.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        field = overlay.locator("input")
        field.fill(str(quantity))
        field.press("Enter")

        self._handle_availability_proposal(spread_delivery)
        return self._read_ordered_quantity(style, code)

    def _handle_availability_proposal(self, spread_delivery: bool) -> None:
        """Resolve the "Insufficient availability" spread-delivery dialog if shown.

        Default (``spread_delivery`` false) declines → a single delivery. True
        accepts the spread across the proposed future dates.
        """

        proposal = self.page.locator("#CartModule-SizeItemProposals")
        try:
            proposal.wait_for(state="visible", timeout=2_000)
        except Exception:  # noqa: BLE001 — no proposal appeared; nothing to do
            return
        button = (
            "#CartModuleSpreadAcceptButton"
            if spread_delivery
            else "#CartModuleSpreadDeclineButton"
        )
        try:
            self.page.click(button)
            proposal.wait_for(state="hidden", timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(
                f"Could not resolve the insufficient-availability dialog: {exc}"
            ) from exc

    def _read_ordered_quantity(self, style: str, code: str) -> int | None:
        """Read the committed ordered quantity from a size cell (post-entry)."""

        ordered = self.page.locator(
            f"#CartModule-SizeTile-OrderedInDate-{style}-{code}"
        )
        try:
            ordered.wait_for(state="visible", timeout=5_000)
            return _to_int(ordered.first.inner_text())
        except Exception:  # noqa: BLE001 — cell may not show a total; don't hard-fail
            return None

    # -- Step 3: checkout details ----------------------------------------

    def fill_checkout(self, request: OrderRequest) -> None:
        """Open the active cart and set the Customer PO, delivery location, and
        shipping method in the cart header.

        Delivery location precedence: ``delivery_location_id`` (pick a saved
        location) > ``ship_to`` (add a one-time / dropship location) > default
        (leave the cart's preset). Shipping method is left at the cart default
        unless ``ship_method`` is given.
        """

        self.page.goto(self.base_url + _CART_PATH, wait_until="domcontentloaded")
        try:
            self.page.wait_for_selector(_CART_HEADER, timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(
                "Could not open the active cart at /adidas/reorder/cart — the "
                "cart header did not render."
            ) from exc

        self._set_customer_po(request.po_number)

        if request.delivery_location_id:
            self._select_saved_location(request.delivery_location_id)
        elif request.ship_to is not None:
            self._add_one_time_location(request.ship_to)
        # else: leave the cart's default delivery location.

        if request.ship_method:
            self._select_shipping_method(request.ship_method)

    def _set_customer_po(self, po_number: str) -> None:
        # Length + character validation happens up front in create_purchase_order
        # (po_number is already sanitized and length-checked here).
        field = self.page.locator(_PO_FIELD)
        try:
            field.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
            field.click()
            field.fill(po_number)  # replaces the default random reference
            field.press("Enter")
            field.blur()
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(f"Could not set the Customer PO #: {exc}") from exc
        # Verify the value stuck.
        actual = field.input_value()
        if _clean(actual) != _clean(po_number):
            raise AdidasAPIError(
                f"Customer PO # did not persist — expected {po_number!r}, "
                f"field shows {actual!r}."
            )

    def _select_saved_location(self, location_id: str) -> None:
        self.page.click(_DELIVERY_DROPDOWN_LABEL)
        self.page.wait_for_selector(_DELIVERY_DROPDOWN_CONTENT, timeout=_DEFAULT_TIMEOUT_MS)
        option = self.page.locator(f"#OptionButton{location_id}Button")
        if option.count() == 0:
            raise AdidasAPIError(
                f"Delivery location {location_id!r} was not found in the saved "
                "locations. Search/select it manually or pass a ship_to for a "
                "one-time location."
            )
        option.first.click()

    def _add_one_time_location(self, ship_to: "ShipTo") -> None:
        """Open the delivery dropdown and file a one-time (dropship) address.

        Field mapping: Attention 1 ← name, Attention 2 ← attention, Street ←
        address1 (+ address2), City ← city, State ← state (dropdown), ZIP ← zip.
        Country is fixed to United States by the form.
        """

        self.page.click(_DELIVERY_DROPDOWN_LABEL)
        self.page.wait_for_selector(_ADD_ONE_TIME_BUTTON, timeout=_DEFAULT_TIMEOUT_MS)
        self.page.click(_ADD_ONE_TIME_BUTTON)
        self.page.wait_for_selector(_ONE_TIME_FORM, timeout=_DEFAULT_TIMEOUT_MS)

        self.page.fill("#Attention1InputField", ship_to.name)
        if ship_to.attention:
            self.page.fill("#Attention2InputField", ship_to.attention)
        street = ", ".join(p for p in (ship_to.address1, ship_to.address2) if p)
        self.page.fill("#StreetInputField", street)
        self.page.fill("#CityTownInputField", ship_to.city)
        self._select_state(ship_to.state)
        self.page.fill("#ZipcodeInputField", ship_to.zip)
        self.page.click(_ONE_TIME_SUBMIT)
        try:
            self.page.wait_for_selector(
                _ONE_TIME_FORM, state="hidden", timeout=_DEFAULT_TIMEOUT_MS
            )
        except Exception:  # noqa: BLE001 — modal may stay if validation failed
            raise AdidasAPIError(
                "The one-time delivery address was not accepted — check the "
                "address fields (PO Boxes are rejected; Latin characters only)."
            )

    def _select_state(self, state: str) -> None:
        """Select a US state in the one-time-address State dropdown.

        Accepts a 2-letter abbreviation (mapped to the full name adidas shows) or
        the full state name; options are matched by exact text so "Virginia" is
        never confused with "West Virginia".
        """

        target = _resolve_state_name(state)
        self.page.click(_STATE_DROPDOWN_LABEL)
        self.page.wait_for_selector(_STATE_DROPDOWN_CONTENT, timeout=_DEFAULT_TIMEOUT_MS)
        if not self._click_option_by_exact_text(_STATE_DROPDOWN_CONTENT, target):
            raise AdidasConfigError(
                f"State {state!r} (resolved to {target!r}) is not in the adidas "
                "Click state list. Pass the full state name as adidas spells it."
            )

    def _select_shipping_method(self, method: str) -> None:
        """Select a shipping method by its 4-letter code (e.g. ``FDGP``) or its
        label (e.g. ``FedEx Ground``)."""

        self.page.click(_SHIPPING_DROPDOWN_LABEL)
        self.page.wait_for_selector(
            _SHIPPING_DROPDOWN_CONTENT, timeout=_DEFAULT_TIMEOUT_MS
        )
        code_button = self.page.locator(
            f"{_SHIPPING_DROPDOWN_CONTENT} #OptionButton{method.strip().upper()}Button"
        )
        if code_button.count() > 0:
            code_button.first.click()
            return
        if self._click_option_by_exact_text(_SHIPPING_DROPDOWN_CONTENT, method):
            return
        raise AdidasConfigError(
            f"Shipping method {method!r} not found. Pass a code "
            f"({', '.join(_SHIPPING_METHOD_CODES)}) or its exact label."
        )

    def _click_option_by_exact_text(self, content_selector: str, target: str) -> bool:
        """Click the option button under ``content_selector`` whose text exactly
        matches ``target`` (case-insensitive). Returns True on a match."""

        buttons = self.page.locator(f"{content_selector} button.m-button")
        target_norm = _norm(target)
        for i in range(buttons.count()):
            button = buttons.nth(i)
            if _norm(button.inner_text()) == target_norm:
                button.click()
                return True
        return False

    # -- Step 4: review + submit -----------------------------------------

    def price_cart(self) -> None:
        """Advance cart → checkout and run **Calc. Net Price**, reading the priced
        totals — but **without** placing the order.

        Shared by two callers: :meth:`complete_submission` (which then clicks
        Order Now) and the pricing check (which then deletes the cart). Sequence:
        click **Next** (cart → ``/adidas/reorder/checkout``) → click **Calc. Net
        Price** and wait for it to finish (it applies the wholesale discounts and
        is slow) → scrape the per-row net prices into ``line_net_prices`` /
        ``order_total``.
        """

        # 4a — advance from the cart to the checkout page. "Next" stays inactive
        # until the cart body is scrolled into view, so scroll it in + wait for
        # it to enable before clicking.
        self.page.wait_for_selector(
            _CHECKOUT_NEXT_BUTTON, state="visible", timeout=_DEFAULT_TIMEOUT_MS
        )
        self._activate_by_scroll(_CHECKOUT_NEXT_BUTTON)
        self.page.click(_CHECKOUT_NEXT_BUTTON)
        self.page.wait_for_url(f"**{_CHECKOUT_PATH}", timeout=_DEFAULT_TIMEOUT_MS)
        self.page.wait_for_load_state("networkidle")

        # 4b — apply wholesale pricing; MUST complete before ordering/reading.
        self.page.click(_CALC_NET_PRICE_BUTTON)
        self._await_net_price_calc()
        self._read_checkout_totals()  # net + retail totals, once priced

    def complete_submission(self) -> str | None:
        """Price the cart, then place the order and read the confirmation number.

        Runs :meth:`price_cart` (Next → Calc. Net Price → read totals) so the
        wholesale discount is applied before ordering, then clicks **Order Now**
        and parses the order number from the confirmation redirect.
        """

        self.price_cart()

        # 4c — place the order.
        submit = self.page.locator(_ORDER_NOW_BUTTON)
        submit.wait_for(state="visible", timeout=_DEFAULT_TIMEOUT_MS)
        submit.click()

        # 4d — Order Now auto-redirects to the confirmation page; the order
        # number is in that URL. (A Qualtrics feedback popup may open afterward;
        # it is ignored — reading the main page URL is unaffected.)
        try:
            self.page.wait_for_url(
                _CONFIRMATION_URL_GLOB, timeout=_DEFAULT_TIMEOUT_MS
            )
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(
                "Order Now was clicked but the confirmation page "
                "(/adidas/reorder/order/…/confirmation) did not load — the order "
                "status is uncertain; verify it in the portal before retrying."
            ) from exc
        return self._read_confirmation_number()

    def _await_net_price_calc(self) -> None:
        """Wait for "Calc. Net Price" to finish before "Order Now" is clicked.

        On completion the ``#NPCCartSimulation`` button is replaced by a "Done!"
        message in the summary-table header. We wait for that "Done!" text (its
        class is hashed, so we match the text) and **raise if it never appears**
        — clicking Order Now before the simulation completes would submit at
        list price instead of our wholesale net price.
        """

        # Best-effort: the button detaches when replaced. Primary gate is "Done!".
        try:
            self.page.wait_for_selector(
                _CALC_NET_PRICE_BUTTON, state="detached", timeout=_CALC_TIMEOUT_MS
            )
        except Exception:  # noqa: BLE001 — some builds hide rather than detach
            pass
        try:
            self.page.get_by_text(_CALC_DONE_TEXT, exact=False).first.wait_for(
                state="visible", timeout=_CALC_TIMEOUT_MS
            )
        except Exception as exc:  # noqa: BLE001
            raise AdidasAPIError(
                "Calc. Net Price did not report 'Done!' within the timeout — the "
                "wholesale pricing may not have applied, so the order was NOT "
                "placed. Retry, or check the cart in the portal."
            ) from exc

    def _read_checkout_totals(self) -> None:
        """Best-effort scrape of the priced per-row net prices on the review page.

        Each order row has a net-price cell ``#OrderReviewShardTotalsNetPrice{N}``
        (N = 1-based row index) whose **first** ``<span>`` is the net price and
        second is the retail comparison. Collects the per-row nets (exposed as
        ``line_net_prices`` for positional assignment to the result lines) and
        sums them into ``order_total``. Never raises — pricing display must not
        block placing the order.
        """

        nets: list[str | None] = []
        try:
            index = 1
            while index <= 500:  # safety cap
                cell = self.page.locator(f"#OrderReviewShardTotalsNetPrice{index}")
                if cell.count() == 0:
                    break
                spans = cell.locator("span")
                nets.append(_clean(spans.first.inner_text()) if spans.count() else None)
                index += 1
        except Exception as exc:  # noqa: BLE001 — informational only
            logger.warning("Could not read checkout net prices: %s", exc)
        self.line_net_prices = nets
        self.order_total = _sum_currency(nets)

    def _read_confirmation_number(self) -> str | None:
        """Extract the order number from the confirmation URL.

        The success page is ``/adidas/reorder/order/{number}/confirmation`` (e.g.
        order ``25709165``), so the number is parsed straight from the URL rather
        than scraped from the page body.
        """

        match = _CONFIRMATION_URL_RE.search(self.page.url)
        return match.group(1) if match else None

    # -- inventory / pricing checks --------------------------------------

    def read_inventory(self, request: OrderRequest) -> list["CheckLineResult"]:
        """Read live inventory for each requested line **without touching a cart**.

        Opens each style's product page once and reads the size-tile inventory
        indicator — the same read the order flow does before entering quantities,
        but here nothing is added to the cart. A line whose ``size`` is blank (or
        ``"*"`` / ``"all"``) expands to **every** size of that style, so a caller
        can ask "how much of JW4306 is in stock across sizes?" in one line.

        A size that isn't offered is reported with a note (not raised) so one bad
        size never aborts the whole check — and likewise a **style** adidas has
        no product page for is reported as ``not_found`` lines and recorded in
        :attr:`missing_products`, so the other styles in the same check still
        get read.
        """

        results: list[CheckLineResult] = []
        for style, lines in _group_by_style(request.lines).items():
            if not self._open_product(style, missing_ok=True):
                for line in lines:
                    entry = self._note_missing_line(style, line.size, line.quantity)
                    results.append(
                        CheckLineResult(
                            style=style,
                            size=line.size,
                            color=line.color,
                            requested_quantity=line.quantity,
                            status="not_found",
                            in_stock=False,
                            note=(
                                "not offered — adidas Click has no product "
                                f"listing for {style} ({entry['detail']})"
                            ),
                        )
                    )
                continue
            product_name = self._read_product_name(style)
            available_today, available_date = self._product_available_today()
            code_map = self._size_code_map()
            for line in lines:
                wants_all = _norm(line.size) in {"", "*", "all"}
                if wants_all:
                    for label, code in code_map.items():
                        results.append(
                            self._inventory_line(
                                style, label, code, product_name, line, None,
                                available_today=available_today,
                                available_date=available_date,
                            )
                        )
                    continue
                code = next(
                    (code_map[key] for key in _size_lookup_keys(line.size)
                     if key in code_map),
                    None,
                )
                if code is None:
                    results.append(
                        CheckLineResult(
                            style=style,
                            size=line.size,
                            color=line.color or (product_name or ""),
                            requested_quantity=line.quantity,
                            note=(
                                f"size {line.size!r} is not offered for {style} "
                                f"(sizes: {', '.join(sorted(code_map)) or '(none read)'})"
                            ),
                        )
                    )
                    continue
                results.append(
                    self._inventory_line(
                        style, line.size, code, product_name, line, line.quantity,
                        available_today=available_today,
                        available_date=available_date,
                    )
                )
        return results

    def _inventory_line(
        self,
        style: str,
        size_label: str,
        code: str,
        product_name: str | None,
        line: OrderLine,
        requested: int | None,
        *,
        available_today: bool = True,
        available_date: str | None = None,
    ) -> "CheckLineResult":
        """Classify one size's stock into a :class:`CheckLineResult` (no cart).

        Short-circuits to ``unavailable`` when the product page's availability
        date isn't today — the size-tile numbers refer to that future date, so
        reading them for a "today" answer would report ghost stock.
        """

        if not available_today:
            return CheckLineResult(
                style=style,
                size=size_label,
                color=line.color or (product_name or ""),
                requested_quantity=requested,
                available=None,
                available_count=0,
                status=_INVENTORY_STATUS["unavailable"],
                in_stock=False,
                note=(
                    f"not available until {available_date} — "
                    "no inventory available today"
                    if available_date
                    else "not available — no inventory available today"
                ),
            )

        # Classify against 1 unit so "short" means "cannot even ship one" (== 0
        # with a restock date); the raw indicator carries the actual level.
        status, indicator, available, restock = self._classify_size(style, code, 1)
        return CheckLineResult(
            style=style,
            size=size_label,
            color=line.color or (product_name or ""),
            requested_quantity=requested,
            available=indicator,
            available_count=available,
            status=_INVENTORY_STATUS.get(status, status),
            in_stock=status == "ok",
            restock_date=restock,
            restock_date_iso=_iso_date(restock),
            # An out-of-stock size is only actionable with its return date, so
            # say it on the line itself — including when adidas posted none.
            note=(
                f"out of stock — restocks {restock}"
                if restock
                else "out of stock — no restock date posted"
            )
            if status == "short"
            else None,
        )

    def delete_cart(self, name: str) -> int:
        """Delete the throwaway cart named ``name`` (cleanup after a pricing check).

        Reuses the same panel + delete path as ``create_new_cart``'s dedup, which
        first activates a different cart if ``name`` is the active one (the active
        cart can't be deleted). Returns the number of carts removed. Raises
        :class:`AdidasConfigError` if the check cart is the account's *only* cart
        (nothing to switch to) — the caller turns that into a warning.
        """

        self._ensure_carts_panel_open()
        return self._delete_carts_named(name)

    # -- delivery tracking (read-only) ------------------------------------

    def find_orders_for_po(self, po_number: str) -> list[dict]:
        """Search the order book for ``po_number`` and return its order rows.

        The search is driven purely through the URL
        (``?searchText=…&page=…&size=…``), so no search-form selectors are
        needed and paging is a URL bump. One PO commonly has **several** adidas
        orders, so every page is walked until a page adds nothing new.

        Returns ``[{order_number, po_number, order_type, exact}, ...]`` in the
        order the portal listed them. ``exact`` marks the rows whose PO cell
        matches the requested PO — adidas's search also matches PO *prefixes*
        (searching ``P1343`` surfaces ``P13433`` and ``P13434``), so the caller
        keeps the exact ones and reports the rest rather than tracking a PO the
        user did not ask about.
        """

        found: dict[str, dict] = {}
        for page_index in range(_ORDER_BOOK_MAX_PAGES):
            url = self.base_url + _ORDER_BOOK_SEARCH_PATH.format(
                po=quote(po_number, safe=""),
                page=page_index,
                size=_ORDER_BOOK_PAGE_SIZE,
            )
            self.page.goto(url, wait_until="domcontentloaded")
            rows = self._collect_order_rows()
            new = [row for row in rows if row["order_number"] not in found]
            for row in new:
                found[row["order_number"]] = row
            # Stop on a short page (last one), or when a page repeats what we
            # already have (the portal ignoring `page` must not loop forever).
            if len(rows) < _ORDER_BOOK_PAGE_SIZE or not new:
                break

        wanted = _norm(po_number)
        for row in found.values():
            row["exact"] = _norm(row["po_number"]) == wanted
        return list(found.values())

    def _collect_order_rows(self) -> list[dict]:
        """Read every order row on the current order-book page.

        The results grid virtualizes its rows, so this scrolls down and re-scans
        until two consecutive passes add nothing — otherwise the orders below
        the fold would silently go missing (and a PO's later orders are exactly
        the ones a tracking lookup must not drop).
        """

        self._wait_for_order_rows()
        seen: dict[str, dict] = {}
        idle_passes = 0
        for _ in range(_ORDER_BOOK_SCROLL_PASSES):
            before = len(seen)
            for row in self.page.locator(_ORDER_ROW).all():
                info = self._order_row_info(row)
                if info and info["order_number"] not in seen:
                    seen[info["order_number"]] = info
            if len(seen) == before:
                idle_passes += 1
                if idle_passes >= 2:
                    break
            else:
                idle_passes = 0
            self.page.mouse.wheel(0, 600)
            self.page.wait_for_timeout(250)
        return list(seen.values())

    def _wait_for_order_rows(self) -> bool:
        """Poll for order rows; return False when the search found nothing.

        A PO with no orders renders no rows at all, and that is a legitimate
        (reportable) outcome rather than an error — so this polls to a modest
        budget instead of blocking on one long ``wait_for_selector``.
        """

        deadline = time.monotonic() + _ORDER_BOOK_WAIT_MS / 1000
        while True:
            if self.page.locator(_ORDER_ROW).count() > 0:
                return True
            if time.monotonic() >= deadline:
                return False
            self.page.wait_for_timeout(_ORDER_BOOK_POLL_MS)

    def _order_row_info(self, row) -> dict | None:
        """Parse one order-book row into ``{order_number, po_number, order_type}``.

        A row that cannot be parsed (a header/placeholder row, or one recycled
        by the grid mid-scan) yields None rather than failing the lookup.
        """

        try:
            heading = row.locator(_ORDER_ROW_HEADING).first
            if heading.count() == 0:
                return None
            order_number = _clean(heading.inner_text())
            if not order_number:
                match = _ORDER_ROW_ID_RE.match(heading.get_attribute("id") or "")
                order_number = match.group(1) if match else ""
            if not order_number:
                return None
            po_locator = row.locator(_ORDER_ROW_PO).first
            po_number = _clean(po_locator.inner_text()) if po_locator.count() else ""
            type_locator = row.locator(_ORDER_ROW_TYPE).first
            order_type = (
                _clean(type_locator.inner_text()) if type_locator.count() else ""
            )
        except Exception:  # noqa: BLE001 — a recycled row is not a failure
            return None
        return {
            "order_number": order_number,
            "po_number": po_number,
            "order_type": order_type or None,
        }

    def open_order(self, order_number: str) -> bool:
        """Open an order's detail page; return True if it has shipment tracking.

        The Delivery Tracking link is rendered **only** for an order with
        shipments, so its absence is the portal's own "nothing has shipped yet"
        tell. To keep a slow render from being read as "unshipped", the page is
        polled for either the link or the article rows, and once the article
        rows are up the link still gets a short grace window.

        Raises :class:`AdidasAPIError` if neither ever appears (the page did not
        load) — the caller downgrades that to one unreadable order.
        """

        self.page.goto(
            self.base_url + _ORDER_DETAIL_PATH.format(order=order_number),
            wait_until="domcontentloaded",
        )
        deadline = time.monotonic() + _ORDER_DETAIL_WAIT_MS / 1000
        while True:
            if self.page.locator(_ORDER_TRACKING_LINK).count() > 0:
                return True
            if self.page.locator(_ARTICLE_WEEK_TOGGLE).count() > 0:
                self.page.wait_for_timeout(_TRACKING_LINK_GRACE_MS)
                return self.page.locator(_ORDER_TRACKING_LINK).count() > 0
            if time.monotonic() >= deadline:
                break
            self.page.wait_for_timeout(_ORDER_BOOK_POLL_MS)
        raise AdidasAPIError(
            f"The adidas order page for {order_number!r} did not render — "
            "neither the Delivery Tracking link nor the article rows appeared."
        )

    def read_delivery_tracking(self, order_number: str) -> list[dict]:
        """Click through to Delivery Tracking and read the carrier / tracking rows.

        Must be called on an order page where :meth:`open_order` returned True.
        One order can ship in several deliveries, and one delivery note can
        carry more than one parcel, so every row of the table is returned:
        ``[{delivery_note, ship_date, carrier, carrier_name, tracking_number,
        tracking_url}, ...]``.

        The row's delivery-note PDF link is **not** read: its href embeds a
        bearer access token, which must not leak into a tool result.
        """

        link = self.page.locator(_ORDER_TRACKING_LINK).first
        href = link.get_attribute("href") or ""
        target = href or _DELIVERIES_PATH.format(order=order_number)
        if target.startswith("/"):
            target = self.base_url + target

        try:
            link.click()
        except Exception:  # noqa: BLE001 — fall back to the link's own target
            self.page.goto(target, wait_until="domcontentloaded")
        if not self._await_delivery_rows() and "/deliveries" not in self.page.url:
            # The click never took (an SPA link that swallowed it): go to the
            # captured href directly rather than reporting an empty table.
            self.page.goto(target, wait_until="domcontentloaded")
            self._await_delivery_rows()

        shipments: list[dict] = []
        for item in self.page.locator(_DELIVERY_ITEM).all():
            shipment = self._delivery_row(item)
            if shipment:
                shipments.append(shipment)
        return shipments

    def _await_delivery_rows(self) -> bool:
        """Poll for the delivery table's rows; False if none showed up in time."""

        try:
            self.page.wait_for_load_state("networkidle")
        except Exception:  # noqa: BLE001 — an idle network is a nicety, not a gate
            pass
        deadline = time.monotonic() + _DELIVERY_WAIT_MS / 1000
        while True:
            if self.page.locator(_DELIVERY_ITEM).count() > 0:
                return True
            if time.monotonic() >= deadline:
                return False
            self.page.wait_for_timeout(_ORDER_BOOK_POLL_MS)

    def _delivery_row(self, item) -> dict | None:
        """Parse one Delivery Tracking row; None if it holds nothing readable."""

        def text(selector: str) -> str:
            locator = item.locator(selector).first
            try:
                return _clean(locator.inner_text()) if locator.count() else ""
            except Exception:  # noqa: BLE001
                return ""

        try:
            tracking = item.locator(_DELIVERY_TRACKING_LINK).first
            tracking_number = _clean(tracking.inner_text()) if tracking.count() else ""
            tracking_url = (
                tracking.get_attribute("href") if tracking.count() else None
            ) or None
            row = {
                "delivery_note": text(_DELIVERY_NOTE_LINK) or None,
                "ship_date": text(_DELIVERY_SHIP_DATE) or None,
                "carrier": text(_DELIVERY_CARRIER) or None,
                "carrier_name": _carrier_from_url(tracking_url),
                "tracking_number": tracking_number or None,
                "tracking_url": tracking_url,
            }
        except Exception:  # noqa: BLE001
            return None
        return row if any(row.values()) else None

    def read_expected_ship_dates(self) -> list[dict]:
        """Expand each article row on an unshipped order and read its ship dates.

        Must be called on an order page where :meth:`open_order` returned False
        (no shipments). Each article carries a chevron toggle that reveals a week
        list whose header is the expected ship date. Returns
        ``[{article, dates: [...]}, ...]``; when the article container class does
        not match, every date found is returned as one order-level entry rather
        than dropping the dates.
        """

        toggles = self.page.locator(_ARTICLE_WEEK_TOGGLE)
        for index in range(min(toggles.count(), 50)):
            toggle = toggles.nth(index)
            try:
                if self._article_dates_shown(toggle):
                    continue  # already expanded — clicking would collapse it
                toggle.scroll_into_view_if_needed(timeout=2_000)
                toggle.click(timeout=5_000)
                self.page.wait_for_timeout(300)
            except Exception:  # noqa: BLE001 — one stubborn row must not stop the rest
                continue

        try:
            articles = self.page.evaluate(
                """
                ([blockSel, nameSel]) => {
                  const dates = (root) => Array.from(
                    root.querySelectorAll(nameSel)
                  ).map(el => (el.textContent || '').trim()).filter(Boolean);
                  const uniq = (xs) => Array.from(new Set(xs));
                  const blocks = Array.from(document.querySelectorAll(blockSel));
                  if (blocks.length) {
                    return blocks.map(b => {
                      const head = b.querySelector('h2, h3, .a-heading');
                      return {
                        article: head ? (head.textContent || '').trim() : null,
                        dates: uniq(dates(b)),
                      };
                    }).filter(a => a.dates.length);
                  }
                  const all = uniq(dates(document));
                  return all.length ? [{article: null, dates: all}] : [];
                }
                """,
                [_ARTICLE_BLOCK, _ARTICLE_WEEK_NAME],
            )
        except Exception:  # noqa: BLE001
            return []
        return articles or []

    def _article_dates_shown(self, toggle) -> bool:
        """True when this article's week list is already expanded."""

        try:
            return bool(
                toggle.evaluate(
                    """
                    (el, [blockSel, nameSel]) => {
                      const root = el.closest(blockSel) || el.closest('li') ||
                        el.parentElement?.parentElement;
                      if (!root) return false;
                      return root.querySelectorAll(nameSel).length > 0;
                    }
                    """,
                    [_ARTICLE_BLOCK, _ARTICLE_WEEK_NAME],
                )
            )
        except Exception:  # noqa: BLE001
            return False

    # -- helpers ----------------------------------------------------------

    def _activate_by_scroll(self, selector: str) -> None:
        """Scroll ``selector`` into view (and nudge-scroll) until it is enabled.

        Some controls (e.g. the cart "Next" button) stay inactive until the
        surrounding content is scrolled into the viewport. Best-effort: returns
        once the element reports enabled, or after the scroll budget — the
        subsequent ``click`` still enforces actionability.
        """

        element = self.page.locator(selector).first
        for _ in range(12):
            try:
                element.scroll_into_view_if_needed(timeout=2_000)
            except Exception:  # noqa: BLE001
                pass
            try:
                if element.is_enabled():
                    return
            except Exception:  # noqa: BLE001
                pass
            self.page.mouse.wheel(0, 500)
            self.page.wait_for_timeout(250)

    def screenshot(self, path: str) -> None:
        try:
            self.page.screenshot(path=path, full_page=True)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not capture screenshot at %s: %s", path, exc)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


@contextmanager
def _browser_page(headless: bool):
    """Launch a stealth Chromium and yield a ready page, tearing it down on exit.

    Centralizes the anti-bot browser setup shared by the order and check flows:
    the ``ADIDAS_CLICK_HEADLESS`` override, a desktop-Chrome User-Agent, the
    auto-started Xvfb virtual display, the ``navigator.webdriver`` mask, and
    teardown. adidas Click's Akamai edge stalls headless Chromium, so this runs
    **headed by default** (``ADIDAS_CLICK_HEADLESS=true`` forces headless).
    """

    # adidas Click is fronted by Akamai Bot Manager, which stalls the response
    # for automated-looking clients. A headless Chromium (UA "HeadlessChrome",
    # navigator.webdriver=true) is fingerprinted and tarpitted even with a
    # spoofed UA, so this skill runs HEADED by default (on a virtual display —
    # started below) and also presents an ordinary desktop-Chrome UA. Set
    # ADIDAS_CLICK_HEADLESS=true to force headless (expect WAF stalls); override
    # the UA via ADIDAS_CLICK_USER_AGENT.
    _headless_env = os.environ.get("ADIDAS_CLICK_HEADLESS")
    if _headless_env is not None:
        headless = _headless_env.strip().lower() not in ("0", "false", "no", "off")
    user_agent = os.environ.get("ADIDAS_CLICK_USER_AGENT") or _DEFAULT_USER_AGENT

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise AdidasConfigError(
            "playwright is required for the adidas Click flows. Install it with "
            "`pip install playwright` and then "
            "`python -m playwright install chromium`."
        ) from exc

    # A headed browser needs a display. adidas's WAF forces headed, so on a
    # *Linux* host with no X server we start a virtual display (Xvfb) and point
    # $DISPLAY at it; tear it down when the process exits. Windows/macOS render on
    # the native GUI and never need Xvfb (_headed_needs_virtual_display gates it).
    if not headless and _headed_needs_virtual_display():
        atexit.register(_stop_process, _start_virtual_display())

    with sync_playwright() as p:
        browser = _launch_chromium(p, headless)
        context = browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1440, "height": 900},
            locale="en-US",
        )
        context.set_default_timeout(_DEFAULT_TIMEOUT_MS)
        context.set_default_navigation_timeout(_NAV_TIMEOUT_MS)
        # Belt-and-suspenders: also mask navigator.webdriver at the JS layer for
        # builds where the launch flag alone doesn't hide it.
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def create_purchase_order(
    *,
    request: OrderRequest,
    credentials: AdidasClickCredentials | None = None,
    confirm: bool = False,
    screenshot_path: str | None = None,
    headless: bool = False,
) -> OrderResult:
    """Fill (and optionally place) an adidas Click purchase order for one order.

    Logs in, adds each product line, fills the PO number + ship-to at checkout,
    then — with ``confirm`` true — places the order.

    With ``confirm`` false (default) it stops before submitting and returns a
    ``dry_run`` preview. Until the flow is fully reverse-engineered, it returns
    a ``not_implemented`` result at the first un-captured step (see the
    ``*_IMPLEMENTED`` gates and references/order_flow_notes.md).
    """

    if not request.po_number:
        raise AdidasConfigError("po_number is required to place an order.")
    if not request.lines:
        raise AdidasConfigError("at least one order line is required.")

    # Validate the out-of-stock / missing-product policies and sanitize the
    # Customer PO up front (fail fast, before launching a browser).
    _validate_policies(request)
    original_po = request.po_number
    clean_po, po_changed = _sanitize_po_number(original_po)
    if not clean_po:
        raise AdidasConfigError(
            f"Customer PO {original_po!r} has no valid characters — adidas Click "
            "allows only letters, numbers, space, and / _ . ? &."
        )
    if len(clean_po) > _PO_MAX_LEN:
        raise AdidasConfigError(
            f"adidas Click Customer PO # is limited to {_PO_MAX_LEN} characters; "
            f"{clean_po!r} is {len(clean_po)}."
        )
    request.po_number = clean_po
    po_warning = (
        f"Customer PO sanitized from {original_po!r} to {clean_po!r} — adidas "
        "Click allows only letters, numbers, space, and / _ . ? &."
        if po_changed
        else None
    )

    if credentials is None:
        credentials = credentials_from_env()

    # Nothing is captured yet — short-circuit with a clear status so the tool
    # is runnable end-to-end while the flow is still being built.
    if not LOGIN_IMPLEMENTED:
        return OrderResult(
            status="not_implemented",
            po_number=request.po_number,
            message=(
                "The adidas Click ordering flow is still being reverse-"
                "engineered. Step 1 (login) has not been captured yet — see "
                "references/order_flow_notes.md."
            ),
        )

    with _browser_page(headless) as page:
        driver = AdidasClickDriver(page, credentials.base_url)
        try:
            driver.login(credentials)

            result = OrderResult(status="dry_run", po_number=request.po_number)
            if po_warning:
                result.warnings.append(po_warning)

            # Isolate this run in its own cart (named with the PO) so a shared
            # account's existing carts are never touched. Any leftover cart with
            # the same PO name (e.g. from an errored prior run) is deleted first.
            if request.new_cart:
                deleted = driver.create_new_cart(request.po_number)
                if deleted:
                    result.warnings.append(
                        f"Deleted {deleted} existing cart(s) named "
                        f"{request.po_number!r} before starting fresh."
                    )

            if not ADD_LINES_IMPLEMENTED:
                result.status = "not_implemented"
                result.message = "Logged in, but Step 2 (line entry) is not captured yet."
                if screenshot_path:
                    driver.screenshot(screenshot_path)
                    result.screenshot_path = screenshot_path
                return result

            try:
                result.lines = driver.add_lines(request)
            except _OrderPause as pause:
                # Something needs a human decision — a short line under
                # on_insufficient_stock="pause", and/or a style adidas does not
                # carry under on_missing_product="pause". Place nothing and hand
                # the decision back to the agent/user.
                result.status = "needs_confirmation"
                result.lines = pause.lines
                result.out_of_stock = pause.out_of_stock
                result.missing_products = pause.missing_products
                result.total_quantity = sum(
                    ln.quantity for ln in pause.lines if ln.quantity
                ) or None
                result.message = " ".join(
                    part
                    for part in (
                        _missing_product_message(pause.missing_products)
                        if pause.missing_products
                        else "",
                        _insufficient_stock_message(pause.out_of_stock)
                        if pause.out_of_stock
                        else "",
                    )
                    if part
                )
                if screenshot_path:
                    driver.screenshot(screenshot_path)
                    result.screenshot_path = screenshot_path
                return result
            result.total_quantity = sum(
                ln.quantity for ln in result.lines if ln.quantity
            ) or None
            # Reached here with missing styles means on_missing_product="skip":
            # the order goes ahead without them, so say plainly what was dropped
            # rather than leaving it to a per-line note.
            result.missing_products = driver.missing_products
            if result.missing_products:
                result.warnings.append(
                    "Skipped "
                    + ", ".join(m["style"] for m in result.missing_products)
                    + " — adidas Click has no product listing for "
                    + ("them" if len(result.missing_products) > 1 else "it")
                    + " (on_missing_product='skip')."
                )

            if not CHECKOUT_IMPLEMENTED:
                result.status = "not_implemented"
                result.message = "Lines added, but Step 3 (checkout) is not captured yet."
                if screenshot_path:
                    driver.screenshot(screenshot_path)
                    result.screenshot_path = screenshot_path
                return result

            driver.fill_checkout(request)

            if screenshot_path:
                driver.screenshot(screenshot_path)
                result.screenshot_path = screenshot_path

            if not confirm:
                result.message = (
                    "Dry run — the order was filled and validated but NOT "
                    "placed. Re-run with confirm=true to submit it."
                )
                return result

            if not FINAL_SUBMIT_IMPLEMENTED:
                result.status = "not_implemented"
                result.message = (
                    "confirm=true was requested, but Step 4 (review → place "
                    "order) is not captured yet. Nothing was submitted."
                )
                return result

            result.confirmation_number = driver.complete_submission()
            result.order_total = driver.order_total
            # Assign each review-page net price to its line (positional; the
            # review rows follow the order the lines were entered).
            nets = driver.line_net_prices
            if nets and len(nets) == len(result.lines):
                for line, net in zip(result.lines, nets):
                    line.line_total = net
                    line.unit_price = _unit_price(net, line.quantity)
            result.status = "submitted"
            result.message = (
                f"Order placed — confirmation #{result.confirmation_number}."
                if result.confirmation_number
                else "Order placed (confirmation number could not be read from "
                "the URL; verify in the portal)."
            )
            return result
        except (AdidasConfigError, AdidasAPIError, AdidasTransportError):
            raise
        except Exception as exc:  # noqa: BLE001 — normalize unexpected failures
            raise AdidasTransportError(
                f"Unexpected failure during the adidas Click order flow: {exc}"
            ) from exc


# ---------------------------------------------------------------------------
# Inventory / pricing check
# ---------------------------------------------------------------------------


def _line_stock(line: OrderLineResult) -> tuple[str | None, bool | None]:
    """Best-effort (status, in_stock) for a priced check line from its indicator.

    The order-flow line result carries the raw inventory indicator (``available``)
    and a note; re-derive the check's stock vocabulary from those.
    """

    note = (line.note or "").lower()
    if "not offered" in note:
        return "not_found", False
    if "not available" in note:
        return "unavailable", False
    count = _parse_available(line.available)
    if count is not None and count == 0:
        return "backorder", False
    if line.available or count is not None:
        return "in_stock", True
    return None, None


def _checkline_results(
    order_lines: list[OrderLineResult], nets: list[str | None]
) -> list[CheckLineResult]:
    """Turn add_lines' order-line results into check lines, attaching net prices.

    Review-page net prices exist only for lines actually entered into the cart
    (committed quantity > 0), in entry order — so map them positionally onto
    those lines and leave dropped/unavailable lines price-less.
    """

    entered = [ln for ln in order_lines if ln.quantity]
    net_by_line = (
        {id(ln): net for ln, net in zip(entered, nets)}
        if nets and len(nets) == len(entered)
        else {}
    )
    out: list[CheckLineResult] = []
    for ln in order_lines:
        net = net_by_line.get(id(ln))
        status, in_stock = _line_stock(ln)
        out.append(
            CheckLineResult(
                style=ln.style,
                size=ln.size,
                color=ln.color,
                requested_quantity=ln.quantity or None,
                available=ln.available,
                available_count=_parse_available(ln.available),
                status=status,
                in_stock=in_stock,
                unit_price=_unit_price(net, ln.quantity) if net else None,
                line_total=net,
                restock_date=ln.restock_date,
                restock_date_iso=ln.restock_date_iso,
                note=ln.note,
            )
        )
    return out


def _safe_delete_cart(
    driver: "AdidasClickDriver", name: str, result: CheckResult
) -> bool:
    """Delete the throwaway check cart, downgrading any failure to a warning.

    Cleanup must never mask the pricing the check already obtained, so a failed
    delete (e.g. the check cart was the account's only cart) is reported as a
    warning and the caller tells the user to remove it manually.
    """

    try:
        driver.delete_cart(name)
        return True
    except Exception as exc:  # noqa: BLE001 — cleanup is best-effort
        result.warnings.append(
            f"Could not delete the throwaway check cart {name!r}: {exc} "
            "Remove it in the portal — it is named to signal DO NOT BUY."
        )
        return False


def _apply_missing_products(
    driver: "AdidasClickDriver",
    result: CheckResult,
    *,
    escalate: bool,
) -> str:
    """Attach any missing styles to a check result; return the message prefix.

    ``escalate`` (``on_missing_product`` left at ``pause``) flips the result to
    ``needs_confirmation`` so the caller takes the missing styles to the user
    instead of quietly reporting a short list of lines. Everything the check
    *did* read is kept either way.
    """

    result.missing_products = driver.missing_products
    if not result.missing_products:
        return ""
    message = _missing_product_message(result.missing_products, ordering=False)
    if escalate:
        result.status = "needs_confirmation"
    else:
        result.warnings.append(message)
        return ""
    return message + " "


def check_inventory_pricing(
    *,
    request: OrderRequest,
    credentials: AdidasClickCredentials | None = None,
    check: str = "both",
    screenshot_path: str | None = None,
    headless: bool = False,
) -> CheckResult:
    """Retrieve live inventory and/or wholesale pricing **without placing an order**.

    Reuses the ordering flow's login + product navigation. ``check`` selects the
    mode:

    - ``inventory`` — read each line's size-tile stock level. **No cart is
      created** (a line with a blank ``size`` expands to every size of the style).
    - ``pricing`` — fill a **throwaway cart**, advance to the priced checkout
      page, run **Calc. Net Price** to apply the wholesale discount, read the net
      unit/line prices and order total, then **delete the cart**.
    - ``both`` — pricing plus the inventory levels read while filling the cart.

    The throwaway cart / Customer PO is named with a loud "DO NOT BUY {rand}"
    marker (override via ``request.po_number``), and the cart is deleted once the
    prices are read, so nothing is ever purchased and no stray cart is left to
    buy. Since the order is never placed, the check never pauses on short stock —
    a ``pause`` policy is upgraded to ``order`` so every orderable line gets a
    price.

    A style adidas serves **no product page** for never aborts the check: those
    lines come back with ``status="not_found"``, the rest are read as usual, and
    the styles are summarised in ``missing_products``. With
    ``on_missing_product`` left at ``pause`` (default) the result's status
    becomes ``needs_confirmation`` so the caller escalates the missing styles to
    the user; ``skip`` reports them as a warning instead, and ``error`` fails the
    check outright.
    """

    check = (check or "both").strip().lower()
    if check not in {"inventory", "pricing", "both"}:
        raise AdidasConfigError(
            f"check must be 'inventory', 'pricing', or 'both'; got {check!r}."
        )
    if not request.lines:
        raise AdidasConfigError(
            "at least one line ({style, size?[, quantity]}) is required for a check."
        )

    needs_cart = check in {"pricing", "both"}

    # A check reports on every style it *can* read and hands the ones adidas has
    # no listing for back to the caller, so the driver never pauses or raises
    # mid-run on a missing style: it drops those lines and the caller escalates
    # from ``missing_products`` below. ``error`` is still honoured for a caller
    # that wants a missing style to fail the check outright.
    _, missing_policy = _validate_policies(request)
    if missing_policy != "error":
        request.on_missing_product = "skip"

    pre_warnings: list[str] = []
    po_number: str | None = None
    if needs_cart:
        # A pricing check fills a throwaway cart just to reach the priced
        # checkout page. Name it (and the Customer PO) with a DO-NOT-BUY marker
        # so a leftover from a crashed run is obviously safe; the caller may
        # override the marker via request.po_number.
        raw_po = request.po_number or _generate_check_po()
        clean_po, po_changed = _sanitize_po_number(raw_po)
        if not clean_po:
            raise AdidasConfigError(
                f"Check PO {raw_po!r} has no valid characters — adidas Click "
                "allows only letters, numbers, space, and / _ . ? &."
            )
        if len(clean_po) > _PO_MAX_LEN:
            raise AdidasConfigError(
                f"Check PO # is limited to {_PO_MAX_LEN} characters; "
                f"{clean_po!r} is {len(clean_po)}. Pass a shorter po_number."
            )
        po_number = clean_po
        request.po_number = clean_po
        request.new_cart = True  # a check always isolates its own throwaway cart
        if po_changed:
            pre_warnings.append(
                f"Check PO sanitized from {raw_po!r} to {clean_po!r}."
            )
        # A check never orders and deletes its cart, so it must never pause on
        # short stock: fill everything orderable to get its price.
        if (request.on_insufficient_stock or "pause").strip().lower() == "pause":
            request.on_insufficient_stock = "order"

    if credentials is None:
        credentials = credentials_from_env()

    with _browser_page(headless) as page:
        driver = AdidasClickDriver(page, credentials.base_url)
        try:
            driver.login(credentials)

            result = CheckResult(status="checked", check=check, po_number=po_number)
            result.warnings.extend(pre_warnings)

            # ---- inventory-only: read product pages, never touch a cart -------
            if not needs_cart:
                result.lines = driver.read_inventory(request)
                result.total_quantity = (
                    sum((ln.requested_quantity or 0) for ln in result.lines) or None
                )
                if screenshot_path:
                    driver.screenshot(screenshot_path)
                    result.screenshot_path = screenshot_path
                prefix = _apply_missing_products(
                    driver, result, escalate=missing_policy == "pause"
                )
                readable = sum(1 for ln in result.lines if ln.status != "not_found")
                result.message = prefix + (
                    f"Inventory check complete for {readable} line(s) — "
                    "no cart was created."
                )
                return result

            # ---- pricing / both: fill a throwaway cart, price it, delete it ---
            deleted_pre = driver.create_new_cart(po_number)
            if deleted_pre:
                result.warnings.append(
                    f"Deleted {deleted_pre} pre-existing cart(s) named "
                    f"{po_number!r} before starting the check."
                )

            try:
                order_lines = driver.add_lines(request)
            except (AdidasConfigError, AdidasAPIError) as exc:
                # e.g. every requested size is unavailable, or a requested size
                # is not offered — nothing to price. Report inventory instead,
                # then clean up the (empty) cart: a throwaway DO-NOT-BUY cart
                # must never be left behind because a line failed to resolve.
                # Delete first, so a failing inventory read cannot strand it.
                result.cart_deleted = _safe_delete_cart(driver, po_number, result)
                result.lines = driver.read_inventory(request)
                result.total_quantity = (
                    sum((ln.requested_quantity or 0) for ln in result.lines) or None
                )
                if screenshot_path:
                    driver.screenshot(screenshot_path)
                    result.screenshot_path = screenshot_path
                prefix = _apply_missing_products(
                    driver, result, escalate=missing_policy == "pause"
                )
                result.message = prefix + (
                    "Pricing check could not add any line to the cart "
                    f"({exc}); inventory levels are reported instead."
                )
                return result

            driver.fill_checkout(request)  # sets the DO-NOT-BUY Customer PO
            driver.price_cart()            # Next → Calc. Net Price → read totals

            result.order_total = driver.order_total
            result.lines = _checkline_results(order_lines, driver.line_net_prices)
            result.total_quantity = (
                sum((ln.requested_quantity or 0) for ln in result.lines) or None
            )

            if screenshot_path:
                driver.screenshot(screenshot_path)
                result.screenshot_path = screenshot_path

            # Cleanup: delete the throwaway cart so nothing is left to purchase.
            result.cart_deleted = _safe_delete_cart(driver, po_number, result)

            priced = sum(1 for ln in result.lines if ln.line_total)
            tail = (
                " Throwaway cart deleted."
                if result.cart_deleted
                else f" NOTE: the throwaway cart {po_number!r} could NOT be "
                "auto-deleted — remove it in the portal."
            )
            prefix = _apply_missing_products(
                driver, result, escalate=missing_policy == "pause"
            )
            result.message = prefix + (
                f"Pricing check complete — {priced} line(s) priced"
                + (f", order total {result.order_total}." if result.order_total else ".")
                + tail
            )
            return result
        except (AdidasConfigError, AdidasAPIError, AdidasTransportError):
            raise
        except Exception as exc:  # noqa: BLE001 — normalize unexpected failures
            raise AdidasTransportError(
                f"Unexpected failure during the adidas Click check flow: {exc}"
            ) from exc


# ---------------------------------------------------------------------------
# Delivery tracking (read-only)
# ---------------------------------------------------------------------------


def _carrier_from_url(url: str | None) -> str | None:
    """Name the carrier from a tracking URL's host, or None if unrecognized.

    adidas shows only its own carrier code ("UPSN"), so the human carrier is
    read off the link the code wraps (``ups.com/track?...`` -> UPS).
    """

    if not url:
        return None
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:  # noqa: BLE001
        return None
    for domain, name in _CARRIER_HOSTS:
        if host == domain or host.endswith("." + domain):
            return name
    return None


def _parse_ship_date(value: str | None):
    """Parse a portal date ("Feb 4, 2027") to a date, or None if unparseable."""

    text = _clean(value)
    if not text:
        return None
    for fmt in _SHIP_DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _earliest_expected(expected: list[dict]) -> str | None:
    """The earliest expected ship date across an order's articles, as displayed.

    Falls back to the first date seen when none of them parse, so a portal date
    format change degrades to "some date" rather than to nothing.
    """

    dates = [date for entry in expected for date in entry.get("dates", []) if date]
    if not dates:
        return None
    parsed = [(_parse_ship_date(date), date) for date in dates]
    dated = [pair for pair in parsed if pair[0] is not None]
    if not dated:
        return dates[0]
    return min(dated, key=lambda pair: pair[0])[1]


def _cell(value: str | None) -> str:
    """One Markdown table cell — em-dash for empty, pipes escaped."""

    text = _clean(value)
    return text.replace("|", "\\|") if text else "—"


def _tracking_table(pos: list[TrackingPO]) -> str:
    """Render the whole lookup as one Markdown table, PO by PO.

    Shipped rows carry the real delivery note / carrier / tracking number.
    Rows for an order that has **not** shipped are annotated: the ship date is
    marked *(expected)* and the note says so, so an expected date can never be
    mistaken for an actual shipment.
    """

    header = (
        "| PO | Order # | Delivery Note | Ship Date | Carrier | Tracking # | Note |\n"
        "| --- | --- | --- | --- | --- | --- | --- |"
    )
    rows: list[str] = []
    for po in pos:
        if not po.orders:
            rows.append(
                f"| {_cell(po.po_number)} | — | — | — | — | — | "
                f"{_cell(po.note or 'no orders found')} |"
            )
            continue
        for order in po.orders:
            if order.status == "shipped" and order.shipments:
                for shipment in order.shipments:
                    carrier = shipment.carrier_name or shipment.carrier
                    rows.append(
                        f"| {_cell(po.po_number)} | {_cell(order.order_number)} | "
                        f"{_cell(shipment.delivery_note)} | "
                        f"{_cell(shipment.ship_date)} | {_cell(carrier)} | "
                        f"{_cell(shipment.tracking_number)} | shipped |"
                    )
            elif order.status == "not_shipped":
                entries = order.expected_ship_dates or [{"article": None, "dates": []}]
                for entry in entries:
                    article = entry.get("article")
                    dates = entry.get("dates") or [None]
                    for date in dates:
                        note = "not shipped — expected ship date"
                        if article:
                            note += f" ({article})"
                        rows.append(
                            f"| {_cell(po.po_number)} | {_cell(order.order_number)} | "
                            f"— | "
                            + (f"{_cell(date)} *(expected)*" if date else "—")
                            + f" | — | not shipped yet | {_cell(note)} |"
                        )
            else:
                rows.append(
                    f"| {_cell(po.po_number)} | {_cell(order.order_number)} | — | — | "
                    f"— | — | {_cell(order.note or 'could not be read')} |"
                )
    return "\n".join([header, *rows])


def _po_status(orders: list[TrackingOrder]) -> str:
    """Roll an order list up to the PO's status (see :class:`TrackingPO`).

    An order that could not be read is never folded into "not shipped" — we do
    not know whether it shipped, and reporting a guess as a fact is worse than
    saying the PO is only partly known.
    """

    if not orders:
        return "not_found"
    statuses = [o.status for o in orders]
    if all(status == "unreadable" for status in statuses):
        return "unreadable"
    if all(status == "shipped" for status in statuses):
        return "shipped"
    if all(status == "not_shipped" for status in statuses):
        return "not_shipped"
    return "partial"


def get_order_tracking(
    *,
    po_numbers: list[str],
    credentials: AdidasClickCredentials | None = None,
    screenshot_path: str | None = None,
    headless: bool = False,
) -> TrackingResult:
    """Look up carrier tracking numbers for one or more PO numbers. **READ-ONLY.**

    Logs in once (same headed/anti-bot browser as the ordering flow) and then,
    **one PO at a time**: searches the order book for the PO, opens every order
    it returned (a PO commonly has several), and either reads that order's
    Delivery Tracking table (carrier + tracking number per delivery) or — when
    the order has no Delivery Tracking link, i.e. nothing has shipped — expands
    its article rows and reads the **expected** ship dates instead.

    Nothing is written: no cart is created, no order is touched. The result
    carries per-PO/per-order detail plus a ready-to-render Markdown ``table``
    where expected ship dates are annotated as such.

    A PO the order book returns no orders for is reported with
    ``status="not_found"`` and flips the overall status to
    ``needs_confirmation`` so the caller can check the PO number with the user;
    every other PO is still looked up.
    """

    wanted = [_clean(po) for po in (po_numbers or []) if _clean(po)]
    if not wanted:
        raise AdidasConfigError(
            "at least one PO number is required (po_numbers: [\"P13434\", ...])."
        )
    # De-duplicate while keeping the caller's order — searching the same PO
    # twice would just repeat the same browser work.
    seen: set[str] = set()
    po_list = [po for po in wanted if not (_norm(po) in seen or seen.add(_norm(po)))]

    if credentials is None:
        credentials = credentials_from_env()

    result = TrackingResult(status="checked")
    with _browser_page(headless) as page:
        driver = AdidasClickDriver(page, credentials.base_url)
        try:
            driver.login(credentials)

            for po_number in po_list:
                po_result = TrackingPO(po_number=po_number)
                rows = driver.find_orders_for_po(po_number)
                exact = [row for row in rows if row.get("exact")]
                other = [row for row in rows if not row.get("exact")]
                if other:
                    # adidas's order-book search also matches PO prefixes, so
                    # say plainly which orders were left out rather than
                    # reporting tracking for a PO nobody asked about.
                    result.warnings.append(
                        f"Search for {po_number!r} also returned "
                        f"{len(other)} order(s) for other POs ("
                        + ", ".join(
                            sorted({row["po_number"] or "?" for row in other})
                        )
                        + ") — those were not tracked."
                    )

                for row in exact:
                    po_result.orders.append(
                        _track_one_order(driver, row, po_number, result)
                    )

                po_result.order_count = len(po_result.orders)
                po_result.shipment_count = sum(
                    len(order.shipments) for order in po_result.orders
                )
                po_result.status = _po_status(po_result.orders)
                if po_result.status == "not_found":
                    po_result.note = (
                        "The adidas order book returned no order carrying this "
                        "PO number."
                        + (
                            " The search did match other POs — check the number."
                            if other
                            else ""
                        )
                    )
                    result.not_found_pos.append(po_number)
                result.pos.append(po_result)

            result.total_orders = sum(po.order_count for po in result.pos)
            result.total_shipments = sum(po.shipment_count for po in result.pos)
            result.table = _tracking_table(result.pos)
            unreadable = [
                order.order_number
                for po in result.pos
                for order in po.orders
                if order.status == "unreadable"
            ]
            # A PO with no orders, or an order whose page would not load, means
            # the answer is incomplete — flag it rather than handing back a
            # table that silently omits an order.
            if result.not_found_pos or unreadable:
                result.status = "needs_confirmation"

            if screenshot_path:
                driver.screenshot(screenshot_path)
                result.screenshot_path = screenshot_path

            found_pos = len(result.pos) - len(result.not_found_pos)
            result.message = (
                f"Tracking lookup complete — {found_pos} of {len(result.pos)} PO(s) "
                f"matched {result.total_orders} order(s) with "
                f"{result.total_shipments} shipment(s)."
            )
            if result.not_found_pos:
                result.message += (
                    " No orders were found for "
                    + ", ".join(result.not_found_pos)
                    + " — confirm the PO number(s) with the user."
                )
            if unreadable:
                result.message += (
                    " Order(s) " + ", ".join(unreadable) + " could not be read "
                    "— their status is unknown (see warnings)."
                )
            return result
        except (AdidasConfigError, AdidasAPIError, AdidasTransportError):
            raise
        except Exception as exc:  # noqa: BLE001 — normalize unexpected failures
            raise AdidasTransportError(
                f"Unexpected failure during the adidas Click tracking lookup: {exc}"
            ) from exc


def _track_one_order(
    driver: "AdidasClickDriver",
    row: dict,
    po_number: str,
    result: TrackingResult,
) -> TrackingOrder:
    """Read one order's shipments (or expected ship dates), never raising.

    A single unreadable order must not lose the tracking already gathered for
    the other orders/POs in the run, so any failure here becomes that order's
    ``unreadable`` status plus a run warning.
    """

    order = TrackingOrder(
        order_number=row["order_number"],
        po_number=row.get("po_number") or po_number,
        order_type=row.get("order_type"),
    )
    try:
        if driver.open_order(order.order_number):
            order.shipments = [
                TrackingShipment(**shipment)
                for shipment in driver.read_delivery_tracking(order.order_number)
            ]
            order.status = "shipped"
            if not order.shipments:
                # The Delivery Tracking link was there but the table came back
                # empty — say so rather than implying "nothing shipped".
                order.note = (
                    "The order has a Delivery Tracking page but no delivery rows "
                    "could be read — check it in the portal."
                )
        else:
            order.status = "not_shipped"
            order.expected_ship_dates = driver.read_expected_ship_dates()
            order.expected_ship_date = _earliest_expected(order.expected_ship_dates)
            if not order.expected_ship_dates:
                order.note = (
                    "Nothing has shipped and no expected ship date was shown on "
                    "the order."
                )
    except Exception as exc:  # noqa: BLE001 — one bad order must not sink the run
        order.status = "unreadable"
        order.note = str(exc)
        result.warnings.append(
            f"Order {order.order_number} (PO {po_number}) could not be read: {exc}"
        )
    return order
