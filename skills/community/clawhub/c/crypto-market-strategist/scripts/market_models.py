"""Deterministic, non-trading models for derivatives research dossiers."""
from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime, timezone


def _number(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _normal_cdf(value: float) -> float:
    return 0.5 * (1 + math.erf(value / math.sqrt(2)))


def black76_greeks(forward: float, strike: float, years: float, iv_pct: float, option_type: str, rate: float = 0, index_price: float | None = None) -> dict | None:
    """Return forward Black-76 sensitivities with explicit inverse-value conversion."""
    if min(forward, strike, years, iv_pct) <= 0 or option_type not in {"call", "put"}:
        return None
    vol, root = iv_pct / 100, math.sqrt(years)
    d1 = (math.log(forward / strike) + vol * vol * years / 2) / (vol * root)
    d2, discount = d1 - vol * root, math.exp(-rate * years)
    pdf = math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
    sign = 1 if option_type == "call" else -1
    delta = discount * (sign * _normal_cdf(sign * d1))
    price = discount * (sign * (forward * _normal_cdf(sign * d1) - strike * _normal_cdf(sign * d2)))
    result = {
        "model": "Black-76 forward-price greeks",
        "forward_price": forward,
        "interest_rate": rate,
        "option_value_usd_per_unit": price,
        "forward_delta_usd_per_usd": delta,
        "forward_gamma_per_usd": discount * pdf / (forward * vol * root),
        "vega_usd_per_vol_point": discount * forward * pdf * root / 100,
        "theta_usd_per_day": -discount * forward * pdf * vol / (2 * root) / 365,
        "rho_usd": -years * price,
    }
    if index_price and index_price > 0:
        result["inverse_value_base_currency"] = price / index_price
        result["inverse_delta_base_per_index_usd"] = delta / index_price - price / (index_price * index_price)
        result["inverse_conversion_assumption"] = "Forward and index move one-for-one; account-level net transaction delta remains venue and position specific."
    return result


def _fit_raw_svi(points: list[tuple[float, float, float]]) -> dict | None:
    """Calibrate raw SVI with deterministic multi-start search and local refinement."""
    if len(points) < 6 or len({round(k, 5) for k, _, _ in points}) < 6:
        return None
    def evaluate(rho: float, m: float, sigma: float):
        if not -.999 < rho < .999 or sigma <= .002:
            return None
        basis = [rho * (k - m) + math.sqrt((k - m) ** 2 + sigma * sigma) for k, _, _ in points]
        sw = sum(weight for _, _, weight in points)
        sx = sum(weight * x for x, (_, _, weight) in zip(basis, points))
        sy = sum(weight * y for _, y, weight in points)
        sxx = sum(weight * x * x for x, (_, _, weight) in zip(basis, points))
        sxy = sum(weight * x * y for x, (_, y, weight) in zip(basis, points))
        denominator = sw * sxx - sx * sx
        if denominator <= 1e-14:
            return None
        b = (sw * sxy - sx * sy) / denominator
        a = (sy - b * sx) / sw
        minimum_variance = a + b * sigma * math.sqrt(1 - rho * rho)
        if b <= 0 or minimum_variance <= 0:
            return None
        fitted = [a + b * x for x in basis]
        error = sum(weight * (actual - estimate) ** 2 for estimate, (_, actual, weight) in zip(fitted, points)) / sw
        return {"a": a, "b": b, "rho": rho, "m": m, "sigma": sigma, "weighted_rmse_total_variance": math.sqrt(error)}

    best = None
    for rho in (-.9, -.7, -.5, -.3, -.1, .1, .3, .5, .7, .9):
        for m in (-.4, -.25, -.1, 0, .1, .25, .4):
            for sigma in (.02, .05, .1, .2, .35, .55):
                candidate = evaluate(rho, m, sigma)
                if candidate and (best is None or candidate["weighted_rmse_total_variance"] < best["weighted_rmse_total_variance"]):
                    best = candidate
    if best:
        steps = {"rho": .1, "m": .08, "sigma": .08}
        for _ in range(10):
            improved = False
            for parameter in ("rho", "m", "sigma"):
                for direction in (-1, 1):
                    values = {name: best[name] for name in ("rho", "m", "sigma")}
                    values[parameter] += direction * steps[parameter]
                    candidate = evaluate(values["rho"], values["m"], values["sigma"])
                    if candidate and candidate["weighted_rmse_total_variance"] + 1e-12 < best["weighted_rmse_total_variance"]:
                        best, improved = candidate, True
            if not improved:
                steps = {name: value / 2 for name, value in steps.items()}
    return best


def _liquidity_weight(row: dict) -> float:
    oi, volume = _number(row.get("open_interest")) or 0, _number(row.get("volume")) or 0
    two_sided = row.get("bid_price") is not None and row.get("ask_price") is not None
    spread = None
    if two_sided:
        bid, ask = _number(row.get("bid_price")), _number(row.get("ask_price"))
        midpoint = (bid + ask) / 2 if bid is not None and ask is not None else None
        spread = (ask - bid) / midpoint if midpoint and ask >= bid else None
    quote_quality = 1 / (1 + 5 * spread) if spread is not None else .35
    return quote_quality * (1 + math.log1p(max(0, oi) + max(0, volume)))


def _svi_variance(parameters: dict, k: float) -> float:
    x = k - parameters["m"]
    return parameters["a"] + parameters["b"] * (parameters["rho"] * x + math.sqrt(x * x + parameters["sigma"] ** 2))


def _svi_iv(parameters: dict, k: float, years: float) -> float | None:
    variance = _svi_variance(parameters, k)
    return math.sqrt(variance / years) * 100 if variance > 0 and years > 0 else None


def _butterfly_arbitrage_check(parameters: dict) -> dict:
    minimum_g = float("inf")
    violating = 0
    for step in range(161):
        k = -2 + step * .025
        x = k - parameters["m"]
        root = math.sqrt(x * x + parameters["sigma"] ** 2)
        w = _svi_variance(parameters, k)
        first = parameters["b"] * (parameters["rho"] + x / root)
        second = parameters["b"] * parameters["sigma"] ** 2 / root ** 3
        g = (1 - k * first / (2 * w)) ** 2 - first * first * (1 / w + .25) / 4 + second / 2
        minimum_g = min(minimum_g, g)
        violating += g < -1e-8
    return {"passed": violating == 0, "minimum_density_condition": round(minimum_g, 8), "violating_grid_points": violating}


def fit_option_surface(snapshot: dict) -> dict:
    """Fit quote-aware raw SVI smiles and validate static-arbitrage conditions."""
    spot = _number(snapshot.get("spot_index_usd"))
    as_of = datetime.fromisoformat(snapshot["as_of"].replace("Z", "+00:00"))
    rows_by_expiry = snapshot.get("expiry_slices", {})
    fitted, warnings = [], []
    for expiry_key, rows in sorted(rows_by_expiry.items(), key=lambda item: int(item[0])):
        expiry = int(expiry_key)
        years = max((expiry / 1000 - as_of.timestamp()) / (365 * 86400), 0)
        candidates, discarded = [], 0
        for row in rows:
            strike, iv = _number(row.get("strike")), _number(row.get("mark_iv"))
            forward = _number(row.get("underlying_price"))
            if not forward or not strike or not iv or not 5 <= iv <= 500 or years <= 0:
                discarded += 1
                continue
            k = math.log(strike / forward)
            if abs(k) > 1.5:
                discarded += 1
                continue
            candidates.append((k, (iv / 100) ** 2 * years, _liquidity_weight(row), row))

        # Prefer OTM options, which normally carry the cleaner crypto smile quote.
        by_strike = defaultdict(list)
        for candidate in candidates:
            by_strike[round(_number(candidate[3]["strike"]), 8)].append(candidate)
        usable = []
        for strike_rows in by_strike.values():
            preferred = [item for item in strike_rows if (item[0] < 0 and item[3].get("option_type") == "put") or (item[0] >= 0 and item[3].get("option_type") == "call")]
            usable.append(max(preferred or strike_rows, key=lambda item: item[2]))

        svi = _fit_raw_svi([(k, variance, weight) for k, variance, weight, _ in usable])
        forward = _number(usable[0][3].get("underlying_price")) if usable else None
        rate = math.log(forward / spot) / years if forward and spot and years else 0
        errors = []
        if svi:
            for k, _, weight, row in usable:
                fitted_iv = _svi_iv(svi, k, years)
                errors.append((fitted_iv - _number(row["mark_iv"]), weight))
        weighted_rmse_iv = math.sqrt(sum(weight * error * error for error, weight in errors) / sum(weight for _, weight in errors)) if errors else None
        max_error_iv = max((abs(error) for error, _ in errors), default=None)
        butterfly = _butterfly_arbitrage_check(svi) if svi else None
        if not svi:
            status, quality = "insufficient_quality_or_strike_coverage", "rejected"
        elif not butterfly["passed"] or weighted_rmse_iv > 5:
            status, quality = "fit_warning", "usable_with_warning"
        elif weighted_rmse_iv <= 2:
            status, quality = "ok", "good"
        else:
            status, quality = "ok", "usable"

        atm_iv = _svi_iv(svi, 0, years) if svi else None
        if svi:
            x = -svi["m"]
            root = math.sqrt(x * x + svi["sigma"] ** 2)
            variance_slope = svi["b"] * (svi["rho"] + x / root)
            variance_curvature = svi["b"] * svi["sigma"] ** 2 / root ** 3
            delta_points = {}
            for option_type, target in (("call", .25), ("put", -.25)):
                best = None
                for step in range(801):
                    k = -1 + step / 400
                    iv = _svi_iv(svi, k, years)
                    greeks = black76_greeks(forward, forward * math.exp(k), years, iv, option_type, rate, spot)
                    distance = abs(greeks["forward_delta_usd_per_usd"] - target)
                    if best is None or distance < best[0]:
                        best = (distance, k, iv)
                delta_points[option_type] = best
            rr = delta_points["call"][2] - delta_points["put"][2]
        else:
            variance_slope = variance_curvature = rr = None
        fitted.append({
            "expiry_timestamp": expiry,
            "expiry": datetime.fromtimestamp(expiry / 1000, timezone.utc).isoformat(),
            "days_to_expiry": round(years * 365, 2),
            "fit_status": status,
            "fit_quality": quality,
            "fit_method": "quote-quality-weighted OTM raw-SVI fit in Black-76 forward log-moneyness",
            "svi_parameters": svi,
            "forward_price_for_fit": forward,
            "index_price_for_rate": spot,
            "implied_interest_rate_annualized": round(rate, 8) if forward and spot else None,
            "fitted_atm_iv_pct": round(atm_iv, 3) if atm_iv is not None else None,
            "weighted_rmse_iv_pct_points": round(weighted_rmse_iv, 3) if weighted_rmse_iv is not None else None,
            "maximum_absolute_error_iv_pct_points": round(max_error_iv, 3) if max_error_iv is not None else None,
            "butterfly_arbitrage_check": butterfly,
            "total_variance_slope_atm": round(variance_slope, 8) if variance_slope is not None else None,
            "total_variance_curvature_atm": round(variance_curvature, 8) if variance_curvature is not None else None,
            "fitted_25_delta_risk_reversal_pct_points": round(rr, 3) if rr is not None else None,
            "contract_count": len(rows),
            "candidate_contract_count": len(candidates),
            "used_unique_strikes": len(usable),
            "discarded_contract_count": discarded,
        })
        if not svi:
            warnings.append(f"{expiry}: insufficient quote quality or strike coverage for SVI")

    usable_fits = [row for row in fitted if row["svi_parameters"]]
    jumps, calendar_flags = [], []
    for left, right in zip(usable_fits, usable_fits[1:]):
        change = right["fitted_atm_iv_pct"] - left["fitted_atm_iv_pct"]
        if abs(change) >= 4:
            jumps.append({"from_expiry": left["expiry"], "to_expiry": right["expiry"], "atm_iv_change_pct_points": round(change, 3), "flag": "event_or_liquidity_bump_requires_review"})
        violations = 0
        minimum_change = float("inf")
        for step in range(81):
            k = -.8 + step * .02
            change_in_variance = _svi_variance(right["svi_parameters"], k) - _svi_variance(left["svi_parameters"], k)
            minimum_change = min(minimum_change, change_in_variance)
            violations += change_in_variance < -1e-8
        if violations:
            calendar_flags.append({"from_expiry": left["expiry"], "to_expiry": right["expiry"], "violating_grid_points": violations, "minimum_total_variance_change": round(minimum_change, 8)})
    return {
        "model": "quote-aware raw-SVI per expiry with Black-76 forward moneyness",
        "status": "ok" if usable_fits else "unavailable",
        "spot_index_usd": spot,
        "expiry_fits": fitted,
        "term_structure_event_flags": jumps,
        "calendar_arbitrage_flags": calendar_flags,
        "coverage": {
            "listed_expiries": len(rows_by_expiry),
            "fitted_expiries": len(usable_fits),
            "good_expiries": sum(row["fit_quality"] == "good" for row in fitted),
            "warning_expiries": sum(row["fit_quality"] == "usable_with_warning" for row in fitted),
            "raw_contracts": sum(len(rows) for rows in rows_by_expiry.values()),
        },
        "limitations": [
            "Static-arbitrage conditions are tested and reported; flagged smiles are not silently repaired.",
            "Inverse conversions describe one-contract model sensitivity, not portfolio or account liquidation risk.",
            *warnings,
        ],
    }


def _pava(values: list[float], weights: list[float], increasing: bool) -> list[float]:
    signed = values if increasing else [-value for value in values]
    blocks = [[value * weight, weight, index, index] for index, (value, weight) in enumerate(zip(signed, weights))]
    index = 0
    while index < len(blocks) - 1:
        if blocks[index][0] / blocks[index][1] <= blocks[index + 1][0] / blocks[index + 1][1]:
            index += 1
            continue
        left, right = blocks[index], blocks[index + 1]
        blocks[index:index + 2] = [[left[0] + right[0], left[1] + right[1], left[2], right[3]]]
        index = max(0, index - 1)
    result = [0.0] * len(values)
    for total, weight, start, end in blocks:
        for index in range(start, end + 1):
            result[index] = total / weight
    return result if increasing else [-value for value in result]


def fit_prediction_market(markets: dict) -> dict:
    """Normalize comparable terminal ladders; preserve barriers as path-risk data."""
    terminal = defaultdict(list)
    for row in markets.get("terminal_markets", []):
        ctx = row.get("current_price_context", {})
        strike, direction, probability = _number(ctx.get("parsed_strike_usd")), ctx.get("parsed_condition_direction"), _number(row.get("midpoint_probability_pct"))
        if strike and probability is not None and direction in {"above", "below"}:
            terminal[row.get("event_slug")].append(row)
    ladders = []
    for slug, rows in terminal.items():
        directions = {row["current_price_context"]["parsed_condition_direction"] for row in rows}
        rules = {row.get("rules") for row in rows}
        if len(directions) != 1 or len(rules) != 1:
            ladders.append({"event_slug": slug, "fit_status": "not_comparable", "reason": "mixed condition direction or non-identical rules", "contract_count": len(rows)})
            continue
        direction = directions.pop()
        rows = sorted(rows, key=lambda row: row["current_price_context"]["parsed_strike_usd"])
        observed = [row["midpoint_probability_pct"] / 100 for row in rows]
        weights = []
        for row in rows:
            liquidity = (_number(row.get("book_depth_notional")) or 0) + (_number(row.get("reported_liquidity")) or 0)
            spread = _number(row.get("spread_pct_points"))
            quote_quality = 1 / (1 + (spread or 10) / 5)
            weights.append(quote_quality * (1 + math.log1p(liquidity)))
        fitted = _pava(observed, weights, increasing=direction == "below")
        residuals = [abs(left - right) for left, right in zip(observed, fitted)]
        anchors = [{"strike_usd": row["current_price_context"]["parsed_strike_usd"], "observed_probability_pct": round(observed[index] * 100, 3), "fitted_probability_pct": round(fitted[index] * 100, 3), "spread_pct_points": row.get("spread_pct_points"), "book_depth_notional": row.get("book_depth_notional"), "contract_slug": row.get("slug")} for index, row in enumerate(rows)]
        reference = _number(markets.get("current_underlying_reference", {}).get("price_usd"))
        interpolated = None
        if reference and anchors[0]["strike_usd"] <= reference <= anchors[-1]["strike_usd"]:
            for left, right in zip(anchors, anchors[1:]):
                if left["strike_usd"] <= reference <= right["strike_usd"]:
                    fraction = (reference - left["strike_usd"]) / max(right["strike_usd"] - left["strike_usd"], 1e-12)
                    interpolated = left["fitted_probability_pct"] + fraction * (right["fitted_probability_pct"] - left["fitted_probability_pct"])
                    break
        average_spread = sum((_number(row.get("spread_pct_points")) or 100) for row in rows) / len(rows)
        ladders.append({"event_slug": slug, "event_title": rows[0].get("event_title"), "rule_window_at": rows[0].get("rule_window_at"), "fit_status": "isotonic_terminal_probability_curve", "direction": direction, "contract_count": len(rows), "quote_quality": "good" if average_spread <= 3 else "usable" if average_spread <= 8 else "weak", "average_spread_pct_points": round(average_spread, 3), "max_monotonicity_adjustment_pct_points": round(max(residuals, default=0) * 100, 3), "mean_adjustment_pct_points": round(sum(residuals) / max(1, len(residuals)) * 100, 3), "reference_price_usd": reference, "interpolated_probability_at_reference_pct": round(interpolated, 3) if interpolated is not None else None, "anchors": anchors})
    barrier_groups = defaultdict(list)
    for row in markets.get("barrier_markets", []):
        barrier_groups[row.get("event_slug")].append(row)
    barriers = [{"event_slug": slug, "event_title": rows[0].get("event_title"), "rule_window_at": rows[0].get("rule_window_at"), "contract_count": len(rows), "status": "path_risk_only_not_fitted_as_terminal_distribution"} for slug, rows in barrier_groups.items()]
    return {"model": "rule-aware, quote-quality-weighted isotonic terminal probability curves", "terminal_ladders": ladders, "barrier_groups": barriers, "coverage": {"terminal_contracts": len(markets.get("terminal_markets", [])), "terminal_ladders_fitted": sum(row.get("fit_status") == "isotonic_terminal_probability_curve" for row in ladders), "barrier_contracts": len(markets.get("barrier_markets", []))}, "limitations": ["Only terminal contracts with identical rules and one condition direction are normalized together.", "Interpolation is piecewise linear inside quoted strike bounds and is not a full risk-neutral density.", "Barrier contracts are deliberately not combined with terminal ladders."]}
