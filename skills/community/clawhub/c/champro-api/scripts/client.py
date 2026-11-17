"""HTTP transport for the CHAMPRO REST API and the Custom Builder API.

Two hosts, and they are not interchangeable:

* `https://api.champrosports.com` — the REST API (ProductInfo, Inventory,
  PlaceOrder, OrderStatus). Authenticates with `APICustomerKey`.
* `https://cb.champrosports.com` — the Custom Builder API (GetOrderInfo,
  GetFile, PlaceOrder-from-session). Authenticates with `CustomerKey` for the
  read methods and `APICustomerKey` for placing an order.

Sandbox is **selected by URL, not by a flag**, and the two paths are one
character apart:

    production   POST /api/Order/PlaceOrder
    sandbox      POST /api/OrderSandBox/PlaceOrder

Verified live: `/api/OrderSandBox/<anything>` is a catch-all that routes every
path to the sandbox place-order, while `/api/Order/<bogus>` correctly 404s.
That asymmetry is why this module never builds an order URL by string
concatenation from caller input — `place_order()` takes a boolean and picks
the whole path itself. There is no `IsSandBox` field on the REST API; that flag
exists only on the Custom Builder's own PlaceOrder.
"""

from __future__ import annotations

import json
import os
from typing import Any

from errors import (
    ChamproAPIError,
    ChamproConfigError,
    ChamproTransportError,
    extract_envelope_errors,
)

API_BASE = "https://api.champrosports.com"
CB_BASE = "https://cb.champrosports.com"

# Production and sandbox place-order paths, kept as literals so no caller can
# assemble a production URL by accident.
_PLACE_ORDER_PROD = "/api/Order/PlaceOrder"
_PLACE_ORDER_SANDBOX = "/api/OrderSandBox/PlaceOrder"

DEFAULT_TIMEOUT = 60


def _requests():
    try:
        import requests  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - import guard
        raise ChamproConfigError(
            "The `requests` package is required: pip install 'requests>=2.28'"
        ) from exc
    return requests


def resolve_api_key(explicit: str | None = None) -> str:
    key = (explicit or os.environ.get("CHAMPRO_API_CUSTOMER_KEY") or "").strip()
    if not key:
        raise ChamproConfigError(
            "No CHAMPRO API customer key. Set CHAMPRO_API_CUSTOMER_KEY, or pass "
            "`api_customer_key` in the stdin JSON. Generate one on "
            "https://champrosports.com/AccountAndContactInfo"
        )
    return key


def resolve_cb_key(explicit: str | None = None) -> str:
    """The Custom Builder *embed* key — a different credential from the API key.

    The docs use both on the same page (`CustomBuilderCustomerKey` vs
    `CustomBuilderAPICustomerKey`) and they are generated separately on the
    Account & Contact Info page. Mixing them up produces a 404 on `GetFile` and
    a bare `[]` on `GetOrderInfo`, neither of which says "wrong key".
    """

    key = (explicit or os.environ.get("CHAMPRO_CB_CUSTOMER_KEY") or "").strip()
    if not key:
        raise ChamproConfigError(
            "No CHAMPRO Custom Builder embed key. Set CHAMPRO_CB_CUSTOMER_KEY, or "
            "pass `cb_customer_key`. This is the 'Customer Builder Embed Key' from "
            "https://champrosports.com/AccountAndContactInfo — NOT the API Customer Key."
        )
    return key


