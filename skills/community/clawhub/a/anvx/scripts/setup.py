"""First-run setup — check deps, create data dir, connect accounts, initial fetch."""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from engine.analytics import EventTracker
from engine.connectors import (
    AWSCostsConnector,
    AnthropicBillingConnector,
    BinanceExchangeConnector,
    CloudflareCostsConnector,
    CoinbaseExchangeConnector,
    CryptoWalletConnector,
    DatadogCostsConnector,
    GCPCostsConnector,
    LangSmithCostsConnector,
    OpenAIBillingConnector,
    PineconeCostsConnector,
    SendGridCostsConnector,
    StripeConnector,
    TavilyCostsConnector,
    TwilioCostsConnector,
    VercelCostsConnector,
)
from engine.intelligence import FinancialModelManager, categorise_records
from engine.utils import format_currency, get_date_range, is_onboarding_test_mode, is_synthetic_mode

_DATA_DIR = Path.home() / ".token-economy-intel"

_ACCOUNT_GROUPS = [
    {
        "group": "LLM Billing",
        "accounts": [
            {"name": "openai", "label": "OpenAI", "cls": OpenAIBillingConnector,
             "fields": [("api_key", "OpenAI API key (sk-...)")]},
            {"name": "anthropic", "label": "Anthropic", "cls": AnthropicBillingConnector,
             "fields": [("api_key", "Anthropic API key")]},
        ],
    },
    {
        "group": "Payments",
        "accounts": [
            {"name": "stripe", "label": "Stripe", "cls": StripeConnector,
             "fields": [("api_key", "Stripe secret key (sk_...)")]},
        ],
    },
    {
        "group": "Crypto",
        "accounts": [
            {"name": "crypto_wallet", "label": "Crypto Wallet", "cls": CryptoWalletConnector,
             "fields": [("wallet_addresses", "Wallet address(es), comma-separated (public addresses only — never share secret keys)")]},
            {"name": "coinbase", "label": "Coinbase", "cls": CoinbaseExchangeConnector,
             "fields": [("api_key", "Coinbase API key (read-only)"), ("api_secret", "Coinbase API secret")]},
            {"name": "binance", "label": "Binance", "cls": BinanceExchangeConnector,
             "fields": [("api_key", "Binance API key (read-only)"), ("api_secret", "Binance API secret")]},
        ],
    },
    {
        "group": "Infrastructure",
        "accounts": [
            {"name": "aws", "label": "AWS", "cls": AWSCostsConnector,
             "fields": [("access_key_id", "AWS Access Key ID"), ("secret_access_key", "AWS Secret Access Key")]},
            {"name": "gcp", "label": "GCP", "cls": GCPCostsConnector,
             "fields": [("service_account_json", "GCP service account JSON (paste full JSON)")]},
            {"name": "vercel", "label": "Vercel", "cls": VercelCostsConnector,
             "fields": [("api_token", "Vercel API token")]},
            {"name": "cloudflare", "label": "Cloudflare", "cls": CloudflareCostsConnector,
             "fields": [("api_token", "Cloudflare API token")]},
        ],
    },
    {
        "group": "Communication",
        "accounts": [
            {"name": "twilio", "label": "Twilio", "cls": TwilioCostsConnector,
             "fields": [("account_sid", "Twilio Account SID"), ("auth_token", "Twilio Auth Token")]},
            {"name": "sendgrid", "label": "SendGrid", "cls": SendGridCostsConnector,
             "fields": [("api_key", "SendGrid API key")]},
        ],
    },
    {
        "group": "Monitoring",
        "accounts": [
            {"name": "datadog", "label": "Datadog", "cls": DatadogCostsConnector,
             "fields": [("api_key", "Datadog API key"), ("app_key", "Datadog App key")]},
            {"name": "langsmith", "label": "LangSmith", "cls": LangSmithCostsConnector,
             "fields": [("api_key", "LangSmith API key")]},
        ],
    },
    {
        "group": "Search & Data",
        "accounts": [
            {"name": "pinecone", "label": "Pinecone", "cls": PineconeCostsConnector,
             "fields": [("api_key", "Pinecone API key")]},
            {"name": "tavily", "label": "Tavily", "cls": TavilyCostsConnector,
             "fields": [("api_key", "Tavily API key")]},
        ],
    },
]


