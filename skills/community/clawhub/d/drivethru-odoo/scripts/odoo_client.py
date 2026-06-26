#!/usr/bin/env python3
"""Self-contained HTTP client for the Odoo `agent_api` module.

Talks to the custom `/agent_api/v1/*` REST surface exposed by the Odoo
`agent_api` addon, authenticating with the `X-Agent-API-Key` header. Covers
three domains:

  * Sales      — eBay products, inventory, sale orders, tracking
  * AP         — purchase orders, vendor bills, vendors
  * Production — MRP batch scheduling (overview, batches, workcenters, …)

This module has no third-party dependency beyond `requests` and no imports
from any host application — it is meant to be vendored inside a ClawHub skill
and driven by the thin CLI wrappers (`sales.py`, `ap.py`, `production.py`).

All methods return plain JSON-serialisable dicts / lists (the raw shapes
returned by the Odoo agent_api), so the calling agent can consume them
directly.
"""

from __future__ import annotations

import os
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - surfaced by the CLI wrappers
    requests = None  # type: ignore


# ── Errors ──────────────────────────────────────────────────────────────────


class OdooConnectionError(RuntimeError):
    """Raised when the Odoo API is unreachable or misconfigured."""


class OdooAPIError(RuntimeError):
    """Raised when Odoo returns an error response."""

    def __init__(self, status: int, body: str) -> None:
        self.status = status
        self.body = body
        super().__init__(f"Odoo API error {status}: {str(body)[:300]}")


# ── Client ──────────────────────────────────────────────────────────────────


