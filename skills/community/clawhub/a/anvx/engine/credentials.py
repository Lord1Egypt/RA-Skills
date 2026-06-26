"""Credential store — reads API keys from system keyring, env vars, or test mode.

Lookup order:
1. Onboarding test mode → returns TEST_CREDENTIALS
2. System keyring (via `keyring` library)
3. Environment variables (e.g. OPENAI_API_KEY)
4. Explicitly passed credentials (caller's responsibility)

Keys are stored in the system keychain under service name
"anvx-token-economy-intel" with key format "{provider}:{label}:{field}".
"""
import json
import logging
import os
from typing import Any

import keyring

logger = logging.getLogger(__name__)

_SERVICE = "anvx-token-economy-intel"

# Maps provider names to their credential fields
PROVIDER_FIELDS: dict[str, list[str]] = {
    "openai": ["api_key"],
    "anthropic": ["api_key"],
    "aws": ["access_key_id", "secret_access_key"],
    "gcp": ["service_account_json"],
    "vercel": ["api_token"],
    "cloudflare": ["api_token"],
    "stripe": ["api_key"],
    "twilio": ["account_sid", "auth_token"],
    "sendgrid": ["api_key"],
    "datadog": ["api_key", "app_key"],
    "langsmith": ["api_key"],
    "pinecone": ["api_key"],
    "tavily": ["api_key"],
    "crypto_wallet": ["address"],  # special: chain+address pairs
    "coinbase": ["api_key", "api_secret"],
    "binance": ["api_key", "api_secret"],
}

# Maps provider+field to environment variable name
_ENV_VAR_MAP: dict[str, str] = {
    "openai:api_key": "OPENAI_API_KEY",
    "anthropic:api_key": "ANTHROPIC_API_KEY",
    "aws:access_key_id": "AWS_ACCESS_KEY_ID",
    "aws:secret_access_key": "AWS_SECRET_ACCESS_KEY",
    "stripe:api_key": "STRIPE_API_KEY",
    "vercel:api_token": "VERCEL_TOKEN",
    "cloudflare:api_token": "CLOUDFLARE_API_TOKEN",
    "twilio:account_sid": "TWILIO_ACCOUNT_SID",
    "twilio:auth_token": "TWILIO_AUTH_TOKEN",
    "sendgrid:api_key": "SENDGRID_API_KEY",
    "datadog:api_key": "DD_API_KEY",
    "datadog:app_key": "DD_APP_KEY",
    "langsmith:api_key": "LANGSMITH_API_KEY",
    "pinecone:api_key": "PINECONE_API_KEY",
    "tavily:api_key": "TAVILY_API_KEY",
    "coinbase:api_key": "COINBASE_API_KEY",
    "coinbase:api_secret": "COINBASE_API_SECRET",
    "binance:api_key": "BINANCE_API_KEY",
    "binance:api_secret": "BINANCE_API_SECRET",
}


class CredentialStore:
    """Reads credentials from keyring, env vars, or test mode."""

    @staticmethod
    def get_credential(
        provider: str, label: str = "default", field: str = "api_key"
    ) -> str | None:
        """Read a single credential value.

        Checks: test mode → keyring → env var. Returns None if not found.
        """
        # 1. Test mode
        from engine.utils import is_onboarding_test_mode, TEST_CREDENTIALS
        if is_onboarding_test_mode():
            return _get_test_credential(provider, field)

        # 2. Keyring
        try:
            key = f"{provider}:{label}:{field}"
            value = keyring.get_password(_SERVICE, key)
            if value:
                return value
        except Exception as exc:
            logger.debug("Keyring read failed for %s: %s", provider, exc)

        # 3. Environment variable
        env_key = _ENV_VAR_MAP.get(f"{provider}:{field}")
        if env_key:
            value = os.environ.get(env_key)
            if value:
                return value

        return None

    @staticmethod
    def get_manifest() -> dict[str, list[str]]:
        """Returns the provider manifest: {provider: [labels]}."""
        from engine.utils import is_onboarding_test_mode
        if is_onboarding_test_mode():
            from engine.utils import TEST_CREDENTIALS
            return {p: ["default"] for p in TEST_CREDENTIALS}

        try:
            raw = keyring.get_password(_SERVICE, "manifest")
            return json.loads(raw) if raw else {}
        except Exception:
            return {}

    @staticmethod
    def get_all_credentials(
        provider: str, label: str = "default"
    ) -> dict[str, str]:
        """Returns all fields for a provider as a dict.

        E.g. {"api_key": "sk-...", "api_secret": "..."}
        """
        fields = PROVIDER_FIELDS.get(provider, ["api_key"])
        result: dict[str, str] = {}
        for field in fields:
            value = CredentialStore.get_credential(provider, label, field)
            if value:
                result[field] = value
        return result

    @staticmethod
    def store_credential(
        provider: str, label: str, field: str, value: str
    ) -> None:
        """Store a credential in the system keyring."""
        key = f"{provider}:{label}:{field}"
        keyring.set_password(_SERVICE, key, value)

    @staticmethod
    def update_manifest(provider: str, label: str) -> None:
        """Add a provider+label to the manifest."""
        manifest = CredentialStore.get_manifest()
        labels = manifest.get(provider, [])
        if label not in labels:
            labels.append(label)
        manifest[provider] = labels
        keyring.set_password(_SERVICE, "manifest", json.dumps(manifest))


def _get_test_credential(provider: str, field: str) -> str | None:
    """Extract a specific field from TEST_CREDENTIALS."""
    from engine.utils import TEST_CREDENTIALS
    creds = TEST_CREDENTIALS.get(provider)
    if creds is None:
        return None
    if isinstance(creds, list):
        return creds[0] if field == "api_key" else None
    if isinstance(creds, dict):
        return creds.get(field)
    return None
