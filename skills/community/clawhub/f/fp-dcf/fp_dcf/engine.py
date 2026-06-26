from __future__ import annotations

from datetime import date
from math import isfinite

from .market_implied_growth import (
    reject_removed_market_implied_blocks,
    resolve_market_implied_growth_input,
    resolve_market_inputs,
)
from .schemas import (
    CapitalStructure,
    DataFreshnessSummary,
    FCFFSummary,
    MarketImpliedGrowthOutput,
    TaxAssumptions,
    ValuationOutput,
    ValuationSummary,
    WACCInputs,
)

_SUPPORTED_VALUATION_MODELS = {
    "steady_state_single_stage",
    "two_stage",
    "three_stage",
}


def _coerce_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if isfinite(out) else None


def _coerce_bool(value, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _coerce_string(value) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _append_once(items: list[str], item: str) -> None:
    if item not in items:
        items.append(item)


def _mark_degraded(reasons: list[str], key: str) -> None:
    _append_once(reasons, key)


def _resolve_data_freshness(
    payload: dict,
    *,
    warnings: list[str],
    diagnostics: list[str],
    degradation_reasons: list[str],
) -> DataFreshnessSummary:
    raw = payload.get("_data_freshness")
    if not isinstance(raw, dict):
        freshness = DataFreshnessSummary(
            provider="user_supplied",
            snapshot_as_of=_coerce_string(payload.get("as_of_date")),
            cache_created_at=None,
            cache_age_hours=None,
            freshness_class="user_supplied",
            requires_refresh=False,
        )
    else:
        freshness_class = _coerce_string(raw.get("freshness_class")) or "unknown"
        freshness = DataFreshnessSummary(
            provider=_coerce_string(raw.get("provider")),
            snapshot_as_of=_coerce_string(raw.get("snapshot_as_of")),
            cache_created_at=_coerce_string(raw.get("cache_created_at")),
            cache_age_hours=_coerce_float(raw.get("cache_age_hours")),
            freshness_class=freshness_class,
            requires_refresh=_coerce_bool(raw.get("requires_refresh"), default=True),
        )

    _append_once(diagnostics, f"data_freshness:{freshness.freshness_class}")
    if freshness.freshness_class == "stale":
        _append_once(warnings, "provider_data_stale")
        _mark_degraded(degradation_reasons, "degraded_due_to_provider_data_stale")
    elif freshness.freshness_class == "unknown":
        _append_once(warnings, "provider_data_freshness_unknown")
        _mark_degraded(
            degradation_reasons,
            "degraded_due_to_provider_data_freshness_unknown",
        )
    elif freshness.freshness_class == "missing":
        _append_once(warnings, "provider_data_missing")
        _mark_degraded(degradation_reasons, "degraded_due_to_provider_data_missing")
    return freshness


def _resolve_requested_valuation_model(
    payload: dict,
    warnings: list[str],
) -> tuple[str | None, str]:
    raw_model = payload.get("valuation_model")
    if raw_model is None:
        _append_once(
            warnings,
            "valuation_model_missing_defaulted_to_steady_state_single_stage",
        )
        return None, "steady_state_single_stage"

    requested_model = str(raw_model).strip()
    if not requested_model:
        _append_once(
            warnings,
            "valuation_model_missing_defaulted_to_steady_state_single_stage",
        )
        return None, "steady_state_single_stage"

    return requested_model, _validate_valuation_model(requested_model)


def _resolve_fcff_preferred_path(assumptions: dict, warnings: list[str]) -> str:
    preferred_path = str(assumptions.get("fcff_preferred_path") or "cfo").strip().lower()
    if preferred_path not in {"cfo", "ebiat"}:
        _append_once(warnings, "fcff_preferred_path_invalid_defaulted_to_cfo")
        return "cfo"
    return preferred_path


def _clip_rate(value: float | None, *, low: float = 0.0, high: float = 0.95) -> float | None:
    if value is None:
        return None
    return min(max(value, low), high)


def _coerce_positive_int(value, *, field_name: str) -> int:
    numeric = _coerce_float(value)
    if numeric is None:
        raise ValueError(f"Missing assumptions.{field_name} for three_stage valuation_model")
    if not float(numeric).is_integer() or numeric <= 0:
        raise ValueError(f"assumptions.{field_name} must be a positive integer")
    return int(numeric)


def _validate_valuation_model(model: str) -> str:
    normalized_model = str(model or "steady_state_single_stage").strip() or "steady_state_single_stage"
    if normalized_model not in _SUPPORTED_VALUATION_MODELS:
        raise ValueError(f"unsupported valuation_model: {normalized_model}")
    return normalized_model


def _resolve_rate_input(
    assumptions: dict,
    field_name: str,
    *,
    low: float,
    high: float,
    warnings: list[str],
    required: bool = False,
    default: float | None = None,
    missing_warning: str | None = None,
    clip_warning: str | None = None,
) -> float:
    value = _coerce_float(assumptions.get(field_name))
    if value is None:
        if required:
            raise ValueError(f"Missing assumptions.{field_name} for three_stage valuation_model")
        if default is None:
            raise ValueError(f"Missing assumptions.{field_name}")
        if missing_warning is not None:
            _append_once(warnings, missing_warning)
        return default

    clipped = _clip_rate(value, low=low, high=high)
    if clipped != value and clip_warning is not None:
        _append_once(warnings, clip_warning)
    return float(clipped)


def _clamp_growth_below_wacc(
    growth_rate: float,
    wacc: float,
    *,
    warnings: list[str],
    warning_key: str,
) -> float:
    if growth_rate < wacc:
        return growth_rate
    _append_once(warnings, warning_key)
    return max(0.0, wacc - 0.01)


def _resolve_two_stage_inputs(
    assumptions: dict,
    warnings: list[str],
) -> tuple[float, int]:
    growth_rate_high = _clip_rate(
        _coerce_float(assumptions.get("high_growth_rate")),
        low=-0.5,
        high=1.0,
    )
    if growth_rate_high is None:
        growth_rate_high = _clip_rate(
            _coerce_float(assumptions.get("stage1_growth_rate")),
            low=-0.5,
            high=1.0,
        )
    if growth_rate_high is None:
        growth_rate_high = 0.10
        warnings.append("high_growth_rate_missing_defaulted_to_0.10")

    years_high = _coerce_float(assumptions.get("high_growth_years"))
    if years_high is None:
        years_high = _coerce_float(assumptions.get("stage1_years"))
    return growth_rate_high, int(years_high or 5)


def _normalize_weights(
    equity_weight: float | None,
    debt_weight: float | None,
    source: str | None = None,
) -> tuple[float, float, str]:
    ew = _coerce_float(equity_weight)
    dw = _coerce_float(debt_weight)

    if ew is None and dw is None:
        return 0.7, 0.3, "default"
    if ew is None and dw is not None:
        ew = max(0.0, 1.0 - dw)
    if dw is None and ew is not None:
        dw = max(0.0, 1.0 - ew)

    ew = 0.0 if ew is None else max(0.0, ew)
    dw = 0.0 if dw is None else max(0.0, dw)
    total = ew + dw
    if total <= 0:
        return 0.7, 0.3, "default"
    return ew / total, dw / total, source or "manual_input"


def _resolve_tax_inputs(
    payload: dict,
    warnings: list[str],
    diagnostics: list[str],
) -> TaxAssumptions:
    assumptions = payload.get("assumptions") or {}
    effective = _clip_rate(_coerce_float(assumptions.get("effective_tax_rate")))
    marginal = _clip_rate(_coerce_float(assumptions.get("marginal_tax_rate")))
    effective_source = (
        assumptions.get("effective_tax_rate_source")
        if effective is not None
        else None
    )
    marginal_source = (
        assumptions.get("marginal_tax_rate_source")
        if marginal is not None
        else None
    )
    if effective is not None and not effective_source:
        effective_source = "manual_input"
    if marginal is not None and not marginal_source:
        marginal_source = "manual_input"

    if effective is None and marginal is not None:
        effective = marginal
        effective_source = "reused_marginal_tax_rate"
        warnings.append("effective_tax_rate_missing_reused_marginal_tax_rate")
    elif effective is None:
        effective = 0.25
        effective_source = "default"
        warnings.append("effective_tax_rate_missing_defaulted_to_0.25")

    if marginal is None and assumptions.get("effective_tax_rate") is not None:
        marginal = effective
        marginal_source = "reused_effective_tax_rate"
        warnings.append("marginal_tax_rate_missing_reused_effective_tax_rate")
    elif marginal is None:
        marginal = 0.25
        marginal_source = "default"
        warnings.append("marginal_tax_rate_missing_defaulted_to_0.25")

    if effective_source != marginal_source or effective != marginal:
        diagnostics.append("tax_rate_paths_are_separated")
    else:
        diagnostics.append("tax_rate_paths_are_shared")

    return TaxAssumptions(
        effective_tax_rate=effective,
        effective_tax_rate_source=effective_source,
        marginal_tax_rate=marginal,
        marginal_tax_rate_source=marginal_source,
    )


def _resolve_delta_nwc(fundamentals: dict, warnings: list[str]) -> tuple[float, str]:
    candidates = [
        ("delta_nwc", "delta_nwc"),
        ("op_nwc_delta", "OpNWC_delta"),
        ("nwc_delta", "NWC_delta"),
    ]
    for key, source in candidates:
        value = _coerce_float(fundamentals.get(key))
        if value is not None:
            return value, str(fundamentals.get("delta_nwc_source") or source)

    change_wc = _coerce_float(fundamentals.get("change_in_working_capital"))
    if change_wc is not None:
        warnings.append("delta_nwc_derived_from_cash_flow_change_in_working_capital")
        return -change_wc, "cashflow_change_in_working_capital"

    warnings.append("delta_nwc_missing_assumed_zero")
    return 0.0, "assumed_zero"


def _resolve_after_tax_interest_adjustment_from_values(
    interest_paid: float | None,
    interest_expense: float | None,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[float | None, str | None]:
    if interest_paid is not None:
        return abs(interest_paid) * (1.0 - float(tax.effective_tax_rate or 0.25)), "interest_paid"

    if interest_expense is not None:
        _append_once(warnings, "interest_paid_missing_used_interest_expense_proxy")
        return (
            abs(interest_expense) * (1.0 - float(tax.effective_tax_rate or 0.25)),
            "interest_expense_proxy",
        )

    return None, None


def _resolve_after_tax_interest_adjustment(
    fundamentals: dict,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[float | None, str | None]:
    return _resolve_after_tax_interest_adjustment_from_values(
        _coerce_float(fundamentals.get("interest_paid")),
        _coerce_float(fundamentals.get("interest_expense")),
        tax,
        warnings,
    )


def _coerce_history_series(value) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}
    out: dict[str, float] = {}
    for key, raw in value.items():
        numeric = _coerce_float(raw)
        if numeric is not None:
            out[str(key)] = numeric
    return dict(sorted(out.items()))


def _get_historical_series(fundamentals: dict, key: str) -> dict[str, float]:
    historical_series = fundamentals.get("historical_series") or {}
    if not isinstance(historical_series, dict):
        return {}
    return _coerce_history_series(historical_series.get(key))


def _last_n_periods(series: dict[str, float], limit: int = 3) -> list[tuple[str, float]]:
    return list(sorted(series.items()))[-limit:]


def _average_period_values(periods: list[tuple[str, float]]) -> float | None:
    if not periods:
        return None
    return sum(value for _, value in periods) / len(periods)


def _warn_on_large_fcff_gap(reconciliation_gap_pct: float | None, warnings: list[str]) -> None:
    if reconciliation_gap_pct is not None and abs(reconciliation_gap_pct) > 0.10:
        _append_once(warnings, "fcff_reconciliation_gap_pct_above_0.10")


def _summarize_interest_sources(sources: list[str]) -> str | None:
    if not sources:
        return None
    unique_sources = sorted(set(sources))
    if len(unique_sources) == 1:
        return unique_sources[0]
    return "mixed_interest_sources"


def _build_historical_fcff_paths(
    fundamentals: dict,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, str]]:
    ebit_series = _get_historical_series(fundamentals, "ebit")
    ocf_series = _get_historical_series(fundamentals, "ocf")
    da_series = _get_historical_series(fundamentals, "da")
    capex_series = _get_historical_series(fundamentals, "capex")
    delta_nwc_series = _get_historical_series(fundamentals, "delta_nwc")
    interest_paid_series = _get_historical_series(fundamentals, "interest_paid")
    interest_expense_series = _get_historical_series(fundamentals, "interest_expense")

    ebiat_path_anchors: dict[str, float] = {}
    for period, ebit in ebit_series.items():
        ebiat = ebit * (1.0 - float(tax.effective_tax_rate or 0.25))
        ebiat_path_anchors[period] = (
            ebiat
            + da_series.get(period, 0.0)
            - capex_series.get(period, 0.0)
            - delta_nwc_series.get(period, 0.0)
        )

    cfo_path_anchors: dict[str, float] = {}
    cfo_after_tax_interest: dict[str, float] = {}
    cfo_interest_sources: dict[str, str] = {}
    for period, ocf in ocf_series.items():
        after_tax_interest, interest_source = _resolve_after_tax_interest_adjustment_from_values(
            interest_paid_series.get(period),
            interest_expense_series.get(period),
            tax,
            warnings,
        )
        if after_tax_interest is None:
            continue
        cfo_after_tax_interest[period] = after_tax_interest
        cfo_path_anchors[period] = ocf + after_tax_interest - capex_series.get(period, 0.0)
        if interest_source is not None:
            cfo_interest_sources[period] = interest_source

    return ebiat_path_anchors, cfo_path_anchors, cfo_after_tax_interest, cfo_interest_sources


def _compute_historical_mode_fcff_anchor(
    fundamentals: dict,
    assumptions: dict,
    tax: TaxAssumptions,
    warnings: list[str],
    anchor_mode: str,
) -> FCFFSummary | None:
    ebiat_history, cfo_history, cfo_after_tax_interest, cfo_interest_sources = _build_historical_fcff_paths(
        fundamentals,
        tax,
        warnings,
    )
    preferred_path = _resolve_fcff_preferred_path(assumptions, warnings)
    if not ebiat_history and not cfo_history:
        return None

    if anchor_mode == "reconciled_average":
        common_periods = sorted(set(ebiat_history) & set(cfo_history))[-3:]
        if common_periods:
            if len(common_periods) < 3:
                _append_once(
                    warnings,
                    "fcff_anchor_mode_reconciled_average_used_less_than_three_periods",
                )
            cfo_periods = [(period, cfo_history[period]) for period in common_periods]
            ebiat_periods = [(period, ebiat_history[period]) for period in common_periods]
            cfo_average = _average_period_values(cfo_periods)
            ebiat_average = _average_period_values(ebiat_periods)
            anchor = None
            if cfo_average is not None and ebiat_average is not None:
                anchor = (cfo_average + ebiat_average) / 2.0
            gap = None
            gap_pct = None
            if cfo_average is not None and ebiat_average is not None and anchor not in (None, 0):
                gap = cfo_average - ebiat_average
                gap_pct = gap / abs(anchor)
            _warn_on_large_fcff_gap(gap_pct, warnings)
            return FCFFSummary(
                anchor=anchor,
                anchor_method="reconciled_average_of_cfo_and_ebiat_paths",
                selected_path="reconciled",
                anchor_ebiat_path=ebiat_average,
                anchor_cfo_path=cfo_average,
                ebiat_path_available=ebiat_average is not None,
                cfo_path_available=cfo_average is not None,
                after_tax_interest=_average_period_values(
                    [
                        (period, cfo_after_tax_interest[period])
                        for period in common_periods
                        if period in cfo_after_tax_interest
                    ]
                ),
                after_tax_interest_source=_summarize_interest_sources(
                    [
                        cfo_interest_sources[period]
                        for period in common_periods
                        if period in cfo_interest_sources
                    ]
                ),
                reconciliation_gap=gap,
                reconciliation_gap_pct=gap_pct,
                anchor_mode="reconciled_average",
                anchor_observation_count=len(common_periods),
                delta_nwc_source=str(fundamentals.get("delta_nwc_source") or "historical_series"),
                last_report_period=common_periods[-1],
            )
        _append_once(
            warnings,
            "fcff_anchor_mode_reconciled_average_unavailable_fallback_to_three_period_average",
        )

    cfo_periods = _last_n_periods(cfo_history)
    ebiat_periods = _last_n_periods(ebiat_history)
    if not cfo_periods and not ebiat_periods:
        return None

    if cfo_periods and ebiat_periods:
        selected_path = preferred_path
        selected_periods = cfo_periods if preferred_path == "cfo" else ebiat_periods
    else:
        selected_periods = cfo_periods if cfo_periods else ebiat_periods
        selected_path = "cfo" if cfo_periods else "ebiat"
    if len(selected_periods) < 3:
        _append_once(warnings, "fcff_anchor_mode_three_period_average_used_less_than_three_periods")

    cfo_average = _average_period_values(cfo_periods)
    ebiat_average = _average_period_values(ebiat_periods)
    anchor = cfo_average if selected_path == "cfo" else ebiat_average
    gap = None
    gap_pct = None
    if cfo_average is not None and ebiat_average is not None and anchor not in (None, 0):
        gap = cfo_average - ebiat_average
        gap_pct = gap / abs(anchor)
    _warn_on_large_fcff_gap(gap_pct, warnings)

    return FCFFSummary(
        anchor=anchor,
        anchor_method=(
            "cfo_plus_after_tax_interest_minus_capex_three_period_average"
            if selected_path == "cfo"
            else "ebiat_plus_da_minus_capex_minus_delta_nwc_three_period_average"
        ),
        selected_path=selected_path,
        anchor_ebiat_path=ebiat_average,
        anchor_cfo_path=cfo_average,
        ebiat_path_available=ebiat_average is not None,
        cfo_path_available=cfo_average is not None,
        after_tax_interest=_average_period_values(
            [
                (period, cfo_after_tax_interest[period])
                for period, _ in cfo_periods
                if period in cfo_after_tax_interest
            ]
        ),
        after_tax_interest_source=(
            _summarize_interest_sources(
                [
                    cfo_interest_sources[period]
                    for period, _ in cfo_periods
                    if period in cfo_interest_sources
                ]
            )
            if selected_path == "cfo"
            else None
        ),
        reconciliation_gap=gap,
        reconciliation_gap_pct=gap_pct,
        anchor_mode="three_period_average",
        anchor_observation_count=len(selected_periods),
        delta_nwc_source=str(fundamentals.get("delta_nwc_source") or "historical_series"),
        last_report_period=selected_periods[-1][0],
    )


def _compute_ebiat_path_anchor(
    fundamentals: dict,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[float | None, str | None]:
    ebit = _coerce_float(fundamentals.get("ebit"))
    if ebit is None:
        return None, None

    da = _coerce_float(fundamentals.get("da")) or 0.0
    capex = _coerce_float(fundamentals.get("capex")) or 0.0
    delta_nwc, delta_source = _resolve_delta_nwc(fundamentals, warnings)
    ebiat = ebit * (1.0 - float(tax.effective_tax_rate or 0.25))
    return ebiat + da - capex - delta_nwc, delta_source


def _compute_cfo_path_anchor(
    fundamentals: dict,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[float | None, float | None, str | None]:
    ocf = _coerce_float(fundamentals.get("ocf"))
    if ocf is None:
        return None, None, None

    after_tax_interest, interest_source = _resolve_after_tax_interest_adjustment(
        fundamentals,
        tax,
        warnings,
    )
    if after_tax_interest is None:
        return None, None, None

    capex = _coerce_float(fundamentals.get("capex")) or 0.0
    return ocf + after_tax_interest - capex, after_tax_interest, interest_source


def _compute_fcff_anchor(
    fundamentals: dict,
    assumptions: dict,
    tax: TaxAssumptions,
    warnings: list[str],
    diagnostics: list[str],
) -> FCFFSummary:
    explicit_anchor = _coerce_float(fundamentals.get("fcff_anchor"))
    if explicit_anchor is not None:
        return FCFFSummary(
            anchor=explicit_anchor,
            anchor_method=str(fundamentals.get("fcff_anchor_method") or "manual_input"),
            selected_path="manual_anchor",
            ebiat_path_available=False,
            cfo_path_available=False,
            anchor_mode="manual",
            anchor_observation_count=1,
            delta_nwc_source=str(fundamentals.get("delta_nwc_source") or "manual_input"),
            last_report_period=fundamentals.get("last_report_period"),
        )

    anchor_mode = str(assumptions.get("fcff_anchor_mode") or "latest").strip().lower()
    if anchor_mode not in {"manual", "latest", "three_period_average", "reconciled_average"}:
        _append_once(warnings, "fcff_anchor_mode_invalid_defaulted_to_latest")
        anchor_mode = "latest"
    if anchor_mode == "manual":
        raise ValueError("Missing fundamentals.fcff_anchor for manual fcff_anchor_mode")
    if anchor_mode in {"three_period_average", "reconciled_average"}:
        historical_fcff = _compute_historical_mode_fcff_anchor(
            fundamentals,
            assumptions,
            tax,
            warnings,
            anchor_mode,
        )
        if historical_fcff is not None:
            return historical_fcff
        _append_once(
            warnings,
            f"fcff_anchor_mode_{anchor_mode}_history_unavailable_fallback_to_latest",
        )

    preferred_path = _resolve_fcff_preferred_path(assumptions, warnings)
    ebiat_path_anchor, delta_source = _compute_ebiat_path_anchor(fundamentals, tax, warnings)
    cfo_path_anchor, after_tax_interest, interest_source = _compute_cfo_path_anchor(
        fundamentals,
        tax,
        warnings,
    )
    ebiat_path_available = ebiat_path_anchor is not None
    cfo_path_available = cfo_path_anchor is not None

    if not ebiat_path_available and not cfo_path_available:
        raise ValueError(
            "Missing FCFF anchor inputs: provide fundamentals.fcff_anchor, "
            "EBIAT-path inputs, or CFO-path inputs"
        )

    if cfo_path_available and ebiat_path_available:
        if preferred_path == "ebiat":
            anchor = float(ebiat_path_anchor)
            anchor_method = "ebiat_plus_da_minus_capex_minus_delta_nwc"
            selected_path = "ebiat"
            diagnostics.append("fcff_path_selector_preferred_ebiat")
        else:
            anchor = float(cfo_path_anchor)
            anchor_method = "cfo_plus_after_tax_interest_minus_capex"
            selected_path = "cfo"
            diagnostics.append("fcff_path_selector_preferred_cfo")
    elif cfo_path_available:
        anchor = cfo_path_anchor
        anchor_method = "cfo_plus_after_tax_interest_minus_capex"
        selected_path = "cfo"
        diagnostics.append("fcff_path_selector_only_cfo_available")
    else:
        anchor = float(ebiat_path_anchor)
        anchor_method = "ebiat_plus_da_minus_capex_minus_delta_nwc"
        selected_path = "ebiat"
        diagnostics.append("fcff_path_selector_only_ebiat_available")

    reconciliation_gap = None
    reconciliation_gap_pct = None
    if cfo_path_available and ebiat_path_available:
        reconciliation_gap = cfo_path_anchor - ebiat_path_anchor
        if anchor != 0:
            reconciliation_gap_pct = reconciliation_gap / abs(anchor)
    _warn_on_large_fcff_gap(reconciliation_gap_pct, warnings)

    return FCFFSummary(
        anchor=anchor,
        anchor_method=anchor_method,
        selected_path=selected_path,
        anchor_ebiat_path=ebiat_path_anchor,
        anchor_cfo_path=cfo_path_anchor,
        ebiat_path_available=ebiat_path_available,
        cfo_path_available=cfo_path_available,
        after_tax_interest=after_tax_interest,
        after_tax_interest_source=interest_source,
        reconciliation_gap=reconciliation_gap,
        reconciliation_gap_pct=reconciliation_gap_pct,
        anchor_mode="latest",
        anchor_observation_count=1,
        delta_nwc_source=delta_source,
        last_report_period=fundamentals.get("last_report_period"),
    )


def _compute_wacc(
    payload: dict,
    tax: TaxAssumptions,
    warnings: list[str],
) -> tuple[WACCInputs, CapitalStructure]:
    assumptions = payload.get("assumptions") or {}
    rf = _clip_rate(_coerce_float(assumptions.get("risk_free_rate")), low=0.0, high=0.25)
    erp = _clip_rate(_coerce_float(assumptions.get("equity_risk_premium")), low=0.0, high=0.25)
    beta = _coerce_float(assumptions.get("beta"))
    rd = _clip_rate(_coerce_float(assumptions.get("pre_tax_cost_of_debt")), low=0.0, high=0.25)

    rf_source = assumptions.get("risk_free_rate_source") if rf is not None else "default"
    erp_source = assumptions.get("equity_risk_premium_source") if erp is not None else "default"
    beta_source = assumptions.get("beta_source") if beta is not None else "default"
    rd_source = assumptions.get("pre_tax_cost_of_debt_source") if rd is not None else "default"
    if rf is not None and not rf_source:
        rf_source = "manual_input"
    if erp is not None and not erp_source:
        erp_source = "manual_input"
    if beta is not None and not beta_source:
        beta_source = "manual_input"
    if rd is not None and not rd_source:
        rd_source = "manual_input"

    if rf is None:
        rf = 0.04
        warnings.append("risk_free_rate_missing_defaulted_to_0.04")
    if erp is None:
        erp = 0.05
        warnings.append("equity_risk_premium_missing_defaulted_to_0.05")
    if beta is None:
        beta = 1.0
        warnings.append("beta_missing_defaulted_to_1.0")
    if rd is None:
        rd = 0.03
        warnings.append("pre_tax_cost_of_debt_missing_defaulted_to_0.03")

    equity_weight, debt_weight, weight_source = _normalize_weights(
        assumptions.get("equity_weight"),
        assumptions.get("debt_weight"),
        assumptions.get("capital_structure_source"),
    )
    cost_of_equity = rf + beta * erp
    wacc = (
        equity_weight * cost_of_equity
        + debt_weight * rd * (1.0 - float(tax.marginal_tax_rate or 0.25))
    )

    return (
        WACCInputs(
            risk_free_rate=rf,
            risk_free_rate_source=rf_source,
            equity_risk_premium=erp,
            equity_risk_premium_source=erp_source,
            beta=beta,
            beta_source=beta_source,
            cost_of_equity=cost_of_equity,
            pre_tax_cost_of_debt=rd,
            pre_tax_cost_of_debt_source=rd_source,
            wacc=wacc,
        ),
        CapitalStructure(
            equity_weight=equity_weight,
            debt_weight=debt_weight,
            source=weight_source,
        ),
    )


def _steady_state_valuation(
    fcff_anchor: float,
    wacc: float,
    growth_rate: float,
    net_debt: float,
    shares_out: float | None,
    warnings: list[str],
) -> ValuationSummary:
    effective_growth = _clamp_growth_below_wacc(
        growth_rate,
        wacc,
        warnings=warnings,
        warning_key="terminal_growth_rate_clamped_below_wacc",
    )

    fcff_1 = fcff_anchor * (1.0 + effective_growth)
    enterprise_value = fcff_1 / (wacc - effective_growth)
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares_out if shares_out and shares_out > 0 else None

    if shares_out in (None, 0):
        warnings.append("shares_out_missing_per_share_value_unavailable")

    return ValuationSummary(
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        per_share_value=per_share,
        terminal_growth_rate=growth_rate,
        terminal_growth_rate_effective=effective_growth,
        present_value_stage1=0.0,
        present_value_stage2=None,
        present_value_terminal=enterprise_value,
        terminal_value=enterprise_value,
        terminal_value_share=1.0,
        explicit_forecast_years=0,
    )


def _two_stage_valuation(
    fcff_anchor: float,
    wacc: float,
    growth_rate_high: float,
    years_high: int,
    growth_rate_stable: float,
    net_debt: float,
    shares_out: float | None,
    warnings: list[str],
) -> ValuationSummary:
    years = max(1, int(years_high))
    g_stable_eff = _clamp_growth_below_wacc(
        growth_rate_stable,
        wacc,
        warnings=warnings,
        warning_key="stable_growth_rate_clamped_below_wacc",
    )

    fcff_t = fcff_anchor
    pv_stage1 = 0.0
    for year in range(1, years + 1):
        fcff_t = fcff_t * (1.0 + growth_rate_high)
        pv_stage1 += fcff_t / ((1.0 + wacc) ** year)

    fcff_terminal = fcff_t * (1.0 + g_stable_eff)
    terminal_value = fcff_terminal / (wacc - g_stable_eff)
    pv_terminal = terminal_value / ((1.0 + wacc) ** years)
    enterprise_value = pv_stage1 + pv_terminal
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares_out if shares_out and shares_out > 0 else None

    if shares_out in (None, 0):
        warnings.append("shares_out_missing_per_share_value_unavailable")

    terminal_share = pv_terminal / enterprise_value if enterprise_value else None
    if terminal_share is not None and terminal_share > 0.75:
        warnings.append("terminal_value_share_above_0.75")

    return ValuationSummary(
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        per_share_value=per_share,
        terminal_growth_rate=growth_rate_stable,
        terminal_growth_rate_effective=g_stable_eff,
        present_value_stage1=pv_stage1,
        present_value_stage2=None,
        present_value_terminal=pv_terminal,
        terminal_value=terminal_value,
        terminal_value_share=terminal_share,
        explicit_forecast_years=years,
    )


def _build_three_stage_growth_schedule(
    *,
    stage1_growth_rate: float,
    stage1_years: int,
    stage2_end_growth_rate: float,
    stage2_years: int,
    stage2_decay_mode: str = "linear",
) -> tuple[list[float], int, int, str]:
    if stage1_years <= 0:
        raise ValueError("assumptions.stage1_years must be a positive integer")
    if stage2_years <= 0:
        raise ValueError("assumptions.stage2_years must be a positive integer")

    decay_mode = str(stage2_decay_mode or "linear").strip() or "linear"
    if decay_mode != "linear":
        raise ValueError(f"unsupported stage2_decay_mode: {decay_mode}")

    growth_rates = [stage1_growth_rate] * stage1_years
    linear_step = (stage2_end_growth_rate - stage1_growth_rate) / stage2_years
    growth_rates.extend(
        stage1_growth_rate + (linear_step * year)
        for year in range(1, stage2_years + 1)
    )
    return growth_rates, stage1_years, stage2_years, decay_mode


def _three_stage_valuation(
    *,
    fcff_anchor: float,
    wacc: float,
    stage1_growth_rate: float,
    stage1_years: int,
    stage2_end_growth_rate: float,
    stage2_years: int,
    terminal_growth_rate: float,
    net_debt: float,
    shares_out: float | None,
    warnings: list[str],
    stage2_decay_mode: str = "linear",
) -> ValuationSummary:
    growth_schedule, stage1_years, stage2_years, decay_mode = _build_three_stage_growth_schedule(
        stage1_growth_rate=stage1_growth_rate,
        stage1_years=stage1_years,
        stage2_end_growth_rate=stage2_end_growth_rate,
        stage2_years=stage2_years,
        stage2_decay_mode=stage2_decay_mode,
    )
    effective_terminal_growth = _clamp_growth_below_wacc(
        terminal_growth_rate,
        wacc,
        warnings=warnings,
        warning_key="terminal_growth_rate_clamped_below_wacc",
    )

    fcff_t = fcff_anchor
    pv_stage1 = 0.0
    pv_stage2 = 0.0
    for year, growth_rate in enumerate(growth_schedule, start=1):
        fcff_t = fcff_t * (1.0 + growth_rate)
        present_value = fcff_t / ((1.0 + wacc) ** year)
        if year <= stage1_years:
            pv_stage1 += present_value
        else:
            pv_stage2 += present_value

    explicit_forecast_years = stage1_years + stage2_years
    fcff_terminal = fcff_t * (1.0 + effective_terminal_growth)
    terminal_value = fcff_terminal / (wacc - effective_terminal_growth)
    pv_terminal = terminal_value / ((1.0 + wacc) ** explicit_forecast_years)
    enterprise_value = pv_stage1 + pv_stage2 + pv_terminal
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares_out if shares_out and shares_out > 0 else None
    terminal_share = pv_terminal / enterprise_value if enterprise_value else None

    if shares_out in (None, 0):
        warnings.append("shares_out_missing_per_share_value_unavailable")
    if terminal_share is not None and terminal_share > 0.75:
        warnings.append("terminal_value_share_above_0.75")

    return ValuationSummary(
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        per_share_value=per_share,
        terminal_growth_rate=terminal_growth_rate,
        terminal_growth_rate_effective=effective_terminal_growth,
        present_value_stage1=pv_stage1,
        present_value_stage2=pv_stage2,
        present_value_terminal=pv_terminal,
        terminal_value=terminal_value,
        terminal_value_share=terminal_share,
        explicit_forecast_years=explicit_forecast_years,
        stage1_years=stage1_years,
        stage2_years=stage2_years,
        stage2_decay_mode=decay_mode,
    )


def _resolve_market_implied_solver(valuation_model: str, solver: str) -> str:
    requested_solver = str(solver or "auto").strip().lower()
    if requested_solver not in {"auto", "closed_form", "bisection"}:
        raise ValueError("market_implied_growth.solver must be one of {auto, closed_form, bisection}")
    if valuation_model == "steady_state_single_stage":
        return "closed_form"
    if requested_solver == "closed_form":
        raise ValueError(
            "market_implied_growth solver closed_form is only supported for steady_state_single_stage"
        )
    return "bisection"


def _resolve_market_implied_target(
    market_inputs,
    *,
    shares_out: float | None,
    net_debt: float | None,
) -> dict:
    resolved_shares_out = _coerce_float(market_inputs.shares_out)
    if resolved_shares_out is None:
        resolved_shares_out = shares_out

    resolved_net_debt = _coerce_float(market_inputs.net_debt)
    if resolved_net_debt is None:
        resolved_net_debt = net_debt

    market_price = _coerce_float(market_inputs.market_price)
    enterprise_value_market = _coerce_float(market_inputs.enterprise_value_market)

    if market_price is None and enterprise_value_market is None:
        raise ValueError(
            "market_implied_growth requires market_inputs.market_price or market_inputs.enterprise_value_market"
        )

    if market_price is not None and enterprise_value_market is None:
        if resolved_shares_out is None or resolved_shares_out <= 0:
            raise ValueError(
                "market_implied_growth requires shares_out to resolve market_inputs.market_price"
            )
        if resolved_net_debt is None:
            raise ValueError(
                "market_implied_growth requires net_debt to resolve market_inputs.market_price"
            )
        enterprise_value_market = (market_price * resolved_shares_out) + resolved_net_debt

    target_metric = "enterprise_value"
    target_value = enterprise_value_market
    if market_price is not None:
        target_metric = "per_share_value"
        target_value = market_price
    elif (
        enterprise_value_market is not None
        and resolved_shares_out is not None
        and resolved_shares_out > 0
        and resolved_net_debt is not None
    ):
        market_price = (enterprise_value_market - resolved_net_debt) / resolved_shares_out
        target_metric = "per_share_value"
        target_value = market_price

    if target_value is None:
        raise ValueError("market_implied_growth could not resolve a market target")

    return {
        "target_metric": target_metric,
        "target_value": target_value,
        "market_price": market_price,
        "enterprise_value_market": enterprise_value_market,
        "shares_out": resolved_shares_out,
        "net_debt": 0.0 if resolved_net_debt is None else resolved_net_debt,
    }


def _extract_market_implied_metric(valuation: ValuationSummary, target_metric: str) -> float:
    if target_metric == "per_share_value":
        value = valuation.per_share_value
    elif target_metric == "enterprise_value":
        value = valuation.enterprise_value
    else:  # pragma: no cover - guarded by caller
        raise ValueError(f"unsupported market-implied target metric: {target_metric}")

    numeric = _coerce_float(value)
    if numeric is None:
        raise ValueError(f"market_implied_growth requires valuation.{target_metric}")
    return numeric


def _bisect_market_implied_growth(
    *,
    evaluate_metric,
    target_value: float,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
) -> dict:
    def objective(candidate_growth_rate: float) -> float:
        return evaluate_metric(candidate_growth_rate) - target_value

    f_lower = objective(lower_bound)
    f_upper = objective(upper_bound)
    if abs(f_lower) <= tolerance:
        return {
            "success": True,
            "solved_value": lower_bound,
            "iterations": 0,
            "residual": abs(f_lower),
            "reason": None,
        }
    if abs(f_upper) <= tolerance:
        return {
            "success": True,
            "solved_value": upper_bound,
            "iterations": 0,
            "residual": abs(f_upper),
            "reason": None,
        }
    if f_lower * f_upper > 0:
        return {
            "success": False,
            "solved_value": None,
            "iterations": None,
            "residual": None,
            "reason": "unbracketed_bounds",
        }

    lower = lower_bound
    upper = upper_bound
    iterations = 0
    while iterations < max_iterations:
        midpoint = (lower + upper) / 2.0
        f_mid = objective(midpoint)
        if abs(f_mid) <= tolerance or abs(upper - lower) <= tolerance:
            return {
                "success": True,
                "solved_value": midpoint,
                "iterations": iterations + 1,
                "residual": abs(f_mid),
                "reason": None,
            }
        if f_lower * f_mid <= 0:
            upper = midpoint
            f_upper = f_mid
        else:
            lower = midpoint
            f_lower = f_mid
        iterations += 1

    midpoint = (lower + upper) / 2.0
    return {
        "success": False,
        "solved_value": None,
        "iterations": max_iterations,
        "residual": abs(objective(midpoint)),
        "reason": "max_iterations_exceeded",
    }


def _solve_market_implied_growth_single_stage(
    *,
    fcff_anchor: float,
    wacc: float,
    enterprise_value_market: float | None,
) -> dict:
    if enterprise_value_market is None or enterprise_value_market <= 0 or fcff_anchor <= 0 or wacc <= 0:
        return {
            "success": False,
            "solved_value": None,
            "iterations": None,
            "residual": None,
            "reason": "invalid_market_inputs",
        }

    denominator = enterprise_value_market + fcff_anchor
    if denominator == 0:
        return {
            "success": False,
            "solved_value": None,
            "iterations": None,
            "residual": None,
            "reason": "invalid_market_inputs",
        }

    solved_value = (enterprise_value_market * wacc - fcff_anchor) / denominator
    return {
        "success": True,
        "solved_value": solved_value,
        "iterations": 0,
        "residual": 0.0,
        "reason": None,
    }


def _solve_market_implied_growth_bisection(
    *,
    build_valuation,
    base_growth_rate: float,
    target_metric: str,
    target_value: float | None,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
) -> dict:
    if target_value is None or target_value <= 0:
        return {
            "success": False,
            "solved_value": None,
            "iterations": None,
            "residual": None,
            "reason": "invalid_market_inputs",
        }

    base_case_valuation = build_valuation(base_growth_rate)
    base_case_value = _extract_market_implied_metric(base_case_valuation, target_metric)
    result = _bisect_market_implied_growth(
        evaluate_metric=lambda candidate_growth_rate: _extract_market_implied_metric(
            build_valuation(candidate_growth_rate),
            target_metric,
        ),
        target_value=target_value,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )
    result["base_case_value"] = base_case_value
    result["base_case_per_share_value"] = _coerce_float(base_case_valuation.per_share_value)
    result["base_case_enterprise_value"] = _coerce_float(base_case_valuation.enterprise_value)
    return result


def _solve_market_implied_growth_two_stage(
    *,
    fcff_anchor: float,
    wacc: float,
    stage1_growth_rate: float,
    stage1_years: int,
    terminal_growth_rate: float,
    target_metric: str,
    target_value: float,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
    net_debt: float,
    shares_out: float | None,
) -> dict:
    def build_valuation(candidate_growth_rate: float) -> ValuationSummary:
        return _two_stage_valuation(
            fcff_anchor=fcff_anchor,
            wacc=wacc,
            growth_rate_high=candidate_growth_rate,
            years_high=stage1_years,
            growth_rate_stable=terminal_growth_rate,
            net_debt=net_debt,
            shares_out=shares_out,
            warnings=[],
        )

    return _solve_market_implied_growth_bisection(
        build_valuation=build_valuation,
        base_growth_rate=stage1_growth_rate,
        target_metric=target_metric,
        target_value=target_value,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )


def _solve_market_implied_growth_three_stage(
    *,
    fcff_anchor: float,
    wacc: float,
    stage1_growth_rate: float,
    stage1_years: int,
    stage2_end_growth_rate: float,
    stage2_years: int,
    stage2_decay_mode: str,
    terminal_growth_rate: float,
    target_metric: str,
    target_value: float,
    lower_bound: float,
    upper_bound: float,
    tolerance: float,
    max_iterations: int,
    net_debt: float,
    shares_out: float | None,
) -> dict:
    def build_valuation(candidate_growth_rate: float) -> ValuationSummary:
        return _three_stage_valuation(
            fcff_anchor=fcff_anchor,
            wacc=wacc,
            stage1_growth_rate=candidate_growth_rate,
            stage1_years=stage1_years,
            stage2_end_growth_rate=stage2_end_growth_rate,
            stage2_years=stage2_years,
            terminal_growth_rate=terminal_growth_rate,
            net_debt=net_debt,
            shares_out=shares_out,
            warnings=[],
            stage2_decay_mode=stage2_decay_mode,
        )

    return _solve_market_implied_growth_bisection(
        build_valuation=build_valuation,
        base_growth_rate=stage1_growth_rate,
        target_metric=target_metric,
        target_value=target_value,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )


def _market_implied_growth_failure_message(reason: str | None) -> str:
    if reason == "unbracketed_bounds":
        return "No sign change in bounds for market-implied growth solver."
    if reason == "max_iterations_exceeded":
        return "Market-implied growth solver did not converge within the configured iteration limit."
    if reason == "invalid_market_inputs":
        return "Invalid market EV / shares_out / price inputs."
    return "Market-implied growth solver could not resolve a result."


def _build_market_implied_growth_summary(
    *,
    payload: dict,
    valuation_model: str,
    valuation: ValuationSummary,
    fcff_anchor: float,
    wacc: float,
    context: dict | None,
    shares_out: float | None,
    net_debt: float | None,
) -> MarketImpliedGrowthOutput | None:
    request = resolve_market_implied_growth_input(payload)
    if request is None:
        return None

    if valuation_model not in _SUPPORTED_VALUATION_MODELS:
        raise ValueError("market_implied_growth requires valuation_model in {steady_state_single_stage, two_stage, three_stage}")

    market_inputs = resolve_market_inputs(payload)
    solved_field = "growth_rate" if valuation_model == "steady_state_single_stage" else "stage1_growth_rate"
    solver_used = _resolve_market_implied_solver(valuation_model, request.solver)

    try:
        market_target = _resolve_market_implied_target(
            market_inputs,
            shares_out=shares_out,
            net_debt=net_debt,
        )
    except ValueError as exc:
        return MarketImpliedGrowthOutput(
            enabled=True,
            success=False,
            valuation_model=valuation_model,
            solved_field=solved_field,
            solver_used=solver_used,
            lower_bound=request.lower_bound,
            upper_bound=request.upper_bound,
            market_price=_coerce_float(market_inputs.market_price),
            market_enterprise_value=_coerce_float(market_inputs.enterprise_value_market),
            base_case_per_share_value=_coerce_float(valuation.per_share_value),
            base_case_enterprise_value=_coerce_float(valuation.enterprise_value),
            message=str(exc),
        )

    target_value = _coerce_float(market_target.get("target_value"))
    market_price = _coerce_float(market_target.get("market_price"))
    market_enterprise_value = _coerce_float(market_target.get("enterprise_value_market"))
    if target_value is None or target_value <= 0:
        return MarketImpliedGrowthOutput(
            enabled=True,
            success=False,
            valuation_model=valuation_model,
            solved_field=solved_field,
            solver_used=solver_used,
            lower_bound=request.lower_bound,
            upper_bound=request.upper_bound,
            market_price=market_price,
            market_enterprise_value=market_enterprise_value,
            base_case_per_share_value=_coerce_float(valuation.per_share_value),
            base_case_enterprise_value=_coerce_float(valuation.enterprise_value),
            message="Invalid market EV / shares_out / price inputs.",
        )

    result: dict
    if valuation_model == "steady_state_single_stage":
        result = _solve_market_implied_growth_single_stage(
            fcff_anchor=fcff_anchor,
            wacc=wacc,
            enterprise_value_market=market_enterprise_value,
        )
    elif valuation_model == "two_stage":
        if context is None:
            raise ValueError("market_implied_growth requires resolved valuation inputs")
        result = _solve_market_implied_growth_two_stage(
            fcff_anchor=fcff_anchor,
            wacc=wacc,
            stage1_growth_rate=float(context["stage1_growth_rate"]),
            stage1_years=int(context["stage1_years"]),
            terminal_growth_rate=float(context["terminal_growth_rate"]),
            target_metric=str(market_target["target_metric"]),
            target_value=target_value,
            lower_bound=float(request.lower_bound),
            upper_bound=float(request.upper_bound),
            tolerance=float(request.tolerance),
            max_iterations=int(request.max_iterations),
            net_debt=float(market_target["net_debt"]),
            shares_out=market_target["shares_out"],
        )
    else:
        if context is None:
            raise ValueError("market_implied_growth requires resolved valuation inputs")
        result = _solve_market_implied_growth_three_stage(
            fcff_anchor=fcff_anchor,
            wacc=wacc,
            stage1_growth_rate=float(context["stage1_growth_rate"]),
            stage1_years=int(context["stage1_years"]),
            stage2_end_growth_rate=float(context["stage2_end_growth_rate"]),
            stage2_years=int(context["stage2_years"]),
            stage2_decay_mode=str(context["stage2_decay_mode"]),
            terminal_growth_rate=float(context["terminal_growth_rate"]),
            target_metric=str(market_target["target_metric"]),
            target_value=target_value,
            lower_bound=float(request.lower_bound),
            upper_bound=float(request.upper_bound),
            tolerance=float(request.tolerance),
            max_iterations=int(request.max_iterations),
            net_debt=float(market_target["net_debt"]),
            shares_out=market_target["shares_out"],
        )

    success = bool(result.get("success"))
    message = (
        "Market-implied growth solved successfully."
        if success
        else _market_implied_growth_failure_message(str(result.get("reason") or ""))
    )
    return MarketImpliedGrowthOutput(
        enabled=True,
        success=success,
        valuation_model=valuation_model,
        solved_field=solved_field,
        solved_value=_coerce_float(result.get("solved_value")),
        solver_used=solver_used,
        lower_bound=float(request.lower_bound),
        upper_bound=float(request.upper_bound),
        iterations=result.get("iterations"),
        residual=_coerce_float(result.get("residual")),
        market_price=market_price,
        market_enterprise_value=market_enterprise_value,
        base_case_per_share_value=_coerce_float(valuation.per_share_value),
        base_case_enterprise_value=_coerce_float(valuation.enterprise_value),
        message=message,
    )


def run_valuation(payload: dict) -> ValuationOutput:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")
    reject_removed_market_implied_blocks(payload)

    fundamentals = payload.get("fundamentals") or {}
    assumptions = payload.get("assumptions") or {}
    warnings: list[str] = list(payload.get("_prefill_warnings", []))
    diagnostics: list[str] = list(payload.get("_prefill_diagnostics", []))
    degradation_reasons: list[str] = []
    requested_valuation_model, effective_valuation_model = _resolve_requested_valuation_model(
        payload,
        warnings,
    )

    tax = _resolve_tax_inputs(payload, warnings, diagnostics)
    fcff = _compute_fcff_anchor(fundamentals, assumptions, tax, warnings, diagnostics)
    if fcff.anchor is None:
        raise ValueError("Unable to compute FCFF anchor")
    if fcff.anchor <= 0:
        warnings.append("fcff_anchor_non_positive")
    if fcff.selected_path:
        diagnostics.append(f"fcff_path_selected:{fcff.selected_path}")

    wacc_inputs, capital_structure = _compute_wacc(payload, tax, warnings)
    if wacc_inputs.wacc is None or wacc_inputs.wacc <= 0:
        raise ValueError("Unable to compute a positive WACC")

    fundamentals_net_debt = _coerce_float(fundamentals.get("net_debt"))
    net_debt = fundamentals_net_debt or 0.0
    shares_out = _coerce_float(fundamentals.get("shares_out"))
    market_implied_context: dict | None = None

    if effective_valuation_model == "steady_state_single_stage":
        growth_rate = _resolve_rate_input(
            assumptions,
            "terminal_growth_rate",
            low=0.0,
            high=0.15,
            warnings=warnings,
            default=0.03,
            missing_warning="terminal_growth_rate_missing_defaulted_to_0.03",
            clip_warning="terminal_growth_rate_clipped_to_supported_range",
        )
        valuation = _steady_state_valuation(
            fcff_anchor=fcff.anchor,
            wacc=wacc_inputs.wacc,
            growth_rate=growth_rate,
            net_debt=net_debt,
            shares_out=shares_out,
            warnings=warnings,
        )
        market_implied_context = {"growth_rate": growth_rate}
        diagnostics.append("valuation_model_steady_state_single_stage")
    elif effective_valuation_model == "two_stage":
        growth_rate = _resolve_rate_input(
            assumptions,
            "terminal_growth_rate",
            low=0.0,
            high=0.15,
            warnings=warnings,
            default=0.03,
            missing_warning="terminal_growth_rate_missing_defaulted_to_0.03",
            clip_warning="terminal_growth_rate_clipped_to_supported_range",
        )
        growth_rate_high, years_high = _resolve_two_stage_inputs(assumptions, warnings)
        valuation = _two_stage_valuation(
            fcff_anchor=fcff.anchor,
            wacc=wacc_inputs.wacc,
            growth_rate_high=growth_rate_high,
            years_high=years_high,
            growth_rate_stable=growth_rate,
            net_debt=net_debt,
            shares_out=shares_out,
            warnings=warnings,
        )
        market_implied_context = {
            "stage1_growth_rate": growth_rate_high,
            "stage1_years": years_high,
            "terminal_growth_rate": growth_rate,
            "net_debt": fundamentals_net_debt,
            "shares_out": shares_out,
        }
        diagnostics.append("valuation_model_two_stage")
    else:
        stage1_growth_rate = _resolve_rate_input(
            assumptions,
            "stage1_growth_rate",
            low=0.0,
            high=1.0,
            warnings=warnings,
            required=True,
            clip_warning="stage1_growth_rate_clipped_to_supported_range",
        )
        stage2_end_growth_rate = _resolve_rate_input(
            assumptions,
            "stage2_end_growth_rate",
            low=0.0,
            high=1.0,
            warnings=warnings,
            required=True,
            clip_warning="stage2_end_growth_rate_clipped_to_supported_range",
        )
        terminal_growth_rate = _resolve_rate_input(
            assumptions,
            "terminal_growth_rate",
            low=0.0,
            high=0.15,
            warnings=warnings,
            required=True,
            clip_warning="terminal_growth_rate_clipped_to_supported_range",
        )
        if not (
            stage1_growth_rate >= stage2_end_growth_rate >= terminal_growth_rate
        ):
            raise ValueError(
                "three_stage growth rates must satisfy "
                "stage1_growth_rate >= stage2_end_growth_rate >= terminal_growth_rate"
            )
        stage1_years = _coerce_positive_int(
            assumptions.get("stage1_years"),
            field_name="stage1_years",
        )
        stage2_years = _coerce_positive_int(
            assumptions.get("stage2_years"),
            field_name="stage2_years",
        )
        stage2_decay_mode = str(assumptions.get("stage2_decay_mode") or "linear").strip() or "linear"

        valuation = _three_stage_valuation(
            fcff_anchor=fcff.anchor,
            wacc=wacc_inputs.wacc,
            stage1_growth_rate=stage1_growth_rate,
            stage1_years=stage1_years,
            stage2_end_growth_rate=stage2_end_growth_rate,
            stage2_years=stage2_years,
            terminal_growth_rate=terminal_growth_rate,
            net_debt=net_debt,
            shares_out=shares_out,
            warnings=warnings,
            stage2_decay_mode=stage2_decay_mode,
        )
        market_implied_context = {
            "stage1_growth_rate": stage1_growth_rate,
            "stage1_years": stage1_years,
            "stage2_end_growth_rate": stage2_end_growth_rate,
            "stage2_years": stage2_years,
            "stage2_decay_mode": stage2_decay_mode,
            "terminal_growth_rate": terminal_growth_rate,
            "net_debt": fundamentals_net_debt,
            "shares_out": shares_out,
        }
        diagnostics.append("valuation_model_three_stage")

    if capital_structure.source == "default":
        _append_once(warnings, "capital_structure_weights_defaulted_to_0.7_0.3")
        _mark_degraded(
            degradation_reasons,
            "degraded_due_to_default_capital_structure",
        )

    if fcff.delta_nwc_source == "assumed_zero":
        _mark_degraded(
            degradation_reasons,
            "degraded_due_to_assumed_zero_delta_nwc",
        )

    if fcff.selected_path == "ebiat" and fcff.cfo_path_available is False:
        _mark_degraded(
            degradation_reasons,
            "degraded_due_to_ebiat_only_fcff_anchor",
        )
        if fcff.delta_nwc_source == "assumed_zero":
            _append_once(
                warnings,
                "fcff_anchor_quality_is_low_ebiat_only_with_assumed_zero_delta_nwc",
            )

    if valuation.per_share_value is None and (shares_out is None or shares_out <= 0):
        _mark_degraded(
            degradation_reasons,
            "degraded_due_to_missing_shares_out",
        )

    data_freshness = _resolve_data_freshness(
        payload,
        warnings=warnings,
        diagnostics=diagnostics,
        degradation_reasons=degradation_reasons,
    )

    degraded = bool(degradation_reasons)

    market_implied_growth = _build_market_implied_growth_summary(
        payload=payload,
        valuation_model=effective_valuation_model,
        valuation=valuation,
        fcff_anchor=fcff.anchor,
        wacc=wacc_inputs.wacc,
        context=market_implied_context,
        shares_out=shares_out,
        net_debt=fundamentals_net_debt,
    )

    output = ValuationOutput(
        ticker=str(payload.get("ticker") or "UNKNOWN"),
        market=str(payload.get("market") or "UNKNOWN"),
        currency=payload.get("currency"),
        as_of_date=str(payload.get("as_of_date") or date.today().isoformat()),
        valuation_model=effective_valuation_model,
        requested_valuation_model=requested_valuation_model,
        effective_valuation_model=effective_valuation_model,
        degraded=degraded,
        degradation_reasons=degradation_reasons,
        tax=tax,
        wacc_inputs=wacc_inputs,
        capital_structure=capital_structure,
        fcff=fcff,
        valuation=valuation,
        market_implied_growth=market_implied_growth,
        data_freshness=data_freshness,
        diagnostics=diagnostics,
        warnings=warnings,
    )
    return output