def main() -> None:
    tracker = EventTracker()
    synthetic = is_synthetic_mode()

    print("Token Economy Intelligence — Setup")
    print("=" * 50)
    print()

    # 1. Create data directory
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Data directory: {_DATA_DIR}")

    # 2. Check if model already exists
    model = FinancialModelManager()
    model.load()
    if model.get_summary().record_count > 0:
        print(f"Existing model found: {model.get_summary().record_count:,} records")
        print("Run scripts/status.py for current overview.")
        return

    test_mode = is_onboarding_test_mode()

    if synthetic:
        print("Running in SYNTHETIC MODE — no real API keys needed.")
        print()
        _run_synthetic(model, tracker)
    else:
        if test_mode:
            print("Running in ONBOARDING TEST MODE — use test credentials.")
            print()
        print("Let's connect your accounts. Skip any you don't use.")
        print()
        credentials = _collect_credentials()
        asyncio.run(_connect_and_fetch(model, credentials, tracker))

        # Bank statement CSV upload — after all providers are connected
        print()
        answer = input("Would you like to upload a bank statement CSV for a fuller picture of your spending? (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            _prompt_csv_upload(model, test_mode)

    print()
    mode = "test" if test_mode else ("synthetic" if synthetic else "live")
    tracker.track("setup_complete", "lifecycle", "openclaw", {"mode": mode})


def _prompt_csv_upload(model: FinancialModelManager, test_mode: bool) -> None:
    """Prompt for a bank CSV path, with test-mode shortcut."""
    _SYNTHETIC_CSV = str(
        Path(__file__).resolve().parents[2]
        / "engine" / "testing" / "data" / "bank_statement.csv"
    )

    if test_mode:
        print('  Send me a CSV file path, or type "test" to load the synthetic bank statement.')
    else:
        print("  Send me a CSV with columns: Date, Description, Amount, Balance")

    while True:
        csv_path = input("  File path: ").strip()
        if not csv_path:
            print("  Skipped bank CSV upload.")
            return

        # Handle "test" keyword
        if csv_path.lower() == "test":
            if test_mode:
                csv_path = _SYNTHETIC_CSV
                print(f"  Loading synthetic bank statement: {csv_path}")
                break
            else:
                print('  Invalid file path. Please provide a path to a .csv file.')
                continue

        # Validate the path looks like a CSV
        if not csv_path.endswith(".csv"):
            print("  File must be a .csv file. Try again or press Enter to skip.")
            continue

        break

    _parse_bank_csv(csv_path, model)


def _parse_bank_csv(csv_path: str, model: FinancialModelManager) -> None:
    """Parse a bank statement CSV, categorise, and add to the model."""
    import csv
    from collections import Counter
    from decimal import Decimal
    from datetime import date as date_cls

    from engine.models import FinancialRecord, Provider, SpendCategory

    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            records: list[FinancialRecord] = []
            vendor_counter: Counter[str] = Counter()
            skipped = 0

            for row_num, row in enumerate(reader, start=2):  # row 1 is header
                try:
                    description = row.get("description", "")
                    amount = Decimal(row.get("amount", "0"))
                    record_date = date_cls.fromisoformat(row.get("date", "").strip())
                except (ValueError, ArithmeticError) as exc:
                    print(f"  Warning: skipping row {row_num} — {exc}")
                    skipped += 1
                    continue

                # Extract vendor name (first word or text before *)
                vendor = description.split("*")[0].strip().split(" ")[0]
                vendor_counter[vendor] += 1

                category = SpendCategory.OTHER
                desc_upper = description.upper()
                if amount > 0:
                    category = SpendCategory.REVENUE
                elif any(kw in desc_upper for kw in ("OPENAI", "ANTHROPIC")):
                    category = SpendCategory.AI_INFERENCE
                elif any(kw in desc_upper for kw in ("AWS", "GOOGLE CLOUD", "VERCEL", "CLOUDFLARE", "DIGITALOCEAN")):
                    category = SpendCategory.CLOUD_INFRASTRUCTURE
                elif "STRIPE" in desc_upper and "FEE" in desc_upper:
                    category = SpendCategory.PAYMENT_PROCESSING
                elif any(kw in desc_upper for kw in ("TWILIO", "SENDGRID", "SLACK")):
                    category = SpendCategory.COMMUNICATION
                elif any(kw in desc_upper for kw in ("DATADOG", "LANGSMITH")):
                    category = SpendCategory.MONITORING
                elif any(kw in desc_upper for kw in ("PINECONE", "TAVILY")):
                    category = SpendCategory.SEARCH_DATA

                records.append(
                    FinancialRecord(
                        record_date=record_date,
                        amount=amount,
                        category=category,
                        provider=Provider.OTHER,
                        source="bank_csv",
                        raw_description=description,
                    )
                )

            if not records:
                print("  No valid transactions found in CSV.")
                return

            n = model.add_records(records, "bank_csv")
            categorised_count = sum(1 for r in records if r.category != SpendCategory.OTHER)
            pct = round(categorised_count / len(records) * 100)
            top_vendors = [v for v, _ in vendor_counter.most_common(5)]

            print(f"  Parsed {len(records)} transactions. Categorised {pct}%. "
                  f"Top vendors: {', '.join(top_vendors)}.")
            if skipped:
                print(f"  ({skipped} malformed rows skipped)")
            print(f"  Added {n} bank records to model.")

    except FileNotFoundError:
        print(f"  File not found: {csv_path}")
    except Exception as exc:
        print(f"  Error parsing CSV: {exc}")


def _run_synthetic(model: FinancialModelManager, tracker: EventTracker) -> None:
    """Load synthetic data from all connectors."""
    start, end = get_date_range(90)
    total = 0

    for group in _ACCOUNT_GROUPS:
        for account in group["accounts"]:
            connector = account["cls"]()
            records = connector.get_synthetic_records(start, end)
            n = model.add_records(records, account["name"])
            total += n
            print(f"  {account['label']}: {n} synthetic records")

    # Categorise
    categorised = asyncio.run(categorise_records(model.records))
    model._state.records = categorised

    model.save()
    print(f"\nLoaded {total:,} records across all connectors.")
    print()

    # Show initial overview
    _print_overview(model)


def _collect_credentials() -> dict[str, dict]:
    """Walk user through credential collection."""
    credentials: dict[str, dict] = {}

    for group in _ACCOUNT_GROUPS:
        print(f"--- {group['group']} ---")
        for account in group["accounts"]:
            answer = input(f"  Connect {account['label']}? (y/n): ").strip().lower()
            if answer != "y":
                continue

            creds: dict[str, str] = {}
            for field_key, field_label in account["fields"]:
                value = input(f"    {field_label}: ").strip()
                if field_key == "wallet_addresses":
                    creds[field_key] = [a.strip() for a in value.split(",")]
                else:
                    creds[field_key] = value
            credentials[account["name"]] = creds
        print()

    return credentials


async def _connect_and_fetch(
    model: FinancialModelManager,
    credentials: dict[str, dict],
    tracker: EventTracker,
) -> None:
    """Connect to each account, fetch records, categorise, save."""
    start, end = get_date_range(90)
    total = 0

    for group in _ACCOUNT_GROUPS:
        for account in group["accounts"]:
            name = account["name"]
            if name not in credentials:
                continue

            connector = account["cls"]()

            try:
                connected = await connector.connect(credentials[name])
                if not connected:
                    print(f"  {account['label']}: FAILED (check credentials)")
                    continue

                records = await connector.fetch_records(start, end)
                n = model.add_records(records, name)
                total += n

                # Summary: days of data and distinct models/services
                if records:
                    days = (max(r.record_date for r in records)
                            - min(r.record_date for r in records)).days + 1
                    services = {
                        r.model or r.subcategory or r.category.value
                        for r in records
                    }
                    print(f"  Connected {account['label']}. "
                          f"Found {days} days of data across "
                          f"{len(services)} models/services.")
                else:
                    print(f"  Connected {account['label']}. No records in range.")

                tracker.track("account_connected", "lifecycle", "openclaw",
                              {"provider": name})
            except Exception as exc:
                print(f"  {account['label']}: ERROR — {exc}")

    if total > 0:
        categorised = await categorise_records(model.records)
        model._state.records = categorised
        model.save()
        print(f"\nFetched {total:,} records. Model saved.")
    else:
        print("\nNo records fetched. Run setup again to connect accounts.")


def _print_overview(model: FinancialModelManager) -> None:
    """Print a concise first-run overview."""
    summary = model.get_summary()

    print("Your Token Economy at a Glance")
    print("-" * 40)
    print(f"Monthly spend:  {format_currency(summary.total_monthly_spend)}")

    if summary.spend_by_category:
        for cat, amount in sorted(summary.spend_by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:<28} {format_currency(amount)}")

    if summary.revenue_monthly and summary.revenue_monthly > 0:
        print(f"Monthly revenue: {format_currency(summary.revenue_monthly)}")

    if summary.crypto_holdings_usd and summary.crypto_holdings_usd > 0:
        print(f"Crypto holdings: {format_currency(summary.crypto_holdings_usd)}")
        print()
        print("Crypto balances shown for informational purposes only. "
              "This tool does not execute transactions, provide investment "
              "advice, or manage wallets.")

    print(f"\n{summary.record_count:,} records across {len(summary.connected_accounts)} accounts")


if __name__ == "__main__":
    main()
