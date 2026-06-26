"""Prompt caching estimator — analyses input token consistency to estimate caching opportunity."""
import logging
import math
from collections import defaultdict
from decimal import Decimal

from engine.intelligence.optimization.base_module import OptimizationModule
from engine.intelligence.pricing_fetcher import CACHED_TOKEN_DISCOUNTS, PricingFetcher
from engine.models import (
    FinancialRecord,
    FinancialSummary,
    Recommendation,
    SpendCategory,
)

logger = logging.getLogger(__name__)

# Providers that support prompt caching
_CACHEABLE_PROVIDERS = {"openai", "anthropic"}


class CachingEstimatorModule(OptimizationModule):
    """Estimates prompt caching savings using data-derived cacheable ratio.

    Instead of assuming a cache hit percentage, calculates it from the
    coefficient of variation (CV) of input token counts per provider:
    - LOW CV (<0.3): highly consistent inputs → high caching opportunity
    - MEDIUM CV (0.3-0.7): moderate opportunity
    - HIGH CV (>0.7): content varies too much, caching won't help
    """

    name = "caching_estimator"
    description = "Estimate savings from prompt caching based on input consistency"

    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        recs: list[Recommendation] = []

        # Group AI records by (provider, model) to avoid mixing different
        # token distributions (e.g. per-request vs daily aggregate models)
        by_provider_model: dict[tuple[str, str], list[FinancialRecord]] = defaultdict(list)
        for r in records:
            if (
                r.category == SpendCategory.AI_INFERENCE
                and r.provider.value in _CACHEABLE_PROVIDERS
                and r.model
                and r.tokens_input is not None
                and r.tokens_input > 0
            ):
                by_provider_model[(r.provider.value, r.model)].append(r)

        for (provider, model_name), provider_records in by_provider_model.items():
            if len(provider_records) < 20:
                continue

            # Calculate coefficient of variation of input tokens
            input_tokens = [r.tokens_input for r in provider_records if r.tokens_input]
            mean_input = sum(input_tokens) / len(input_tokens)
            if mean_input == 0:
                continue

            variance = sum((t - mean_input) ** 2 for t in input_tokens) / len(input_tokens)
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_input

            # Consistency score: 1 - CV (clamped to 0-1)
            consistency_score = max(0.0, min(1.0, 1.0 - cv))

            if cv > 0.7:
                continue  # too variable for caching to help

            # Estimated cacheable ratio derived from consistency
            cacheable_ratio = Decimal(str(round(consistency_score, 2)))

            # Get cached token discount for this provider
            discount_rate = CACHED_TOKEN_DISCOUNTS.get(provider)
            if discount_rate is None:
                continue

            # Calculate savings
            total_input_tokens = sum(input_tokens)
            cacheable_tokens = int(float(cacheable_ratio) * total_input_tokens)

            # Get input price for this specific model
            model_price = pricing.get_price(model_name)
            if model_price is None:
                continue

            avg_input_price = model_price["input_per_million"]

            # Current cost of cacheable tokens
            cacheable_cost = (
                avg_input_price * Decimal(str(cacheable_tokens)) / Decimal("1000000")
            )
            # With caching: cacheable tokens cost discount_rate of normal price
            cached_cost = cacheable_cost * discount_rate
            savings_total = cacheable_cost - cached_cost

            # Scale to monthly
            date_range = (
                max(r.record_date for r in provider_records)
                - min(r.record_date for r in provider_records)
            ).days or 1
            monthly_factor = Decimal("30") / Decimal(str(date_range))
            monthly_savings = (savings_total * monthly_factor).quantize(Decimal("0.01"))

            if monthly_savings <= Decimal("0.50"):
                continue

            cached_price = (avg_input_price * discount_rate).quantize(Decimal("0.01"))
            uncached_price = avg_input_price.quantize(Decimal("0.01"))
            pct_cacheable = int(float(cacheable_ratio) * 100)

            confidence = "high" if cv < 0.3 else "medium"

            recs.append(
                Recommendation(
                    rec_type="prompt_caching",
                    description=(
                        f"Your {provider.title()} {model_name} calls have a consistency "
                        f"score of {consistency_score:.2f} (scale: 0=unique, 1=identical). "
                        f"~{pct_cacheable}% of input tokens appear to be repeated content. "
                        f"Enabling prompt caching could save ~${monthly_savings}/month."
                    ),
                    estimated_monthly_savings=monthly_savings,
                    confidence=confidence,
                    action_required=(
                        f"Enable prompt caching for {provider.title()} {model_name} calls. "
                        f"Structure prompts with static system content first."
                    ),
                    category=SpendCategory.AI_INFERENCE,
                    source_module=self.name,
                    methodology=(
                        f"Input token CV = {cv:.3f} (std_dev={std_dev:.0f}, mean={mean_input:.0f}) "
                        f"across {len(input_tokens):,} {model_name} requests. "
                        f"Consistency score: {consistency_score:.2f} → ~{pct_cacheable}% cacheable. "
                        f"At {provider.title()} cached token pricing "
                        f"(${cached_price}/M tokens vs ${uncached_price}/M uncached), "
                        f"savings on {cacheable_tokens:,} cacheable tokens/period = "
                        f"${monthly_savings}/mo. "
                        f"Discount rate: {float(discount_rate)*100:.0f}% of input price "
                        f"(published {provider.title()} rate)."
                    ),
                )
            )

        return recs
