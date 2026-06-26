"""ANVX Token Economy Intelligence — Interactive Setup.

Guides users through provider selection, credential collection (via getpass),
validation, and secure storage in the system keychain.

Usage: uv run python -m engine.setup
"""
import asyncio
import getpass
import json
import platform
import sys
from typing import Any

from engine.credentials import CredentialStore, PROVIDER_FIELDS, _SERVICE

# ── Provider registry ──────────────────────────────────────────────

_PROVIDERS: list[dict[str, Any]] = [
    # AI Inference
    {"num": 1,  "name": "openai",        "label": "OpenAI",              "group": "AI Inference",
     "fields": [("api_key", "API key (sk-...)")],
     "help": "Find your keys at platform.openai.com/api-keys. Tip: Create a dedicated read-only key labelled 'ANVX'."},
    {"num": 2,  "name": "anthropic",     "label": "Anthropic",           "group": "AI Inference",
     "fields": [("api_key", "Admin API key")],
     "help": "Find your keys at console.anthropic.com/settings/admin-keys (separate from regular API keys)."},
    # Infrastructure
    {"num": 3,  "name": "aws",           "label": "AWS",                 "group": "Infrastructure",
     "fields": [("access_key_id", "Access Key ID"), ("secret_access_key", "Secret Access Key")],
     "help": "AWS Console -> IAM -> Users -> Create user with CostExplorer read-only policy -> Security credentials -> Create access key."},
    {"num": 4,  "name": "gcp",           "label": "GCP",                 "group": "Infrastructure",
     "fields": [("service_account_json", "Service account JSON (paste full contents)")],
     "help": "GCP Console -> IAM & Admin -> Service Accounts -> Create with 'Billing Account Viewer' role -> Keys -> Add JSON key."},
    {"num": 5,  "name": "vercel",        "label": "Vercel",              "group": "Infrastructure",
     "fields": [("api_token", "API token")],
     "help": "vercel.com/account/tokens -> 'Create Token' with read scope on your team."},
    {"num": 6,  "name": "cloudflare",    "label": "Cloudflare",          "group": "Infrastructure",
     "fields": [("api_token", "API token")],
     "help": "dash.cloudflare.com/profile/api-tokens -> 'Create Token' with Analytics Read + R2 Read permissions."},
    # Payments
    {"num": 7,  "name": "stripe",        "label": "Stripe",              "group": "Payments",
     "fields": [("api_key", "Restricted or secret key (sk_... or rk_...)")],
     "help": "dashboard.stripe.com/apikeys -> 'Create restricted key' with read permissions on Charges, Balance, Payouts."},
    # Communication
    {"num": 8,  "name": "twilio",        "label": "Twilio",              "group": "Communication",
     "fields": [("account_sid", "Account SID"), ("auth_token", "Auth Token")],
     "help": "console.twilio.com -> Account -> API keys & tokens. SID and Auth Token are on the dashboard."},
    {"num": 9,  "name": "sendgrid",      "label": "SendGrid",            "group": "Communication",
     "fields": [("api_key", "API key")],
     "help": "app.sendgrid.com/settings/api_keys -> 'Create API Key' with Read Access on Stats and Account."},
    # Monitoring
    {"num": 10, "name": "datadog",       "label": "Datadog",             "group": "Monitoring",
     "fields": [("api_key", "API key"), ("app_key", "Application key")],
     "help": "app.datadoghq.com/organization-settings/api-keys for API key, /application-keys for App key."},
    {"num": 11, "name": "langsmith",     "label": "LangSmith",           "group": "Monitoring",
     "fields": [("api_key", "API key")],
     "help": "smith.langchain.com/settings -> API keys -> 'Create API Key'."},
    # Search & Data
    {"num": 12, "name": "pinecone",      "label": "Pinecone",            "group": "Search & Data",
     "fields": [("api_key", "API key")],
     "help": "app.pinecone.io -> API Keys -> 'Create API Key'."},
    {"num": 13, "name": "tavily",        "label": "Tavily",              "group": "Search & Data",
     "fields": [("api_key", "API key (tvly-...)")],
     "help": "app.tavily.com -> API Keys."},
    # Crypto
    {"num": 14, "name": "crypto_wallet", "label": "On-chain wallets",    "group": "Crypto",
     "fields": [],  # special handling
     "help": "Public wallet addresses only. NEVER share secret keys or recovery phrases."},
    {"num": 15, "name": "coinbase",      "label": "Coinbase",            "group": "Crypto",
     "fields": [("api_key", "API key"), ("api_secret", "API secret")],
     "help": "coinbase.com/settings/api -> 'New API Key'. Grant ONLY 'wallet:accounts:read' — read-only, no other permissions."},
    {"num": 16, "name": "binance",       "label": "Binance",             "group": "Crypto",
     "fields": [("api_key", "API key"), ("api_secret", "API secret")],
     "help": "binance.com/en/my/settings/api-management -> 'Create API'. Enable ONLY 'Read Info' — all other permissions disabled."},
]

