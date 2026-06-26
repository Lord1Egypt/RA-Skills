"""Price comparison module — compares actual workload costs across alternative models."""
import logging
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


class PriceComparisonModule(OptimizationModule):
    """Compares what the user's actual workload would cost on alternative models.

    For each model the user uses:
    - Get their ACTUAL usage (tokens in, tokens out)
    - Fetch CURRENT pricing for that model AND comparable models
    - Calculate exact cost on each alternative
    """

    name = "price_comparison"
    description = "Compare actual workload costs across alternative models"

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        # Group AI records by model
        by_model: dict[str, list[FinancialRecord]] = defaultdict(list)
        for r in records:
            if (
                r.category == SpendCategory.AI_INFERENCE
                and r.model
                and r.tokens_input is not None
                and r.tokens_output is not None
            ):
                by_model[r.model].append(r)

        for model_name, model_records in by_model.items():
            if len(model_records) < 10:
                continue

            model_price = pricing.get_price(model_name)
            if model_price is None:
                continue

            # Actual usage totals
            total_input = sum(r.tokens_input or 0 for r in model_records)
            total_output = sum(r.tokens_output or 0 for r in model_records)
            input_millions = Decimal(str(total_input)) / Decimal("1000000")
            output_millions = Decimal(str(total_output)) / Decimal("1000000")

            # Current cost (calculated from pricing, not from record amounts,
            # to ensure apples-to-apples comparison)
            current_cost = (
                model_price["input_per_million"] * input_millions
                + model_price["output_per_million"] * output_millions
            )

            # Scale to monthly
            date_range = (
                max(r.record_date for r in model_records)
                - min(r.record_date for r in model_records)
            ).days or 1
            monthly_factor = Decimal("30") / Decimal(str(date_range))
            monthly_current = current_cost * monthly_factor

            # Get comparable models (same tier + one tier below)
            comparables = pricing.get_comparable_models(model_name)
            if not comparables:
                continue

            # Calculate cost on each alternative
            best_alt = None
            best_savings = Decimal("0")
            best_alt_cost = Decimal("0")

            for alt in comparables:
                alt_cost = (
                    alt["input_per_million"] * input_millions
                    + alt["output_per_million"] * output_millions
                ) * monthly_factor

                savings = monthly_current - alt_cost
                if savings > best_savings:
                    best_savings = savings
                    best_alt = alt
                    best_alt_cost = alt_cost

            if best_alt is None or best_savings <= Decimal("1.00"):
                continue

            monthly_savings = best_savings.quantize(Decimal("0.01"))
            pct_reduction = (
                float(best_savings / monthly_current * 100)
                if monthly_current > 0
                else 0
            )

            recs.append(
                Recommendation(
                    rec_type="price_comparison",
                    description=(
                        f"Your {model_name} workload: "
                        f"{float(input_millions * monthly_factor):.1f}M input + "
                        f"{float(output_millions * monthly_factor):.1f}M output tokens/mo "
                        f"= ${monthly_current:.2f}. "
                        f"Same workload on {best_alt['model']}: "
                        f"${best_alt_cost:.2f} "
                        f"(savings: ${monthly_savings}/mo, {pct_reduction:.0f}% reduction)."
                    ),
                    estimated_monthly_savings=monthly_savings,
                    confidence="medium",
                    action_required=(
                        f"Evaluate {best_alt['model']} ({best_alt['tier']} tier) "
                        f"as replacement for {model_name}. "
                        f"Test on a subset of workload to verify quality."
                    ),
                    category=SpendCategory.AI_INFERENCE,
                    source_module=self.name,
                    methodology=(
                        f"Actual usage over {date_range} days: "
                        f"{total_input:,} input + {total_output:,} output tokens "
                        f"on {model_name}. "
                        f"Current pricing: ${model_price['input_per_million']}/M in, "
                        f"${model_price['output_per_million']}/M out "
                        f"= ${monthly_current:.2f}/mo. "
                        f"Alternative {best_alt['model']}: "
                        f"${best_alt['input_per_million']}/M in, "
                        f"${best_alt['output_per_million']}/M out "
                        f"= ${best_alt_cost:.2f}/mo. "
                        f"Prices fetched {pricing.last_updated:%Y-%m-%d} "
                        f"from {pricing.source}."
                    ),
                )
            )

        return recs
