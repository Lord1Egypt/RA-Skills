"""Abstract base class for optimization modules."""
from abc import ABC, abstractmethod

from engine.intelligence.pricing_fetcher import PricingFetcher
from engine.models import FinancialRecord, FinancialSummary, Recommendation


class OptimizationModule(ABC):
    """Base class for all optimization analysis modules.

    Every module must produce recommendations with:
    - estimated_monthly_savings (specific dollar amount)
    - confidence (high/medium/low)
    - methodology (how the number was calculated)
    """

    name: str = ""
    description: str = ""
    required_providers: list[str] = []

    @abstractmethod
    def analyse(
        self,
        records: list[FinancialRecord],
        summary: FinancialSummary,
        pricing: PricingFetcher,
    ) -> list[Recommendation]:
        """Run analysis and return recommendations."""
        ...
