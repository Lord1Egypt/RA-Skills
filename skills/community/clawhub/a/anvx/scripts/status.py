"""Quick financial overview — refreshes data if stale."""
import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from engine.analytics import EventTracker
from engine.intelligence import (
    FinancialModelManager,
    categorise_records,
    detect_anomalies,
)
from engine.utils import format_currency, format_percent, get_date_range, is_synthetic_mode

_STALE_HOURS = 24


def main() -> None:
    tracker = EventTracker()
    refresh = "--refresh" in sys.argv

    model = FinancialModelManager()
    model.load()

    summary = model.get_summary()

    if summary.record_count == 0:
        print("No data yet. Run setup.py first.")
        sys.exit(1)

    # Check staleness
    hours_since = (datetime.now() - summary.last_updated).total_seconds() / 3600
    if refresh or hours_since > _STALE_HOURS:
        if is_synthetic_mode() or os.getenv("SYNTHETIC_MODE", "").lower() == "true":
            _refresh_synthetic(model)
        else:
            print(f"Data is {hours_since:.0f}h old. Refresh with live connectors not yet implemented.")
            print("Showing cached data.\n")

    summary = model.get_summary()

    # Header
    print(f"Token Economy — {summary.last_updated:%Y-%m-%d %H:%M}")
    print(f"{summary.record_count:,} records | {summary.data_coverage_days} days | {len(summary.connected_accounts)} accounts")
    print()

    # Spend by category
    print(f"Monthly spend: {format_currency(summary.total_monthly_spend)}")
    if summary.spend_by_category:
        for cat, amount in sorted(summary.spend_by_category.items(), key=lambda x: x[1], reverse=True):
            pct = float(amount / summary.total_monthly_spend * 100) if summary.total_monthly_spend else 0
            print(f"  {cat:<28} {format_currency(amount):>10}  ({pct:.1f}%)")
    print()

    # Revenue
    if summary.revenue_monthly and summary.revenue_monthly > 0:
        print(f"Monthly revenue: {format_currency(summary.revenue_monthly)}")
        if summary.total_monthly_spend > 0:
            margin = float(
                (summary.revenue_monthly - summary.total_monthly_spend)
                / summary.revenue_monthly * 100
            )
            print(f"Gross margin: {format_percent(margin)}")
        print()

    # Crypto
    if summary.crypto_holdings_usd and summary.crypto_holdings_usd > 0:
        print(f"Crypto holdings: {format_currency(summary.crypto_holdings_usd)}")
        print("Crypto balances shown for informational purposes only. "
              "This tool does not execute transactions, provide investment "
              "advice, or manage wallets.")
        print()

    # Anomalies
    anomalies = detect_anomalies(model.records)
    if anomalies:
        print(f"Anomalies detected ({len(anomalies)}):")
        for a in anomalies[:3]:
            print(f"  [{a.severity.upper()}] {a.description}")
        if len(anomalies) > 3:
            print(f"  ... and {len(anomalies) - 3} more")
        print()

    tracker.track("status_viewed", "ui", "openclaw")
    model.save()


def _refresh_synthetic(model: FinancialModelManager) -> None:
    """Reload synthetic data for all connectors."""
    from engine.connectors import (
        AWSCostsConnector, AnthropicBillingConnector, BinanceExchangeConnector,
        CloudflareCostsConnector, CoinbaseExchangeConnector,
        CryptoWalletConnector, DatadogCostsConnector, GCPCostsConnector,
        LangSmithCostsConnector, OpenAIBillingConnector, PineconeCostsConnector,
        SendGridCostsConnector, StripeConnector, TavilyCostsConnector,
        TwilioCostsConnector, VercelCostsConnector,
    )

    connectors = [
        ("openai", OpenAIBillingConnector), ("anthropic", AnthropicBillingConnector),
        ("stripe", StripeConnector), ("crypto_wallet", CryptoWalletConnector),
        ("coinbase", CoinbaseExchangeConnector), ("binance", BinanceExchangeConnector),
        ("aws", AWSCostsConnector), ("gcp", GCPCostsConnector),
        ("vercel", VercelCostsConnector), ("cloudflare", CloudflareCostsConnector),
        ("twilio", TwilioCostsConnector), ("sendgrid", SendGridCostsConnector),
        ("datadog", DatadogCostsConnector), ("langsmith", LangSmithCostsConnector),
        ("pinecone", PineconeCostsConnector), ("tavily", TavilyCostsConnector),
    ]

    start, end = get_date_range(90)
    model.reset()
    for name, cls in connectors:
        records = cls().get_synthetic_records(start, end)
        model.add_records(records, name)

    categorised = asyncio.run(categorise_records(model.records))
    model._state.records = categorised
    model.save()


if __name__ == "__main__":
    main()
