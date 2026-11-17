"""Deterministic market summary, regime classification, and setup-fit scoring."""
from __future__ import annotations

import math
from datetime import datetime

from strategy_library import STRATEGIES


def _number(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _clamp(value, lower=0, upper=100):
    return max(lower, min(upper, value))


def _closest(rows, target_days, value_key="days_to_expiry"):
    usable = [row for row in rows if _number(row.get(value_key)) is not None]
    return min(usable, key=lambda row: abs(_number(row[value_key]) - target_days)) if usable else None


def _prediction_read(dossier, spot, as_of):
    """Summarize the closest fitted terminal ladder without mixing barrier risk."""
    candidates = []
    now = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    for ladder in dossier.get("terminal_ladders", []):
        if ladder.get("fit_status") != "isotonic_terminal_probability_curve":
            continue
        try:
            days = (datetime.fromisoformat(str(ladder["rule_window_at"]).replace("Z", "+00:00")) - now).total_seconds() / 86400
        except (KeyError, TypeError, ValueError):
            continue
        anchors = ladder.get("anchors", [])
        if days <= 0 or not anchors or not spot:
            continue
        anchor = min(anchors, key=lambda row: abs(abs(_number(row.get("strike_usd")) / spot - 1) - .05))
        probability = _number(anchor.get("fitted_probability_pct"))
        if probability is not None:
            candidates.append((abs(days - 30), days, ladder, anchor, probability))
    ladder_summaries = [{
        "event_slug": row.get("event_slug"),
        "rule_window_at": row.get("rule_window_at"),
        "direction": row.get("direction"),
        "contract_count": row.get("contract_count"),
        "quote_quality": row.get("quote_quality"),
        "average_spread_pct_points": row.get("average_spread_pct_points"),
        "interpolated_probability_at_reference_pct": row.get("interpolated_probability_at_reference_pct"),
    } for row in dossier.get("terminal_ladders", []) if row.get("fit_status") == "isotonic_terminal_probability_curve"]
    if not candidates:
        return {"bias": "unavailable", "horizon_days": None, "reference_probability_pct": None, "terminal_ladder_summaries": ladder_summaries, "barrier_group_count": len(dossier.get("barrier_groups", []))}
    _, days, ladder, anchor, probability = min(candidates, key=lambda item: item[0])
    direction = ladder.get("direction")
    strike_distance = (anchor.get("strike_usd") / spot - 1) * 100
    if direction == "above" and strike_distance > 0:
        tail_side = "upside_tail"
    elif direction == "below" and strike_distance < 0:
        tail_side = "downside_tail"
    else:
        tail_side = "inside_or_cross_spot_threshold"
    return {
        "bias": "not_directional_from_single_ladder",
        "tail_side": tail_side,
        "horizon_days": round(days, 1),
        "reference_probability_pct": round(probability, 2),
        "reference_direction": direction,
        "reference_strike_usd": anchor.get("strike_usd"),
        "event_slug": ladder.get("event_slug"),
        "quote_quality": ladder.get("quote_quality"),
        "reference_strike_distance_pct": round(strike_distance, 2),
        "terminal_ladder_summaries": ladder_summaries,
        "barrier_group_count": len(dossier.get("barrier_groups", [])),
    }


def market_metrics(asset_data, as_of):
    """Reduce complete source data to stable metrics used by the strategy analysis."""
    technical = asset_data.get("perp_technical_snapshot", {})
    carry = asset_data.get("perp_carry_snapshot", {})
    deribit = asset_data.get("deribit_market_snapshot", {})
    surface = deribit.get("surface_dossier", {})
    expiry = _closest([row for row in surface.get("expiry_fits", []) if row.get("fit_quality") in {"good", "usable", "usable_with_warning"} or row.get("fit_status") == "ok"], 30)
    future = _closest(deribit.get("dated_futures_curve", []), 30)
    spot = _number(deribit.get("spot_index_usd")) or _number(technical.get("perpetual_close"))
    risk_reversal = _number((expiry or {}).get("fitted_25_delta_risk_reversal_pct_points"))
    if risk_reversal is None:
        risk_reversal = _number((expiry or {}).get("approx_25_delta_risk_reversal_pct_points"))
    implied = _number((expiry or {}).get("fitted_atm_iv_pct"))
    realized = _number(technical.get("realized_vol_30d_pct"))
    prediction = _prediction_read(
        asset_data.get("polymarket_crypto_markets", {}).get("prediction_market_dossier", {}),
        spot,
        as_of,
    )
    context = asset_data.get("hyperliquid_context", {})
    volatility = context.get("realized_volatility_dossier", {})
    levels = context.get("price_level_dossier", {})
    realized_windows = {row["window_days"]: row for row in volatility.get("estimators", [])}
    expiry_days = _number((expiry or {}).get("days_to_expiry"))
    surface_read = {
        "model": surface.get("model"),
        "status": surface.get("status"),
        "coverage": surface.get("coverage", {}),
        "term_structure_event_flags": surface.get("term_structure_event_flags", []),
        "calendar_arbitrage_flags": surface.get("calendar_arbitrage_flags", []),
        "expiry_summaries": [{
            "maturity_at": row.get("expiry"),
            "days_to_expiry": row.get("days_to_expiry"),
            "fit_quality": row.get("fit_quality"),
            "fitted_atm_iv_pct": row.get("fitted_atm_iv_pct"),
            "fitted_25_delta_risk_reversal_pct_points": row.get("fitted_25_delta_risk_reversal_pct_points"),
            "weighted_rmse_iv_pct_points": row.get("weighted_rmse_iv_pct_points"),
        } for row in surface.get("expiry_fits", [])],
    }
    futures_curve = [{
        "maturity_at": row.get("expiry"),
        "days_to_expiry": row.get("days_to_expiry"),
        "basis_annualized_simple_pct": row.get("basis_annualized_simple_pct"),
        "open_interest": row.get("open_interest"),
    } for row in deribit.get("dated_futures_curve", [])]
    return {
        "spot_price": spot,
        "return_7d_pct": _number(technical.get("return_7d_pct")),
        "return_30d_pct": _number(technical.get("return_30d_pct")),
        "sma_20": _number(technical.get("sma_20")),
        "sma_50": _number(technical.get("sma_50")),
        "sma_200": _number(technical.get("sma_200")),
        "rsi_14d": _number(technical.get("rsi_14")),
        "funding_annualized_pct": _number(carry.get("current_funding_annualized_simple_pct")),
        "funding_30d_average_annualized_pct": _number(carry.get("average_funding_annualized_simple_30d_pct")),
        "futures_basis_annualized_pct": _number((future or {}).get("basis_annualized_simple_pct")),
        "futures_basis_tenor_days": _number((future or {}).get("days_to_expiry")),
        "atm_iv_pct": implied,
        "atm_iv_tenor_days": expiry_days,
        "implied_one_sigma_move_pct": implied * math.sqrt(expiry_days / 365) if implied and expiry_days else None,
        "realized_vol_30d_pct": realized,
        "realized_volatility_by_horizon": realized_windows,
        "realized_volatility_percentile": _number(volatility.get("current_30d_yang_zhang_percentile")),
        "iv_to_realized_ratio": implied / realized if implied and realized else None,
        "put_call_skew_pct_points": -risk_reversal if risk_reversal is not None else None,
        "surface_fit_quality": (expiry or {}).get("fit_quality"),
        "surface_fit_rmse_iv_pct_points": _number((expiry or {}).get("weighted_rmse_iv_pct_points")),
        "option_surface_read": surface_read,
        "futures_curve_read": futures_curve,
        "price_levels": levels,
        "prediction_market_read": prediction,
    }


def classify_regime(metrics, source_reads):
    """Classify one predefined regime from transparent, fixed market features."""
    price = metrics.get("spot_price")
    score = 0
    for moving_average in (metrics.get("sma_20"), metrics.get("sma_50")):
        if price and moving_average:
            score += 1 if price > moving_average else -1
    for change in (metrics.get("return_7d_pct"), metrics.get("return_30d_pct")):
        if change is not None:
            score += 1 if change > 0 else -1

    rsi = metrics.get("rsi_14d")
    skew = metrics.get("put_call_skew_pct_points")
    near_event = source_reads.get("near_event", False)
    event_bump = source_reads.get("surface_event_flag_count", 0) > 0
    vol_ratio = metrics.get("iv_to_realized_ratio")

    if near_event and (event_bump or (vol_ratio is not None and vol_ratio >= 1.15)):
        regime = "event_volatility"
    elif score >= 3 and rsi is not None and rsi >= 67:
        regime = "late_uptrend_mixed"
    elif score >= 3:
        regime = "strong_uptrend"
    elif score <= -3:
        regime = "downtrend"
    elif score < 0 and ((skew or 0) >= 4 or (rsi is not None and rsi >= 50)):
        regime = "distribution_risk"
    elif score > 0 and price and metrics.get("sma_50") and price < metrics["sma_50"]:
        regime = "recovery_reversal"
    else:
        regime = "range_balanced"

    observed = sum(value is not None for value in (
        price, metrics.get("sma_20"), metrics.get("sma_50"), metrics.get("rsi_14d"),
        metrics.get("funding_annualized_pct"), metrics.get("atm_iv_pct"),
        metrics.get("realized_vol_30d_pct"), metrics.get("futures_basis_annualized_pct"),
    ))
    data_quality = observed / 8
    directional_agreement = min(abs(score) / 4, 1)
    if metrics.get("surface_fit_quality") == "usable_with_warning":
        data_quality *= .85
    if source_reads.get("surface_calendar_arbitrage_flag_count", 0):
        data_quality *= .9
    prediction_quality = metrics.get("prediction_market_read", {}).get("quote_quality")
    if prediction_quality == "weak":
        data_quality *= .9
    if regime == "event_volatility":
        event_agreement = sum((near_event, event_bump, vol_ratio is not None and vol_ratio >= 1.15)) / 3
        confidence = .35 + .25 * data_quality + .25 * event_agreement
    elif regime == "range_balanced":
        range_agreement = 1 - directional_agreement
        confidence = .35 + .25 * data_quality + .25 * range_agreement
    else:
        confidence = .35 + .25 * data_quality + .25 * directional_agreement
    confidence = _clamp(confidence, .35, .85)
    summaries = {
        "strong_uptrend": "Trend and medium-term returns are aligned upward without a dominant late-cycle warning.",
        "late_uptrend_mixed": "Trend remains positive, but stretched momentum or protection demand weakens the immediate setup.",
        "range_balanced": "Directional evidence is balanced and current price remains broadly range-bound.",
        "event_volatility": "A near catalyst and the volatility surface make event risk the dominant feature.",
        "distribution_risk": "Trend evidence is weakening while downside protection or momentum signals remain defensive.",
        "downtrend": "Trend and recent returns are aligned downward.",
        "recovery_reversal": "Short-term improvement is emerging before the medium-term trend has fully recovered.",
    }
    return {"type": regime, "confidence": round(confidence, 2), "summary": summaries[regime], "directional_signal": score}


def _score_strategy(strategy, regime, metrics, source_reads):
    strategy_id = strategy["strategy_id"]
    directional = regime["directional_signal"]
    vol_ratio = metrics.get("iv_to_realized_ratio")
    funding = metrics.get("funding_annualized_pct")
    near_event = source_reads.get("near_event", False)
    surface_available = metrics.get("atm_iv_pct") is not None

    score = 55 if regime["type"] in strategy["eligible_regimes"] else 28
    if strategy_id in {"long", "call_spread", "covered_call"}:
        score += directional * 5
    elif strategy_id in {"short", "put_spread", "protective_put"}:
        score -= directional * 5
    elif strategy_id in {"long_straddle", "long_strangle"}:
        score += 18 if near_event and (vol_ratio is None or vol_ratio < 1.2) else -10
    elif strategy_id in {"short_straddle", "short_strangle"}:
        score += 18 if not near_event and vol_ratio is not None and vol_ratio >= 1.15 else -15
    elif strategy_id == "breakout_capture":
        breakout_state = metrics.get("price_levels", {}).get("breakout_state")
        confirmed = breakout_state in {"upside_breakout_confirming", "downside_breakout_confirming"}
        score += abs(directional) * 4 + (8 if near_event else 0) + (12 if confirmed else -4)
    elif strategy_id == "range_grid":
        defined_range = metrics.get("price_levels", {}).get("status") == "ok" and metrics.get("price_levels", {}).get("breakout_state") == "inside_range"
        score += 18 if regime["type"] == "range_balanced" and not near_event and defined_range else -12
    elif strategy_id == "wait":
        specific_reason = near_event or not surface_available or abs(funding or 0) >= 25
        score += 20 if specific_reason else -18

    if strategy_id in {"call_spread", "put_spread", "protective_put"} and surface_available:
        score += 6
    if strategy_id in {"long", "short", "range_grid"} and funding is not None and abs(funding) <= 20:
        score += 4
    return int(round(_clamp(score)))


def rank_strategies(regime, metrics, source_reads):
    """Rank every strategy using one setup-fit score."""
    ranked = []
    for strategy in STRATEGIES:
        score = _score_strategy(strategy, regime, metrics, source_reads)
        ranked.append({
            "strategy_id": strategy["strategy_id"],
            "score": score,
            "eligible_for_regime": regime["type"] in strategy["eligible_regimes"],
            "horizon_days": strategy["horizon_days"],
            "risk_profile": strategy["risk_profile"],
            "recommended_parameter_range": strategy["parameter_range"],
        })
    return sorted(ranked, key=lambda row: (-row["score"], row["strategy_id"]))


def build_strategy_inputs(asset_data, as_of):
    """Return fitted decision inputs while leaving complete observations on disk."""
    surface = asset_data.get("deribit_market_snapshot", {}).get("surface_dossier", {})
    macro = asset_data.get("polymarket_macro_events", {})
    now = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    future_macro = []
    for event in macro.get("events", []):
        try:
            days = (datetime.fromisoformat(str(event.get("rule_window_at")).replace("Z", "+00:00")) - now).total_seconds() / 86400
        except (TypeError, ValueError):
            continue
        if 0 <= days <= 14:
            future_macro.append({"event_title": event.get("event_title"), "days": round(days, 1), "macro_topic": event.get("macro_topic")})
    source_reads = {
        "surface_status": surface.get("status", "unavailable"),
        "surface_expiries_fitted": surface.get("coverage", {}).get("fitted_expiries", 0),
        "surface_event_flag_count": len(surface.get("term_structure_event_flags", [])),
        "surface_calendar_arbitrage_flag_count": len(surface.get("calendar_arbitrage_flags", [])),
        "price_level_status": asset_data.get("hyperliquid_context", {}).get("price_level_dossier", {}).get("status", "unavailable"),
        "realized_volatility_status": asset_data.get("hyperliquid_context", {}).get("realized_volatility_dossier", {}).get("status", "unavailable"),
        "prediction_terminal_ladders_fitted": asset_data.get("polymarket_crypto_markets", {}).get("prediction_market_dossier", {}).get("coverage", {}).get("terminal_ladders_fitted", 0),
        "prediction_barrier_contracts": asset_data.get("polymarket_crypto_markets", {}).get("prediction_market_dossier", {}).get("coverage", {}).get("barrier_contracts", 0),
        "near_macro_events": future_macro,
        "near_event": bool(future_macro),
        "source_status": asset_data.get("source_status", {}),
    }
    metrics = market_metrics(asset_data, as_of)
    regime = classify_regime(metrics, source_reads)
    return {
        "market_metrics": metrics,
        "market_regime": regime,
        "source_reads": source_reads,
        "ranked_strategies": rank_strategies(regime, metrics, source_reads),
        "score_definition": "Heuristic setup fit from 0 to 100; it is not a win rate or expected return.",
    }
