"""FP-DCF public package scaffold."""

from .engine import run_valuation
from .market_implied_growth import resolve_market_inputs
from .normalize import normalize_payload
from .sensitivity import build_wacc_terminal_growth_sensitivity
from .schemas import (
    CapitalStructure,
    DataFreshnessSummary,
    FCFFSummary,
    MarketImpliedGrowthInput,
    MarketImpliedGrowthOutput,
    MarketInputsSummary,
    SensitivityHeatmapOutput,
    TaxAssumptions,
    ValuationOutput,
    ValuationSummary,
    VALUATION_OUTPUT_CONTRACT_VERSION,
    WACCInputs,
)

__all__ = [
    "CapitalStructure",
    "DataFreshnessSummary",
    "FCFFSummary",
    "MarketImpliedGrowthInput",
    "MarketImpliedGrowthOutput",
    "MarketInputsSummary",
    "SensitivityHeatmapOutput",
    "TaxAssumptions",
    "ValuationOutput",
    "ValuationSummary",
    "VALUATION_OUTPUT_CONTRACT_VERSION",
    "WACCInputs",
    "build_wacc_terminal_growth_sensitivity",
    "run_valuation",
    "normalize_payload",
    "resolve_market_inputs",
]

__version__ = "0.6.0"
