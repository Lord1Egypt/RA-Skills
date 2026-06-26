"""Answer a spending question using the financial model."""
import asyncio
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from engine.analytics import EventTracker
from engine.intelligence import FinancialModelManager
from engine.models import FinancialRecord, SpendCategory
from engine.utils import format_currency, format_percent

_CATEGORY_KEYWORDS: list[tuple[list[str], SpendCategory, str]] = [
    (["ai inference", "ai spend", "llm", "model cost", "openai cost", "anthropic cost", "gpt", "claude"],
     SpendCategory.AI_INFERENCE, "AI Inference"),
    (["ai training", "fine-tun", "training"],
     SpendCategory.AI_TRAINING, "AI Training"),
    (["cloud", "infrastructure", "aws", "gcp", "vercel", "cloudflare", "hosting"],
     SpendCategory.CLOUD_INFRASTRUCTURE, "Cloud Infrastructure"),
    (["saas", "subscription"],
     SpendCategory.SAAS_SUBSCRIPTION, "SaaS Subscriptions"),
    (["payment process", "stripe fee"],
     SpendCategory.PAYMENT_PROCESSING, "Payment Processing"),
    (["communication", "twilio", "sendgrid", "sms", "email"],
     SpendCategory.COMMUNICATION, "Communication"),
    (["monitoring", "datadog", "langsmith", "observability"],
     SpendCategory.MONITORING, "Monitoring"),
    (["search", "pinecone", "tavily", "vector"],
     SpendCategory.SEARCH_DATA, "Search & Data"),
    (["crypto", "wallet", "bitcoin", "ethereum"],
     SpendCategory.CRYPTO_HOLDINGS, "Crypto Holdings"),
    (["revenue", "income", "sales", "stripe revenue"],
     SpendCategory.REVENUE, "Revenue"),
]

_PROVIDER_KEYWORDS: dict[str, str] = {
    "openai": "openai", "anthropic": "anthropic", "stripe": "stripe",
    "aws": "aws", "gcp": "gcp", "vercel": "vercel", "cloudflare": "cloudflare",
    "twilio": "twilio", "sendgrid": "sendgrid", "datadog": "datadog",
    "langsmith": "langsmith", "pinecone": "pinecone", "tavily": "tavily",
}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: query.py \"<your question>\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    tracker = EventTracker()

    model = FinancialModelManager()
    model.load()

    if model.get_summary().record_count == 0:
        print("No data yet. Run setup.py first.")
        sys.exit(1)

    model.record_query(question)
    query_lower = question.lower()
    thirty_days_ago = date.today() - timedelta(days=30)
    recent = [r for r in model.records if r.record_date >= thirty_days_ago]

    # Match category
    for keywords, category, label in _CATEGORY_KEYWORDS:
        if any(kw in query_lower for kw in keywords):
            _show_category(recent, category, label)
            tracker.track("query", "intelligence", "openclaw",
                          {"intent": "category", "category": category.value})
            model.save()
            return

    # Match provider
    for keyword, provider in _PROVIDER_KEYWORDS.items():
        if keyword in query_lower:
            _show_provider(recent, provider)
            tracker.track("query", "intelligence", "openclaw",
                          {"intent": "provider", "provider": provider})
            model.save()
            return

    # Top/biggest
    if any(w in query_lower for w in ["biggest", "largest", "top", "most"]):
        _show_top_categories(model)
        tracker.track("query", "intelligence", "openclaw", {"intent": "top"})
        model.save()
        return

    # Total/overview
    if any(w in query_lower for w in ["total", "how much", "overview", "summary"]):
        _show_total(model)
        tracker.track("query", "intelligence", "openclaw", {"intent": "total"})
        model.save()
        return

    # Fallback: show LLM context
    print(model.get_context_for_llm())
    tracker.track("query", "intelligence", "openclaw", {"intent": "fallback"})
    model.save()


def _show_category(records: list[FinancialRecord], category: SpendCategory, label: str) -> None:
    filtered = [r for r in records if r.category == category]
    if not filtered:
        print(f"No {label} spending in the last 30 days.")
        return

    total = sum(abs(r.amount) for r in filtered)
    print(f"{label}: {format_currency(total)} (last 30 days)")
    print()

    by_sub: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        key = r.model or r.subcategory or r.provider.value
        by_sub[key] += abs(r.amount)

    for sub, amount in sorted(by_sub.items(), key=lambda x: x[1], reverse=True):
        pct = float(amount / total * 100) if total else 0
        print(f"  {sub:<32} {format_currency(amount):>10}  ({pct:.1f}%)")

    by_prov: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        by_prov[r.provider.value] += abs(r.amount)
    if len(by_prov) > 1:
        print()
        for prov, amount in sorted(by_prov.items(), key=lambda x: x[1], reverse=True):
            print(f"  via {prov}: {format_currency(amount)}")

    if category == SpendCategory.CRYPTO_HOLDINGS:
        print()
        print("Crypto balances shown for informational purposes only. "
              "This tool does not execute transactions, provide investment "
              "advice, or manage wallets.")


def _show_provider(records: list[FinancialRecord], provider: str) -> None:
    filtered = [r for r in records if r.provider.value == provider]
    if not filtered:
        print(f"No {provider} records in the last 30 days.")
        return

    costs = sum(abs(r.amount) for r in filtered if r.amount < 0)
    revenue = sum(r.amount for r in filtered if r.amount > 0)

    print(f"{provider.upper()} (last 30 days)")
    if costs > 0:
        print(f"  Costs: {format_currency(costs)}")
    if revenue > 0:
        print(f"  Revenue: {format_currency(revenue)}")
    print()

    by_sub: dict[str, Decimal] = defaultdict(Decimal)
    for r in filtered:
        key = r.model or r.subcategory or r.category.value
        by_sub[key] += abs(r.amount)

    for sub, amount in sorted(by_sub.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sub:<32} {format_currency(amount):>10}")


def _show_top_categories(model: FinancialModelManager) -> None:
    s = model.get_summary()
    print(f"Top spend categories (last 30 days):")
    print(f"Total: {format_currency(s.total_monthly_spend)}")
    print()
    if s.spend_by_category:
        for cat, amount in sorted(s.spend_by_category.items(), key=lambda x: x[1], reverse=True):
            pct = float(amount / s.total_monthly_spend * 100) if s.total_monthly_spend else 0
            print(f"  {cat:<28} {format_currency(amount):>10}  ({pct:.1f}%)")


def _show_total(model: FinancialModelManager) -> None:
    s = model.get_summary()
    print(f"Monthly spend: {format_currency(s.total_monthly_spend)}")
    if s.revenue_monthly and s.revenue_monthly > 0:
        print(f"Monthly revenue: {format_currency(s.revenue_monthly)}")
        margin = float((s.revenue_monthly - s.total_monthly_spend) / s.revenue_monthly * 100)
        print(f"Gross margin: {format_percent(margin)}")


if __name__ == "__main__":
    main()
