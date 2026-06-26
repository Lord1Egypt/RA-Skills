"""Comprehensive synthetic data profile across ALL connectors.

Generates a complete test dataset representing a realistic AI-native
business's financial footprint. Use this as the canonical test fixture.
"""
from datetime import date, timedelta
from decimal import Decimal

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
from engine.models import FinancialRecord

# All connectors with their expected monthly spend profile
CONNECTOR_PROFILES: list[dict] = [
    {"name": "OpenAI",      "cls": OpenAIBillingConnector,      "monthly_est": 400},
    {"name": "Anthropic",   "cls": AnthropicBillingConnector,   "monthly_est": 250},
    {"name": "Stripe",      "cls": StripeConnector,             "monthly_est": -1800},  # revenue (positive amounts)
    {"name": "Crypto Wallet","cls": CryptoWalletConnector,       "monthly_est": 0},      # holdings, not spend
    {"name": "Coinbase",    "cls": CoinbaseExchangeConnector,   "monthly_est": 0},      # holdings
    {"name": "Binance",     "cls": BinanceExchangeConnector,    "monthly_est": 0},      # holdings
    {"name": "AWS",         "cls": AWSCostsConnector,           "monthly_est": 200},
    {"name": "GCP",         "cls": GCPCostsConnector,           "monthly_est": 150},
    {"name": "Vercel",      "cls": VercelCostsConnector,        "monthly_est": 20},
    {"name": "Cloudflare",  "cls": CloudflareCostsConnector,    "monthly_est": 8},
    {"name": "Twilio",      "cls": TwilioCostsConnector,        "monthly_est": 45},
    {"name": "SendGrid",    "cls": SendGridCostsConnector,      "monthly_est": 90},
    {"name": "Datadog",     "cls": DatadogCostsConnector,       "monthly_est": 75},
    {"name": "LangSmith",   "cls": LangSmithCostsConnector,     "monthly_est": 52},
    {"name": "Pinecone",    "cls": PineconeCostsConnector,      "monthly_est": 8},
    {"name": "Tavily",      "cls": TavilyCostsConnector,        "monthly_est": 24},
]


def generate_full_synthetic_dataset(
    days_back: int = 90,
) -> tuple[list[FinancialRecord], dict[str, list[FinancialRecord]]]:
    """Generate synthetic data from ALL connectors.

    Returns:
        (all_records, by_connector) where by_connector maps connector name
        to its individual record list.
    """
    end = date.today()
    start = end - timedelta(days=days_back)

    all_records: list[FinancialRecord] = []
    by_connector: dict[str, list[FinancialRecord]] = {}

    for profile in CONNECTOR_PROFILES:
        connector = profile["cls"]()
        records = connector.get_synthetic_records(start, end)
        by_connector[profile["name"]] = records
        all_records.extend(records)

    return all_records, by_connector


def print_summary(
    all_records: list[FinancialRecord],
    by_connector: dict[str, list[FinancialRecord]],
) -> None:
    """Print a formatted summary of the full synthetic dataset."""
    print("=" * 65)
    print("  FULL SYNTHETIC DATASET — AI-Native Business Profile")
    print("=" * 65)
    print()

    total_costs = Decimal("0")
    total_revenue = Decimal("0")
    total_holdings = Decimal("0")

    for profile in CONNECTOR_PROFILES:
        name = profile["name"]
        records = by_connector.get(name, [])
        costs = sum(r.amount for r in records if r.amount < 0)
        revenue = sum(r.amount for r in records if r.amount > 0)
        monthly_est = abs(costs) / Decimal("3") if costs else revenue / Decimal("3")

        total_costs += costs
        total_revenue += revenue

        label = f"{name} ({len(records)} records)"
        if revenue > 0 and costs < 0:
            print(f"  {label:<35} rev ${revenue:>10.2f}  costs ${abs(costs):>10.2f}")
        elif revenue > 0:
            print(f"  {label:<35} rev ${revenue:>10.2f}  (~${monthly_est:.0f}/mo)")
        elif costs < 0:
            print(f"  {label:<35}     ${abs(costs):>10.2f}  (~${monthly_est:.0f}/mo)")
        else:
            total_holdings += sum(r.amount for r in records)
            print(f"  {label:<35}     holdings: ${sum(r.amount for r in records):>10.2f}")

    print()
    print(f"  {'TOTALS':<35}")
    print(f"    Records:       {len(all_records):,}")
    print(f"    Revenue:       ${total_revenue:,.2f}")
    print(f"    Costs:         ${abs(total_costs):,.2f}")
    print(f"    Holdings:      ${total_holdings:,.2f}")
    print(f"    Net (rev-cost): ${total_revenue + total_costs:,.2f}")
    print()


if __name__ == "__main__":
    all_records, by_connector = generate_full_synthetic_dataset()
    print_summary(all_records, by_connector)
    print("Synthetic data generation complete.")
