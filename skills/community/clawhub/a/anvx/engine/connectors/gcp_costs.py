"""GCP Cloud Billing connector — fetches daily costs by service."""
import logging
import random
from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import httpx

from engine.connectors.base_connector import BaseConnector
from engine.models import FinancialRecord, Provider, SpendCategory

logger = logging.getLogger(__name__)

_GCP_BILLING_API = "https://cloudbilling.googleapis.com/v1"


class GCPCostsConnector(BaseConnector):
    """Connector for GCP Cloud Billing daily cost data."""

    provider = Provider.GCP

    def __init__(self) -> None:
        self.is_connected: bool = False
        self._access_token: str = ""
        self._billing_account_id: str = ""
        self._client: httpx.AsyncClient | None = None

    async def connect(self, credentials: dict[str, Any]) -> bool:
        # ── Onboarding test mode ───────────────────────────────
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            if self.validate_test_credentials(credentials):
                import asyncio
                print("Connecting to GCP Cloud Billing...")
                await asyncio.sleep(1)
                print("Authenticated with GCP service account (test mode)")
                self._client = httpx.AsyncClient()
                self.is_connected = True
                return True
            logger.error("Invalid GCP service account JSON")
            return False

        # ── Normal mode ────────────────────────────────────────
        service_account_json = credentials.get("service_account_json", "")
        if not service_account_json:
            logger.error("Missing GCP service_account_json")
            return False

        # Exchange service account JSON for an access token
        try:
            import json
            sa = json.loads(service_account_json) if isinstance(service_account_json, str) else service_account_json
        except (json.JSONDecodeError, TypeError):
            logger.error("Invalid GCP service account JSON")
            return False

        self._client = httpx.AsyncClient(timeout=30.0)

        # Exchange service account credentials for an access token
        try:
            token_resp = await self._client.post(
                "https://accounts.google.com/o/token",
                data={
                    "grant_type": "urn:ietf:params:grant-type:jwt-bearer",
                    "assertion": _build_jwt_assertion(sa),
                },
            )
            token_resp.raise_for_status()
            self._access_token = token_resp.json()["access_token"]
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                logger.error("GCP service account credentials invalid")
            else:
                logger.error("GCP auth failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("GCP auth timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("GCP auth error: %s", exc)
            return False
        except (KeyError, ValueError) as exc:
            logger.error("GCP auth response parse error: %s", exc)
            return False

        # List billing accounts to validate access and get account ID
        try:
            resp = await self._client.get(
                f"{_GCP_BILLING_API}/billingAccounts",
                headers={"Authorization": f"Bearer {self._access_token}"},
            )
            resp.raise_for_status()
            accounts = resp.json().get("billingAccounts", [])
            if not accounts:
                logger.error("No GCP billing accounts found")
                return False
            self._billing_account_id = accounts[0]["name"]
            self.is_connected = True
            return True
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                logger.error("GCP billing access denied")
            else:
                logger.error("GCP billing list failed: HTTP %s", exc.response.status_code)
            return False
        except httpx.TimeoutException:
            logger.error("GCP billing list timed out")
            return False
        except httpx.HTTPError as exc:
            logger.error("GCP billing list error: %s", exc)
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
            # Query BigQuery export of billing data via Cloud Billing API
            resp = await self._client.get(
                f"{_GCP_BILLING_API}/{self._billing_account_id}/costs",
                headers={"Authorization": f"Bearer {self._access_token}"},
                params={
                    "startDate": start_date.isoformat(),
                    "endDate": end_date.isoformat(),
                    "groupBy": "service",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            for entry in data.get("costs", []):
                entry_date = date.fromisoformat(entry["date"])
                service = entry.get("service", "Unknown")
                cost = Decimal(str(entry.get("amount", 0))).quantize(Decimal("0.01"))
                if cost == 0:
                    continue

                records.append(
                    FinancialRecord(
                        record_date=entry_date,
                        amount=-cost,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory=service,
                        provider=Provider.GCP,
                        source="gcp_cloud_billing",
                        raw_description=f"GCP {service}",
                    )
                )

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 429:
                logger.warning("GCP billing rate limit — returning partial results")
            else:
                logger.error("GCP billing fetch failed: HTTP %s", exc.response.status_code)
        except httpx.TimeoutException:
            logger.error("GCP billing fetch timed out — returning partial results")
        except httpx.HTTPError as exc:
            logger.error("GCP billing fetch error: %s", exc)

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
        """Generate realistic GCP cost data.

        Profile: ~$150/month total
          - Compute Engine: ~$60/month
          - Cloud Run: ~$40/month
          - Cloud Storage: ~$20/month
          - BigQuery: ~$30/month
        """
        rng = random.Random(301)

        service_daily: dict[str, float] = {
            "Compute Engine": 60.0 / 30,
            "Cloud Run": 40.0 / 30,
            "Cloud Storage": 20.0 / 30,
            "BigQuery": 30.0 / 30,
        }

        records: list[FinancialRecord] = []
        current = start_date
        while current <= end_date:
            for service, daily_target in service_daily.items():
                # Weekday/weekend: storage is constant, compute drops on weekends
                is_weekend = current.weekday() >= 5
                if is_weekend and service in ("Compute Engine", "Cloud Run", "BigQuery"):
                    base = daily_target * 0.7
                else:
                    base = daily_target
                cost = base * rng.uniform(0.85, 1.15)
                cost_dec = Decimal(str(round(cost, 2)))

                records.append(
                    FinancialRecord(
                        record_date=current,
                        amount=-cost_dec,
                        category=SpendCategory.CLOUD_INFRASTRUCTURE,
                        subcategory=service,
                        provider=Provider.GCP,
                        source="synthetic",
                        raw_description=f"Synthetic GCP {service}",
                    )
                )

            current += timedelta(days=1)

        return records


def _build_jwt_assertion(sa: dict) -> str:
    """Build a JWT assertion for service account authentication.

    Stub — real implementation uses the google-auth library to create
    a properly authenticated JWT. The connect() method handles failures.
    """
    import base64
    import json
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).decode()
    payload = base64.urlsafe_b64encode(json.dumps({
        "iss": sa.get("client_email", ""),
        "scope": "https://www.googleapis.com/auth/cloud-billing.readonly",
        "aud": "https://accounts.google.com/o/token",
    }).encode()).decode()
    # Stub assertion — will be rejected by Google, connect() handles the error
    return f"{header}.{payload}.stub"
