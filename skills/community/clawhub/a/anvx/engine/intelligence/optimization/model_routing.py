"""Model routing optimization — identifies misrouted workloads using data-derived thresholds."""
import logging
from collections import defaultdict
from decimal import Decimal

import statistics

from engine.intelligence.optimization.base_module import OptimizationModule
from engine.intelligence.pricing_fetcher import PricingFetcher
from engine.models import (
    FinancialRecord,
    FinancialSummary,
    Recommendation,
    SpendCategory,
)

logger = logging.getLogger(__name__)


class ModelRoutingModule(OptimizationModule):
    """Identifies requests on expensive models that could use cheaper alternatives.

    Uses DATA-DERIVED thresholds: calculates percentiles from the user's own
    request distribution rather than hardcoded token counts.
    """

    name = "model_routing"
    description = "Detect expensive model usage on simple tasks"

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        # Collect AI inference records with token data, grouped by model
        by_model: dict[str, list[FinancialRecord]] = defaultdict(list)
        all_token_counts: list[int] = []

        for r in records:
            if (
                r.category == SpendCategory.AI_INFERENCE
                and r.model
                and r.tokens_input is not None
                and r.tokens_output is not None
            ):
                by_model[r.model].append(r)
                all_token_counts.append(r.tokens_input + r.tokens_output)

        if len(all_token_counts) < 10:
            return recs

        # Data-derived threshold: 25th percentile of ALL user requests
        all_token_counts.sort()
        p25_index = max(0, len(all_token_counts) // 4 - 1)
        p25_threshold = all_token_counts[p25_index]
        median = statistics.median(all_token_counts)

        for model_name, model_records in by_model.items():
            model_price = pricing.get_price(model_name)
            if model_price is None:
                continue

            tier = pricing.get_tier(model_name)
            if tier == "efficient":
                continue  # already on a cheap model

            # Find records below the 25th percentile (candidate for cheaper model)
            short_records = [
                r for r in model_records
                if (r.tokens_input or 0) + (r.tokens_output or 0) < p25_threshold
            ]

            if not short_records or len(short_records) < 5:
                continue

            short_ratio = len(short_records) / len(model_records)
            if short_ratio < 0.10:
                continue

            # Calculate current cost of short records
            short_cost = sum(abs(r.amount) for r in short_records)

            # Scale to monthly
            date_range = (
                max(r.record_date for r in model_records)
                - min(r.record_date for r in model_records)
            ).days or 1
            monthly_factor = Decimal("30") / Decimal(str(date_range))
            short_cost_monthly = short_cost * monthly_factor

            # Calculate cost on comparable cheaper models
            comparables = pricing.get_comparable_models(model_name)
            if not comparables:
                continue

            # Pick the cheapest comparable
            cheapest = comparables[0]

            # Calculate exact savings using actual token volumes
            total_input = sum(r.tokens_input or 0 for r in short_records)
            total_output = sum(r.tokens_output or 0 for r in short_records)

            current_cost_exact = (
                model_price["input_per_million"] * Decimal(str(total_input)) / Decimal("1000000")
                + model_price["output_per_million"] * Decimal(str(total_output)) / Decimal("1000000")
            ) * monthly_factor

            alt_cost_exact = (
                cheapest["input_per_million"] * Decimal(str(total_input)) / Decimal("1000000")
                + cheapest["output_per_million"] * Decimal(str(total_output)) / Decimal("1000000")
            ) * monthly_factor

            savings = (current_cost_exact - alt_cost_exact).quantize(Decimal("0.01"))
            if savings <= Decimal("0.10"):
                continue

            recs.append(
                Recommendation(
                    rec_type="model_routing",
                    description=(
                        f"{len(short_records)} of {len(model_records)} {model_name} requests "
                        f"({short_ratio:.0%}) had token count below your 25th percentile "
                        f"({p25_threshold:,} tokens). These simple tasks could use "
                        f"{cheapest['model']} instead."
                    ),
                    estimated_monthly_savings=savings,
                    confidence="high" if short_ratio > 0.3 else "medium",
                    action_required=(
                        f"Route requests with <{p25_threshold:,} tokens from "
                        f"{model_name} to {cheapest['model']}"
                    ),
                    category=SpendCategory.AI_INFERENCE,
                    source_module=self.name,
                    methodology=(
                        f"25th percentile of your {len(all_token_counts):,} requests = "
                        f"{p25_threshold:,} tokens (median: {int(median):,}). "
                        f"{len(short_records)} {model_name} requests below this threshold "
                        f"cost ${current_cost_exact:.2f}/mo at "
                        f"${model_price['input_per_million']}/M input. "
                        f"Same volume on {cheapest['model']} at "
                        f"${cheapest['input_per_million']}/M input = "
                        f"${alt_cost_exact:.2f}/mo. "
                        f"Prices from {pricing.source}."
                    ),
                )
            )

        return recs
