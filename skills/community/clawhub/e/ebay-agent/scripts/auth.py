"""
eBay OAuth 2.0 client credentials authentication.

Supports the client credentials flow (app-level, no user consent required)
for Browse API and Marketplace Insights API access. Fetches a fresh token
on each invocation (client credentials tokens are cheap and fast).
"""

import os
import base64

import httpx
from dotenv import load_dotenv

load_dotenv()

SANDBOX_TOKEN_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
PRODUCTION_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# Default scope for Browse API (no user auth required)
BROWSE_SCOPE = "https://api.ebay.com/oauth/api_scope"


def _get_credentials() -> tuple[str, str]:
    """Load eBay App ID and Cert ID from environment variables."""
    app_id = os.getenv("EBAY_APP_ID")
    cert_id = os.getenv("EBAY_CERT_ID")

    if not app_id or not cert_id:
        raise EnvironmentError(
            "Missing eBay credentials. Set EBAY_APP_ID and EBAY_CERT_ID in your environment."
        )

    return app_id, cert_id


def _get_token_url() -> str:
    """Return the appropriate OAuth token endpoint based on EBAY_ENVIRONMENT."""
    env = os.getenv("EBAY_ENVIRONMENT", "production").lower()
    return SANDBOX_TOKEN_URL if env == "sandbox" else PRODUCTION_TOKEN_URL


def get_app_access_token(scope: str = BROWSE_SCOPE) -> str:
    """
    Obtain a client credentials (app-level) OAuth access token.

    Fetches a fresh token from eBay's OAuth endpoint each time.
    Uses HTTP Basic auth as required by eBay's OAuth 2.0 spec.
    """
    app_id, cert_id = _get_credentials()
    token_url = _get_token_url()
    credentials = base64.b64encode(f"{app_id}:{cert_id}".encode()).decode()

    response = httpx.post(
        token_url,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": scope,
        },
    )
    response.raise_for_status()

    return response.json()["access_token"]
