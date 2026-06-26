from __future__ import annotations

from dataclasses import asdict, dataclass, field


VALUATION_OUTPUT_CONTRACT_VERSION = "fp-dcf.valuation_output.v1"


@dataclass(slots=True)
class TaxAssumptions:
    effective_tax_rate: float | None = None
    effective_tax_rate_source: str | None = None
    marginal_tax_rate: float | None = None
    marginal_tax_rate_source: str | None = None


@dataclass(slots=True)
class CapitalStructure:
    equity_weight: float | None = None
    debt_weight: float | None = None
    source: str | None = None


@dataclass(slots=True)
class WACCInputs:
    risk_free_rate: float | None = None
    risk_free_rate_source: str | None = None
    equity_risk_premium: float | None = None
    equity_risk_premium_source: str | None = None
    beta: float | None = None
    beta_source: str | None = None
    cost_of_equity: float | None = None
    pre_tax_cost_of_debt: float | None = None
    pre_tax_cost_of_debt_source: str | None = None
    wacc: float | None = None


@dataclass(slots=True)
class FCFFSummary:
    anchor: float | None = None
    anchor_method: str | None = None
    selected_path: str | None = None
    anchor_ebiat_path: float | None = None
    anchor_cfo_path: float | None = None
    ebiat_path_available: bool | None = None
    cfo_path_available: bool | None = None
    after_tax_interest: float | None = None
    after_tax_interest_source: str | None = None
    reconciliation_gap: float | None = None
    reconciliation_gap_pct: float | None = None
    anchor_mode: str | None = None
    anchor_observation_count: int | None = None
    delta_nwc_source: str | None = None
    last_report_period: str | None = None

    @property
    def path_selected(self) -> str | None:
        return self.selected_path

    @path_selected.setter
    def path_selected(self, value: str | None) -> None:
        self.selected_path = value

    @property
    def ebiat_path_anchor(self) -> float | None:
        return self.anchor_ebiat_path

    @ebiat_path_anchor.setter
    def ebiat_path_anchor(self, value: float | None) -> None:
        self.anchor_ebiat_path = value

    @property
    def cfo_path_anchor(self) -> float | None:
        return self.anchor_cfo_path

    @cfo_path_anchor.setter
    def cfo_path_anchor(self, value: float | None) -> None:
        self.anchor_cfo_path = value

    @property
    def interest_adjustment_source(self) -> str | None:
        return self.after_tax_interest_source

    @interest_adjustment_source.setter
    def interest_adjustment_source(self, value: str | None) -> None:
        self.after_tax_interest_source = value


@dataclass(slots=True)
class MarketInputsSummary:
    enterprise_value_market: float | None = None
    enterprise_value_market_source: str | None = None
    equity_value_market: float | None = None
    market_price: float | None = None
    market_price_source: str | None = None
    shares_out: float | None = None
    shares_out_source: str | None = None
    net_debt: float | None = None
    net_debt_source: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class DataFreshnessSummary:
    provider: str | None = None
    snapshot_as_of: str | None = None
    cache_created_at: str | None = None
    cache_age_hours: float | None = None
    freshness_class: str = "unknown"
    requires_refresh: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class MarketImpliedGrowthInput:
    enabled: bool = False
    lower_bound: float = -0.5
    upper_bound: float = 0.5
    solver: str = "auto"
    tolerance: float = 1e-6
    max_iterations: int = 100

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class MarketImpliedGrowthOutput:
    enabled: bool = False
    success: bool = False
    valuation_model: str | None = None
    solved_field: str | None = None
    solved_value: float | None = None
    solver_used: str | None = None
    lower_bound: float | None = None
    upper_bound: float | None = None
    iterations: int | None = None
    residual: float | None = None
    market_price: float | None = None
    market_enterprise_value: float | None = None
    base_case_per_share_value: float | None = None
    base_case_enterprise_value: float | None = None
    message: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ValuationSummary:
    enterprise_value: float | None = None
    equity_value: float | None = None
    per_share_value: float | None = None
    terminal_growth_rate: float | None = None
    terminal_growth_rate_effective: float | None = None
    present_value_stage1: float | None = None
    present_value_stage2: float | None = None
    present_value_terminal: float | None = None
    terminal_value: float | None = None
    terminal_value_share: float | None = None
    explicit_forecast_years: int | None = None
    stage1_years: int | None = None
    stage2_years: int | None = None
    stage2_decay_mode: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ValuationOutput:
    ticker: str
    market: str
    valuation_model: str
    contract_version: str = VALUATION_OUTPUT_CONTRACT_VERSION
    requested_valuation_model: str | None = None
    effective_valuation_model: str | None = None
    degraded: bool = False
    degradation_reasons: list[str] = field(default_factory=list)
    currency: str | None = None
    as_of_date: str | None = None
    tax: TaxAssumptions = field(default_factory=TaxAssumptions)
    wacc_inputs: WACCInputs = field(default_factory=WACCInputs)
    capital_structure: CapitalStructure = field(default_factory=CapitalStructure)
    fcff: FCFFSummary = field(default_factory=FCFFSummary)
    valuation: ValuationSummary = field(default_factory=ValuationSummary)
    market_implied_growth: MarketImpliedGrowthOutput | None = None
    data_freshness: DataFreshnessSummary | None = None
    diagnostics: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        payload = asdict(self)
        if payload.get("market_implied_growth") is None:
            payload.pop("market_implied_growth", None)
        if payload.get("data_freshness") is None:
            payload.pop("data_freshness", None)
        return payload


@dataclass(slots=True)
class SensitivityHeatmapOutput:
    ticker: str
    market: str
    valuation_model: str
    metric: str
    metric_label: str
    currency: str | None = None
    as_of_date: str | None = None
    base_wacc: float | None = None
    base_terminal_growth_rate: float | None = None
    base_metric_value: float | None = None
    market_price: float | None = None
    wacc_values: list[float] = field(default_factory=list)
    terminal_growth_values: list[float] = field(default_factory=list)
    matrix: list[list[float | None]] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_summary_dict(
        self,
        *,
        include_grid: bool = False,
        exclude_diagnostics: set[str] | None = None,
        exclude_warnings: set[str] | None = None,
    ) -> dict:
        exclude_diagnostics = exclude_diagnostics or set()
        exclude_warnings = exclude_warnings or set()

        summary = {
            "metric": self.metric,
            "metric_label": self.metric_label,
            "base_wacc": self.base_wacc,
            "base_terminal_growth_rate": self.base_terminal_growth_rate,
            "base_metric_value": self.base_metric_value,
            "market_price": self.market_price,
            "wacc_axis": {
                "min": self.wacc_values[0] if self.wacc_values else None,
                "max": self.wacc_values[-1] if self.wacc_values else None,
                "points": len(self.wacc_values),
            },
            "terminal_growth_axis": {
                "min": self.terminal_growth_values[0] if self.terminal_growth_values else None,
                "max": self.terminal_growth_values[-1] if self.terminal_growth_values else None,
                "points": len(self.terminal_growth_values),
            },
            "diagnostics": [item for item in self.diagnostics if item not in exclude_diagnostics],
            "warnings": [item for item in self.warnings if item not in exclude_warnings],
        }

        if include_grid:
            summary["grid"] = {
                "wacc_values": list(self.wacc_values),
                "terminal_growth_values": list(self.terminal_growth_values),
                "matrix": [list(row) for row in self.matrix],
            }

        return summary
