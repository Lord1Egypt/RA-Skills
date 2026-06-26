"""Shared utilities for Token Economy Intelligence."""
import os
from datetime import date, timedelta
from decimal import Decimal
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def is_synthetic_mode() -> bool:
	return os.getenv("SYNTHETIC_MODE", "false").lower() == "true"

def is_onboarding_test_mode() -> bool:
	"""Check if onboarding test mode is enabled.

	When ONBOARDING_TEST_MODE=true, the full onboarding UX runs but
	credential validation uses TEST_CREDENTIALS instead of real APIs.
	"""
	return os.getenv("ONBOARDING_TEST_MODE", "false").lower() == "true"


# Test credentials accepted as "valid" in onboarding test mode.
# These never touch real APIs — they exist solely for end-to-end UX testing.
TEST_CREDENTIALS: dict[str, Any] = {
	"openai": ["sk-test-openai-12345", "sk-test-openai-demo"],
	"anthropic": ["sk-ant-test-anthropic-12345", "sk-ant-test-demo"],
	"aws": {
		"access_key_id": "AKIATEST12345",
		"secret_access_key": "test-secret-12345",
	},
	"gcp": {
		"service_account_json": "test-gcp-sa.json",
	},
	"vercel": ["test-vercel-token-12345"],
	"cloudflare": ["test-cf-token-12345"],
	"stripe": ["sk_test_stripe_12345", "sk_test_demo"],
	"twilio": {
		"account_sid": "ACtest12345",
		"auth_token": "test-auth-token-12345",
	},
	"sendgrid": ["SG.test-sendgrid-12345"],
	"datadog": {
		"api_key": "test-dd-api-12345",
		"app_key": "test-dd-app-12345",
	},
	"langsmith": ["test-ls-key-12345"],
	"pinecone": ["test-pc-key-12345"],
	"tavily": ["tvly-test-12345"],
	"gemini": ["test-gemini-key-12345"],
	"google_ads": {
		"developer_token": "test-gads-dev-token-12345",
		"customer_id": "123-456-7890",
	},
	"meta": {
		"access_token": "test-meta-token-12345",
		"ad_account_id": "act_test12345",
	},
	"crypto_wallet": {
		"_test_addresses": [
			"0xTEST1234567890abcdef",
			"TESTso1ana1234567890",
		],
	},
	"coinbase": {
		"api_key": "test-coinbase-key-12345",
		"api_secret": "test-coinbase-secret-12345",
	},
	"binance": {
		"api_key": "test-binance-key-12345",
		"api_secret": "test-binance-secret-12345",
	},
}


def get_test_credential(provider: str) -> Any:
	"""Return the primary test credential for a given provider.

	For list-style providers, returns the first credential string.
	For dict-style providers, returns the full credentials dict.
	"""
	creds = TEST_CREDENTIALS.get(provider)
	if creds is None:
		return None
	if isinstance(creds, list):
		return creds[0] if creds else None
	return creds

def get_date_range(days_back: int = 90) -> tuple[date, date]:
	end = date.today()
	start = end - timedelta(days=days_back)
	return start, end

def format_currency(amount: Decimal, currency: str = "USD") -> str:
	if currency == "USD":
		prefix = "-$" if amount < 0 else "$"
		return f"{prefix}{abs(amount):,.2f}"
	return f"{amount:,.2f} {currency}"

def format_percent(value: float) -> str:
	sign = "+" if value > 0 else ""
	return f"{sign}{value:.1f}%"
