"""Legacy Python port of @functionspace/core belief construction math (v0.0.1).

NOTE: main.py does not import this module. The current mech-v0-4 skill path uses
server-side position recipes (default: ``position_type='density'`` with
``num_buckets`` values). This file preserves the older raw-vector convention for
reference only, where vectors have length ``num_buckets + 2``.

Engine conventions (npm 0.0.1 / live dev engine, 2026-06-12):
- A belief vector has length ``num_buckets + 2`` (grid point k at
  u = k/(num_buckets+1) over the normalized outcome space).
- Vectors are normalized to MEAN 1 (sum == length), not sum 1. The llms.txt
  description (sum-1, length K+1) is stale — trust this, it matches the
  engine's validator.
"""

import math

EPS_FLOOR = 0.02  # inverted-point floor, mirrors JS


def validate_belief_vector(vector, num_buckets):
    expected = num_buckets + 2
    if len(vector) != expected:
        raise ValueError(
            f"Belief vector length {len(vector)} does not match expected "
            f"numBuckets+2 = {expected}"
        )
    if any(not math.isfinite(v) for v in vector):
        raise ValueError("Belief vector contains non-finite values")
    if any(v < 0 for v in vector):
        raise ValueError("Belief vector contains negative values")
    total = sum(vector)
    if abs(total / expected - 1) >= 1e-6:
        raise ValueError(f"Belief vector does not sum to {expected} (sum = {total})")


def _normalize(raw):
    total = sum(raw)
    if total <= 0:
        return [1.0] * len(raw)
    target = len(raw)
    return [v * target / total for v in raw]


def _point_kernel(region, num_buckets, lower_bound, upper_bound):
    span = upper_bound - lower_bound
    u_center = (region["center"] - lower_bound) / span
    u_spread = region["spread"] / span
    skew = region.get("skew") or 0
    inverted = region.get("inverted", False)
    raw = []
    for k in range(num_buckets + 2):
        u = k / (num_buckets + 1)
        effective_spread = u_spread
        if skew:
            intensity = abs(skew)
            wider = 1 + 2 * intensity
            narrow = 1 - 0.7 * intensity
            if u < u_center:
                effective_spread = u_spread * (wider if skew < 0 else narrow)
            else:
                effective_spread = u_spread * (wider if skew > 0 else narrow)
        if effective_spread == 0:
            diff = math.nan if u == u_center else math.inf
        else:
            diff = (u - u_center) / effective_spread
        value = math.exp(-0.5 * diff * diff) if math.isfinite(diff) else (
            math.nan if math.isnan(diff) else 0.0
        )
        if inverted:
            value = max(1 - value, EPS_FLOOR)
        raw.append(value)
    return raw


def _range_kernel(region, num_buckets, lower_bound, upper_bound):
    span = upper_bound - lower_bound
    u_low = (region["low"] - lower_bound) / span
    u_high = (region["high"] - lower_bound) / span
    sharpness = region.get("sharpness") or 0
    eps = 1e-3 - sharpness * 9e-4
    taper_width = 2 / num_buckets * (1 - sharpness)
    raw = []
    for k in range(num_buckets + 2):
        u = k / (num_buckets + 1)
        if u_low <= u <= u_high:
            raw.append(1.0)
        elif taper_width > 0 and u < u_low and u >= u_low - taper_width:
            t = (u_low - u) / taper_width
            raw.append(0.5 * (1 + math.cos(math.pi * t)))
        elif taper_width > 0 and u > u_high and u <= u_high + taper_width:
            t = (u - u_high) / taper_width
            raw.append(0.5 * (1 + math.cos(math.pi * t)))
        else:
            raw.append(eps)
    return raw


def _spline_kernel(region, num_buckets, lower_bound, upper_bound):
    control_x = region["controlX"]
    control_y = region["controlY"]
    n = len(control_x)
    if n <= 1:
        val = max(0.0, control_y[0]) if n == 1 else 0.0
        return [val] * (num_buckets + 2)
    span = upper_bound - lower_bound
    x_min, x_max = control_x[0], control_x[n - 1]
    norm_x_min = (x_min - lower_bound) / span
    norm_x_max = (x_max - lower_bound) / span
    big_n = n - 1
    h = 1 / big_n
    raw = []
    for i in range(num_buckets + 2):
        u = i / (num_buckets + 1)
        if u <= norm_x_min:
            raw.append(max(0.0, control_y[0] * 0.5))
            continue
        if u >= norm_x_max:
            raw.append(max(0.0, control_y[big_n] * 0.5))
            continue
        x = (u - norm_x_min) / (norm_x_max - norm_x_min)
        k = min(int(x / h), big_n - 1)
        tau = x - k * h
        c_prev = control_y[k - 1] if k > 0 else 0.0
        c_curr = control_y[k]
        c_next = control_y[k + 1] if k + 1 < len(control_y) else 0.0
        value = (
            c_prev * (h - tau) * (h - tau) / (2 * h * h)
            + c_curr * (0.5 + tau / h - tau * tau / (h * h))
            + c_next * (tau * tau) / (2 * h * h)
        )
        raw.append(max(0.0, value))
    return raw


_KERNELS = {"point": _point_kernel, "range": _range_kernel, "spline": _spline_kernel}


def generate_belief(regions, num_buckets, lower_bound, upper_bound):
    """Universal constructor. Regions are additive, then mean-1 normalized."""
    combined = [0.0] * (num_buckets + 2)
    for region in regions:
        weight = region.get("weight", 1)
        raw = _KERNELS[region["type"]](region, num_buckets, lower_bound, upper_bound)
        for k in range(num_buckets + 2):
            combined[k] += raw[k] * weight
    return _normalize(combined)


def generate_gaussian(center, spread, num_buckets, lower_bound, upper_bound):
    return generate_belief(
        [{"type": "point", "center": center, "spread": spread}],
        num_buckets, lower_bound, upper_bound,
    )


def generate_range(low, high, num_buckets, lower_bound, upper_bound, sharpness=1):
    # NB: JS bundle defaults sharpness to 1 (hard cliff); llms.txt claims 0.5 — stale.
    return generate_belief(
        [{"type": "range", "low": low, "high": high, "sharpness": sharpness}],
        num_buckets, lower_bound, upper_bound,
    )


def generate_dip(center, spread, num_buckets, lower_bound, upper_bound):
    return generate_belief(
        [{"type": "point", "center": center, "spread": spread * 1.5, "inverted": True}],
        num_buckets, lower_bound, upper_bound,
    )


def generate_left_skew(center, spread, num_buckets, lower_bound, upper_bound, skew_amount=1):
    return generate_belief(
        [{"type": "point", "center": center, "spread": spread, "skew": -skew_amount}],
        num_buckets, lower_bound, upper_bound,
    )


def generate_right_skew(center, spread, num_buckets, lower_bound, upper_bound, skew_amount=1):
    return generate_belief(
        [{"type": "point", "center": center, "spread": spread, "skew": skew_amount}],
        num_buckets, lower_bound, upper_bound,
    )


def generate_custom_shape(control_values, num_buckets, lower_bound, upper_bound):
    n = len(control_values)
    if n == 1:
        control_x = [(lower_bound + upper_bound) / 2]
    else:
        control_x = [
            lower_bound + i / (n - 1) * (upper_bound - lower_bound) for i in range(n)
        ]
    return generate_belief(
        [{"type": "spline", "controlX": control_x, "controlY": control_values}],
        num_buckets, lower_bound, upper_bound,
    )
