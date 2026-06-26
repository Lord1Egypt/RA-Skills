"""READ-ONLY Coinbase exchange balance reader.

Fetches account balances via the Coinbase API using read-only API keys.
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

_COINBASE_API = "https://api.coinbase.com/v2"

# Synthetic holdings for test mode
_SYNTHETIC_HOLDINGS: list[tuple[str, Decimal, Decimal]] = [
    ("BTC", Decimal("0.5"), Decimal("64000")),
    ("ETH", Decimal("3"), Decimal("1900")),
    ("USDC", Decimal("2000"), Decimal("1.00")),
    ("SOL", Decimal("100"), Decimal("135")),
]


class CoinbaseExchangeConnector(BaseConnector):
    """READ-ONLY connector for Coinbase exchange balances.

    SECURITY: This class provides ZERO write methods. It cannot
    transfer or modify any exchange state. Only read-only
    API permissions are used. All calls are GET requests.
    """

    provider = Provider.COINBASE

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._api_secret: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        """Connect with Coinbase read-only API key.

        Accepts: {"api_key": "...", "api_secret": "..."}
        """
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Coinbase...")
                await asyncio.sleep(1)
                print("Authenticated with Coinbase (test mode, read-only)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Coinbase credentials")
            return False

        api_key = credentials.get("api_key", "")
        api_secret = credentials.get("api_secret", "")
        if not api_key or not api_secret:
            logger.error("Missing Coinbase api_key or api_secret")
            return False

        self._api_key = api_key
        self._api_secret = api_secret
        self._client = httpx.AsyncClient(
            base_url=_COINBASE_API,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/user")
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("Coinbase API key is invalid or expired")
            else:
                logger.error("Coinbase validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Coinbase connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Coinbase connection error: %s", exc)
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
            resp = await self._client.get("/accounts")
            resp.raise_for_status()
            data = resp.json()

            for account in data.get("data", []):
                balance = Decimal(account.get("balance", {}).get("amount", "0"))
                currency = account.get("balance", {}).get("currency", "")
                if balance <= 0 or not currency:
                    continue

                native_amount = Decimal(
                    account.get("native_balance", {}).get("amount", "0")
                )
                usd_value = native_amount.quantize(Decimal("0.01"))

                records.append(FinancialRecord(
                    record_date=end_date,
                    amount=usd_value,
                    category=SpendCategory.CRYPTO_HOLDINGS,
                    subcategory=currency,
                    provider=Provider.COINBASE,
                    source="coinbase_api",
                    raw_description=f"{balance} {currency} on Coinbase. {CRYPTO_DISCLAIMER}",
                ))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Coinbase rate limit hit")
            else:
                logger.error("Coinbase fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Coinbase fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Coinbase fetch error: %s", exc)

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
        """Synthetic Coinbase holdings: 0.5 BTC, 3 ETH, 2K USDC, 100 SOL."""
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
                provider=Provider.COINBASE,
                source="synthetic",
                raw_description=f"Synthetic: {qty} {token} on Coinbase @ ${price}. {CRYPTO_DISCLAIMER}",
            ))
        return records
