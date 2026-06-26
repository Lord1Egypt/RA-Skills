"""Unit economics module — analyses cost structure relative to revenue."""
import logging
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal

from engine.intelligence.optimization.base_module import OptimizationModule
from engine.intelligence.pricing_fetcher import PricingFetcher
from engine.models import (
    FinancialRecord,
    FinancialSummary,
    Recommendation,
    SpendCategory,
)

logger = logging.getLogger(__name__)


class UnitEconomicsModule(OptimizationModule):
    """Analyses unit economics using actual revenue and cost data.

    Only activates when BOTH Stripe revenue AND cost data are present.
    All calculations are derived from the user's data — nothing assumed.
    """

    name = "unit_economics"
    description = "Analyse cost-to-revenue ratios and margin trajectory"
    required_providers = ["stripe"]

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        if not records:
            return recs

        # Split into cost and revenue records
        cost_records = [r for r in records if r.amount < 0]
        revenue_records = [
            r for r in records
            if r.category == SpendCategory.REVENUE and r.amount > 0
        ]

        if not revenue_records or not cost_records:
            return recs

        # Calculate monthly aggregates for trend analysis
        monthly_costs: dict[str, Decimal] = defaultdict(Decimal)
        monthly_revenue: dict[str, Decimal] = defaultdict(Decimal)
        monthly_ai_costs: dict[str, Decimal] = defaultdict(Decimal)

        for r in cost_records:
            month_key = r.record_date.strftime("%Y-%m")
            monthly_costs[month_key] += abs(r.amount)
            if r.category in (SpendCategory.AI_INFERENCE, SpendCategory.AI_TRAINING):
                monthly_ai_costs[month_key] += abs(r.amount)

        for r in revenue_records:
            month_key = r.record_date.strftime("%Y-%m")
            monthly_revenue[month_key] += r.amount

        # Need at least 2 months for growth rate calculation
        months = sorted(set(monthly_costs.keys()) & set(monthly_revenue.keys()))
        if len(months) < 2:
            return recs

        # Drop partial last month (<20 days) to avoid artificial decline
        last_month_cost_records = [
            r for r in cost_records
            if r.record_date.strftime("%Y-%m") == months[-1]
        ]
        if last_month_cost_records:
            last_month_days = len({r.record_date for r in last_month_cost_records})
            if last_month_days < 20:
                months = months[:-1]
        if len(months) < 2:
            return recs

        # Current month (most recent)
        current_month = months[-1]
        current_costs = monthly_costs[current_month]
        current_revenue = monthly_revenue[current_month]
        current_ai_costs = monthly_ai_costs.get(current_month, Decimal("0"))

        if current_revenue <= 0:
            return recs

        # Derived metrics
        gross_margin = float((current_revenue - current_costs) / current_revenue * 100)
        ai_cost_ratio = float(current_ai_costs / current_revenue * 100)

        # Count revenue events as proxy for customer transactions
        recent_revenue = [
            r for r in revenue_records
            if r.record_date.strftime("%Y-%m") == current_month
        ]
        charge_count = len(recent_revenue)
        if charge_count == 0:
            return recs

        revenue_per_charge = current_revenue / Decimal(str(charge_count))
        cost_per_charge = current_costs / Decimal(str(charge_count))
        ai_cost_per_charge = current_ai_costs / Decimal(str(charge_count))

        # Calculate month-over-month growth rates from data
        cost_growth_rates: list[float] = []
        revenue_growth_rates: list[float] = []
        for i in range(1, len(months)):
            prev_cost = monthly_costs.get(months[i - 1], Decimal("0"))
            curr_cost = monthly_costs.get(months[i], Decimal("0"))
            if prev_cost > 0:
                cost_growth_rates.append(float((curr_cost - prev_cost) / prev_cost))

            prev_rev = monthly_revenue.get(months[i - 1], Decimal("0"))
            curr_rev = monthly_revenue.get(months[i], Decimal("0"))
            if prev_rev > 0:
                revenue_growth_rates.append(float((curr_rev - prev_rev) / prev_rev))

        avg_cost_growth = (
            sum(cost_growth_rates) / len(cost_growth_rates)
            if cost_growth_rates
            else 0
        )
        avg_revenue_growth = (
            sum(revenue_growth_rates) / len(revenue_growth_rates)
            if revenue_growth_rates
            else 0
        )

        # Project forward 3 and 6 months
        projected_costs_3m = float(current_costs) * (1 + avg_cost_growth) ** 3
        projected_revenue_3m = float(current_revenue) * (1 + avg_revenue_growth) ** 3
        projected_margin_3m = (
            (projected_revenue_3m - projected_costs_3m) / projected_revenue_3m * 100
            if projected_revenue_3m > 0
            else 0
        )

        projected_costs_6m = float(current_costs) * (1 + avg_cost_growth) ** 6
        projected_revenue_6m = float(current_revenue) * (1 + avg_revenue_growth) ** 6
        projected_margin_6m = (
            (projected_revenue_6m - projected_costs_6m) / projected_revenue_6m * 100
            if projected_revenue_6m > 0
            else 0
        )

        # Flag if margin is declining or AI costs are high
        margin_warning = projected_margin_6m < 50 or ai_cost_ratio > 30
        if not margin_warning:
            return recs

        # Estimated savings: the excess AI spend above 20% of revenue
        target_ai_ratio = Decimal("0.20")
        target_ai_cost = current_revenue * target_ai_ratio
        excess = current_ai_costs - target_ai_cost
        monthly_savings = max(Decimal("0"), excess).quantize(Decimal("0.01"))

        if monthly_savings <= Decimal("0"):
            return recs

        recs.append(
            Recommendation(
                rec_type="unit_economics",
                description=(
                    f"AI costs are {ai_cost_ratio:.1f}% of revenue "
                    f"(${current_ai_costs:.2f} vs ${current_revenue:.2f}). "
                    f"Gross margin: {gross_margin:.1f}%. "
                    f"At current growth rates, margin will be "
                    f"{projected_margin_3m:.0f}% in 3 months "
                    f"and {projected_margin_6m:.0f}% in 6 months."
                ),
                estimated_monthly_savings=monthly_savings,
                confidence="high" if len(months) >= 3 else "medium",
                action_required=(
                    f"Reduce AI inference costs to below 20% of revenue "
                    f"(target: ${target_ai_cost:.2f}/mo). "
                    f"Consider model routing, caching, and batch optimizations."
                ),
                category=SpendCategory.AI_INFERENCE,
                source_module=self.name,
                methodology=(
                    f"Derived from {len(months)} months of data. "
                    f"Current: revenue=${current_revenue:.2f}, "
                    f"total costs=${current_costs:.2f}, "
                    f"AI costs=${current_ai_costs:.2f} ({ai_cost_ratio:.1f}% of rev). "
                    f"Per charge ({charge_count} charges): "
                    f"rev=${revenue_per_charge:.2f}, "
                    f"cost=${cost_per_charge:.2f}, "
                    f"AI=${ai_cost_per_charge:.2f}. "
                    f"Cost growth: {avg_cost_growth*100:+.1f}%/mo, "
                    f"revenue growth: {avg_revenue_growth*100:+.1f}%/mo "
                    f"(calculated from your billing data). "
                    f"6-month projection: costs=${projected_costs_6m:.0f}, "
                    f"revenue=${projected_revenue_6m:.0f}, "
                    f"margin={projected_margin_6m:.0f}%."
                ),
            )
        )

        return recs
