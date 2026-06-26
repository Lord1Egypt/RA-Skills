"""Datadog connector — fetches usage metering data and calculates costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_DATADOG_API = "https://api.datadoghq.com"

# Published Datadog pricing (Pro plan, as of early 2026)
_PRICING: dict[str, dict[str, Any]] = {
    "infra_hosts": {
        "label": "Infrastructure Hosts",
        "rate": Decimal("15.00"),  # per host/month
        "unit": "hosts",
    },
    "logs_ingested_gb": {
        "label": "Log Management",
        "rate": Decimal("3.00"),  # per GB ingested/month (after 1st GB)
        "unit": "GB",
    },
    "apm_hosts": {
        "label": "APM Hosts",
        "rate": Decimal("8.00"),  # per host/month (Pro)
        "unit": "hosts",
    },
}


class DatadogCostsConnector(BaseConnector):
    """Connector for Datadog usage metering and cost data.

    Requires Pro or Enterprise plan for usage metering API access.
    """

    provider = Provider.DATADOG

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._app_key: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Datadog...")
                await asyncio.sleep(1)
                print("Authenticated with Datadog API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Datadog credentials")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        app_key = credentials.get("app_key", "")

        if not api_key or not app_key:
            logger.error("Missing Datadog api_key or app_key")
            return False

        self._api_key = api_key
        self._app_key = app_key
        self._client = httpx.AsyncClient(
            base_url=_DATADOG_API,
            headers={
                "DD-API-KEY": self._api_key,
                "DD-APPLICATION-KEY": self._app_key,
            },
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/api/v1/validate")
            resp.raise_for_status()
            data = resp.json()
            if not data.get("valid"):
                logger.error("Datadog API key validation returned invalid")
                return False
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Datadog API credentials invalid or insufficient permissions")
            else:
                logger.error("Datadog validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Datadog connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Datadog connection error: %s", exc)
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

        # ── Infrastructure hosts ────────────────────────────────
        records.extend(
            await self._fetch_product_usage(
                product_key="infra_hosts",
                endpoint="/api/v2/usage/hosts",
                extract_usage=lambda data: _extract_daily_max(data, "host_count"),
                start_date=start_date,
                end_date=end_date,
            )
        )

        # ── Logs ingested ───────────────────────────────────────
        records.extend(
            await self._fetch_product_usage(
                product_key="logs_ingested_gb",
                endpoint="/api/v2/usage/logs",
                extract_usage=lambda data: _extract_daily_sum(data, "ingested_bytes", scale=1 / 1_073_741_824),
                start_date=start_date,
                end_date=end_date,
            )
        )

        # ── APM hosts ──────────────────────────────────────────
        records.extend(
            await self._fetch_product_usage(
                product_key="apm_hosts",
                endpoint="/api/v2/usage/apm",
                extract_usage=lambda data: _extract_daily_max(data, "apm_host_count"),
                start_date=start_date,
                end_date=end_date,
            )
        )

        return records

    async def _fetch_product_usage(
        self,
        product_key: str,
        endpoint: str,
        extract_usage: Any,
        start_date: date,
        end_date: date,
    ) -> list[FinancialRecord]:
        """Fetch usage for a single Datadog product and calculate cost."""
        assert self._client is not None
        pricing = _PRICING[product_key]
        records: list[FinancialRecord] = []

        try:
            resp = await self._client.get(
                endpoint,
                params={
                    "start_hr": f"{start_date.isoformat()}T00",
                    "end_hr": f"{end_date.isoformat()}T23",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            daily_usage = extract_usage(data)
            for usage_date, quantity in daily_usage.items():
                if quantity <= 0:
                    continue
                # Prorate monthly rate to daily
                daily_cost = (
                    pricing["rate"] * Decimal(str(quantity)) / Decimal("30")
                ).quantize(Decimal("0.01"))

                records.append(
                    FinancialRecord(
                        record_date=usage_date,
                        amount=-daily_cost,
                        category=SpendCategory.MONITORING,
                        subcategory=pricing["label"],
                        provider=Provider.DATADOG,
                        source="datadog_usage_api",
                        raw_description=(
                            f"Datadog {pricing['label']}: "
                            f"{quantity} {pricing['unit']}"
                        ),
                    )
                )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("Datadog rate limit on %s — returning partial results", product_key)
            elif exc.response.status_code == 403:
                logger.warning("Datadog %s requires Pro/Enterprise plan", product_key)
            else:
                logger.error("Datadog %s fetch failed: HTTP %s", product_key, exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("Datadog %s fetch timed out", product_key)
        except httpx.HTTPError as exc:
            logger.error("Datadog %s fetch error: %s", product_key, exc)

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        month_start = today.replace(day=1)
        records = await self.fetch_records(month_start, today)
        total = sum(r.amount for r in records)
        by_product: dict[str, Decimal] = {}
        for r in records:
            product = r.subcategory or "unknown"
            by_product[product] = by_product.get(product, Decimal("0")) + r.amount
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "current_month_spend": str(total),
            "spend_by_product": {k: str(v) for k, v in by_product.items()},
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Datadog cost data.

        Profile: ~$75/month total
          - Infrastructure: 3 hosts × $15 = $45/month
          - Logs: 5 GB × $3 = $15/month
          - APM: 2 hosts × $8 = $16/month (rounds to ~$75 with variance)
        Daily records prorated from monthly rates.
        """
        rng = random.Random(801)

        # Daily prorated costs
        products: dict[str, dict[str, Any]] = {
            "Infrastructure Hosts": {
                "base_quantity": 3.0,
                "rate": Decimal("15.00"),
                "unit": "hosts",
            },
            "Log Management": {
                "base_quantity": 5.0,
                "rate": Decimal("3.00"),
                "unit": "GB",
            },
            "APM Hosts": {
                "base_quantity": 2.0,
                "rate": Decimal("8.00"),
                "unit": "hosts",
            },
        }

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            for label, info in products.items():
                # Hosts are stable; logs vary more
                if info["unit"] == "GB":
                    quantity = info["base_quantity"] * rng.uniform(0.6, 1.4)
                else:
                    quantity = info["base_quantity"]

                daily_cost = (
                    info["rate"] * Decimal(str(round(quantity, 2))) / Decimal("30")
                ).quantize(Decimal("0.01"))

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-daily_cost,
                        category=SpendCategory.MONITORING,
                        subcategory=label,
                        provider=Provider.DATADOG,
                        source="synthetic",
                        raw_description=(
                            f"Synthetic Datadog {label}: "
                            f"{round(quantity, 1)} {info['unit']}"
                        ),
                    )
                )

            current += timedelta(days=1)

        return records


def _extract_daily_max(data: dict, count_key: str) -> dict[date, float]:
    """Extract daily max values from Datadog usage response."""
    result: dict[date, float] = {}
    for entry in data.get("data", []):
        attrs = entry.get("attributes", {})
        hour_str = attrs.get("hour", "")
        if not hour_str:
            continue
        entry_date = date.fromisoformat(hour_str[:10])
        value = float(attrs.get(count_key, 0))
        result[entry_date] = max(result.get(entry_date, 0), value)
    return result


def _extract_daily_sum(
    data: dict, sum_key: str, scale: float = 1.0
) -> dict[date, float]:
    """Extract daily summed values from Datadog usage response."""
    result: dict[date, float] = {}
    for entry in data.get("data", []):
        attrs = entry.get("attributes", {})
        hour_str = attrs.get("hour", "")
        if not hour_str:
            continue
        entry_date = date.fromisoformat(hour_str[:10])
        value = float(attrs.get(sum_key, 0)) * scale
        result[entry_date] = result.get(entry_date, 0) + value
    return result
