"""Batch processing detector — identifies consistent-volume workloads eligible for batch APIs."""
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

# Published batch discount rates (verifiable from provider docs)
_BATCH_DISCOUNTS: dict[str, Decimal] = {
    "openai": Decimal("0.50"),  # 50% discount on batch API
    # Anthropic does not currently offer a batch discount
}


class BatchDetectorModule(OptimizationModule):
    """Detects workloads suitable for batch processing.

    Analyses daily request volume patterns:
    - Calculates daily volumes and identifies "steady state" days
      (within 1 standard deviation of the mean)
    - If >70% of days are steady state, the workload is a batch candidate
    - Batch-eligible percentage is derived from (steady days / total days)
    """

    name = "batch_detector"
    description = "Detect workloads suitable for batch API processing"

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        # Group AI inference records by provider
        by_provider: dict[str, list[FinancialRecord]] = defaultdict(list)
        for r in records:
            if r.category == SpendCategory.AI_INFERENCE:
                by_provider[r.provider.value].append(r)

        for provider, provider_records in by_provider.items():
            # Only providers with batch API discounts
            if provider not in _BATCH_DISCOUNTS:
                continue

            # Need enough data
            if len(provider_records) < 30:
                continue

            # Calculate daily request counts
            daily_counts: dict[str, int] = defaultdict(int)
            daily_costs: dict[str, Decimal] = defaultdict(Decimal)
            for r in provider_records:
                day_key = r.record_date.isoformat()
                daily_counts[day_key] += 1
                daily_costs[day_key] += abs(r.amount)

            counts = list(daily_counts.values())
            total_days = len(counts)
            if total_days < 14:
                continue

            # Calculate mean and std dev of daily request counts
            mean_count = sum(counts) / total_days
            if mean_count == 0:
                continue
            variance = sum((c - mean_count) ** 2 for c in counts) / total_days
            std_dev = math.sqrt(variance)

            # Steady state days: within 1 std dev of mean
            steady_days = sum(
                1 for c in counts
                if abs(c - mean_count) <= std_dev
            )
            steady_pct = steady_days / total_days

            if steady_pct < 0.70:
                continue  # too variable for batch

            # Batch-eligible percentage derived from data
            batch_eligible_pct = Decimal(str(round(steady_pct, 2)))

            # Calculate savings
            total_cost = sum(daily_costs.values())
            date_range = (
                max(r.record_date for r in provider_records)
                - min(r.record_date for r in provider_records)
            ).days or 1
            monthly_factor = Decimal("30") / Decimal(str(date_range))
            monthly_cost = total_cost * monthly_factor

            discount = _BATCH_DISCOUNTS[provider]
            batchable_cost = monthly_cost * batch_eligible_pct
            monthly_savings = (batchable_cost * discount).quantize(Decimal("0.01"))

            if monthly_savings <= Decimal("0.50"):
                continue

            recs.append(
                Recommendation(
                    rec_type="batch_processing",
                    description=(
                        f"Your {provider.title()} usage shows consistent daily volumes "
                        f"({int(steady_pct * 100)}% of days within normal range). "
                        f"{int(float(batch_eligible_pct) * 100)}% of your workload appears "
                        f"schedulable. At {provider.title()}'s batch rate "
                        f"({int(float(discount) * 100)}% discount), "
                        f"estimated savings: ${monthly_savings}/month."
                    ),
                    estimated_monthly_savings=monthly_savings,
                    confidence="high" if steady_pct > 0.80 else "medium",
                    action_required=(
                        f"Migrate consistent {provider.title()} workloads to the Batch API. "
                        f"Submit requests as batch jobs for non-time-sensitive tasks."
                    ),
                    category=SpendCategory.AI_INFERENCE,
                    source_module=self.name,
                    methodology=(
                        f"Daily volume analysis over {total_days} days: "
                        f"mean={mean_count:.1f} requests/day, std_dev={std_dev:.1f}. "
                        f"{steady_days}/{total_days} days within 1 std dev ({int(steady_pct*100)}% steady). "
                        f"Monthly {provider.title()} spend: ${monthly_cost:.2f}. "
                        f"Batchable fraction: {int(float(batch_eligible_pct)*100)}% = "
                        f"${batchable_cost:.2f}. "
                        f"Batch discount: {int(float(discount)*100)}% "
                        f"(published {provider.title()} rate). "
                        f"Savings: ${monthly_savings}/mo."
                    ),
                )
            )

        return recs
