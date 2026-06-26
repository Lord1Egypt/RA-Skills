"""Google Ads connector — fetches ad spend from Google Ads API."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_GOOGLE_ADS_API = "https://googleads.googleapis.com/v18"


class GoogleAdsConnector(BaseConnector):
    """Connector for Google Ads (Search, Display, YouTube) spend data."""

    provider = Provider.GOOGLE_ADS

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._developer_token: str = ""
        self._customer_id: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Google Ads...")
                await asyncio.sleep(1)
                print("Authenticated with Google Ads API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid Google Ads credentials")
            return False

        developer_token = credentials.get("developer_token", "")
        customer_id = credentials.get("customer_id", "")
        if not developer_token or not customer_id:
            logger.error("Missing Google Ads developer_token or customer_id")
            return False

        self._developer_token = developer_token
        self._customer_id = customer_id.replace("-", "")
        self._client = httpx.AsyncClient(
            headers={
                "developer-token": self._developer_token,
                "login-customer-id": self._customer_id,
            },
            timeout=30.0,
        )

        try:
            resp = await self._client.get(
                f"{_GOOGLE_ADS_API}/customers/{self._customer_id}",
            )
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Google Ads credentials invalid or insufficient permissions")
            else:
                logger.error("Google Ads validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Google Ads connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Google Ads connection error: %s", exc)
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
            query = (
                "SELECT campaign.name, segments.date, "
                "metrics.cost_micros, metrics.impressions, metrics.clicks, "
                "campaign.advertising_channel_type "
                f"FROM campaign WHERE segments.date BETWEEN "
                f"'{start_date.isoformat()}' AND '{end_date.isoformat()}'"
            )
            resp = await self._client.post(
                f"{_GOOGLE_ADS_API}/customers/{self._customer_id}/googleAds:searchStream",
                json={"query": query},
            )
            resp.raise_for_status()

            for batch in resp.json():
                for row in batch.get("results", []):
                    campaign_name = row.get("campaign", {}).get("name", "Unknown")
                    cost_micros = int(row.get("metrics", {}).get("costMicros", 0))
                    cost_usd = Decimal(str(cost_micros)) / Decimal("1000000")
                    if cost_usd <= 0:
                        continue
                    row_date = date.fromisoformat(row.get("segments", {}).get("date", ""))
                    channel = row.get("campaign", {}).get("advertisingChannelType", "SEARCH")

                    subcategory = {
                        "SEARCH": "google_search",
                        "DISPLAY": "google_display",
                        "VIDEO": "google_youtube",
                    }.get(channel, "google_other")

                    records.append(FinancialRecord(
                        record_date=row_date,
                        amount=-cost_usd.quantize(Decimal("0.01")),
                        category=SpendCategory.ADVERTISING,
                        subcategory=subcategory,
                        provider=Provider.GOOGLE_ADS,
                        source="google_ads_api",
                        raw_description=f"Google Ads: {campaign_name}",
                    ))

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Google Ads rate limit — returning partial results")
            else:
                logger.error("Google Ads fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Google Ads fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Google Ads fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(abs(r.amount) for r in records)
        by_channel: dict[str, Decimal] = {}
        for r in records:
            key = r.subcategory or "unknown"
            by_channel[key] = by_channel.get(key, Decimal("0")) + abs(r.amount)
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_channel": {k: str(v) for k, v in by_channel.items()},
        }

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Google Ads spend data.

        Profile: ~$1,200/month total
          - Search campaigns: ~$700/month
          - Display campaigns: ~$300/month
          - YouTube campaigns: ~$200/month
        Daily variance, weekend dip, one spike week.
        """
        rng = random.Random(8888)

        campaigns = [
            ("Search — Brand Terms", "google_search", 300.0 / 30),
            ("Search — Competitor", "google_search", 250.0 / 30),
            ("Search — Long Tail", "google_search", 150.0 / 30),
            ("Display — Retargeting", "google_display", 200.0 / 30),
            ("Display — Prospecting", "google_display", 100.0 / 30),
            ("YouTube — Pre-roll", "google_youtube", 120.0 / 30),
            ("YouTube — Discovery", "google_youtube", 80.0 / 30),
        ]

        total_days = (end_date - start_date).days
        spike_start = start_date + timedelta(days=max(25, total_days // 2))
        spike_end = spike_start + timedelta(days=7)

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            is_spike = spike_start <= current < spike_end

            for campaign_name, channel, daily_target in campaigns:
                base = daily_target * (0.55 if is_weekend else 1.0)
                if is_spike:
                    base *= 1.8
                cost = base * rng.uniform(0.8, 1.2)
                cost_dec = Decimal(str(round(cost, 2)))

                impressions = int(cost * rng.uniform(600, 1100))
                clicks = int(impressions * rng.uniform(0.02, 0.06))

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-cost_dec,
                        category=SpendCategory.ADVERTISING,
                        subcategory=channel,
                        provider=Provider.GOOGLE_ADS,
                        source="synthetic",
                        raw_description=(
                            f"Synthetic Google Ads: {campaign_name} — "
                            f"{impressions:,} impressions, {clicks:,} clicks"
                        ),
                    )
                )

            current += timedelta(days=1)

        return records
