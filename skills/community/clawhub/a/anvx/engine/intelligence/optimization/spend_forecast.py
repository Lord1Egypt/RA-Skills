"""Spend forecast module — projects costs forward using actual historical growth rates."""
import logging
import math
from collections import defaultdict
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

_MIN_DAYS_FOR_FORECAST = 60


class SpendForecastModule(OptimizationModule):
    """Projects spend forward using growth rates calculated from the user's data.

    Requires minimum 60 days of data. Calculates compound monthly growth rate
    per category and overall. Flags if costs are growing faster than revenue.
    """

    name = "spend_forecast"
    description = "Project future spend based on historical growth trends"

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        if not records:
            return recs

        # Check data coverage
        dates = [r.record_date for r in records]
        date_span = (max(dates) - min(dates)).days
        if date_span < _MIN_DAYS_FOR_FORECAST:
            return recs

        # Aggregate monthly costs by category
        monthly_by_cat: dict[str, dict[str, Decimal]] = defaultdict(
            lambda: defaultdict(Decimal)
        )
        monthly_total_cost: dict[str, Decimal] = defaultdict(Decimal)
        monthly_revenue: dict[str, Decimal] = defaultdict(Decimal)

        for r in records:
            month_key = r.record_date.strftime("%Y-%m")
            if r.category == SpendCategory.REVENUE and r.amount > 0:
                monthly_revenue[month_key] += r.amount
            elif r.amount < 0:
                monthly_by_cat[r.category.value][month_key] += abs(r.amount)
                monthly_total_cost[month_key] += abs(r.amount)

        months = sorted(monthly_total_cost.keys())
        if len(months) < 2:
            return recs

        # Drop the last month if it's a partial month (<20 days of data)
        # to avoid an artificial "decline" from incomplete data
        last_month_records = [
            r for r in records
            if r.record_date.strftime("%Y-%m") == months[-1]
        ]
        if last_month_records:
            last_month_days = len({r.record_date for r in last_month_records})
            if last_month_days < 20:
                months = months[:-1]
        if len(months) < 2:
            return recs

        # Calculate compound monthly growth rate for total costs
        total_cost_growth = _calc_monthly_growth(
            [monthly_total_cost.get(m, Decimal("0")) for m in months]
        )

        # Calculate growth for each category
        fastest_growing_cat = None
        fastest_growth_rate = 0.0
        for cat, month_data in monthly_by_cat.items():
            values = [month_data.get(m, Decimal("0")) for m in months]
            growth = _calc_monthly_growth(values)
            if growth > fastest_growth_rate and growth > 0.05:  # >5%/month
                fastest_growth_rate = growth
                fastest_growing_cat = cat

        # Revenue growth
        rev_months = sorted(monthly_revenue.keys())
        revenue_growth = 0.0
        has_revenue = len(rev_months) >= 2
        if has_revenue:
            revenue_growth = _calc_monthly_growth(
                [monthly_revenue.get(m, Decimal("0")) for m in rev_months]
            )

        # Project forward
        current_cost = monthly_total_cost.get(months[-1], Decimal("0"))
        projected_3m = float(current_cost) * (1 + total_cost_growth) ** 3
        projected_6m = float(current_cost) * (1 + total_cost_growth) ** 6

        # Build recommendation if costs are growing significantly
        cost_growing_fast = total_cost_growth > 0.05  # >5%/month
        costs_outpace_revenue = has_revenue and total_cost_growth > revenue_growth

        if not cost_growing_fast and not costs_outpace_revenue:
            return recs

        # Estimated savings: difference between projected and flat costs at 3 months
        flat_3m = float(current_cost) * 3
        projected_3m_total = sum(
            float(current_cost) * (1 + total_cost_growth) ** i
            for i in range(1, 4)
        )
        excess_spend = Decimal(str(max(0, projected_3m_total - flat_3m) / 3)).quantize(
            Decimal("0.01")
        )

        desc_parts = [
            f"Your overall costs grew {total_cost_growth*100:+.1f}%/month over "
            f"the last {len(months)} months (from your billing data). "
            f"Projected: ${projected_3m:,.0f} in 3 months, "
            f"${projected_6m:,.0f} in 6 months."
        ]

        if fastest_growing_cat:
            cat_monthly = monthly_by_cat[fastest_growing_cat]
            cat_current = cat_monthly.get(months[-1], Decimal("0"))
            desc_parts.append(
                f" Fastest growing category: {fastest_growing_cat} "
                f"at {fastest_growth_rate*100:+.1f}%/mo "
                f"(currently ${cat_current:.2f}/mo)."
            )

        if costs_outpace_revenue:
            current_rev = monthly_revenue.get(rev_months[-1], Decimal("0"))
            projected_rev_3m = float(current_rev) * (1 + revenue_growth) ** 3
            margin_now = float(
                (current_rev - current_cost) / current_rev * 100
            ) if current_rev > 0 else 0
            margin_3m = (
                (projected_rev_3m - projected_3m) / projected_rev_3m * 100
                if projected_rev_3m > 0
                else 0
            )
            desc_parts.append(
                f" Revenue grows {revenue_growth*100:+.1f}%/mo — "
                f"costs are outpacing revenue. "
                f"Margin: {margin_now:.0f}% now → {margin_3m:.0f}% in 3 months."
            )

        meth_parts = [
            f"Growth calculated from {len(months)} monthly data points "
            f"({months[0]} to {months[-1]}). "
            f"Cost CMGR: {total_cost_growth*100:+.1f}%."
        ]
        if has_revenue:
            meth_parts.append(f" Revenue CMGR: {revenue_growth*100:+.1f}%.")
        if fastest_growing_cat:
            meth_parts.append(
                f" Fastest category: {fastest_growing_cat} "
                f"at {fastest_growth_rate*100:+.1f}%/mo."
            )
        meth_parts.append(
            f" Projection uses compound growth on current "
            f"${current_cost:.2f}/mo baseline."
        )

        recs.append(
            Recommendation(
                rec_type="spend_forecast",
                description="".join(desc_parts),
                estimated_monthly_savings=excess_spend if excess_spend > 0 else None,
                confidence="high" if len(months) >= 3 else "medium",
                action_required=(
                    "Review cost growth drivers. Focus optimization on "
                    f"{'the ' + fastest_growing_cat + ' category' if fastest_growing_cat else 'highest-growth categories'}. "
                    "Consider setting budget alerts at projected thresholds."
                ),
                category=SpendCategory.OTHER,
                source_module=self.name,
                methodology="".join(meth_parts),
            )
        )

        return recs


def _calc_monthly_growth(monthly_values: list[Decimal]) -> float:
    """Calculate compound monthly growth rate from a series of monthly values.

    Uses the geometric mean of month-over-month changes, ignoring
    months with zero values.
    """
    if len(monthly_values) < 2:
        return 0.0

    rates: list[float] = []
    for i in range(1, len(monthly_values)):
        prev = float(monthly_values[i - 1])
        curr = float(monthly_values[i])
        if prev > 0 and curr > 0:
            rates.append(curr / prev - 1)

    if not rates:
        return 0.0

    # Geometric mean of (1 + rate) - 1
    product = 1.0
    for r in rates:
        product *= (1 + r)

    if product <= 0:
        return 0.0

    cmgr = product ** (1.0 / len(rates)) - 1
    return cmgr
