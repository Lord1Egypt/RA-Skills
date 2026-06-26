"""Tavily connector — tracks search API credit usage and costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_TAVILY_API = "https://api.tavily.com"

# Published Tavily pricing (as of early 2026)
_CREDIT_COST = Decimal("0.008")  # per search credit
_PLAN_PRICING: dict[str, dict[str, Any]] = {
    "researcher": {"monthly_cost": Decimal("0"), "credits_included": 1000},
    "business": {"monthly_cost": Decimal("0"), "credits_included": 5000},
}


class TavilyCostsConnector(BaseConnector):
    """Connector for Tavily search API usage and cost data.

    Tavily doesn't expose a full usage API, so this connector checks
    remaining credits via the API and tracks usage over time.
    """

    provider = Provider.TAVILY

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._client: httpx.AsyncClient | None = None
        self._total_credits: int = 0
        self._remaining_credits: int = 0

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Tavily...")
                await asyncio.sleep(1)
                print("Authenticated with Tavily API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Tavily API key")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        if not api_key:
            logger.error("Missing Tavily api_key")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(timeout=30.0)

        # Validate by checking credits endpoint or making a lightweight call
        try:
            resp = await self._client.post(
                f"{_TAVILY_API}/search",
                json={
                    "api_key": self._api_key,
                    "query": "test",
                    "max_results": 1,
                    "search_depth": "basic",
                },
            )
            resp.raise_for_status()

            # Check response headers for credit info if available
            self._remaining_credits = int(
                resp.headers.get("x-credits-remaining", 0)
            )
            self._total_credits = int(
                resp.headers.get("x-credits-total", 0)
            )

            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Tavily API key invalid")
            elif exc.response.status_code == 429:
                logger.error("Tavily rate limit during validation — try again later")
            else:
                logger.error("Tavily validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Tavily connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Tavily connection error: %s", exc)
            return False

    async def fetch_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        if not self.is_connected or self._client is None:
            logger.error("Not connected — call connect() first")
            return []

        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            return self.get_synthetic_records(start_date, end_date)

        records: list[FinancialRecord] = []

        # Tavily doesn't have a historical usage API. We can only report
        # current credit state. For tracking over time, the financial model
        # should snapshot credits periodically.
        if self._total_credits > 0:
            credits_used = self._total_credits - self._remaining_credits
            cost = (Decimal(str(credits_used)) * _CREDIT_COST).quantize(Decimal("0.01"))

            records.append(
                FinancialRecord(
                    record_date=end_date,
                    amount=-cost,
                    category=SpendCategory.SEARCH_DATA,
                    subcategory="Tavily Search Credits",
                    provider=Provider.TAVILY,
                    source="tavily_api",
                    raw_description=(
                        f"Tavily: {credits_used:,} credits used "
                        f"({self._remaining_credits:,} remaining)"
                    ),
                )
            )

        return records

    async def get_summary(self) -> dict:
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "total_credits": self._total_credits,
            "remaining_credits": self._remaining_credits,
            "credits_used": self._total_credits - self._remaining_credits,
            "cost_per_credit": str(_CREDIT_COST),
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Tavily cost data.

        Profile: Researcher plan, 3,000 searches/month at $0.008/credit = $24/month.
        Daily records with weekday/weekend variance.
        """
        rng = random.Random(903)
        records: list[FinancialRecord] = []

        daily_searches = 3000 / 30  # 100/day

        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            weekend_factor = 0.3 if is_weekend else 1.0

            searches = int(daily_searches * weekend_factor * rng.uniform(0.6, 1.4))
            cost = (Decimal(str(searches)) * _CREDIT_COST).quantize(Decimal("0.01"))

            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-cost,
                    category=SpendCategory.SEARCH_DATA,
                    subcategory="Tavily Search Credits",
                    provider=Provider.TAVILY,
                    source="synthetic",
                    raw_description=f"Synthetic Tavily: {searches} searches",
                )
            )

            current += timedelta(days=1)

        return records