_PROVIDER_BY_NUM = {p["num"]: p for p in _PROVIDERS}


# ── Main ───────────────────────────────────────────────────────────


def main() -> None:
    _print_welcome()
    selected = _select_providers()
    if not selected:
        print("\nNo providers selected. Run again when ready.")
        return

    connected: list[str] = []

    for provider in selected:
        print()
        print(f"  {provider['label']}")
        print(f"  {provider['help']}")
        print()

        if provider["name"] == "crypto_wallet":
            _collect_crypto_wallets(provider)
            connected.append(f"{provider['label']}")
            continue

        # Collect credentials (multi-key support)
        label = "default"
        first = True
        while True:
            creds = _collect_fields(provider, label)
            if not creds:
                break

            # Validate
            ok = _validate_provider(provider, creds, label)
            if ok:
                connected.append(
                    f"{provider['label']}" if label == "default"
                    else f"{provider['label']} ({label})"
                )

            if first:
                first = False
            # Ask for additional keys
            extra = input(
                f"  Enter another key for {provider['label']}, or type 'done': "
            ).strip()
            if extra.lower() in ("done", "d", ""):
                break
            label = input("  Label for this key (e.g., 'production', 'personal'): ").strip()
            if not label:
                label = "extra"

    _print_completion(connected)


# ── Welcome & provider selection ───────────────────────────────────


def _print_welcome() -> None:
    print()
    print("=" * 60)
    print("  ANVX Token Economy Intelligence  --  Setup")
    print("=" * 60)
    print()
    print("  This script stores your API keys securely in your")
    print("  system keychain. Keys never leave your machine.")
    print()

    if platform.system() == "Linux":
        print("  Note: Keyring requires a system secret service")
        print("  (gnome-keyring or kwallet). If you encounter issues,")
        print("  see: https://github.com/jaraco/keyring#linux")
        print()


def _select_providers() -> list[dict]:
    current_group = ""
    for p in _PROVIDERS:
        if p["group"] != current_group:
            current_group = p["group"]
            print(f"  {current_group}:")
        print(f"    {p['num']:>2}. {p['label']}")
    print()

    raw = input(
        "  Which providers do you want to connect?\n"
        "  Enter numbers separated by commas (e.g., 1,2,7): "
    ).strip()

    if not raw:
        return []

    selected = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and int(part) in _PROVIDER_BY_NUM:
            selected.append(_PROVIDER_BY_NUM[int(part)])
        else:
            print(f"  Skipping invalid selection: {part}")

    return selected


# ── Credential collection ──────────────────────────────────────────


def _collect_fields(provider: dict, label: str) -> dict[str, str]:
    """Collect credentials for a provider using getpass (hidden input)."""
    creds: dict[str, str] = {}
    for field_key, field_label in provider["fields"]:
        value = getpass.getpass(f"  {field_label}: ")
        if not value.strip():
            print(f"  Skipped (empty {field_label})")
            return {}
        creds[field_key] = value.strip()
    return creds


