from __future__ import annotations

from copy import deepcopy
from math import isfinite

from .engine import run_valuation
from .schemas import SensitivityHeatmapOutput, ValuationSummary


_METRIC_LABELS = {
    "per_share_value": "Per Share Value",
    "equity_value": "Equity Value",
    "enterprise_value": "Enterprise Value",
}


def _coerce_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if isfinite(out) else None


def _clip_rate(value: float | None, *, low: float, high: float) -> float | None:
    if value is None:
        return None
    return min(max(value, low), high)


def _grid_around(center: float, *, range_bps: int, step_bps: int, floor: float, ceiling: float) -> list[float]:
    if step_bps <= 0:
        raise ValueError("step_bps must be positive")
    if range_bps < 0:
        raise ValueError("range_bps must be non-negative")

    values: list[float] = []
    for offset_bps in range(-range_bps, range_bps + 1, step_bps):
        value = center + (offset_bps / 10000.0)
        if floor <= value <= ceiling:
            values.append(round(value, 6))

    values.sort()
    return values


def _metric_value(summary: ValuationSummary, metric: str) -> float | None:
    if metric not in _METRIC_LABELS:
        raise ValueError(f"Unsupported sensitivity metric: {metric}")
    return _coerce_float(getattr(summary, metric, None))


def _steady_state_value(
    *,
    fcff_anchor: float,
    wacc: float,
    terminal_growth_rate: float,
    net_debt: float,
    shares_out: float | None,
) -> ValuationSummary | None:
    if terminal_growth_rate >= wacc:
        return None

    fcff_1 = fcff_anchor * (1.0 + terminal_growth_rate)
    enterprise_value = fcff_1 / (wacc - terminal_growth_rate)
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares_out if shares_out and shares_out > 0 else None
    return ValuationSummary(
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        per_share_value=per_share,
        terminal_growth_rate=terminal_growth_rate,
        terminal_growth_rate_effective=terminal_growth_rate,
        present_value_stage1=0.0,
        present_value_terminal=enterprise_value,
        terminal_value_share=1.0,
    )


def _two_stage_value(
    *,
    fcff_anchor: float,
    wacc: float,
    high_growth_rate: float,
    high_growth_years: int,
    terminal_growth_rate: float,
    net_debt: float,
    shares_out: float | None,
) -> ValuationSummary | None:
    if terminal_growth_rate >= wacc:
        return None

    years = max(1, int(high_growth_years))
    fcff_t = fcff_anchor
    pv_stage1 = 0.0
    for year in range(1, years + 1):
        fcff_t = fcff_t * (1.0 + high_growth_rate)
        pv_stage1 += fcff_t / ((1.0 + wacc) ** year)

    fcff_terminal = fcff_t * (1.0 + terminal_growth_rate)
    terminal_value = fcff_terminal / (wacc - terminal_growth_rate)
    pv_terminal = terminal_value / ((1.0 + wacc) ** years)
    enterprise_value = pv_stage1 + pv_terminal
    equity_value = enterprise_value - net_debt
    per_share = equity_value / shares_out if shares_out and shares_out > 0 else None
    terminal_share = pv_terminal / enterprise_value if enterprise_value else None

    return ValuationSummary(
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        per_share_value=per_share,
        terminal_growth_rate=terminal_growth_rate,
        terminal_growth_rate_effective=terminal_growth_rate,
        present_value_stage1=pv_stage1,
        present_value_terminal=pv_terminal,
        terminal_value_share=terminal_share,
    )