class OdooClient:
    """HTTP client for the Odoo agent_api module.

    In `dry_run` mode the write methods (create order, schedule batch, …)
    return a synthetic result and never touch the network.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        dry_run: bool = False,
        timeout: int = 30,
    ) -> None:
        if requests is None:
            raise OdooConnectionError(
                "The 'requests' package is not installed. Install it with: "
                "pip install 'requests>=2.28'"
            )
        if not base_url or not api_key:
            raise OdooConnectionError(
                "Odoo not configured. Set ODOO_URL and ODOO_API_KEY env vars."
            )
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._dry_run = dry_run
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "X-Agent-API-Key": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    @property
    def dry_run(self) -> bool:
        return self._dry_run

    # ── generic request ─────────────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        try:
            resp = self._session.request(
                method.upper(),
                url,
                params=params,
                json=json_body,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:  # type: ignore[union-attr]
            raise OdooConnectionError(f"Request to {url} failed: {exc}") from exc

        if resp.status_code == 401:
            raise OdooAPIError(401, "Unauthorized — check ODOO_API_KEY")

        if not resp.ok:
            try:
                body = resp.json()
                err_msg = body.get("error", resp.text)
            except ValueError:
                err_msg = resp.text
            raise OdooAPIError(resp.status_code, err_msg)

        try:
            body = resp.json()
        except ValueError:
            raise OdooAPIError(resp.status_code, f"Non-JSON response: {resp.text[:200]}")

        if not body.get("success", True):
            raise OdooAPIError(resp.status_code, body.get("error", "Unknown error"))

        return body.get("data", body)

    # ── Sales: products & inventory ─────────────────────────────────────────

    def fetch_ebay_products(self) -> list[dict[str, Any]]:
        """Fetch all products in the Odoo 'eBay' category."""
        data = self._request("GET", "/agent_api/v1/ebay/products")
        return data.get("products", [])

    def get_inventory_levels(self, skus: list[str]) -> dict[str, int]:
        """Get current stock levels for a list of SKUs."""
        if not skus:
            return {}
        data = self._request(
            "GET",
            "/agent_api/v1/ebay/inventory",
            params={"skus": ",".join(skus)},
        )
        levels = data.get("levels", {})
        return {sku: int(qty or 0) for sku, qty in levels.items()}

    # ── Sales: orders ───────────────────────────────────────────────────────

    def create_sale_order(self, order: dict[str, Any]) -> dict[str, Any]:
        """Push an eBay order to Odoo.

        `order` is the eBay order shape (see references/agent_api_endpoints.md
        and scripts/sales.py `mock-order`). Returns the agent_api result with
        `odoo_order_id`, `odoo_order_name`, `already_existed`, `confirmed`, …
        """
        payload = _order_to_payload(order)

        if self._dry_run:
            return {
                "odoo_order_id": 0,
                "odoo_order_name": f"DRYRUN-{order.get('legacy_order_id', '')}",
                "already_existed": False,
                "confirmed": False,
                "dry_run": True,
            }

        return self._request("POST", "/agent_api/v1/ebay/orders", json_body=payload)

    def get_tracking_info(self, odoo_order_id: int | str) -> dict[str, Any] | None:
        """Get tracking info for a shipped Odoo order.

        `odoo_order_id` is the numeric Odoo order id (not the display name).
        Returns None when the order is not yet shipped.
        """
        data = self._request(
            "GET",
            f"/agent_api/v1/ebay/orders/{odoo_order_id}/tracking",
        )
        if not data.get("shipped"):
            return None
        return {
            "carrier": data.get("carrier", ""),
            "tracking_number": data.get("tracking_number", ""),
            "shipped_date": data.get("shipped_date", ""),
        }

    # ── AP: purchase orders ─────────────────────────────────────────────────

    def search_purchase_orders(
        self,
        *,
        search: str | None = None,
        vendor: str | None = None,
        state: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search for purchase orders by name, vendor ref, or vendor name."""
        params: dict[str, Any] = {"limit": limit}
        if search:
            params["search"] = search
        if vendor:
            params["vendor"] = vendor
        if state:
            params["state"] = state
        data = self._request("GET", "/agent_api/v1/ap/purchase_orders", params=params)
        return data.get("purchase_orders", [])

    def get_purchase_order(self, po_id: int) -> dict[str, Any]:
        """Fetch full PO detail including lines, receipt status, and existing bills."""
        return self._request("GET", f"/agent_api/v1/ap/purchase_orders/{po_id}")

    def update_po_lines(
        self,
        po_id: int,
        *,
        lines: list[dict[str, Any]] | None = None,
        freight_cost: float | None = None,
        fees_cost: float | None = None,
    ) -> dict[str, Any]:
        """Update PO line prices and/or freight/fees before bill creation.

        `lines` is a list of {"line_id": int, "price_unit": float}.
        """
        body: dict[str, Any] = {}
        if lines:
            body["lines"] = lines
        if freight_cost is not None:
            body["freight_cost"] = freight_cost
        if fees_cost is not None:
            body["fees_cost"] = fees_cost
        return self._request(
            "PUT",
            f"/agent_api/v1/ap/purchase_orders/{po_id}/lines",
            json_body=body,
        )

    # ── AP: vendor bills ────────────────────────────────────────────────────

    def create_vendor_bill(
        self,
        *,
        po_id: int,
        vendor_bill_number: str = "",
        invoice_date: str = "",
        line_ids: list[int] | None = None,
        reviewer_user_id: int | None = None,
        review_note: str = "",
        expected_total: float | None = None,
        tolerance: float = 0.05,
    ) -> dict[str, Any]:
        """Create a draft vendor bill from a PO.

        Odoo's create() override automatically adds fee/freight/misc lines as
        configured. The bill is created in draft; `reviewer_user_id` receives an
        Odoo activity to review and post it.
        """
        if self._dry_run:
            return {
                "dry_run": True,
                "po_id": po_id,
                "would_create_bill": True,
                "vendor_bill_number": vendor_bill_number,
            }

        body: dict[str, Any] = {"po_id": po_id, "tolerance": tolerance}
        if vendor_bill_number:
            body["vendor_bill_number"] = vendor_bill_number
        if invoice_date:
            body["invoice_date"] = invoice_date
        if line_ids:
            body["line_ids"] = line_ids
        if reviewer_user_id is not None:
            body["reviewer_user_id"] = reviewer_user_id
        if review_note:
            body["review_note"] = review_note
        if expected_total is not None:
            body["expected_total"] = expected_total
        return self._request("POST", "/agent_api/v1/ap/invoices", json_body=body)

    def get_vendor_bill(self, bill_id: int) -> dict[str, Any]:
        """Fetch full detail for an existing vendor bill."""
        return self._request("GET", f"/agent_api/v1/ap/invoices/{bill_id}")

    def search_vendors(
        self,
        *,
        search: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search vendor partners by name or email."""
        params: dict[str, Any] = {"limit": limit}
        if search:
            params["search"] = search
        data = self._request("GET", "/agent_api/v1/ap/vendors", params=params)
        return data.get("vendors", [])

    # ── Production: overview ─────────────────────────────────────────────────

    def get_overview(
        self,
        *,
        batch_detail: bool = False,
        batch_limit: int = 200,
        unscheduled_only: bool = False,
    ) -> dict[str, Any]:
        """Fetch everything needed for a planning pass in one round-trip.

        Returns a dict with `batches`, `workcenters`, `production_centers`,
        `decoration_methods`, and `open_batch_total`.
        """
        params: dict[str, Any] = {"batch_limit": batch_limit}
        if batch_detail:
            params["batch_detail"] = "true"
        if unscheduled_only:
            params["unscheduled_only"] = "true"
        return self._request("GET", "/agent_api/v1/production/overview", params=params)

    # ── Production: batches ─────────────────────────────────────────────────

    def get_batches(
        self,
        *,
        unscheduled_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List open production batches (summary shape) with pagination meta."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if unscheduled_only:
            params["unscheduled_only"] = "true"
        return self._request("GET", "/agent_api/v1/production/batches", params=params)

    def get_batch(self, batch_id: int) -> dict[str, Any]:
        """Fetch the full scheduling payload for a single batch."""
        return self._request("GET", f"/agent_api/v1/production/batches/{batch_id}")

    def schedule_batch(
        self,
        batch_id: int,
        *,
        primary_workcenter_id: int | None = None,
        production_center_id: int | None = None,
        date_planned_start: str | None = None,
        date_planned_finished: str | None = None,
        activity_message: str = "",
    ) -> dict[str, Any]:
        """Apply scheduling decisions to a single batch.

        Any subset of the four scheduling fields is allowed (partial updates).
        At least one must be non-None. In dry-run mode, returns the intended
        change set without writing.
        """
        scheduling_fields = {
            k: v
            for k, v in {
                "primary_workcenter_id": primary_workcenter_id,
                "production_center_id": production_center_id,
                "date_planned_start": date_planned_start,
                "date_planned_finished": date_planned_finished,
            }.items()
            if v is not None
        }
        if not scheduling_fields:
            raise ValueError("No scheduling fields provided")

        if self._dry_run:
            return {
                "dry_run": True,
                "batch_id": batch_id,
                "changes_applied": scheduling_fields,
                "success": True,
            }

        body: dict[str, Any] = dict(scheduling_fields)
        if activity_message:
            body["activity_message"] = activity_message
        return self._request(
            "PUT",
            f"/agent_api/v1/production/batches/{batch_id}/schedule",
            json_body=body,
        )

    def plan_batch(self, batch_id: int) -> dict[str, Any]:
        """Run Odoo's native button_plan() on a batch (requires a workcenter set)."""
        if self._dry_run:
            return {"dry_run": True, "batch_id": batch_id, "would_plan": True}
        return self._request(
            "POST", f"/agent_api/v1/production/batches/{batch_id}/plan", json_body={}
        )

    def bulk_schedule(
        self,
        updates: list[dict[str, Any]],
        *,
        atomic: bool = True,
    ) -> dict[str, Any]:
        """Apply many schedule edits in one request.

        Each update dict must include 'batch_id' plus any subset of the four
        scheduling fields. `atomic=True` aborts the whole request on any error.
        """
        if not updates:
            raise ValueError("bulk_schedule requires a non-empty updates list")

        if self._dry_run:
            return {
                "dry_run": True,
                "atomic": atomic,
                "applied_count": len(updates),
                "error_count": 0,
                "results": [
                    {"index": i, "batch_id": u.get("batch_id")}
                    for i, u in enumerate(updates)
                ],
            }

        body = {"atomic": atomic, "updates": updates}
        return self._request(
            "POST", "/agent_api/v1/production/batches/bulk_schedule", json_body=body
        )

    # ── Production: workcenters & reference data ────────────────────────────

    def get_workcenters(self, *, active_only: bool = True) -> list[dict[str, Any]]:
        """List all workcenters with their scheduled_batches inlined."""
        params: dict[str, Any] = {}
        if active_only:
            params["active"] = "true"
        data = self._request("GET", "/agent_api/v1/production/workcenters", params=params)
        return data.get("workcenters", [])

    def get_workcenter(self, workcenter_id: int) -> dict[str, Any]:
        """Fetch a single workcenter with its current scheduled load."""
        return self._request(
            "GET", f"/agent_api/v1/production/workcenters/{workcenter_id}"
        )

    def get_production_centers(self) -> list[dict[str, Any]]:
        """List all production centers with piece-count minimums and methods."""
        data = self._request("GET", "/agent_api/v1/production/production_centers")
        return data.get("production_centers", [])

    def get_decoration_methods(self) -> list[dict[str, Any]]:
        """List all active decoration methods."""
        data = self._request("GET", "/agent_api/v1/production/decoration_methods")
        return data.get("decoration_methods", [])


# ── Helpers ─────────────────────────────────────────────────────────────────


def _order_to_payload(order: dict[str, Any]) -> dict[str, Any]:
    """Map an eBay order dict to the agent_api order-create payload."""
    return {
        "ebay_order_id": order.get("order_id", ""),
        "ebay_legacy_order_id": order.get("legacy_order_id", ""),
        "creation_date": order.get("creation_date", ""),
        "buyer_username": order.get("buyer_username", ""),
        "buyer_email": order.get("buyer_email", ""),
        "currency": order.get("currency", "USD"),
        "subtotal": order.get("subtotal", 0.0),
        "tax": order.get("tax", 0.0),
        "shipping": order.get("shipping", 0.0),
        "total": order.get("total", 0.0),
        "line_items": order.get("line_items", []),
        "shipping_address": order.get("shipping_address"),
        "billing_address": order.get("billing_address"),
    }


def client_from_env() -> OdooClient:
    """Build an OdooClient from environment variables.

    Required:
      ODOO_URL      — base URL (e.g. https://staging.yourcompany.odoo.com)
      ODOO_API_KEY  — agent_api X-Agent-API-Key value

    Optional:
      ODOO_DRY_RUN  — if 'true'/'1'/'yes', log intent without making writes
    """
    base_url = os.getenv("ODOO_URL", "").strip()
    api_key = os.getenv("ODOO_API_KEY", "").strip()
    dry_run = os.getenv("ODOO_DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    return OdooClient(base_url=base_url, api_key=api_key, dry_run=dry_run)