def _collect_crypto_wallets(provider: dict) -> None:
    """Collect chain + address pairs for on-chain wallets."""
    supported = ["ethereum", "solana", "base", "arbitrum", "polygon"]
    wallets_added = 0

    while True:
        chain = input(
            f"  Enter chain ({'/'.join(supported)}): "
        ).strip().lower()
        if chain in ("done", "d", ""):
            break
        if chain not in supported:
            print(f"  Unsupported chain: {chain}. Supported: {', '.join(supported)}")
            continue

        address = input("  Enter wallet address: ").strip()
        if not address:
            continue

        label = f"{chain}_{wallets_added + 1}"
        CredentialStore.store_credential("crypto_wallet", label, "chain", chain)
        CredentialStore.store_credential("crypto_wallet", label, "address", address)
        CredentialStore.update_manifest("crypto_wallet", label)
        wallets_added += 1
        print(f"  Stored {chain} wallet: {address[:10]}...")

        more = input("  Add another wallet? (enter chain or 'done'): ").strip().lower()
        if more in ("done", "d", ""):
            break
        if more in supported:
            # Re-enter the loop with this chain
            address = input("  Enter wallet address: ").strip()
            if address:
                label = f"{more}_{wallets_added + 1}"
                CredentialStore.store_credential("crypto_wallet", label, "chain", more)
                CredentialStore.store_credential("crypto_wallet", label, "address", address)
                CredentialStore.update_manifest("crypto_wallet", label)
                wallets_added += 1
                print(f"  Stored {more} wallet: {address[:10]}...")

    if wallets_added:
        print(f"  {wallets_added} wallet(s) saved to keychain.")


# ── Validation ─────────────────────────────────────────────────────


def _validate_provider(
    provider: dict, creds: dict[str, str], label: str
) -> bool:
    """Validate credentials by calling the connector's connect() method."""
    from engine.connectors import (
        AWSCostsConnector, AnthropicBillingConnector, BinanceExchangeConnector,
        CloudflareCostsConnector, CoinbaseExchangeConnector, CryptoWalletConnector,
        DatadogCostsConnector, GCPCostsConnector, LangSmithCostsConnector,
        OpenAIBillingConnector, PineconeCostsConnector, SendGridCostsConnector,
        StripeConnector, TavilyCostsConnector, TwilioCostsConnector,
        VercelCostsConnector,
    )

    _CONNECTOR_MAP = {
        "openai": OpenAIBillingConnector,
        "anthropic": AnthropicBillingConnector,
        "aws": AWSCostsConnector,
        "gcp": GCPCostsConnector,
        "vercel": VercelCostsConnector,
        "cloudflare": CloudflareCostsConnector,
        "stripe": StripeConnector,
        "twilio": TwilioCostsConnector,
        "sendgrid": SendGridCostsConnector,
        "datadog": DatadogCostsConnector,
        "langsmith": LangSmithCostsConnector,
        "pinecone": PineconeCostsConnector,
        "tavily": TavilyCostsConnector,
        "coinbase": CoinbaseExchangeConnector,
        "binance": BinanceExchangeConnector,
    }

    cls = _CONNECTOR_MAP.get(provider["name"])
    if cls is None:
        print(f"  No connector for {provider['name']} — storing credentials only.")
        _store_creds(provider["name"], label, creds)
        return True

    connector = cls()
    print(f"  Validating...", end=" ", flush=True)

    while True:
        try:
            ok = asyncio.run(connector.connect(creds))
        except Exception as exc:
            ok = False
            print(f"\n  Connection error: {exc}")

        if ok:
            print(f"Connected to {provider['label']}!")
            _store_creds(provider["name"], label, creds)
            return True

        print(f"Connection failed.")
        choice = input("  Try again, skip, or quit? (t/s/q): ").strip().lower()
        if choice == "t":
            # Re-collect credentials
            creds = _collect_fields(provider, label)
            if not creds:
                return False
            connector = cls()
            print(f"  Validating...", end=" ", flush=True)
            continue
        elif choice == "q":
            print("  Setup cancelled.")
            sys.exit(0)
        else:
            print(f"  Skipped {provider['label']}.")
            return False


def _store_creds(provider: str, label: str, creds: dict[str, str]) -> None:
    """Store credentials in keyring and update manifest."""
    for field, value in creds.items():
        CredentialStore.store_credential(provider, label, field, value)
    CredentialStore.update_manifest(provider, label)


# ── Completion ─────────────────────────────────────────────────────


def _print_completion(connected: list[str]) -> None:
    print()
    print("=" * 60)
    if connected:
        print("  Setup complete!")
        print(f"  Connected: {', '.join(connected)}")
        print("  Credentials stored in system keychain.")
    else:
        print("  No providers were connected.")
    print()
    print("  To add more providers later:")
    print("    uv run python -m engine.setup")
    print()
    print("  Credentials will be read automatically from your keychain")
    print("  by both OpenClaw and the MCP server — no config needed.")
    print("=" * 60)
    print()


# ── Entry point ────────────────────────────────────────────────────


if __name__ == "__main__":
    main()
