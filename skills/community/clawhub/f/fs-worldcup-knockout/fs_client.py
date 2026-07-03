#!/usr/bin/env python3
"""
FunctionSpace propSPACE API client — joule engine (v0.4).

Stdlib-only. Covers the mech-v0-4 surface:
  /api/auth/*      signup, login, me
  /api/indexer/*   markets (paginated), market detail, positions
  /api/sdk/*       flows/buy, flows/sell, preview/buy, preview/payout_curve,
                   preview/claim, preview/sell

Auth model: HS256 bearer JWT, ~60-day expiry, no refresh.
Token is persisted to token_store (if given) and reused across runs.
On 401, call client.relogin(username, password) and retry.

NOTE: The old v0.3 B-spline API (/api/views/*, /api/market/trading/*,
num_buckets+2 vectors) is dead. This client targets mech-v0-4 only.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class FSHTTPError(Exception):
    def __init__(self, code: int, body: str):
        self.code = code
        self.body = body
        super().__init__(f"HTTP {code}: {body[:300]}")


class FSClient:
    def __init__(self, base_url: str, token_store: Path | None = None):
        """
        base_url:    Engine root URL, e.g.
                     "https://fs-engine-api-mech-v0-4.onrender.com"
        token_store: Optional path to a JSON file where the bearer token +
                     user_id are persisted across runs (avoids re-auth on
                     every execution).
        """
        self.base = base_url.rstrip("/") + "/api"
        self._token_store = token_store
        self.token: str | None = None
        self.user_id: int | None = None
        self._load_stored_token()

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def signup_or_login(self, username: str, password: str) -> dict:
        """
        Try login; if the account doesn't exist yet (401/404), sign up.
        Returns the user dict. Persists the token for future runs.
        """
        try:
            return self._login(username, password)
        except FSHTTPError as e:
            if e.code in (401, 404):
                return self._signup(username, password)
            raise

    def relogin(self, username: str, password: str) -> dict:
        """Force re-authentication (call when a buy returns 401). Returns user dict."""
        return self._login(username, password)

    def me(self) -> dict:
        """Current user + live wallet_value. Requires token."""
        return self._get("/auth/me", auth=True)

    def _signup(self, username: str, password: str) -> dict:
        resp = self._post("/auth/signup", {"username": username, "password": password})
        self._persist_token(resp)
        return resp["user"]

    def _login(self, username: str, password: str) -> dict:
        resp = self._post("/auth/login", {"username": username, "password": password})
        self._persist_token(resp)
        return resp["user"]

    # ------------------------------------------------------------------
    # Market discovery
    # ------------------------------------------------------------------

    def list_markets(self, status: str = "open", page_size: int = 50) -> list[dict]:
        """
        Return all markets with the given status, auto-paginating.
        Includes state_vector (needed for consensus computation).
        """
        all_markets: list[dict] = []
        page = 1
        while True:
            resp = self._get("/indexer/markets", params={
                "status": status,
                "page": page,
                "page_size": page_size,
                "include_state_vector": "true",
            })
            batch: list[dict] = resp.get("markets", [])
            all_markets.extend(batch)
            total = resp.get("total")
            if total is not None and len(all_markets) >= int(total):
                break
            if len(batch) < page_size:
                break
            page += 1
        return all_markets

    def market_state(self, market_id: int) -> dict:
        """Fetch a single market by ID (includes state_vector)."""
        return self._get(f"/indexer/markets/{market_id}")

    # ------------------------------------------------------------------
    # Trading — recipe-based (recommended)
    # ------------------------------------------------------------------

    def buy(
        self,
        market_id: int,
        position_type: str,
        position_params: dict,
        collateral: float,
        metadata: dict | None = None,
    ) -> dict:
        """
        Place a trade using a server-side recipe. Supported position_type values:
          "normal"  — Gaussian: params {"mean": 0..1, "std_dev": 0..1}
          "box"     — range band: params {"lower": 0..1, "upper": 0..1}
          "density" — explicit histogram: params {"density": [... length=num_buckets]}
          "raw"     — raw vector: params {"position_vector": [...]}
          "uniform" — flat: params {}

        mean/std_dev/lower/upper are in normalized [0,1] axis space:
          norm = (pts - lower_bound) / (upper_bound - lower_bound)

        Returns the "result" dict from the engine:
          position_id, position_vector, trade_size, collateral.
        """
        body: dict = {
            "collateral": collateral,
            "position_type": position_type,
            "position_params": position_params,
        }
        if metadata:
            body["metadata"] = metadata
        resp = self._authed_post(f"/sdk/flows/buy/{market_id}", body)
        return resp.get("result", resp)

    def sell(self, market_id: int, position_id: int) -> dict:
        """Close an open position (sell back into the pool)."""
        return self._authed_post(f"/sdk/flows/sell/{market_id}/{position_id}", {})

    # ------------------------------------------------------------------
    # Previews (no auth, no spend)
    # ------------------------------------------------------------------

    def preview_buy(
        self,
        market_id: int,
        position_type: str,
        position_params: dict,
        collateral: float,
    ) -> dict:
        """Preview the position a buy would create (no spend)."""
        return self._post(f"/sdk/preview/buy/{market_id}", {
            "collateral": collateral,
            "position_type": position_type,
            "position_params": position_params,
        })

    def payout_curve(
        self,
        market_id: int,
        position_type: str,
        position_params: dict,
        collateral: float,
        num_outcomes: int | None = None,
    ) -> dict:
        """
        Sweep every possible outcome and return payout + P&L at each.
        Set num_outcomes = market["num_buckets"] + 1 for exactly one row per bucket.
        """
        body: dict = {
            "collateral": collateral,
            "position_type": position_type,
            "position_params": position_params,
        }
        if num_outcomes is not None:
            body["num_outcomes"] = num_outcomes
        return self._post(f"/sdk/preview/payout_curve/{market_id}", body)

    def preview_claim(
        self, market_id: int, position_id: int, outcome_index: int | None = None
    ) -> dict:
        """Value an existing position at a specific outcome bucket."""
        path = f"/sdk/preview/claim/{market_id}/{position_id}"
        params = {"outcome_index": outcome_index} if outcome_index is not None else {}
        return self._get(path, params=params or None)

    def preview_sell(self, market_id: int, position_id: int) -> dict:
        """Current cash-out value of a position (no auth)."""
        return self._get(f"/sdk/preview/sell/{market_id}/{position_id}")

    # ------------------------------------------------------------------
    # Positions
    # ------------------------------------------------------------------

    def positions(
        self,
        user_id: int | None = None,
        market_id: int | None = None,
        page_size: int = 200,
    ) -> list[dict]:
        """Read positions. Scoped to a specific market if market_id given."""
        uid = user_id or self.user_id
        if market_id is not None:
            path = f"/indexer/users/by-id/{uid}/markets/{market_id}/positions"
        else:
            path = f"/indexer/users/by-id/{uid}/positions"
        resp = self._get(path, params={"page_size": page_size})
        return resp.get("positions", [])

    # ------------------------------------------------------------------
    # Consensus helpers
    # ------------------------------------------------------------------

    @staticmethod
    def consensus_mean(market: dict) -> float:
        """
        Compute the expected-value mean of the current market state_vector
        (in absolute fantasy points). Falls back to current_consensus
        (normalized peak → absolute pts) if state_vector is absent or empty.
        """
        sv = market.get("state_vector")
        lower: float = market["lower_bound"]
        upper: float = market["upper_bound"]
        n: int = market["num_buckets"]

        if sv and len(sv) == n:
            width = (upper - lower) / n
            total = wsum = 0.0
            for i, v in enumerate(sv):
                wsum += (lower + (i + 0.5) * width) * v
                total += v
            if total > 0:
                return wsum / total

        # Fallback: current_consensus is a normalized [0,1] peak location
        cc = market.get("current_consensus")
        if cc is not None:
            return lower + float(cc) * (upper - lower)
        return (lower + upper) / 2.0

    @staticmethod
    def normalize(pts: float, market: dict) -> float:
        """Convert fantasy points to normalized [0,1] axis position."""
        lo, hi = market["lower_bound"], market["upper_bound"]
        return max(0.0, min(1.0, (pts - lo) / (hi - lo)))

    @staticmethod
    def denormalize(norm: float, market: dict) -> float:
        """Convert normalized [0,1] position back to fantasy points."""
        lo, hi = market["lower_bound"], market["upper_bound"]
        return lo + norm * (hi - lo)

    # ------------------------------------------------------------------
    # Token persistence internals
    # ------------------------------------------------------------------

    def _persist_token(self, resp: dict) -> None:
        self.token = resp.get("access_token")
        user = resp.get("user") or {}
        self.user_id = user.get("user_id")
        if self._token_store and self.token:
            self._token_store.parent.mkdir(parents=True, exist_ok=True)
            self._token_store.write_text(json.dumps({
                "access_token": self.token,
                "user_id": self.user_id,
            }, indent=2))

    def _load_stored_token(self) -> None:
        if self._token_store and self._token_store.exists():
            try:
                data = json.loads(self._token_store.read_text())
                self.token = data.get("access_token")
                self.user_id = data.get("user_id")
            except Exception:
                pass

    # ------------------------------------------------------------------
    # HTTP primitives
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict | None = None, auth: bool = False) -> dict:
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        if auth and self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        return self._send(req)

    def _post(self, path: str, body: dict) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            self.base + path, data=data,
            headers={"Content-Type": "application/json"},
        )
        return self._send(req)

    def _authed_post(self, path: str, body: dict) -> dict:
        data = json.dumps(body).encode()
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(self.base + path, data=data, headers=headers)
        return self._send(req)

    @staticmethod
    def _send(req: urllib.request.Request) -> dict:
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                return json.loads(res.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise FSHTTPError(e.code, body) from e
