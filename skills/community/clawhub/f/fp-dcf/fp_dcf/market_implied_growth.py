from __future__ import annotations

from math import isfinite

from .schemas import MarketImpliedGrowthInput, MarketInputsSummary


def _coerce_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if isfinite(out) else None


def _pick_float(*candidates: tuple[object, str]) -> tuple[float | None, str | None]:
    for value, source in candidates:
        coerced = _coerce_float(value)
        if coerced is not None:
            return coerced, source
    return None, None


def _coerce_bool(value, *, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def reject_removed_market_implied_blocks(payload: dict) -> None:
    if "implied_growth" in payload:
        raise ValueError("`implied_growth` has been removed. Use `market_implied_growth` instead.")
    if "market_implied_stage1_growth" in payload:
        raise ValueError(
            "`market_implied_stage1_growth` has been removed. Use `market_implied_growth` instead."
        )


def resolve_market_implied_growth_input(payload: dict) -> MarketImpliedGrowthInput | None:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    reject_removed_market_implied_blocks(payload)

    config = payload.get("market_implied_growth")
    if config is None:
        return None
    if not isinstance(config, dict):
        raise TypeError("payload.market_implied_growth must be an object when provided")

    enabled = _coerce_bool(config.get("enabled"), default=False)
    if not enabled:
        return None

    solver = str(config.get("solver") or "auto").strip().lower()
    if solver not in {"auto", "closed_form", "bisection"}:
        raise ValueError("market_implied_growth.solver must be one of {auto, closed_form, bisection}")

    lower_bound = _coerce_float(config.get("lower_bound"))
    upper_bound = _coerce_float(config.get("upper_bound"))
    tolerance = _coerce_float(config.get("tolerance"))
    max_iterations_value = _coerce_float(config.get("max_iterations"))

    resolved = MarketImpliedGrowthInput(
        enabled=True,
        lower_bound=-0.5 if lower_bound is None else lower_bound,
        upper_bound=0.5 if upper_bound is None else upper_bound,
        solver=solver,
        tolerance=1e-6 if tolerance is None else tolerance,
        max_iterations=100 if max_iterations_value is None else int(max_iterations_value),
    )
    if resolved.lower_bound >= resolved.upper_bound:
        raise ValueError("market_implied_growth bounds must satisfy lower_bound < upper_bound")
    if resolved.tolerance <= 0:
        raise ValueError("market_implied_growth tolerance must be positive")
    if resolved.max_iterations <= 0:
        raise ValueError("market_implied_growth max_iterations must be positive")
    return resolved


def resolve_market_inputs(payload: dict) -> MarketInputsSummary:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    market_inputs = payload.get("market_inputs") or {}
    fundamentals = payload.get("fundamentals") or {}

    enterprise_value_market, enterprise_value_market_source = _pick_float(
        (market_inputs.get("enterprise_value_market"), "market_inputs.enterprise_value_market"),
    )
    market_price, market_price_source = _pick_float(
        (market_inputs.get("market_price"), "market_inputs.market_price"),
        (fundamentals.get("market_price"), "fundamentals.market_price"),
    )
    shares_out, shares_out_source = _pick_float(
        (market_inputs.get("shares_out"), "market_inputs.shares_out"),
        (fundamentals.get("shares_out"), "fundamentals.shares_out"),
    )
    net_debt, net_debt_source = _pick_float(
        (market_inputs.get("net_debt"), "market_inputs.net_debt"),
        (fundamentals.get("net_debt"), "fundamentals.net_debt"),
    )

    equity_value_market = None
    if market_price is not None and shares_out is not None:
        equity_value_market = market_price * shares_out

    if enterprise_value_market is None and equity_value_market is not None and net_debt is not None:
        enterprise_value_market = equity_value_market + net_debt
        enterprise_value_market_source = "derived_from_market_price_shares_out_and_net_debt"

    return MarketInputsSummary(
        enterprise_value_market=enterprise_value_market,
        enterprise_value_market_source=enterprise_value_market_source,
        equity_value_market=equity_value_market,
        market_price=market_price,
        market_price_source=market_price_source,
        shares_out=shares_out,
        shares_out_source=shares_out_source,
        net_debt=net_debt,
        net_debt_source=net_debt_source,
    )