class ChamproClient:
    """Thin JSON client that treats a 200 with a body error as a failure."""

    def __init__(
        self,
        api_customer_key: str | None = None,
        *,
        cb_customer_key: str | None = None,
        api_base: str | None = None,
        cb_base: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._api_key = api_customer_key
        self._cb_key = cb_customer_key
        self.api_base = (api_base or os.environ.get("CHAMPRO_API_BASE") or API_BASE).rstrip("/")
        self.cb_base = (cb_base or os.environ.get("CHAMPRO_CB_BASE") or CB_BASE).rstrip("/")
        self.timeout = int(os.environ.get("CHAMPRO_TIMEOUT") or timeout)
        self._session = None

    # -- credentials ---------------------------------------------------------

    @property
    def api_key(self) -> str:
        return resolve_api_key(self._api_key)

    @property
    def cb_key(self) -> str:
        return resolve_cb_key(self._cb_key)

    # -- transport -----------------------------------------------------------

    @property
    def session(self):
        if self._session is None:
            requests = _requests()
            self._session = requests.Session()
            self._session.headers.update(
                {"Accept": "application/json", "User-Agent": "champro-api-skill/1.0"}
            )
        return self._session

    def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
        raw: bool = False,
    ):
        requests = _requests()
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as exc:
            raise ChamproTransportError(f"{method} {url} failed: {exc}") from exc

        if raw:
            return response

        # 404/405 are real here: `GetFile` 404s on an unknown session, and the
        # sandbox controller 405s every GET.
        if response.status_code >= 400:
            snippet = (response.text or "")[:400]
            raise ChamproTransportError(
                f"{method} {url} returned HTTP {response.status_code}: {snippet}"
            )

        text = response.text or ""
        try:
            return json.loads(text) if text.strip() else None
        except json.JSONDecodeError as exc:
            raise ChamproTransportError(
                f"{method} {url} returned non-JSON ({response.headers.get('Content-Type')}): "
                f"{text[:300]}"
            ) from exc

    def _checked(self, payload: Any, endpoint: str) -> Any:
        """Raise if the 200 body carries errors anywhere CHAMPRO hides them."""

        found = extract_envelope_errors(payload, endpoint)
        if found:
            raise ChamproAPIError(
                "; ".join(e["message"] for e in found) or f"{endpoint} failed.",
                endpoint=endpoint,
                errors=found,
                response=payload,
            )
        return payload

    # -- REST API ------------------------------------------------------------

    def product_info(self, product_master: str) -> dict[str, Any]:
        payload = self._request(
            "GET",
            f"{self.api_base}/api/Order/ProductInfo",
            params={"ProductMaster": product_master, "APICustomerKey": self.api_key},
        )
        return self._checked(payload, "ProductInfo")

    def inventory(self, skus: list[str]) -> dict[str, Any]:
        body = {
            "APICustomerKey": self.api_key,
            "Orders": [{"OrderItems": [{"SKU": sku} for sku in skus]}],
        }
        payload = self._request("POST", f"{self.api_base}/api/Order/Inventory", json_body=body)
        return self._checked(payload, "Inventory")

    def order_status(self, order_number: str | int) -> dict[str, Any]:
        payload = self._request(
            "GET",
            f"{self.api_base}/api/Order/OrderStatus",
            params={"OrderNumber": str(order_number), "APICustomerKey": self.api_key},
        )
        return self._checked(payload, "OrderStatus")

    def place_order(self, body: dict[str, Any], *, production: bool) -> dict[str, Any]:
        """POST an order envelope. `production=False` targets the sandbox.

        Returns the raw envelope **without** raising on nested errors: a
        PlaceOrder response routinely reports failed lines alongside suborders
        that were genuinely created, and collapsing that into an exception
        would hide orders that now exist. Classification happens in
        `orders.summarise_place_order`.
        """

        path = _PLACE_ORDER_PROD if production else _PLACE_ORDER_SANDBOX
        body = {**body, "APICustomerKey": self.api_key}
        payload = self._request("POST", f"{self.api_base}{path}", json_body=body)
        if not isinstance(payload, dict):
            raise ChamproTransportError(f"PlaceOrder returned an unexpected body: {payload!r}")
        payload["_endpoint"] = path
        payload["_environment"] = "production" if production else "sandbox"
        return payload

    # -- Custom Builder ------------------------------------------------------

    def cb_order_info(self, session_id: str) -> Any:
        """Roster/design data for a saved Custom Builder design session.

        Verified live: an unknown key or session returns `[]` with HTTP 200 and
        no error field, so "empty" and "unauthorised" are indistinguishable
        here. Callers must surface that ambiguity rather than reporting
        "no items" — see `custom_builder.get_design`.
        """

        return self._request(
            "GET",
            f"{self.cb_base}/api/Order/GetOrderInfo",
            params={"CustomerKey": self.cb_key, "SessionId": session_id},
        )

    def cb_file(self, session_id: str, file_type: str):
        """Binary proof/side-image download. Returns the raw response."""

        return self._request(
            "GET",
            f"{self.cb_base}/api/Order/GetFile",
            params={
                "CustomerKey": self.cb_key,
                "SessionId": session_id,
                "FileType": file_type,
            },
            raw=True,
        )

    def cb_place_order(self, body: dict[str, Any]) -> dict[str, Any]:
        """Place an order from a saved design session.

        Unlike the REST API this one *does* have an `IsSandBox` boolean, which
        the caller sets; there is no separate sandbox host.
        """

        payload = self._request("POST", f"{self.cb_base}/api/Order/PlaceOrder", json_body=body)
        if not isinstance(payload, dict):
            raise ChamproTransportError(f"CB PlaceOrder returned an unexpected body: {payload!r}")
        return payload
