"""Gemini billing connector — fetches token usage and costs from Google AI (Gemini) API."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

# Gemini model pricing (per 1M tokens, early 2026)
_MODEL_PRICING: dict[str, dict[str, Decimal]] = {
    "gemini-pro": {"input": Decimal("1.25"), "output": Decimal("5.00")},
    "gemini-flash": {"input": Decimal("0.075"), "output": Decimal("0.30")},
}

_GOOGLE_AI_API = "https://generativelanguage.googleapis.com/v1beta"


class GeminiBillingConnector(BaseConnector):
    """Connector for Gemini (Google AI) billing and usage data."""

    provider = Provider.GEMINI

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Google AI...")
                await asyncio.sleep(1)
                print("Authenticated with Google AI API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid Google AI API key")
            return False

        api_key = credentials.get("api_key", "")
        if not api_key:
            logger.error("Missing Google AI API key")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(timeout=30.0)

        try:
            resp = await self._client.get(
                f"{_GOOGLE_AI_API}/models",
                params={"key": self._api_key},
            )
            resp.raise_for_status()
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Google AI API key is invalid or insufficient permissions")
            else:
                logger.error("Google AI validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Google AI connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Google AI connection error: %s", exc)
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

        # Google AI doesn't have a public usage/billing API yet.
        # In production, this would query the Google Cloud billing export
        # or the AI Platform usage API when available.
        logger.info("Google AI usage API not yet available — returning empty")
        return []

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(r.amount for r in records)
        by_model: dict[str, Decimal] = {}
        for r in records:
            by_model[r.model or "unknown"] = by_model.get(r.model or "unknown", Decimal("0")) + r.amount
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_model": {k: str(v) for k, v in by_model.items()},
        }

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Google/Gemini billing data.

        Profile: ~$200/month total, growing ~5%/month
          - gemini-pro: ~$150/month (main model for complex tasks)
          - gemini-flash: ~$50/month (fast model for simple tasks)
        """
        rng = random.Random(2026)
        monthly_growth = 1.05

        model_daily: dict[str, float] = {
            "gemini-pro": 150.0 / 30,
            "gemini-flash": 50.0 / 30,
        }

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            is_weekend = current.weekday() >= 5
            weekend_factor = 0.6 if is_weekend else 1.0
            months_elapsed = (current - start_date).days / 30.0
            growth = Decimal(str(round(monthly_growth ** months_elapsed, 4)))

            for model_name, daily_target in model_daily.items():
                base = daily_target * weekend_factor
                cost = base * rng.uniform(0.8, 1.2)
                cost_dec = (Decimal(str(round(cost, 2))) * growth).quantize(Decimal("0.01"))

                pricing = _MODEL_PRICING[model_name]
                input_cost = cost_dec * Decimal("0.4")
                output_cost = cost_dec * Decimal("0.6")
                input_tokens = int(input_cost / pricing["input"] * 1_000_000) if pricing["input"] else 0
                output_tokens = int(output_cost / pricing["output"] * 1_000_000) if pricing["output"] else 0

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-cost_dec,
                        category=SpendCategory.AI_INFERENCE,
                        provider=Provider.GEMINI,
                        model=model_name,
                        tokens_input=input_tokens,
                        tokens_output=output_tokens,
                        source="synthetic",
                        raw_description=f"Synthetic Google {model_name} usage",
                    )
                )

            current += timedelta(days=1)

        return records
