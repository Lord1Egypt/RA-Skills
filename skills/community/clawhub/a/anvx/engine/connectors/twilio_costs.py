"""Twilio connector — fetches actual spend from the Usage Records API."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_TWILIO_API = "https://api.twilio.com/2010-04-01"


class TwilioCostsConnector(BaseConnector):
    """Connector for Twilio usage and cost data.

    Twilio's Usage Records API returns actual dollar amounts (Price field)
    broken down by category, making this one of the cleanest billing APIs.
    """

    provider = Provider.TWILIO

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._account_sid: str = ""
        self._auth_token: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Twilio...")
                await asyncio.sleep(1)
                print("Authenticated with Twilio API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Twilio credentials")
            return False

        # ── Normal mode ────────────────────────────────────────
        account_sid = credentials.get("account_sid", "")
        auth_token = credentials.get("auth_token", "")

        if not account_sid or not auth_token:
            logger.error("Missing Twilio account_sid or auth_token")
            return False

        self._account_sid = account_sid
        self._auth_token = auth_token
        self._client = httpx.AsyncClient(
            auth=(self._account_sid, self._auth_token),
            timeout=30.0,
        )

        try:
            resp = await self._client.get(
                f"{_TWILIO_API}/Accounts/{self._account_sid}.json"
            )
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("Twilio credentials invalid")
            else:
                logger.error("Twilio validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Twilio connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Twilio connection error: %s", exc)
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
                f"{_TWILIO_API}/Accounts/{self._account_sid}/Usage/Records/Daily.json",
                params={
                    "StartDate": start_date.isoformat(),
                    "EndDate": end_date.isoformat(),
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for record in data.get("usage_records", []):
                category = record.get("category", "unknown")
                price_str = record.get("price", "0")
                cost = Decimal(price_str).quantize(Decimal("0.01"))
                if cost == 0:
                    continue

                record_date = date.fromisoformat(record["start_date"])
                count = record.get("count", 0)
                count_unit = record.get("count_unit", "")

                records.append(
                    FinancialRecord(
                        record_date=record_date,
                        amount=-cost,
                        category=SpendCategory.COMMUNICATION,
                        subcategory=category,
                        provider=Provider.TWILIO,
                        source="twilio_usage_api",
                        raw_description=f"Twilio {category}: {count} {count_unit}",
                    )
                )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Twilio rate limit — returning partial results")
            else:
                logger.error("Twilio usage fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Twilio usage fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("Twilio usage fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(r.amount for r in records)
        by_category: dict[str, Decimal] = {}
        for r in records:
            cat = r.subcategory or "unknown"
            by_category[cat] = by_category.get(cat, Decimal("0")) + r.amount
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_category": {k: str(v) for k, v in by_category.items()},
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Twilio cost data.

        Profile: ~$45/month total
          - SMS: ~$30/month (600 messages at ~$0.05 avg)
          - Voice: ~$15/month (50 minutes at ~$0.30/min)
        Daily records with weekday/weekend variance.
        """
        rng = random.Random(601)

        sms_daily_cost = 30.0 / 30  # ~$1/day
        sms_daily_count = 20  # ~600/month
        voice_daily_cost = 15.0 / 30  # ~$0.50/day
        voice_daily_minutes = 50.0 / 30  # ~1.67 min/day

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            weekend_factor = 0.4 if is_weekend else 1.0

            # SMS
            sms_cost = sms_daily_cost * weekend_factor * rng.uniform(0.7, 1.3)
            sms_count = int(sms_daily_count * weekend_factor * rng.uniform(0.7, 1.3))
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-Decimal(str(round(sms_cost, 2))),
                    category=SpendCategory.COMMUNICATION,
                    subcategory="sms",
                    provider=Provider.TWILIO,
                    source="synthetic",
                    raw_description=f"Synthetic Twilio SMS: {sms_count} messages",
                )
            )

            # Voice
            voice_cost = voice_daily_cost * weekend_factor * rng.uniform(0.6, 1.4)
            voice_mins = round(voice_daily_minutes * weekend_factor * rng.uniform(0.6, 1.4), 1)
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-Decimal(str(round(voice_cost, 2))),
                    category=SpendCategory.COMMUNICATION,
                    subcategory="calls",
                    provider=Provider.TWILIO,
                    source="synthetic",
                    raw_description=f"Synthetic Twilio voice: {voice_mins} minutes",
                )
            )

            current += timedelta(days=1)

        return records
