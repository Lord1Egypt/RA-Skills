"""Tests for CyberLens API base URL resolution."""

import pytest
import httpx

from src.api_client import CyberLensAPIClient, CyberLensQuotaExceededError, DEFAULT_API_BASE


def test_client_uses_default_api_base(monkeypatch):
    monkeypatch.delenv("CYBERLENS_API_BASE_URL", raising=False)

    client = CyberLensAPIClient("clns_acct_test")

    assert client.api_base == DEFAULT_API_BASE


def test_client_uses_env_api_base_override(monkeypatch):
    monkeypatch.setenv(
        "CYBERLENS_API_BASE_URL",
        "https://alt-api.cyberlensai.com/functions/v1/public-api-scan",
    )

    client = CyberLensAPIClient("clns_acct_test")

    assert client.api_base == "https://alt-api.cyberlensai.com/functions/v1/public-api-scan"


def test_client_rejects_non_https_api_base():
    with pytest.raises(ValueError, match="https:// URL"):
        CyberLensAPIClient(
            "clns_acct_test",
            api_base="http://localhost:8000/functions/v1/public-api-scan",
        )


def test_client_raises_structured_quota_error():
    client = CyberLensAPIClient("clns_acct_test")
    response = httpx.Response(
        402,
        json={
            "error": {
                "code": "QUOTA_EXCEEDED",
                "message": "Monthly website scan limit reached (3/3). Upgrade your plan to continue scanning immediately.",
                "upgrade_url": "https://www.cyberlensai.com/pricing?source=api_quota_exceeded&quota_type=website#plans",
                "quota_type": "website",
                "used": 3,
                "limit": 3,
            }
        },
    )

    with pytest.raises(CyberLensQuotaExceededError) as exc_info:
        client._read_response_data(response)

    error = exc_info.value
    assert str(error) == "Monthly website scan limit reached (3/3). Upgrade your plan to continue scanning immediately."
    assert error.upgrade_url.endswith("quota_type=website#plans")
    assert error.quota_type == "website"
    assert error.used == 3
    assert error.limit == 3
