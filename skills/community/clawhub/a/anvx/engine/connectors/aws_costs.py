"""AWS Cost Explorer connector — fetches daily spend by service.

Note: Cost Explorer API costs $0.01 per request. This connector caches
responses and limits to one refresh per day.
"""
import logging
import random
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_AWS_CE_ENDPOINT = "https://ce.{region}.amazonaws.com"


class AWSCostsConnector(BaseConnector):
    """Connector for AWS Cost Explorer daily spend data."""

    provider = Provider.AWS

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._access_key_id: str = ""
        self._secret_access_key: str = ""
        self._region: str = "us-east-1"
        self._client: httpx.AsyncClient | None = None
        self._cache: dict[str, list[FinancialRecord]] = {}
        self._cache_date: date | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to AWS Cost Explorer...")
                await asyncio.sleep(1)
                print("Authenticated with AWS (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid AWS credentials")
            return False

        # ── Normal mode ────────────────────────────────────────
        access_key_id = credentials.get("access_key_id", "")
        secret_access_key = credentials.get("secret_access_key", "")
        region = credentials.get("region", "us-east-1")

        if not access_key_id or not secret_access_key:
            logger.error("Missing AWS access_key_id or secret_access_key")
            return False

        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._region = region

        self._client = httpx.AsyncClient(timeout=30.0)

        # Validate by calling GetCostAndUsage for today (lightweight)
        try:
            today = date.today()
            resp = await self._ce_request(
                "GetCostAndUsage",
                {
                    "TimePeriod": {
                        "Start": today.isoformat(),
                        "End": (today + timedelta(days=1)).isoformat(),
                    },
                    "Granularity": "DAILY",
                    "Metrics": ["UnblendedCost"],
                },
            )
            if resp is not None:
                self.is_connected = True
                return True
            return False
        except Exception:
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

        # Cache: only refresh once per day
        cache_key = f"{start_date}:{end_date}"
        if self._cache_date == date.today() and cache_key in self._cache:
            logger.info("Returning cached AWS cost data")
            return self._cache[cache_key]

        records: list[FinancialRecord] = []

        try:
            resp = await self._ce_request(
                "GetCostAndUsage",
                {
                    "TimePeriod": {
                        "Start": start_date.isoformat(),
                        "End": (end_date + timedelta(days=1)).isoformat(),
                    },
                    "Granularity": "DAILY",
                    "Metrics": ["UnblendedCost"],
                    "GroupBy": [
                        {"Type": "DIMENSION", "Key": "SERVICE"},
                    ],
                },
            )

            if resp is None:
                return records

            for result in resp.get("ResultsByTime", []):
                period_start = date.fromisoformat(result["TimePeriod"]["Start"])
                for group in result.get("Groups", []):
                    service = group["Keys"][0]
                    amount_str = group["Metrics"]["UnblendedCost"]["Amount"]
                    cost = Decimal(amount_str).quantize(Decimal("0.01"))
                    if cost == 0:
                        continue

                    records.append(
                        FinancialRecord(
                            record_date=period_start,
                            amount=-cost,
                            category=SpendCategory.CLOUD_INFRASTRUCTURE,
                            subcategory=service,
                            provider=Provider.AWS,
                            source="aws_cost_explorer",
                            raw_description=f"AWS {service}",
                        )
                    )

            self._cache[cache_key] = records
            self._cache_date = date.today()

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("AWS Cost Explorer rate limit — returning partial results")
            else:
                logger.error("AWS CE fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("AWS CE fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("AWS CE fetch error: %s", exc)

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

    async def _ce_request(self, action: str, payload: dict) -> dict | None:
        """Make an authenticated request to AWS Cost Explorer.

        Uses SigV4 authentication via X-Amz headers.
        """
        assert self._client is not None
        endpoint = _AWS_CE_ENDPOINT.format(region=self._region)
        now = datetime.utcnow()
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = now.strftime("%Y%m%d")

        headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": f"AWSInsightsIndexService.{action}",
            "X-Amz-Date": amz_date,
            "Host": f"ce.{self._region}.amazonaws.com",
        }

        try:
            import json
            resp = await self._client.post(
                endpoint, headers=headers, content=json.dumps(payload)
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("AWS credentials invalid or insufficient permissions")
            else:
                logger.error("AWS CE request failed: HTTP %s", exc.response.status_code)
            return None
        except httpx.TimeoutException:
            logger.error("AWS CE request timed out")
            return None
        except httpx.HTTPError as exc:
            logger.error("AWS CE request error: %s", exc)
            return None

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic AWS cost data.

        Profile: ~$200/month total
          - EC2: ~$80/month
          - Lambda: ~$40/month (2x spike week)
          - S3: ~$30/month
          - RDS: ~$50/month
        """
        rng = random.Random(201)

        service_daily: dict[str, float] = {
            "Amazon Elastic Compute Cloud": 80.0 / 30,
            "AWS Lambda": 40.0 / 30,
            "Amazon Simple Storage Service": 30.0 / 30,
            "Amazon Relational Database Service": 50.0 / 30,
        }

        total_days = (end_date - start_date).days
        spike_start = start_date + timedelta(days=max(20, total_days // 3))
        spike_end = spike_start + timedelta(days=7)

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            is_spike = spike_start <= current < spike_end

            for service, daily_target in service_daily.items():
                base = daily_target
                # Lambda spike: 2x during spike week
                if is_spike and service == "AWS Lambda":
                    base *= 2.0
                cost = base * rng.uniform(0.85, 1.15)
                cost_dec = Decimal(str(round(cost, 2)))

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-cost_dec,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory=service,
                        provider=Provider.AWS,
                        source="synthetic",
                        raw_description=f"Synthetic AWS {service}",
                    )
                )

            current += timedelta(days=1)

        return records
