"""Error taxonomy for the CHAMPRO API.

CHAMPRO answers **HTTP 200 for almost every failure**. Verified against the
live service: a bad `APICustomerKey` on `ProductInfo`, `Inventory`,
`OrderStatus` and `PlaceOrder` all return 200 with the failure buried in the
body under four *different* key names. A client that trusts the status code
reports success on every one of them.

So the only reliable failure signal is the body, and every response shape
carries it somewhere else:

| Endpoint      | Where the error lives                                  |
| ------------- | ------------------------------------------------------ |
| `ProductInfo` | `Error` (string)                                       |
| `OrderStatus` | `Error` (string)                                       |
| `Inventory`   | `ResponseMessage` (string) + `ErrorMessages` (list)    |
| `PlaceOrder`  | `RequestErrors[].Response`, then per order              |
|               | `OrderErrors[].Response`, then `SubOrderErrors[]`       |
| CB `GetOrderInfo` | nothing at all — a bad key returns `[]`            |

`extract_envelope_errors` knows all of them and hoists whatever it finds into
one flat list, so the callers never have to remember which endpoint spells it
which way.
"""

from __future__ import annotations

import re
from typing import Any

# --- Documented error codes -------------------------------------------------
#
# Two numbering schemes are in play and they are not the same table.
#
#   * The Custom Builder `PlaceOrder` documents two-digit `MessageCode`s
#     ("01".."25") in its own response object.
#   * The REST API embeds dotted codes in the message text itself
#     ("E2.8.3: <SKU> - Not enough Inventory.", "E4.1: Customer validation
#     error."). These are prefixes on a free-text string, not a field.
#
# Both are kept so a caller can classify a failure without string-matching
# English prose that CHAMPRO may reword.

CB_MESSAGE_CODES: dict[str, str] = {
    "01": "Cannot download Proof File.",
    "02": "Proof file is in incorrect format. Allowed formats: .PDF, .JPG, .JPEG, .PNG.",
    "03": "Request format or data validation error.",
    "04": "Cannot place order with customer default Net Terms.",
    "05": "Customer validation error. Please contact CHAMPRO API Support.",
    "06": "Failed Address Verification.",
    "07": "Cannot process order request for both custom and stock products. Please split the request.",
    "08": "SKU does not Exist.",
    "09": "Cannot place order with customer default Net Terms.",
    "10": "Customer validation error. Please contact CHAMPRO API Support.",
    "11": "Warehouse is not specified. Please specify warehouse or use Auto Warehouse option.",
    "12": "Failed to place the order. Please contact CHAMPRO API Support.",
    "13": "Not enough Inventory.",
    "14": "Failed to place the order. Please contact CHAMPRO API Support.",
    "15": "IP Address is not allowed. Add your IP on the Account and Contact Info page.",
    "16": "Incorrect Customer API Key.",
    "17": "Incorrect PO Number.",
    "18": "Failed to save the order data.",
    "19": "Order has Wrong Format.",
    "20": "Can not find API Customer Key.",
    "21": "Error Lead Time validation: this value is required.",
    "22": "Error Lead Time validation.",
    "23": "Do not allow to place order with your Term of payment.",
    "24": "Recipient Name or Shipping Address is incorrect.",
    "25": "Product must be ordered in quantity increments of its Minimum Order Quantity.",
}

# Codes that mean "your account or network is not set up", not "your data is
# wrong". These are operator problems: retrying with different order data will
# never fix them.
SETUP_MESSAGE_CODES = frozenset({"04", "05", "09", "10", "15", "16", "20", "23"})

# Codes that mean the request will never succeed unchanged. Never auto-retry.
TERMINAL_MESSAGE_CODES = frozenset(
    {"02", "03", "07", "08", "17", "19", "21", "22", "24", "25"} | SETUP_MESSAGE_CODES
)

_DOTTED_CODE = re.compile(r"\bE(\d+(?:\.\d+)*)\s*:\s*")


class ChamproError(Exception):
    """Base for every error this skill raises."""


class ChamproConfigError(ChamproError):
    """Missing/blank API key, unusable base URL, bad environment name."""


class ChamproTransportError(ChamproError):
    """The request never produced a parseable answer (DNS, TLS, timeout, HTML)."""

    retryable = True


class ChamproValidationError(ChamproError):
    """Caught locally, before anything was sent."""


class ChamproAPIError(ChamproError):
    """CHAMPRO answered, and the answer is a failure.

    `errors` is the flat hoisted list; `codes` the dotted/two-digit codes found
    in it; `retryable` is False whenever any code is terminal, because a
    duplicate order costs more than a late one.
    """

    def __init__(
        self,
        message: str,
        *,
        endpoint: str = "",
        errors: list[dict[str, Any]] | None = None,
        response: Any = None,
    ) -> None:
        super().__init__(message)
        self.endpoint = endpoint
        self.errors = errors or []
        self.response = response

    @property
    def codes(self) -> list[str]:
        out: list[str] = []
        for err in self.errors:
            code = err.get("code")
            if code and code not in out:
                out.append(code)
        return out

    @property
    def retryable(self) -> bool:
        for err in self.errors:
            code = str(err.get("code") or "")
            if code in TERMINAL_MESSAGE_CODES:
                return False
            # "E3.1" and friends: the leading segment carries the family, and
            # every documented family is a data/auth problem, not a blip.
            if code.startswith("E"):
                return False
        return False if self.errors else True

    @property
    def is_setup_problem(self) -> bool:
        """True when the fix is on the Account & Contact Info page, not in the payload."""
        if any(str(e.get("code") or "") in SETUP_MESSAGE_CODES for e in self.errors):
            return True
        blob = " ".join(str(e.get("message") or "") for e in self.errors).lower()
        return any(
            token in blob
            for token in (
                "customer validation error",
                "api customer key",
                "ip address is not allowed",
                "term of payment",
                "net terms",
            )
        )


