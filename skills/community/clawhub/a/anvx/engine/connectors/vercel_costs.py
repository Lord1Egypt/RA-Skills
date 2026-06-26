"""Vercel connector — fetches usage data and converts to costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_VERCEL_API = "https://api.vercel.com"

# Published Vercel pricing (Pro plan, as of early 2026)
_PRO_BASE = Decimal("20.00")  # $20/month base
_FUNCTION_INVOCATION_RATE = Decimal("0.60")  # per 1M invocations (first 1M included)
_BANDWIDTH_RATE = Decimal("0.15")  # per GB after 1TB included
_BUILD_MINUTE_RATE = Decimal("0.01")  # per minute after 6000 included
_INCLUDED_INVOCATIONS = 1_000_000
_INCLUDED_BANDWIDTH_GB = 1000
_INCLUDED_BUILD_MINUTES = 6000


class VercelCostsConnector(BaseConnector):
    """Connector for Vercel usage and cost data."""

    provider = Provider.VERCEL

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_token: str = ""
        self._team_id: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Vercel...")
                await asyncio.sleep(1)
                print("Authenticated with Vercel API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Vercel token")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_token = credentials.get("api_token", "")
        if not api_token:
            logger.error("Missing Vercel api_token")
            return False

        self._api_token = api_token
        self._client = httpx.AsyncClient(
            base_url=_VERCEL_API,
            headers={"Authorization": f"Bearer {self._api_token}"},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/v2/user")
            resp.raise_for_status()
            user_data = resp.json().get("user", {})
            self._team_id = user_data.get("defaultTeamId", "")
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("Vercel API token invalid or expired")
            else:
                logger.error("Vercel validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Vercel connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Vercel connection error: %s", exc)
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
            params: dict[str, Any] = {}
            if self._team_id:
                params["teamId"] = self._team_id

            # Fetch usage for the billing period
            resp = await self._client.get("/v1/usage", params=params)
            resp.raise_for_status()
            usage = resp.json()

            # Parse usage metrics and convert to costs
            period_date = end_date  # Usage is aggregated per billing period

            # Function invocations
            invocations = usage.get("functionInvocations", 0)
            overage_invocations = max(0, invocations - _INCLUDED_INVOCATIONS)
            invocation_cost = (
                Decimal(overage_invocations) / Decimal("1000000") * _FUNCTION_INVOCATION_RATE
            ).quantize(Decimal("0.01"))

            # Bandwidth
            bandwidth_gb = Decimal(str(usage.get("bandwidthGB", 0)))
            overage_bw = max(Decimal("0"), bandwidth_gb - _INCLUDED_BANDWIDTH_GB)
            bw_cost = (overage_bw * _BANDWIDTH_RATE).quantize(Decimal("0.01"))

            # Build minutes
            build_minutes = usage.get("buildMinutes", 0)
            overage_build = max(0, build_minutes - _INCLUDED_BUILD_MINUTES)
            build_cost = (Decimal(overage_build) * _BUILD_MINUTE_RATE).quantize(Decimal("0.01"))

            # Base Pro plan cost
            records.append(
                FinancialRecord(
                    record_date=period_date,
                    amount=-_PRO_BASE,
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Vercel Pro Plan",
                    provider=Provider.VERCEL,
                    source="vercel_usage_api",
                    raw_description="Vercel Pro plan base",
                )
            )

            if invocation_cost > 0:
                records.append(
                    FinancialRecord(
                        record_date=period_date,
                        amount=-invocation_cost,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory="Vercel Functions",
                        provider=Provider.VERCEL,
                        source="vercel_usage_api",
                        raw_description=f"Vercel function invocations ({invocations:,} total)",
                    )
                )

            if bw_cost > 0:
                records.append(
                    FinancialRecord(
                        record_date=period_date,
                        amount=-bw_cost,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory="Vercel Bandwidth",
                        provider=Provider.VERCEL,
                        source="vercel_usage_api",
                        raw_description=f"Vercel bandwidth ({bandwidth_gb} GB)",
                    )
                )

            if build_cost > 0:
                records.append(
                    FinancialRecord(
                        record_date=period_date,
                        amount=-build_cost,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory="Vercel Build",
                        provider=Provider.VERCEL,
                        source="vercel_usage_api",
                        raw_description=f"Vercel build minutes ({build_minutes:,} total)",
                    )
                )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Vercel rate limit — returning partial results")
            else:
                logger.error("Vercel usage fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Vercel usage fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("Vercel usage fetch error: %s", exc)

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
        """Generate realistic Vercel cost data.

        Profile: ~$20/month Pro plan, 5,000 function invocations/day,
        100GB bandwidth/month. All within included limits, so only base cost.
        Generates monthly billing records.
        """
        rng = random.Random(401)
        records: list[FinancialRecord] = []

        # Generate one billing record per month
        current = start_date.replace(day=1)
        while current <= end_date:
            month_end = (current + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            if month_end > end_date:
                month_end = end_date

            # Pro plan base
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-_PRO_BASE,
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Vercel Pro Plan",
                    provider=Provider.VERCEL,
                    source="synthetic",
                    raw_description="Synthetic Vercel Pro plan",
                )
            )

            # Function invocations: ~5,000/day = ~150,000/month (within 1M included)
            days_in_month = (month_end - current).days + 1
            invocations = int(5000 * days_in_month * rng.uniform(0.8, 1.2))
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=Decimal("0"),  # within included tier
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Vercel Functions",
                    provider=Provider.VERCEL,
                    source="synthetic",
                    raw_description=f"Synthetic Vercel functions ({invocations:,} invocations, within included)",
                )
            )

            # Bandwidth: ~100GB/month (within 1TB included)
            bandwidth_gb = round(100 * rng.uniform(0.8, 1.2), 1)
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=Decimal("0"),  # within included tier
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Vercel Bandwidth",
                    provider=Provider.VERCEL,
                    source="synthetic",
                    raw_description=f"Synthetic Vercel bandwidth ({bandwidth_gb} GB, within included)",
                )
            )

            # Next month
            current = (current + timedelta(days=32)).replace(day=1)

        return records
