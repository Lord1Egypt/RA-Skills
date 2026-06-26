"""Stripe connector — fetches charges, subscriptions, payouts, and fees."""
import logging
import random
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_STRIPE_API_BASE = "https://api.stripe.com/v1"


class StripeConnector(BaseConnector):
    """Connector for Stripe billing data (revenue, fees, payouts)."""

    provider = Provider.STRIPE

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
                print("Connecting to Stripe...")
                await asyncio.sleep(1)
                print("Authenticated with Stripe API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid API key format")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        if not api_key or not api_key.startswith("sk_"):
            logger.error("Invalid Stripe API key format")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_STRIPE_API_BASE,
            auth=(self._api_key, ""),
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/balance")
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("Stripe API key is invalid or expired")
            else:
                logger.error("Stripe validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Stripe connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Stripe connection error: %s", exc)
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
        start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
        end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp())

        # ── Charges (revenue) ───────────────────────────────────
        try:
            has_more = True
            starting_after: str | None = None
            while has_more:
                params: dict[str, Any] = {
                    "created[gte]": start_ts,
                    "created[lte]": end_ts,
                    "limit": 100,
                }
                if starting_after:
                    params["starting_after"] = starting_after

                resp = await self._client.get("/charges", params=params)
                resp.raise_for_status()
                data = resp.json()

                for charge in data.get("data", []):
                    if charge.get("status") != "succeeded":
                        continue
                    charge_date = date.fromtimestamp(charge["created"])
                    amount_usd = Decimal(str(charge["amount"])) / Decimal("100")
                    fee_usd = Decimal("0")
                    if charge.get("balance_transaction") and isinstance(charge["balance_transaction"], dict):
                        fee_usd = Decimal(str(charge["balance_transaction"].get("fee", 0))) / Decimal("100")

                    # Revenue record
                    records.append(
                        FinancialRecord(
                            record_date=charge_date,
                            amount=amount_usd.quantize(Decimal("0.01")),
                            category=SpendCategory.REVENUE,
                            provider=Provider.STRIPE,
                            source="stripe_charges",
                            raw_description=charge.get("description", "Stripe charge"),
                        )
                    )
                    # Fee record
                    if fee_usd > 0:
                        records.append(
                            FinancialRecord(
                                record_date=charge_date,
                                amount=-fee_usd.quantize(Decimal("0.01")),
                                category=SpendCategory.PAYMENT_PROCESSING,
                                provider=Provider.STRIPE,
                                source="stripe_charges",
                                raw_description="Stripe processing fee",
                            )
                        )

                has_more = data.get("has_more", False)
                if has_more and data["data"]:
                    starting_after = data["data"][-1]["id"]

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Stripe rate limit hit on charges — returning partial results")
            else:
                logger.error("Stripe charges fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Stripe charges fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("Stripe charges fetch error: %s", exc)

        # ── Payouts ─────────────────────────────────────────────
        try:
            resp = await self._client.get(
                "/payouts",
                params={
                    "created[gte]": start_ts,
                    "created[lte]": end_ts,
                    "limit": 100,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for payout in data.get("data", []):
                if payout.get("status") != "paid":
                    continue
                payout_date = date.fromtimestamp(payout["created"])
                amount_usd = Decimal(str(payout["amount"])) / Decimal("100")
                records.append(
                    FinancialRecord(
                        record_date=payout_date,
                        amount=-amount_usd.quantize(Decimal("0.01")),
                        category=SpendCategory.OTHER,
                        subcategory="payout",
                        provider=Provider.STRIPE,
                        source="stripe_payouts",
                        raw_description="Stripe payout to bank",
                    )
                )

        except httpx.HTTPStatusError as exc:
            logger.error("Stripe payouts fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Stripe payouts fetch timed out")
        except httpx.HTTPError as exc:
            logger.error("Stripe payouts fetch error: %s", exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        revenue = sum(r.amount for r in records if r.amount > 0)
        fees = sum(r.amount for r in records if r.category == SpendCategory.PAYMENT_PROCESSING)
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_revenue": str(revenue),
            "current_month_fees": str(fees),
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Stripe data.

        Profile (month 0 = start_date's month):
          - ~$1,800/month subscription revenue, growing 5% MoM
          - ~$120/month in Stripe fees (≈2.9% + $0.30 per charge)
          - Daily charges with realistic variance
        """
        rng = random.Random(77)
        records: list[FinancialRecord] = []

        # Base monthly values at start_date
        base_monthly_revenue = 1800.0
        fee_rate = Decimal("0.029")
        per_charge_fee = Decimal("0.30")
        avg_charges_per_day = 3  # ~90 charges/month

        current = start_date
        ref_month = start_date.month + (start_date.year * 12)

        while current <= end_date:
            # Compute month offset for 5% MoM growth
            cur_month = current.month + (current.year * 12)
            months_elapsed = cur_month - ref_month
            growth_factor = 1.05 ** months_elapsed
            daily_revenue_target = (base_monthly_revenue * growth_factor) / 30

            is_weekend = current.weekday() >= 5
            day_multiplier = 0.7 if is_weekend else 1.0

            # Generate a few charges per day
            n_charges = rng.randint(
                max(1, avg_charges_per_day - 1),
                avg_charges_per_day + 2,
            )
            day_total_revenue = daily_revenue_target * day_multiplier * rng.uniform(0.8, 1.2)
            charge_amounts = _split_amount(day_total_revenue, n_charges, rng)

            for charge_amount in charge_amounts:
                amount_dec = Decimal(str(round(charge_amount, 2)))
                if amount_dec <= 0:
                    continue
                # Revenue
                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=amount_dec,
                        category=SpendCategory.REVENUE,
                        subcategory="subscription",
                        provider=Provider.STRIPE,
                        source="synthetic",
                        raw_description="Synthetic Stripe subscription charge",
                    )
                )
                # Fee: 2.9% + $0.30
                fee = (amount_dec * fee_rate + per_charge_fee).quantize(Decimal("0.01"))
                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-fee,
                        category=SpendCategory.PAYMENT_PROCESSING,
                        provider=Provider.STRIPE,
                        source="synthetic",
                        raw_description="Synthetic Stripe processing fee",
                    )
                )

            current += timedelta(days=1)

        return records


def _split_amount(total: float, n: int, rng: random.Random) -> list[float]:
    """Split a total amount into n roughly-equal random pieces."""
    if n <= 0:
        return []
    weights = [rng.random() for _ in range(n)]
    weight_sum = sum(weights)
    return [total * w / weight_sum for w in weights]
