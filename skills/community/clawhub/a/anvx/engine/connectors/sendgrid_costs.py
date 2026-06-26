"""SendGrid connector — fetches email volumes and calculates plan-based costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_SENDGRID_API = "https://api.sendgrid.com/v3"

# Published SendGrid plan pricing (as of early 2026)
_PLAN_PRICING: dict[str, dict[str, Any]] = {
    "free": {"monthly_cost": Decimal("0"), "emails_included": 100},
    "essentials": {"monthly_cost": Decimal("19.95"), "emails_included": 50_000},
    "pro": {"monthly_cost": Decimal("89.95"), "emails_included": 100_000},
    "premier": {"monthly_cost": Decimal("249.95"), "emails_included": 500_000},
}


class SendGridCostsConnector(BaseConnector):
    """Connector for SendGrid email cost data.

    SendGrid bills by plan tier, not per-email. This connector detects
    the plan from API responses and calculates the monthly cost.
    """

    provider = Provider.SENDGRID

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._plan: str = "free"
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to SendGrid...")
                await asyncio.sleep(1)
                print("Authenticated with SendGrid API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid SendGrid API key")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        if not api_key:
            logger.error("Missing SendGrid api_key")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_SENDGRID_API,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/user/account")
            resp.raise_for_status()
            account = resp.json()
            self._plan = account.get("type", "free").lower()
            if self._plan not in _PLAN_PRICING:
                self._plan = "free"
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("SendGrid API key invalid or insufficient permissions")
            else:
                logger.error("SendGrid validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("SendGrid connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("SendGrid connection error: %s", exc)
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
        plan_info = _PLAN_PRICING.get(self._plan, _PLAN_PRICING["free"])
        monthly_cost: Decimal = plan_info["monthly_cost"]

        # Fetch daily email stats for context
        try:
            resp = await self._client.get(
                "/stats",
                params={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "aggregated_by": "month",
                },
            )
            resp.raise_for_status()
            stats = resp.json()

            for month_stat in stats:
                stat_date = date.fromisoformat(month_stat["date"])
                metrics = month_stat.get("stats", [{}])[0].get("metrics", {})
                emails_sent = metrics.get("requests", 0)
                delivered = metrics.get("delivered", 0)
                opens = metrics.get("opens", 0)

                records.append(
                    FinancialRecord(
                        record_date=stat_date,
                        amount=-monthly_cost,
                        category=SpendCategory.COMMUNICATION,
                        subcategory=f"sendgrid_{self._plan}",
                        provider=Provider.SENDGRID,
                        source="sendgrid_stats_api",
                        raw_description=(
                            f"SendGrid {self._plan} plan: "
                            f"{emails_sent:,} sent, {delivered:,} delivered, "
                            f"{opens:,} opens"
                        ),
                    )
                )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("SendGrid rate limit — returning partial results")
            else:
                logger.error("SendGrid stats fetch failed: HTTP %s", exc.response.status_code)

            # Fallback: generate monthly cost records without stats
            records.extend(
                self._generate_monthly_cost_records(start_date, end_date, monthly_cost)
            )
        except httpx.TimeoutException:
            logger.error("SendGrid stats fetch timed out — using plan cost only")
            records.extend(
                self._generate_monthly_cost_records(start_date, end_date, monthly_cost)
            )
        except httpx.HTTPError as exc:
            logger.error("SendGrid stats fetch error: %s", exc)
            records.extend(
                self._generate_monthly_cost_records(start_date, end_date, monthly_cost)
            )

        return records

    async def get_summary(self) -> dict:
        plan_info = _PLAN_PRICING.get(self._plan, _PLAN_PRICING["free"])
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "plan": self._plan,
            "monthly_cost": str(plan_info["monthly_cost"]),
            "emails_included": plan_info["emails_included"],
        }

    def _generate_monthly_cost_records(
        self, start_date: date, end_date: date, monthly_cost: Decimal
    ) -> list[FinancialRecord]:
        """Generate one cost record per month when stats are unavailable."""
        records: list[FinancialRecord] = []
        current = start_date.replace(day=1)
        while current <= end_date:
            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-monthly_cost,
                    category=SpendCategory.COMMUNICATION,
                    subcategory=f"sendgrid_{self._plan}",
                    provider=Provider.SENDGRID,
                    source="sendgrid_plan_cost",
                    raw_description=f"SendGrid {self._plan} plan monthly cost",
                )
            )
            current = (current + timedelta(days=32)).replace(day=1)
        return records

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic SendGrid cost data.

        Profile: Pro plan at $89.95/month, sending ~50,000 emails/month.
        Monthly billing records with email volume stats.
        """
        rng = random.Random(701)
        records: list[FinancialRecord] = []
        monthly_cost = _PLAN_PRICING["pro"]["monthly_cost"]

        current = start_date.replace(day=1)
        while current <= end_date:
            emails_sent = int(50_000 * rng.uniform(0.8, 1.2))
            delivered = int(emails_sent * rng.uniform(0.96, 0.99))
            opens = int(delivered * rng.uniform(0.18, 0.28))

            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-monthly_cost,
                    category=SpendCategory.COMMUNICATION,
                    subcategory="sendgrid_pro",
                    provider=Provider.SENDGRID,
                    source="synthetic",
                    raw_description=(
                        f"Synthetic SendGrid Pro: "
                        f"{emails_sent:,} sent, {delivered:,} delivered, "
                        f"{opens:,} opens"
                    ),
                )
            )
            current = (current + timedelta(days=32)).replace(day=1)

        return records
