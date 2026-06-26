"""READ-ONLY Binance exchange balance reader.

Fetches account balances via the Binance Spot API using read-only API keys.
READ-ONLY connector. No write, transfer, or withdrawal methods.
Only read-only API permissions should be granted.

SECURITY: Grant only read permissions — no exchange or withdrawal access.
"""
import logging
from datetime import date
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.connectors.crypto_wallet import CRYPTO_DISCLAIMER
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_BINANCE_API = "https://api.binance.com"

# Synthetic holdings for test mode
_SYNTHETIC_HOLDINGS: list[tuple[str, Decimal, Decimal]] = [
    ("BTC", Decimal("1"), Decimal("64000")),
    ("ETH", Decimal("5"), Decimal("1900")),
    ("USDT", Decimal("5000"), Decimal("1.00")),
]


class BinanceExchangeConnector(BaseConnector):
    """READ-ONLY connector for Binance exchange balances.

    SECURITY: This class provides ZERO write methods. It cannot
    transfer or modify any exchange state. Only read-only
    API permissions are used.
    """

    provider = Provider.BINANCE

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._api_secret: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        """Connect with Binance read-only API key.

        Accepts: {"api_key": "...", "api_secret": "..."}
        """
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Binance...")
                await asyncio.sleep(1)
                print("Authenticated with Binance (test mode, read-only)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Binance credentials")
            return False

        api_key = credentials.get("api_key", "")
        api_secret = credentials.get("api_secret", "")
        if not api_key or not api_secret:
            logger.error("Missing Binance api_key or api_secret")
            return False

        self._api_key = api_key
        self._api_secret = api_secret
        self._client = httpx.AsyncClient(
            base_url=_BINANCE_API,
            headers={"X-MBX-APIKEY": self._api_key},
            timeout=30.0,
        )

        # Validate with account info (requires read-only permission)
        try:
            # Binance requires HMAC auth for /api/v3/account
            resp = await self._client.get("/api/v3/account", params=self._auth_params({}))
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Binance API key invalid or insufficient permissions")
            else:
                logger.error("Binance validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Binance connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Binance connection error: %s", exc)
            return False

    async def fetch_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Fetch account balances (READ-ONLY point-in-time snapshots)."""
        if not self.is_connected or self._client is None:
            logger.error("Not connected — call connect() first")
            return []

        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            return self.get_synthetic_records(start_date, end_date)

        records: list[FinancialRecord] = []
        try:
            # Fetch account balances
            resp = await self._client.get(
                "/api/v3/account", params=self._auth_params({})
            )
            resp.raise_for_status()
            account = resp.json()

            # Fetch ticker prices for USD conversion
            prices = await self._get_ticker_prices()

            for balance_entry in account.get("balances", []):
                asset = balance_entry.get("asset", "")
                free = Decimal(balance_entry.get("free", "0"))
                locked = Decimal(balance_entry.get("locked", "0"))
                total = free + locked
                if total <= 0:
                    continue

                # Convert to USD
                usd_value = self._to_usd(asset, total, prices)
                if usd_value <= 0:
                    continue

                records.append(FinancialRecord(
                    record_date=end_date,
                    amount=usd_value,
                    category=SpendCategory.CRYPTO_HOLDINGS,
                    subcategory=asset,
                    provider=Provider.BINANCE,
                    source="binance_api",
                    raw_description=f"{total} {asset} on Binance. {CRYPTO_DISCLAIMER}",
                ))

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Binance rate limit hit")
            else:
                logger.error("Binance fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Binance fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Binance fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        records = await self.fetch_records(today, today)
        total = sum(r.amount for r in records)
        by_asset = {(r.subcategory or "unknown"): str(r.amount) for r in records}
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "total_holdings_usd": str(total),
            "by_asset": by_asset,
            "disclaimer": CRYPTO_DISCLAIMER,
        }

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Synthetic Binance holdings: 1 BTC, 5 ETH, 5K USDT."""
        if end_date is None:
            end_date = date.today()
        records: list[FinancialRecord] = []
        for token, qty, price in _SYNTHETIC_HOLDINGS:
            value = (qty * price).quantize(Decimal("0.01"))
            records.append(FinancialRecord(
                record_date=end_date,
                amount=value,
                category=SpendCategory.CRYPTO_HOLDINGS,
                subcategory=token,
                provider=Provider.BINANCE,
                source="synthetic",
                raw_description=f"Synthetic: {qty} {token} on Binance @ ${price}. {CRYPTO_DISCLAIMER}",
            ))
        return records

    # ── Private helpers ────────────────────────────────────────────

    def _auth_params(self, params: dict) -> dict:
        """Add HMAC authentication digest to request params.

        Binance API requires HMAC-SHA256 auth for account endpoints.
        This is API-level authentication, not blockchain activity.
        """
        import hashlib
        import hmac
        import time as time_mod

        params["timestamp"] = str(int(time_mod.time() * 1000))
        params["recvWindow"] = "5000"
        query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        hmac_digest = hmac.new(
            self._api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["hmac"] = hmac_digest
        return params

    async def _get_ticker_prices(self) -> dict[str, Decimal]:
        """Fetch all USDT ticker prices from Binance."""
        assert self._client is not None
        prices: dict[str, Decimal] = {"USDT": Decimal("1.00"), "USDC": Decimal("1.00")}
        try:
            resp = await self._client.get("/api/v3/ticker/price")
            resp.raise_for_status()
            for item in resp.json():
                symbol = item.get("symbol", "")
                if symbol.endswith("USDT"):
                    asset = symbol[: -len("USDT")]
                    prices[asset] = Decimal(item["price"])
        except httpx.HTTPError as exc:
            logger.warning("Binance ticker fetch failed: %s", exc)
        return prices

    def _to_usd(
        self, asset: str, amount: Decimal, prices: dict[str, Decimal]
    ) -> Decimal:
        """Convert asset amount to USD using ticker prices."""
        if asset in ("USDT", "USDC", "BUSD"):
            return amount.quantize(Decimal("0.01"))
        price = prices.get(asset, Decimal("0"))
        return (amount * price).quantize(Decimal("0.01"))