class ChamproPartialOrderError(ChamproError):
    """Some suborders were created and some lines failed — in ONE response.

    This is not exotic; CHAMPRO's own documented example does it, rejecting two
    SKUs for inventory while still cutting two suborders. Real orders exist at
    that point. Never retry the request: resubmit only the failed lines, as a
    new order.
    """

    def __init__(self, message: str, *, result: Any = None) -> None:
        super().__init__(message)
        self.result = result


def parse_message_code(message: str) -> str | None:
    """Pull a code out of an error string.

    Handles the REST dotted form (`"E2.8.3: BP62YGHBPS - Not enough Inventory."`
    -> `"E2.8.3"`) and returns None when the message carries no code at all,
    which is common for the single-string `Error` fields.
    """

    if not message:
        return None
    match = _DOTTED_CODE.search(message)
    if match:
        return f"E{match.group(1)}"
    return None


def _err(message: Any, *, scope: str, code: str | None = None, **extra: Any) -> dict[str, Any]:
    text = str(message).strip()
    return {
        "scope": scope,
        "message": text,
        "code": code or parse_message_code(text),
        **{k: v for k, v in extra.items() if v is not None},
    }


def _string_errors(value: Any) -> list[str]:
    """Normalise a field that may be a string, a list, or a list of objects."""

    if value in (None, "", []):
        return []
    if isinstance(value, str):
        return [value]
    out: list[str] = []
    for item in value if isinstance(value, list) else [value]:
        if isinstance(item, dict):
            text = item.get("Response") or item.get("Message") or item.get("Error")
            if text:
                out.append(str(text))
        elif item:
            out.append(str(item))
    return out


# Inventory's `ResponseMessage` is populated on success too (it echoes an
# opaque session-ish string), so only these values mean failure.
_INVENTORY_FAILURE_MARKERS = ("request data is incorrect", "error", "not allowed", "invalid")


def extract_envelope_errors(payload: Any, endpoint: str = "") -> list[dict[str, Any]]:
    """Hoist every error out of a 200 response, wherever this endpoint hides it.

    Returns a flat list of `{scope, message, code, ...}`. An empty list means
    the body carried no failure — which is the *only* trustworthy definition of
    success for this API.
    """

    errors: list[dict[str, Any]] = []
    if not isinstance(payload, dict):
        return errors

    # ProductInfo / OrderStatus: a single `Error` string.
    for text in _string_errors(payload.get("Error")):
        errors.append(_err(text, scope="request"))

    # Inventory: `ResponseMessage` doubles as a status line, so only treat it
    # as an error when it actually reads like one.
    response_message = payload.get("ResponseMessage")
    if isinstance(response_message, str) and response_message.strip():
        low = response_message.lower()
        if any(marker in low for marker in _INVENTORY_FAILURE_MARKERS):
            errors.append(_err(response_message, scope="request"))
    for text in _string_errors(payload.get("ErrorMessages")):
        errors.append(_err(text, scope="item"))

    # PlaceOrder: three nested levels, each its own list of `{Response}`.
    for text in _string_errors(payload.get("RequestErrors")):
        errors.append(_err(text, scope="request"))

    for index, order in enumerate(payload.get("Orders") or []):
        if not isinstance(order, dict):
            continue
        po = order.get("PO")
        for text in _string_errors(order.get("OrderErrors")):
            errors.append(_err(text, scope="order", order_index=index, po=po))
        for sub in order.get("SubOrders") or []:
            if not isinstance(sub, dict):
                continue
            for text in _string_errors(sub.get("SubOrderErrors")):
                errors.append(
                    _err(
                        text,
                        scope="suborder",
                        order_index=index,
                        po=po,
                        suborder_id=sub.get("SubOrderID"),
                        warehouse=sub.get("Warehouse"),
                    )
                )

    # Custom Builder PlaceOrder: flat `Result`/`Message`/`MessageCode`.
    if str(payload.get("Result") or "").upper() not in ("", "OK"):
        code = payload.get("MessageCode")
        code = str(code).zfill(2) if code not in (None, "") else None
        errors.append(
            _err(
                payload.get("Message") or "Custom Builder rejected the order.",
                scope="request",
                code=code,
            )
        )

    for err in errors:
        code = err.get("code")
        if code and code in CB_MESSAGE_CODES and not err.get("message"):
            err["message"] = CB_MESSAGE_CODES[code]
    return errors


def describe_code(code: str) -> str | None:
    """Human text for a documented code, or None if it is not one we know."""

    if not code:
        return None
    return CB_MESSAGE_CODES.get(str(code).zfill(2) if str(code).isdigit() else str(code))