def build_wacc_terminal_growth_sensitivity(
    payload: dict,
    *,
    metric: str = "per_share_value",
    market_price: float | None = None,
    wacc_values: list[float] | None = None,
    terminal_growth_values: list[float] | None = None,
    wacc_range_bps: int = 200,
    wacc_step_bps: int = 100,
    growth_range_bps: int = 100,
    growth_step_bps: int = 50,
) -> SensitivityHeatmapOutput:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")
    if metric not in _METRIC_LABELS:
        raise ValueError(f"Unsupported sensitivity metric: {metric}")

    base_payload = deepcopy(payload)
    base_output = run_valuation(base_payload)
    base_metric_value = _metric_value(base_output.valuation, metric)
    if base_metric_value is None:
        raise ValueError(
            f"Unable to compute sensitivity metric '{metric}' from the base valuation. "
            "Choose a different metric or provide the missing fundamentals."
        )

    base_wacc = _coerce_float(base_output.wacc_inputs.wacc)
    base_growth = _coerce_float(base_output.valuation.terminal_growth_rate)
    if base_wacc is None or base_wacc <= 0:
        raise ValueError("Base valuation did not produce a positive WACC")
    if base_growth is None:
        raise ValueError("Base valuation did not produce a terminal growth rate")
    base_wacc = round(base_wacc, 6)
    base_growth = round(base_growth, 6)

    fundamentals = base_payload.get("fundamentals") or {}
    assumptions = base_payload.get("assumptions") or {}
    net_debt = _coerce_float(fundamentals.get("net_debt")) or 0.0
    shares_out = _coerce_float(fundamentals.get("shares_out"))
    fcff_anchor = _coerce_float(base_output.fcff.anchor)
    if fcff_anchor is None:
        raise ValueError("Base valuation did not produce an FCFF anchor")

    valuation_model = str(base_output.valuation_model or "steady_state_single_stage")
    high_growth_rate = _clip_rate(
        _coerce_float(assumptions.get("stage1_growth_rate") or assumptions.get("high_growth_rate")),
        low=-0.5,
        high=1.0,
    )
    if high_growth_rate is None:
        high_growth_rate = 0.10
    high_growth_years = int(
        _coerce_float(assumptions.get("stage1_years") or assumptions.get("high_growth_years")) or 5
    )

    wacc_axis = (
        sorted({round(float(value), 6) for value in wacc_values})
        if wacc_values is not None
        else _grid_around(
            base_wacc,
            range_bps=wacc_range_bps,
            step_bps=wacc_step_bps,
            floor=0.01,
            ceiling=0.5,
        )
    )
    growth_axis = (
        sorted({round(float(value), 6) for value in terminal_growth_values})
        if terminal_growth_values is not None
        else _grid_around(
            base_growth,
            range_bps=growth_range_bps,
            step_bps=growth_step_bps,
            floor=0.0,
            ceiling=0.15,
        )
    )

    invalid_cells = 0
    matrix: list[list[float | None]] = []
    for wacc in wacc_axis:
        row: list[float | None] = []
        for growth in growth_axis:
            if valuation_model == "two_stage":
                summary = _two_stage_value(
                    fcff_anchor=fcff_anchor,
                    wacc=wacc,
                    high_growth_rate=high_growth_rate,
                    high_growth_years=high_growth_years,
                    terminal_growth_rate=growth,
                    net_debt=net_debt,
                    shares_out=shares_out,
                )
            else:
                summary = _steady_state_value(
                    fcff_anchor=fcff_anchor,
                    wacc=wacc,
                    terminal_growth_rate=growth,
                    net_debt=net_debt,
                    shares_out=shares_out,
                )
            if summary is None:
                invalid_cells += 1
                row.append(None)
            else:
                row.append(_metric_value(summary, metric))
        matrix.append(row)

    diagnostics = list(base_output.diagnostics)
    warnings = list(base_output.warnings)
    diagnostics.append("sensitivity_heatmap:wacc_x_terminal_growth")
    diagnostics.append(f"sensitivity_metric:{metric}")
    if invalid_cells:
        diagnostics.append(f"sensitivity_invalid_cells:{invalid_cells}")

    return SensitivityHeatmapOutput(
        ticker=base_output.ticker,
        market=base_output.market,
        currency=base_output.currency,
        as_of_date=base_output.as_of_date,
        valuation_model=valuation_model,
        metric=metric,
        metric_label=_METRIC_LABELS[metric],
        base_wacc=base_wacc,
        base_terminal_growth_rate=base_growth,
        base_metric_value=base_metric_value,
        market_price=market_price,
        wacc_values=wacc_axis,
        terminal_growth_values=growth_axis,
        matrix=matrix,
        diagnostics=diagnostics,
        warnings=warnings,
    )
