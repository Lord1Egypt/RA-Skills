"""
Minimal QuantConnect API client for the backtest-poller skill.

Provides only the endpoints needed by the poller daemon:
  - read_backtest
  - delete_backtest
  - read_backtest_orders

Authentication uses the same HMAC-SHA256 scheme as the QC v2 API:
  Hash  = SHA256(api_token + ":" + unix_timestamp)
  Basic = base64(user_id + ":" + hash)

Required environment variables:
  QC_USER_ID     — your QuantConnect user ID
  QC_API_TOKEN   — your QuantConnect API token
"""
import os
import time
import hashlib
import base64
import logging

import requests

logger = logging.getLogger("backtest_poller.qc_client")

# Retry configuration
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # exponential backoff base (seconds)
RETRYABLE_STATUS_CODES = {500, 502, 503, 504, 429}

BASE_URL = "https://www.quantconnect.com/api/v2"


def _get_credentials() -> tuple:
    """Return (user_id, api_token) from environment variables."""
    user_id = os.environ.get("QC_USER_ID", "")
    api_token = os.environ.get("QC_API_TOKEN", "")
    if not user_id or not api_token:
        raise EnvironmentError(
            "QC_USER_ID and QC_API_TOKEN environment variables are required. "
            "Set them in your shell or in a .env file."
        )
    return user_id, api_token


class QCClient:
    """Lightweight QuantConnect API client with retry logic."""

    def __init__(self):
        self.user_id, self.api_token = _get_credentials()
        self.base_url = BASE_URL

    # ------------------------------------------------------------------
    # HTTP transport
    # ------------------------------------------------------------------
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Execute an API request with HMAC auth and exponential-backoff retry."""
        url = f"{self.base_url}/{endpoint}"
        last_exception = None

        for attempt in range(MAX_RETRIES):
            ts = str(int(time.time()))
            token_hash = hashlib.sha256(
                f"{self.api_token}:{ts}".encode("utf-8")
            ).hexdigest()
            auth_str = f"{self.user_id}:{token_hash}"
            base64_auth = base64.b64encode(auth_str.encode("ascii")).decode("ascii")

            headers = {
                "Accept": "application/json",
                "Timestamp": ts,
                "Authorization": f"Basic {base64_auth}",
            }

            try:
                if method.lower() == "get":
                    response = requests.get(url, params=data, headers=headers, timeout=30)
                elif method.lower() == "post":
                    response = requests.post(url, data=data, headers=headers, timeout=60)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                # Retryable status codes
                if response.status_code in RETRYABLE_STATUS_CODES:
                    wait = RETRY_BACKOFF_BASE ** attempt
                    logger.warning(
                        f"API {endpoint} returned {response.status_code}, "
                        f"retrying in {wait}s ({attempt + 1}/{MAX_RETRIES})"
                    )
                    time.sleep(wait)
                    last_exception = requests.exceptions.HTTPError(
                        f"{response.status_code}: {response.text[:200]}"
                    )
                    continue

                if response.status_code != 200:
                    logger.error(f"API error {response.status_code}: {response.text[:300]}")

                response.raise_for_status()
                return response.json()

            except requests.exceptions.ConnectionError as exc:
                wait = RETRY_BACKOFF_BASE ** attempt
                logger.warning(
                    f"API {endpoint} connection failed, "
                    f"retrying in {wait}s ({attempt + 1}/{MAX_RETRIES}): {exc}"
                )
                time.sleep(wait)
                last_exception = exc
            except requests.exceptions.Timeout as exc:
                wait = RETRY_BACKOFF_BASE ** attempt
                logger.warning(
                    f"API {endpoint} timeout, "
                    f"retrying in {wait}s ({attempt + 1}/{MAX_RETRIES}): {exc}"
                )
                time.sleep(wait)
                last_exception = exc
            except requests.exceptions.RequestException as exc:
                # Non-retryable (4xx, etc.) — raise immediately
                logger.error(f"API request error ({endpoint}): {exc}")
                raise

        # Retries exhausted
        logger.error(f"API {endpoint} still failed after {MAX_RETRIES} retries")
        raise last_exception or RuntimeError(
            f"API {endpoint} failed after {MAX_RETRIES} retries"
        )

    # ------------------------------------------------------------------
    # Backtest endpoints
    # ------------------------------------------------------------------
    def read_backtest(self, project_id: int, backtest_id: str) -> dict:
        """Read backtest status and results."""
        return self._request("get", "backtests/read", data={
            "projectId": project_id,
            "backtestId": backtest_id,
        })

    def delete_backtest(self, project_id: int, backtest_id: str) -> dict:
        """Delete (abort) a running or completed backtest."""
        return self._request("post", "backtests/delete", data={
            "projectId": project_id,
            "backtestId": backtest_id,
        })

    def read_backtest_orders(
        self, project_id: int, backtest_id: str, start: int = 0, end: int = 100
    ) -> dict:
        """Read orders from a completed backtest."""
        return self._request("get", "backtests/orders/read", data={
            "projectId": project_id,
            "backtestId": backtest_id,
            "start": start,
            "end": end,
        })
