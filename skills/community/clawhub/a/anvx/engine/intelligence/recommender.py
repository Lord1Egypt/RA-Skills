"""Cross-bucket recommendation engine for token economy optimisation.

Uses a modular system: each OptimizationModule analyses records independently
and produces recommendations with specific dollar savings and methodology.
Real-time pricing is fetched via PricingFetcher (cached daily).
"""
import logging
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from engine.intelligence.pricing_fetcher import PricingFetcher
from engine.intelligence.optimization import ALL_MODULES
from engine.models import (
    FinancialRecord,
    FinancialSummary,
    Recommendation,
    SpendCategory,
)

logger = logging.getLogger(__name__)

_INACTIVE_DAYS = 30
_MAX_RECOMMENDATIONS = 10


def generate_recommendations(
    records: list[FinancialRecord],
    as_of: date | None = None,
    summary: FinancialSummary | None = None,
) -> list[Recommendation]:
    """Analyse records across all buckets and generate optimisation recommendations.

    Runs all optimization modules plus legacy checks. Each recommendation
    includes its source module, estimated savings, and calculation methodology.

    Args:
        records: All financial records across all connectors.
        as_of: Reference date for calculations. Defaults to today.
        summary: Pre-computed summary. Built from records if not provided.

    Returns:
        Top recommendations sorted by estimated savings (highest first).
    """
    if not records:
        return []

    if as_of is None:
        as_of = date.today()

    # Build summary if not provided
    if summary is None:
        summary = _build_quick_summary(records, as_of)

    # Initialize pricing fetcher (uses cache if available)
    pricing = PricingFetcher()
    pricing.load()

    recommendations: list[Recommendation] = []

    # Run each optimization module
    for module_cls in ALL_MODULES:
        module = module_cls()
        try:
            module_recs = module.analyse(records, summary, pricing)
            recommendations.extend(module_recs)
            if module_recs:
                logger.info(
                    "Module %s produced %d recommendations",
                    module.name, len(module_recs),
                )
        except Exception as exc:
            logger.warning("Module %s failed: %s", module.name, exc)

    # Legacy check: unused subscriptions (no pricing needed)
    recommendations.extend(_check_unused_subscriptions(records, as_of))

    # Sort by estimated savings descending (None last)
    recommendations.sort(
        key=lambda r: r.estimated_monthly_savings or Decimal("0"),
        reverse=True,
    )

    return recommendations[:_MAX_RECOMMENDATIONS]


def _build_quick_summary(
    records: list[FinancialRecord], as_of: date
) -> FinancialSummary:
    """Build a minimal FinancialSummary from records for module use."""
    from datetime import datetime

    thirty_days_ago = as_of - timedelta(days=30)
    recent = [r for r in records if r.record_date >= thirty_days_ago]

    spend_by_cat: dict[str, Decimal] = defaultdict(Decimal)
    spend_by_prov: dict[str, Decimal] = defaultdict(Decimal)
    revenue = Decimal("0")
    crypto = Decimal("0")

    for r in recent:
        if r.category == SpendCategory.REVENUE:
            revenue += r.amount
        elif r.category == SpendCategory.CRYPTO_HOLDINGS:
            crypto += r.amount
        else:
            spend_by_cat[r.category.value] += abs(r.amount)
            spend_by_prov[r.provider.value] += abs(r.amount)

    dates = [r.record_date for r in records]
    coverage = (max(dates) - min(dates)).days + 1 if dates else 0

    return FinancialSummary(
        last_updated=datetime.now(),
        total_monthly_spend=sum(spend_by_cat.values()),
        spend_by_category=dict(spend_by_cat),
        spend_by_provider=dict(spend_by_prov),
        revenue_monthly=revenue if revenue > 0 else None,
        crypto_holdings_usd=crypto if crypto > 0 else None,
        data_coverage_days=coverage,
        record_count=len(records),
    )


def _check_unused_subscriptions(
    records: list[FinancialRecord], as_of: date
) -> list[Recommendation]:
    """Flag SaaS subscriptions with no activity in 30+ days."""
    recs: list[Recommendation] = []

    saas_records: dict[str, list[FinancialRecord]] = defaultdict(list)
    for r in records:
        if r.category == SpendCategory.SAAS_SUBSCRIPTION:
            key = r.subcategory or r.source
            saas_records[key].append(r)

    cutoff = as_of - timedelta(days=_INACTIVE_DAYS)

    for service_name, service_records in saas_records.items():
        last_record = max(r.record_date for r in service_records)
        if last_record >= cutoff:
            continue

        days_inactive = (as_of - last_record).days
        total_cost = sum(abs(r.amount) for r in service_records)
        date_span = (
            max(r.record_date for r in service_records)
            - min(r.record_date for r in service_records)
        ).days or 1
        monthly_cost = (
            total_cost * Decimal("30") / Decimal(str(date_span))
        ).quantize(Decimal("0.01"))

        recs.append(
            Recommendation(
                rec_type="unused_subscription",
                description=(
                    f"No activity from '{service_name}' in {days_inactive} days. "
                    f"Estimated ~${monthly_cost}/month"
                ),
                estimated_monthly_savings=monthly_cost,
                confidence="medium",
                action_required=(
                    f"Review whether '{service_name}' subscription is still needed. "
                    f"Cancel or downgrade if unused."
                ),
                category=SpendCategory.SAAS_SUBSCRIPTION,
                source_module="unused_subscriptions",
                methodology=(
                    f"Last activity: {last_record.isoformat()} ({days_inactive} days ago). "
                    f"Monthly cost estimated from ${total_cost:.2f} over "
                    f"{date_span} days of data."
                ),
            )
        )

    return recs
