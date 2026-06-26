"""Cloudflare connector — fetches Workers, R2, and bandwidth usage costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_CF_API = "https://api.cloudflare.com/client/v4"

# Published Cloudflare pricing (as of early 2026)
_WORKERS_INCLUDED_REQUESTS = 10_000_000  # 10M requests/month on paid plan
_WORKERS_RATE = Decimal("0.30")  # per 1M requests after included
_R2_STORAGE_RATE = Decimal("0.015")  # per GB-month
_R2_CLASS_A_RATE = Decimal("4.50")  # per 1M Class A ops
_R2_CLASS_B_RATE = Decimal("0.36")  # per 1M Class B ops
_WORKERS_PAID_PLAN = Decimal("5.00")  # $5/month base


class CloudflareCostsConnector(BaseConnector):
    """Connector for Cloudflare Workers, R2, and bandwidth cost data."""

    provider = Provider.CLOUDFLARE

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_token: str = ""
        self._account_id: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Cloudflare...")
                await asyncio.sleep(1)
                print("Authenticated with Cloudflare API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Cloudflare token")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_token = credentials.get("api_token", "")
        if not api_token:
            logger.error("Missing Cloudflare api_token")
            return False

        self._api_token = api_token
        self._client = httpx.AsyncClient(
            base_url=_CF_API,
            headers={"Authorization": f"Bearer {self._api_token}"},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/user/tokens/verify")
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success"):
                logger.error("Cloudflare token verification failed")
                return False

            # Get account ID
            acct_resp = await self._client.get("/accounts", params={"per_page": 1})
            acct_resp.raise_for_status()
            accounts = acct_resp.json().get("result", [])
            if not accounts:
                logger.error("No Cloudflare accounts found")
                return False
            self._account_id = accounts[0]["id"]
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("Cloudflare API token invalid or expired")
            else:
                logger.error("Cloudflare validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Cloudflare connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Cloudflare connection error: %s", exc)
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

        # ── Workers analytics ───────────────────────────────────
        try:
            resp = await self._client.get(
                f"/accounts/{self._account_id}/workers/analytics/aggregate",
                params={
                    "since": start_date.isoformat(),
                    "until": end_date.isoformat(),
                },
            )
            resp.raise_for_status()
            data = resp.json()

            totals = data.get("result", {}).get("totals", {})
            requests = totals.get("requests", 0)
            overage = max(0, requests - _WORKERS_INCLUDED_REQUESTS)
            workers_cost = (
                _WORKERS_PAID_PLAN
                + Decimal(overage) / Decimal("1000000") * _WORKERS_RATE
            ).quantize(Decimal("0.01"))

            records.append(
                FinancialRecord(
                    record_date=end_date,
                    amount=-workers_cost,
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Cloudflare Workers",
                    provider=Provider.CLOUDFLARE,
                    source="cloudflare_analytics",
                    raw_description=f"Cloudflare Workers ({requests:,} requests)",
                )
            )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Cloudflare rate limit on Workers analytics")
            else:
                logger.error("Cloudflare Workers fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Cloudflare Workers fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Cloudflare Workers fetch error: %s", exc)

        # ── R2 storage ──────────────────────────────────────────
        try:
            resp = await self._client.get(
                f"/accounts/{self._account_id}/r2/buckets",
            )
            resp.raise_for_status()
            buckets = resp.json().get("result", {}).get("buckets", [])

            total_storage_gb = Decimal("0")
            for bucket in buckets:
                size_bytes = Decimal(str(bucket.get("size", 0)))
                total_storage_gb += size_bytes / Decimal("1073741824")

            r2_cost = (total_storage_gb * _R2_STORAGE_RATE).quantize(Decimal("0.01"))

            if r2_cost > 0:
                records.append(
                    FinancialRecord(
                        record_date=end_date,
                        amount=-r2_cost,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory="Cloudflare R2",
                        provider=Provider.CLOUDFLARE,
                        source="cloudflare_analytics",
                        raw_description=f"Cloudflare R2 storage ({total_storage_gb:.1f} GB)",
                    )
                )

        except httpx.HTTPStatusError as exc:
            logger.error("Cloudflare R2 fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Cloudflare R2 fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Cloudflare R2 fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(r.amount for r in records)
        by_service: dict[str, Decimal] = {}
        for r in records:
            svc = r.subcategory or "unknown"
            by_service[svc] = by_service.get(svc, Decimal("0")) + r.amount
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_service": {k: str(v) for k, v in by_service.items()},
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Cloudflare cost data.

        Profile: ~$5/month Workers, ~$3/month R2 storage, 1M requests/month.
        Generates monthly billing records.
        """
        rng = random.Random(501)
        records: list[FinancialRecord] = []

        current = start_date.replace(day=1)
        while current <= end_date:
            # Workers: $5 base + usage. 1M req/month is within 10M included.
            monthly_requests = int(1_000_000 * rng.uniform(0.8, 1.2))
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-_WORKERS_PAID_PLAN,
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Cloudflare Workers",
                    provider=Provider.CLOUDFLARE,
                    source="synthetic",
                    raw_description=f"Synthetic Cloudflare Workers ({monthly_requests:,} requests)",
                )
            )

            # R2: ~200GB stored at $0.015/GB = ~$3/month
            storage_gb = Decimal(str(round(200 * rng.uniform(0.85, 1.15), 1)))
            r2_cost = (storage_gb * _R2_STORAGE_RATE).quantize(Decimal("0.01"))
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-r2_cost,
                    category=SpendCategory.CLOUD_INFRASTRUCTURE,
                    subcategory="Cloudflare R2",
                    provider=Provider.CLOUDFLARE,
                    source="synthetic",
                    raw_description=f"Synthetic Cloudflare R2 ({storage_gb} GB)",
                )
            )

            current = (current + timedelta(days=32)).replace(day=1)

        return records
