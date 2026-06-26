"""Meta (Facebook/Instagram) Ads connector — fetches ad spend from Meta Marketing API."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_META_GRAPH_API = "https://graph.facebook.com/v21.0"


class MetaAdsConnector(BaseConnector):
    """Connector for Meta (Facebook/Instagram) advertising spend data."""

    provider = Provider.META

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._access_token: str = ""
        self._ad_account_id: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Meta Ads...")
                await asyncio.sleep(1)
                print("Authenticated with Meta Marketing API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid Meta access token or ad account ID")
            return False

        access_token = credentials.get("access_token", "")
        ad_account_id = credentials.get("ad_account_id", "")
        if not access_token or not ad_account_id:
            logger.error("Missing Meta access_token or ad_account_id")
            return False

        self._access_token = access_token
        self._ad_account_id = ad_account_id
        self._client = httpx.AsyncClient(timeout=30.0)

        try:
            resp = await self._client.get(
                f"{_META_GRAPH_API}/{self._ad_account_id}",
                params={
                    "access_token": self._access_token,
                    "fields": "name,account_status",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("account_status") not in (1, 2):  # 1=active, 2=disabled
                logger.error("Meta ad account is not active (status: %s)", data.get("account_status"))
                return False
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Meta access token invalid or expired")
            else:
                logger.error("Meta validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Meta connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Meta connection error: %s", exc)
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
                f"{_META_GRAPH_API}/{self._ad_account_id}/insights",
                params={
                    "access_token": self._access_token,
                    "time_range": f'{{"since":"{start_date.isoformat()}","until":"{end_date.isoformat()}"}}',
                    "time_increment": 1,  # daily
                    "fields": "spend,campaign_name,impressions,clicks",
                    "level": "campaign",
                    "limit": 500,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for entry in data.get("data", []):
                spend = Decimal(entry.get("spend", "0"))
                if spend <= 0:
                    continue
                campaign = entry.get("campaign_name", "Unknown Campaign")
                entry_date = date.fromisoformat(entry.get("date_start", start_date.isoformat()))

                # Determine platform from campaign name heuristic
                subcategory = "facebook_ads"
                if any(kw in campaign.lower() for kw in ("instagram", "ig_", "reels")):
                    subcategory = "instagram_ads"

                records.append(
                    FinancialRecord(
                        record_date=entry_date,
                        amount=-spend.quantize(Decimal("0.01")),
                        category=SpendCategory.ADVERTISING,
                        subcategory=subcategory,
                        provider=Provider.META,
                        source="meta_marketing_api",
                        raw_description=f"Meta Ads: {campaign} — {entry.get('impressions', 0):,} impressions",
                    )
                )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Meta API rate limit — returning partial results")
            else:
                logger.error("Meta insights fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Meta insights fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Meta insights fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(abs(r.amount) for r in records)
        by_platform: dict[str, Decimal] = {}
        for r in records:
            key = r.subcategory or "unknown"
            by_platform[key] = by_platform.get(key, Decimal("0")) + abs(r.amount)
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_platform": {k: str(v) for k, v in by_platform.items()},
        }

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Meta Ads spend data.

        Profile: ~$800/month total
          - Facebook Ads: ~$600/month across 3 campaigns
          - Instagram Ads: ~$200/month across 2 campaigns
        Daily variance, one 2x spike week (campaign push), weekend dip.
        """
        rng = random.Random(7777)

        campaigns = [
            ("FB — Lead Gen US", "facebook_ads", 250.0 / 30),
            ("FB — Retargeting", "facebook_ads", 200.0 / 30),
            ("FB — Brand Awareness", "facebook_ads", 150.0 / 30),
            ("IG — Stories Promo", "instagram_ads", 120.0 / 30),
            ("IG — Reels Engagement", "instagram_ads", 80.0 / 30),
        ]

        total_days = (end_date - start_date).days
        spike_start = start_date + timedelta(days=max(20, total_days // 3))
        spike_end = spike_start + timedelta(days=7)

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            is_spike = spike_start <= current < spike_end

            for campaign_name, platform, daily_target in campaigns:
                base = daily_target * (0.65 if is_weekend else 1.0)
                if is_spike:
                    base *= 2.0
                cost = base * rng.uniform(0.75, 1.25)
                cost_dec = Decimal(str(round(cost, 2)))

                impressions = int(cost * rng.uniform(800, 1200))
                clicks = int(impressions * rng.uniform(0.01, 0.04))

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-cost_dec,
                        category=SpendCategory.ADVERTISING,
                        subcategory=platform,
                        provider=Provider.META,
                        source="synthetic",
                        raw_description=(
                            f"Synthetic Meta Ads: {campaign_name} — "
                            f"{impressions:,} impressions, {clicks:,} clicks"
                        ),
                    )
                )

            current += timedelta(days=1)

        return records
