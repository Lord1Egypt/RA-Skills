"""Token Economy Intelligence — CLI entry point.

Usage:
    uv run python -m engine.main --synthetic --status
    uv run python -m engine.main --synthetic --query "What are my biggest costs?"
    uv run python -m engine.main --synthetic --recommend
    uv run python -m engine.main --synthetic --anomalies
    uv run python -m engine.main --synthetic --providers
"""
import argparse
import asyncio
import logging
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal

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
    GeminiBillingConnector,
    GoogleAdsConnector,
    LangSmithCostsConnector,
    MetaAdsConnector,
    OpenAIBillingConnector,
    PineconeCostsConnector,
    SendGridCostsConnector,
    StripeConnector,
    TavilyCostsConnector,
    TwilioCostsConnector,
    VercelCostsConnector,
)
from engine.intelligence import (
    FinancialModelManager,
    categorise_records,
    detect_anomalies,
    generate_recommendations,
)
from engine.models import SpendCategory
from engine.utils import format_currency, format_percent, get_date_range

logger = logging.getLogger(__name__)

# All connectors grouped by function
_CONNECTOR_REGISTRY: list[dict] = [
    {"name": "OpenAI",      "group": "LLM",          "cls": OpenAIBillingConnector},
    {"name": "Anthropic",   "group": "LLM",          "cls": AnthropicBillingConnector},
    {"name": "Gemini",      "group": "LLM",          "cls": GeminiBillingConnector},
    {"name": "Google Ads",  "group": "Advertising",   "cls": GoogleAdsConnector},
    {"name": "Stripe",      "group": "Payments",      "cls": StripeConnector},
    {"name": "Meta Ads",    "group": "Advertising",   "cls": MetaAdsConnector},
    {"name": "Crypto Wallet","group": "Crypto",        "cls": CryptoWalletConnector},
    {"name": "Coinbase",    "group": "Crypto",        "cls": CoinbaseExchangeConnector},
    {"name": "Binance",     "group": "Crypto",        "cls": BinanceExchangeConnector},
    {"name": "AWS",         "group": "Infra",         "cls": AWSCostsConnector},
    {"name": "GCP",         "group": "Infra",         "cls": GCPCostsConnector},
    {"name": "Vercel",      "group": "Infra",         "cls": VercelCostsConnector},
    {"name": "Cloudflare",  "group": "Infra",         "cls": CloudflareCostsConnector},
    {"name": "Twilio",      "group": "Comms",         "cls": TwilioCostsConnector},
    {"name": "SendGrid",    "group": "Comms",         "cls": SendGridCostsConnector},
    {"name": "Datadog",     "group": "Monitoring",    "cls": DatadogCostsConnector},
    {"name": "LangSmith",   "group": "Monitoring",    "cls": LangSmithCostsConnector},
    {"name": "Pinecone",    "group": "Search/Data",   "cls": PineconeCostsConnector},
    {"name": "Tavily",      "group": "Search/Data",   "cls": TavilyCostsConnector},
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Token Economy Intelligence CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--synthetic", action="store_true", help="Use synthetic data (no real API keys)")
    parser.add_argument("--status", action="store_true", help="Show financial status overview")
    parser.add_argument("--query", type=str, help="Ask a question about your finances")
    parser.add_argument("--recommend", action="store_true", help="Get cost optimisation recommendations")
    parser.add_argument("--verbose", action="store_true", help="Show full methodology details (with --recommend)")
    parser.add_argument("--anomalies", action="store_true", help="Detect spending anomalies")
    parser.add_argument("--providers", action="store_true", help="List all connectors and their status")
    parser.add_argument("--days", type=int, default=90, help="Days of history (default: 90)")
    parser.add_argument("--state-file", type=str, default=None, help="Path to model state file")

    args = parser.parse_args()

    if not any([args.status, args.query, args.recommend, args.anomalies, args.providers]):
        parser.print_help()
        sys.exit(1)

    if args.synthetic:
        os.environ["SYNTHETIC_MODE"] = "true"

    asyncio.run(_run(args))


async def _run(args: argparse.Namespace) -> None:
    tracker = EventTracker()
    model = FinancialModelManager(state_path=args.state_file)
    model.load()

    synthetic = args.synthetic
    start_date, end_date = get_date_range(args.days)

    # ── Fetch data from all connectors ──────────────────────────
    total_new = 0
    connector_status: list[dict] = []

    for entry in _CONNECTOR_REGISTRY:
        connector = entry["cls"]()
        name = entry["name"]
        status = "disconnected"

        if synthetic:
            records = connector.get_synthetic_records(start_date, end_date)
            new_count = model.add_records(records, name.lower())
            total_new += new_count
            status = "synthetic"
        else:
            # In real mode, connect() would be called with credentials
            # from a config file or environment variables
            status = "disconnected"

        connector_status.append({
            "name": name,
            "group": entry["group"],
            "provider": connector.provider.value,
            "status": status,
            "records": len(model.records),
        })

    # ── Categorise uncategorised records ────────────────────────
    categorised = await categorise_records(model.records)
    # Replace records with categorised versions, preserving state
    model._state.records = categorised
    model._state.connected_accounts = [e["name"].lower() for e in _CONNECTOR_REGISTRY]
    model._state.last_updated = datetime.now()

    # ── Process command ─────────────────────────────────────────
    if args.providers:
        _print_providers(connector_status, synthetic)
        tracker.track("providers_listed", "ui", "cli", {"count": len(connector_status)})

    if args.status:
        _print_status(model)
        tracker.track("status_viewed", "ui", "cli")

    if args.anomalies:
        anomalies = detect_anomalies(model.records)
        _print_anomalies(anomalies)
        tracker.track("anomalies_viewed", "ui", "cli", {"count": len(anomalies)})

    if args.recommend:
        recs = generate_recommendations(model.records, as_of=end_date)
        _print_recommendations(recs, verbose=args.verbose)
        tracker.track("recommendations_viewed", "ui", "cli", {"count": len(recs)})

    if args.query:
        model.record_query(args.query)
        _print_query_response(model, args.query)
        tracker.track("query", "ui", "cli")

    # ── Save ────────────────────────────────────────────────────
    model.save()
    await tracker.close()


# ── Output formatters ───────────────────────────────────────────


def _print_providers(statuses: list[dict], synthetic: bool) -> None:
    print()
    print("=" * 60)
    print("  CONNECTORS")
    print("=" * 60)
    mode = "SYNTHETIC" if synthetic else "LIVE"
    print(f"  Mode: {mode}")
    print()

    current_group = ""
    for s in statuses:
        if s["group"] != current_group:
            current_group = s["group"]
            print(f"  {current_group}:")
        icon = "+" if s["status"] == "synthetic" else "-" if s["status"] == "connected" else " "
        print(f"    [{icon}] {s['name']:<15} ({s['provider']}) — {s['status']}")
    print()


def _print_status(model: FinancialModelManager) -> None:
    summary = model.get_summary()

    print()
    print("=" * 60)
    print("  TOKEN ECONOMY — FINANCIAL STATUS")
    print("=" * 60)
    print(f"  Last updated:  {summary.last_updated:%Y-%m-%d %H:%M}")
    print(f"  Data coverage: {summary.data_coverage_days} days, {summary.record_count:,} records")
    print(f"  Connected:     {', '.join(summary.connected_accounts)}")
    print()

    # ── Spend by category ───────────────────────────────────────
    print("  MONTHLY SPEND BY CATEGORY")
    print("  " + "-" * 45)

    # Use friendly labels
    category_labels = {
        "ai_inference": "AI Inference",
        "ai_training": "AI Training",
        "cloud_infrastructure": "Cloud Infrastructure",
        "saas_subscription": "SaaS Subscriptions",
        "payment_processing": "Payment Processing",
        "communication": "Communication",
        "monitoring": "Monitoring",
        "search_data": "Search & Data",
        "advertising": "Advertising",
        "crypto_holdings": "Crypto Holdings",
        "revenue": "Revenue",
        "other": "Other",
    }

    if summary.spend_by_category:
        sorted_cats = sorted(
            summary.spend_by_category.items(), key=lambda x: x[1], reverse=True
        )
        for cat, amount in sorted_cats:
            label = category_labels.get(cat, cat)
            bar_len = min(30, int(float(amount) / float(summary.total_monthly_spend) * 30)) if summary.total_monthly_spend > 0 else 0
            bar = "#" * bar_len
            print(f"    {label:<25} {format_currency(amount):>10}  {bar}")
    print(f"    {'TOTAL':<25} {format_currency(summary.total_monthly_spend):>10}")
    print()

    # ── Spend by provider ───────────────────────────────────────
    print("  MONTHLY SPEND BY PROVIDER")
    print("  " + "-" * 45)
    if summary.spend_by_provider:
        sorted_provs = sorted(
            summary.spend_by_provider.items(), key=lambda x: x[1], reverse=True
        )
        for prov, amount in sorted_provs:
            print(f"    {prov:<25} {format_currency(amount):>10}")
    print()

    # ── Revenue & margin ────────────────────────────────────────
    if summary.revenue_monthly is not None:
        print(f"  Monthly revenue:  {format_currency(summary.revenue_monthly)}")
        if summary.total_monthly_spend > 0:
            margin = float(
                (summary.revenue_monthly - summary.total_monthly_spend)
                / summary.revenue_monthly * 100
            )
            print(f"  Gross margin:     {format_percent(margin)}")
        print()

    if summary.crypto_holdings_usd is not None and summary.crypto_holdings_usd > 0:
        print(f"  Crypto holdings:  {format_currency(summary.crypto_holdings_usd)}")
        print()


def _print_anomalies(anomalies: list) -> None:
    print()
    print("=" * 60)
    print("  SPENDING ANOMALIES")
    print("=" * 60)

    if not anomalies:
        print("  No anomalies detected.")
        print()
        return

    for a in anomalies:
        severity_icon = {"critical": "!!", "high": "!", "medium": "~"}
        icon = severity_icon.get(a.severity, " ")
        print(f"  [{icon}] {a.severity.upper()}: {a.description}")
        print(f"      Current: {format_currency(a.current_amount)}  |  "
              f"Baseline: {format_currency(a.baseline_amount)}  |  "
              f"Deviation: {format_percent(a.deviation_percent)}")
        print()


def _print_recommendations(recs: list, verbose: bool = False) -> None:
    print()

    if not recs:
        print("  No recommendations at this time.")
        print()
        return

    if verbose:
        _print_recommendations_verbose(recs)
    else:
        _print_recommendations_concise(recs)


def _print_recommendations_concise(recs: list) -> None:
    """Top 5 recommendations, one line each + total savings."""
    top = recs[:5]
    total_savings = sum(
        r.estimated_monthly_savings for r in recs
        if r.estimated_monthly_savings
    )

    print("=" * 60)
    print("  TOP 5 COST OPTIMISATIONS")
    print("=" * 60)
    print()

    for i, r in enumerate(top, 1):
        savings = format_currency(r.estimated_monthly_savings) if r.estimated_monthly_savings else "N/A"
        # Build a short description from rec_type
        label = r.rec_type.replace("_", " ").title()
        # Truncate description to first sentence
        short_desc = r.description.split(". ")[0]
        if len(short_desc) > 70:
            short_desc = short_desc[:67] + "..."
        action = r.action_required.split(". ")[0]
        if len(action) > 50:
            action = action[:47] + "..."

        print(f"  {i}. {label}: {short_desc}")
        print(f"     -> {savings}/mo | Action: {action}")
        print()

    print(f"  Total potential savings: {format_currency(total_savings)}/mo")
    if len(recs) > 5:
        print(f"  ({len(recs) - 5} more recommendations available)")
    print("  Run with --verbose for full methodology.")
    print()


def _print_recommendations_verbose(recs: list) -> None:
    """Full details for all recommendations."""
    print("=" * 60)
    print("  COST OPTIMISATION RECOMMENDATIONS (VERBOSE)")
    print("=" * 60)
    print()

    for i, r in enumerate(recs, 1):
        savings = format_currency(r.estimated_monthly_savings) + "/mo" if r.estimated_monthly_savings else "N/A"
        source = f" via {r.source_module}" if r.source_module else ""
        print(f"  {i}. [{r.rec_type}]{source} (confidence: {r.confidence})")
        print(f"     {r.description}")
        print(f"     Estimated savings: {savings}")
        if r.methodology:
            print(f"     Methodology: {r.methodology}")
        print(f"     Action: {r.action_required}")
        print()


_CATEGORY_KEYWORDS: list[tuple[list[str], SpendCategory, str]] = [
    (["ai inference", "ai spend", "llm", "model cost", "openai", "anthropic", "gpt", "claude"],
     SpendCategory.AI_INFERENCE, "AI Inference"),
    (["ai training", "fine-tun", "finetun", "training"],
     SpendCategory.AI_TRAINING, "AI Training"),
    (["cloud", "infrastructure", "aws", "gcp", "vercel", "cloudflare", "hosting", "compute"],
     SpendCategory.CLOUD_INFRASTRUCTURE, "Cloud Infrastructure"),
    (["saas", "subscription", "software"],
     SpendCategory.SAAS_SUBSCRIPTION, "SaaS Subscriptions"),
    (["payment process", "stripe fee", "processing fee"],
     SpendCategory.PAYMENT_PROCESSING, "Payment Processing"),
    (["communication", "twilio", "sendgrid", "sms", "email", "messaging"],
     SpendCategory.COMMUNICATION, "Communication"),
    (["monitoring", "datadog", "langsmith", "observability", "tracing", "apm"],
     SpendCategory.MONITORING, "Monitoring"),
    (["search", "data", "pinecone", "tavily", "vector", "retrieval"],
     SpendCategory.SEARCH_DATA, "Search & Data"),
    (["crypto", "wallet", "bitcoin", "ethereum", "holdings"],
     SpendCategory.CRYPTO_HOLDINGS, "Crypto Holdings"),
    (["revenue", "income", "sales", "earnings"],
     SpendCategory.REVENUE, "Revenue"),
]

_PROVIDER_KEYWORDS: dict[str, str] = {
    "openai": "openai", "anthropic": "anthropic", "stripe": "stripe",
    "aws": "aws", "gcp": "gcp", "vercel": "vercel", "cloudflare": "cloudflare",
    "twilio": "twilio", "sendgrid": "sendgrid", "datadog": "datadog",
    "langsmith": "langsmith", "pinecone": "pinecone", "tavily": "tavily",
}


def _match_category(query_lower: str) -> tuple[SpendCategory | None, str]:
    """Match a query string to a SpendCategory via keywords."""
    for keywords, category, label in _CATEGORY_KEYWORDS:
        if any(kw in query_lower for kw in keywords):
            return category, label
    return None, ""


def _match_provider(query_lower: str) -> str | None:
    """Match a query string to a provider name."""
    for keyword, provider_value in _PROVIDER_KEYWORDS.items():
        if keyword in query_lower:
            return provider_value
    return None


def _print_query_response(model: FinancialModelManager, query: str) -> None:
    """Answer a query using the financial model context.

    Parses query intent to identify category/provider, then shows
    a filtered breakdown. Falls back to full summary if no match.
    """
    print()
    print("=" * 60)
    print(f"  QUERY: {query}")
    print("=" * 60)

    summary = model.get_summary()
    records = model.records
    query_lower = query.lower()
    thirty_days_ago = (date.today() - timedelta(days=30))
    recent = [r for r in records if r.record_date >= thirty_days_ago]

    # ── 1. Try category match first ─────────────────────────────
    matched_cat, cat_label = _match_category(query_lower)
    matched_provider = _match_provider(query_lower)

    if matched_cat is not None:
        _print_category_breakdown(recent, matched_cat, cat_label)
        return

    if matched_provider is not None:
        _print_provider_breakdown(recent, matched_provider)
        return

    # ── 2. General intent keywords ──────────────────────────────
    if any(w in query_lower for w in ["biggest", "largest", "top", "most"]):
        print("  Top spend categories (last 30 days):")
        if summary.spend_by_category:
            sorted_cats = sorted(
                summary.spend_by_category.items(), key=lambda x: x[1], reverse=True
            )
            for cat, amount in sorted_cats[:5]:
                print(f"    {cat:<30} {format_currency(amount)}")
        print()
        return

    if any(w in query_lower for w in ["total", "how much", "overview"]):
        print(f"  Total monthly spend: {format_currency(summary.total_monthly_spend)}")
        if summary.revenue_monthly:
            print(f"  Monthly revenue:     {format_currency(summary.revenue_monthly)}")
            if summary.total_monthly_spend > 0:
                margin = float(
                    (summary.revenue_monthly - summary.total_monthly_spend)
                    / summary.revenue_monthly * 100
                )
                print(f"  Gross margin:        {format_percent(margin)}")
        print()
        return

    # ── 3. Fallback: full context ───────────────────────────────
    print()
    print(model.get_context_for_llm())
    print()
    print("  (In live mode, this context would be sent to Claude for a detailed answer.)")
    print()


def _print_category_breakdown(
    records: list, category: SpendCategory, label: str
) -> None:
    """Show a detailed breakdown for a specific category."""
    filtered = [r for r in records if r.category == category]

    if not filtered:
        print(f"  No {label} records in the last 30 days.")
        print()
        return

    total = sum(abs(r.amount) for r in filtered)
    print(f"  {label} — Last 30 Days")
    print(f"  Total: {format_currency(total)}")
    print()

    # Break down by subcategory or model (whichever is populated)
    by_sub: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        key = r.model or r.subcategory or r.provider.value
        by_sub[key] += abs(r.amount)

    if by_sub:
        print("  Breakdown:")
        sorted_subs = sorted(by_sub.items(), key=lambda x: x[1], reverse=True)
        for sub, amount in sorted_subs:
            pct = float(amount / total * 100) if total > 0 else 0
            print(f"    {sub:<35} {format_currency(amount):>10}  ({pct:.1f}%)")
        print()

    # Provider breakdown (if multiple providers in this category)
    by_prov: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        by_prov[r.provider.value] += abs(r.amount)
    if len(by_prov) > 1:
        print("  By provider:")
        for prov, amount in sorted(by_prov.items(), key=lambda x: x[1], reverse=True):
            print(f"    {prov:<35} {format_currency(amount):>10}")
        print()

    # Record count and date range
    earliest = min(r.record_date for r in filtered)
    latest = max(r.record_date for r in filtered)
    print(f"  {len(filtered)} records from {earliest} to {latest}")
    print()


def _print_provider_breakdown(records: list, provider_value: str) -> None:
    """Show a detailed breakdown for a specific provider."""
    filtered = [r for r in records if r.provider.value == provider_value]

    if not filtered:
        print(f"  No {provider_value} records in the last 30 days.")
        print()
        return

    costs = [r for r in filtered if r.amount < 0]
    revenue = [r for r in filtered if r.amount > 0]
    total_cost = sum(abs(r.amount) for r in costs)
    total_rev = sum(r.amount for r in revenue)

    print(f"  {provider_value.upper()} — Last 30 Days")
    if total_cost > 0:
        print(f"  Costs: {format_currency(total_cost)}")
    if total_rev > 0:
        print(f"  Revenue: {format_currency(total_rev)}")
    print()

    # By subcategory/model
    by_sub: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        key = r.model or r.subcategory or r.category.value
        by_sub[key] += abs(r.amount)

    if by_sub:
        print("  Breakdown:")
        for sub, amount in sorted(by_sub.items(), key=lambda x: x[1], reverse=True):
            print(f"    {sub:<35} {format_currency(amount):>10}")
        print()

    print(f"  {len(filtered)} records")
    print()


if __name__ == "__main__":
    main()
