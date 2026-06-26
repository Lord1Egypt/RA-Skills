"""LangSmith connector — fetches trace/run counts and calculates costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_LANGSMITH_API = "https://api.smith.langchain.com"

# Published LangSmith pricing (as of early 2026)
_BASE_TRACE_RATE = Decimal("2.50")  # per 1K base traces
_EXTENDED_TRACE_RATE = Decimal("5.00")  # per 1K extended traces
_PLUS_SEAT_COST = Decimal("39.00")  # per seat/month
_INCLUDED_TRACES = 5000  # included in Plus plan per month


class LangSmithCostsConnector(BaseConnector):
    """Connector for LangSmith trace usage and cost data."""

    provider = Provider.LANGSMITH

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to LangSmith...")
                await asyncio.sleep(1)
                print("Authenticated with LangSmith API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid LangSmith API key")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        if not api_key:
            logger.error("Missing LangSmith api_key")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_LANGSMITH_API,
            headers={"x-api-key": self._api_key},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/api/v1/info")
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("LangSmith API key invalid or insufficient permissions")
            else:
                logger.error("LangSmith validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("LangSmith connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("LangSmith connection error: %s", exc)
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

        try:
            resp = await self._client.get(
                "/api/v1/usage",
                params={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for period in data.get("usage", []):
                period_date = date.fromisoformat(period["date"])
                base_traces = period.get("base_traces", 0)
                extended_traces = period.get("extended_traces", 0)
                seats = period.get("seats", 1)

                # Seat cost (prorated daily)
                seat_daily = (_PLUS_SEAT_COST * Decimal(seats) / Decimal("30")).quantize(Decimal("0.01"))
                if seat_daily > 0:
                    records.append(
                        FinancialRecord(
                            record_date=period_date,
                            amount=-seat_daily,
                            category=SpendCategory.MONITORING,
                            subcategory="LangSmith Plus Seats",
                            provider=Provider.LANGSMITH,
                            source="langsmith_usage_api",
                            raw_description=f"LangSmith Plus: {seats} seat(s)",
                        )
                    )

                # Base trace overage
                included_daily = _INCLUDED_TRACES / 30
                overage_base = max(0, base_traces - included_daily)
                base_cost = (Decimal(str(overage_base)) / Decimal("1000") * _BASE_TRACE_RATE).quantize(Decimal("0.01"))
                if base_cost > 0:
                    records.append(
                        FinancialRecord(
                            record_date=period_date,
                            amount=-base_cost,
                            category=SpendCategory.MONITORING,
                            subcategory="LangSmith Base Traces",
                            provider=Provider.LANGSMITH,
                            source="langsmith_usage_api",
                            raw_description=f"LangSmith base traces: {base_traces:,}",
                        )
                    )

                # Extended traces (all billable)
                ext_cost = (Decimal(str(extended_traces)) / Decimal("1000") * _EXTENDED_TRACE_RATE).quantize(Decimal("0.01"))
                if ext_cost > 0:
                    records.append(
                        FinancialRecord(
                            record_date=period_date,
                            amount=-ext_cost,
                            category=SpendCategory.MONITORING,
                            subcategory="LangSmith Extended Traces",
                            provider=Provider.LANGSMITH,
                            source="langsmith_usage_api",
                            raw_description=f"LangSmith extended traces: {extended_traces:,}",
                        )
                    )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("LangSmith rate limit — returning partial results")
            else:
                logger.error("LangSmith usage fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("LangSmith usage fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("LangSmith usage fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(r.amount for r in records)
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic LangSmith cost data.

        Profile: Plus plan 1 seat ($39/mo), 15,000 traces/month.
          - 5,000 included → 10,000 overage base traces at $2.50/1K = $25.
          - ~$39 + $25 = ~$64/month but daily proration and variance yield
            roughly $39 seat + ~$12.50 overage = ~$51.50/month.
        """
        rng = random.Random(901)
        records: list[FinancialRecord] = []

        daily_seat = (_PLUS_SEAT_COST / Decimal("30")).quantize(Decimal("0.01"))
        daily_traces_target = 15000 / 30  # 500/day
        daily_included = _INCLUDED_TRACES / 30  # ~167/day

        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            weekend_factor = 0.5 if is_weekend else 1.0

            # Seat cost (constant)
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-daily_seat,
                    category=SpendCategory.MONITORING,
                    subcategory="LangSmith Plus Seats",
                    provider=Provider.LANGSMITH,
                    source="synthetic",
                    raw_description="Synthetic LangSmith Plus: 1 seat",
                )
            )

            # Base traces with overage
            daily_traces = int(daily_traces_target * weekend_factor * rng.uniform(0.7, 1.3))
            overage = max(0, daily_traces - daily_included)
            if overage > 0:
                trace_cost = (Decimal(str(overage)) / Decimal("1000") * _BASE_TRACE_RATE).quantize(Decimal("0.01"))
                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-trace_cost,
                        category=SpendCategory.MONITORING,
                        subcategory="LangSmith Base Traces",
                        provider=Provider.LANGSMITH,
                        source="synthetic",
                        raw_description=f"Synthetic LangSmith traces: {daily_traces:,} ({overage:,} overage)",
                    )
                )

            current += timedelta(days=1)

        return records
