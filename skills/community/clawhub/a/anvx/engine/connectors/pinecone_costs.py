"""Pinecone connector — fetches index stats and calculates serverless costs."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_PINECONE_API = "https://api.pinecone.io"

# Published Pinecone Serverless pricing (as of early 2026)
_QUERY_RATE = Decimal("0.002")  # per 1K read units (queries)
_STORAGE_RATE = Decimal("0.33")  # per GB-month
_WRITE_RATE = Decimal("0.002")  # per 1K write units


class PineconeCostsConnector(BaseConnector):
    """Connector for Pinecone serverless index usage and cost data."""

    provider = Provider.PINECONE

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._api_key: str = ""
        self._client: httpx.AsyncClient | None = None
        self._indexes: list[dict] = []

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to Pinecone...")
                await asyncio.sleep(1)
                print("Authenticated with Pinecone API (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Authentication failed — invalid Pinecone API key")
            return False

        # ── Normal mode ────────────────────────────────────────
        api_key = credentials.get("api_key", "")
        if not api_key:
            logger.error("Missing Pinecone api_key")
            return False

        self._api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=_PINECONE_API,
            headers={"Api-Key": self._api_key},
            timeout=30.0,
        )

        try:
            resp = await self._client.get("/indexes")
            resp.raise_for_status()
            self._indexes = resp.json().get("indexes", [])
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("Pinecone API key invalid or insufficient permissions")
            else:
                logger.error("Pinecone validation failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("Pinecone connection timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("Pinecone connection error: %s", exc)
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

        for index_info in self._indexes:
            index_name = index_info.get("name", "unknown")
            host = index_info.get("host", "")
            if not host:
                continue

            try:
                # Fetch index stats
                index_client = httpx.AsyncClient(
                    base_url=f"https://{host}",
                    headers={"Api-Key": self._api_key},
                    timeout=30.0,
                )
                resp = await index_client.get("/describe_index_stats")
                resp.raise_for_status()
                stats = resp.json()
                await index_client.aclose()

                vector_count = stats.get("totalVectorCount", 0)
                dimension = stats.get("dimension", 0)
                # Estimate storage: vectors × dimensions × 4 bytes (float32) + overhead
                storage_bytes = vector_count * dimension * 4 * 1.2
                storage_gb = Decimal(str(storage_bytes)) / Decimal("1073741824")

                # Storage cost (point-in-time, dated at end_date)
                storage_cost = (storage_gb * _STORAGE_RATE).quantize(Decimal("0.01"))
                if storage_cost > 0:
                    records.append(
                        FinancialRecord(
                            record_date=end_date,
                            amount=-storage_cost,
                            category=SpendCategory.SEARCH_DATA,
                            subcategory=f"Pinecone Storage ({index_name})",
                            provider=Provider.PINECONE,
                            source="pinecone_api",
                            raw_description=(
                                f"Pinecone {index_name}: {vector_count:,} vectors, "
                                f"{storage_gb:.2f} GB"
                            ),
                        )
                    )

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 429:
                    logger.warning("Pinecone rate limit on index %s", index_name)
                else:
                    logger.error("Pinecone stats fetch failed for %s: HTTP %s", index_name, exc.response.status_code)
            except httpx.TimeoutException:
                logger.error("Pinecone stats fetch timed out for %s", index_name)
            except httpx.HTTPError as exc:
                logger.error("Pinecone stats fetch error for %s: %s", index_name, exc)

        # Note: query/write unit usage requires Pinecone's usage API or billing export.
        # Cost estimation for read/write units would require tracking at the application layer.

        return records

    async def get_summary(self) -> dict:
        today = date.today()
        records = await self.fetch_records(today, today)
        total = sum(r.amount for r in records)
        return {
            "provider": self.provider.value,
            "connected": self.is_connected,
            "indexes": len(self._indexes),
            "current_spend": str(total),
        }

    # ── Synthetic data ──────────────────────────────────────────

    def get_synthetic_records(
        self, start_date: date, end_date: date
    ) -> list[FinancialRecord]:
        """Generate realistic Pinecone cost data.

        Profile: 1 serverless index, 50K vectors (1536-dim), 100K queries/month.
          - Storage: 50K × 1536 × 4 bytes × 1.2 ≈ 0.34 GB → ~$0.11/month
          - Queries: 100K/month at $0.002/1K = ~$0.20/month
          - Realistic minimum: ~$8/month (Pinecone has minimum billing thresholds)
        Monthly billing records.
        """
        rng = random.Random(902)
        records: list[FinancialRecord] = []

        current = start_date.replace(day=1)
        while current <= end_date:
            # Storage cost
            vectors = int(50_000 * rng.uniform(0.9, 1.1))
            storage_gb = Decimal(str(round(vectors * 1536 * 4 * 1.2 / 1_073_741_824, 4)))
            storage_cost = max(
                (storage_gb * _STORAGE_RATE).quantize(Decimal("0.01")),
                Decimal("0.11"),
            )

            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-storage_cost,
                    category=SpendCategory.SEARCH_DATA,
                    subcategory="Pinecone Storage",
                    provider=Provider.PINECONE,
                    source="synthetic",
                    raw_description=f"Synthetic Pinecone: {vectors:,} vectors, {storage_gb:.3f} GB",
                )
            )

            # Query cost
            monthly_queries = int(100_000 * rng.uniform(0.7, 1.3))
            query_cost = (Decimal(str(monthly_queries)) / Decimal("1000") * _QUERY_RATE).quantize(Decimal("0.01"))

            records.append(
                FinancialRecord(
                    record_date=current,
                    amount=-query_cost,
                    category=SpendCategory.SEARCH_DATA,
                    subcategory="Pinecone Queries",
                    provider=Provider.PINECONE,
                    source="synthetic",
                    raw_description=f"Synthetic Pinecone: {monthly_queries:,} queries",
                )
            )

            # Write units (upserts)
            monthly_writes = int(5_000 * rng.uniform(0.5, 1.5))
            write_cost = (Decimal(str(monthly_writes)) / Decimal("1000") * _WRITE_RATE).quantize(Decimal("0.01"))
            if write_cost > 0:
                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-write_cost,
                        category=SpendCategory.SEARCH_DATA,
                        subcategory="Pinecone Writes",
                        provider=Provider.PINECONE,
                        source="synthetic",
                        raw_description=f"Synthetic Pinecone: {monthly_writes:,} write units",
                    )
                )

            # Minimum billing threshold makes realistic total ~$8/month
            # Add platform fee to reach realistic minimum
            subtotal = storage_cost + query_cost + write_cost
            if subtotal < Decimal("8.00"):
                platform_fee = (Decimal("8.00") - subtotal).quantize(Decimal("0.01"))
                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-platform_fee,
                        category=SpendCategory.SEARCH_DATA,
                        subcategory="Pinecone Platform",
                        provider=Provider.PINECONE,
                        source="synthetic",
                        raw_description="Synthetic Pinecone platform minimum",
                    )
                )

            current = (current + timedelta(days=32)).replace(day=1)

        return records
