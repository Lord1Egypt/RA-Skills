#!/usr/bin/env python3
"""Diet Plateau Decoder — true stall vs water mask vs logging drift.

Reads a daily weight series, fits a linear trend, compares slope against the
expected loss rate from your deficit, estimates the water-retention budget
from context flags (sodium, new training, menstrual phase, alcohol, sleep,
refeed), and issues NOT A PLATEAU / TRUE PLATEAU / LOG BROKEN with an
action plan. 7-day rolling averages; noise bands from the data itself.

stdlib only. No network.
"""
import argparse
import json
import statistics
import sys

WATER_FLAGS = {
    "high-sodium": {"kg": 0.3, "days": 2, "why": "restaurant/processed day: +0.3-1.2 kg 1-3 days"},
    "new-training": {"kg": 1.0, "days": 10, "why": "muscle-repair edema: +0.5-2 kg for 1-2 weeks"},
    "luteal": {"kg": 1.0, "days": 7, "why": "menstrual luteal water: +0.5-2 kg, resolves with menses"},
    "refeed": {"kg": 0.8, "days": 3, "why": "glycogen refill binds water 3:1: +0.5-1.5 kg"},
    "alcohol": {"kg": 0.5, "days": 1, "why": "diuretic then rebound: +0.3-1 kg"},
    "poor-sleep": {"kg": 0.5, "days": 3, "why": "cortisol-driven retention: +0.3-1 kg"},
    "constipation": {"kg": 0.4, "days": 1, "why": "gut content: +0.2-0.8 kg"},
    "weekend-overshoot": {"kg": 0.0, "days": 0, "why": "not water — arithmetic: weekend surplus erases weekday deficit"},
}


def parse_series(s):
    try:
        vals = [float(x) for x in s.replace(" ", "").split(",") if x != ""]
    except ValueError:
        sys.exit("weights must be comma-separated numbers")
    if len(vals) < 10:
        sys.exit(f"need >=10 daily weights for a meaningful trend (got {len(vals)})")
    if any(abs(v) > 500 for v in vals):
        sys.exit("weights look wrong (unit mix? kg vs lb)")
    return vals


def linreg_slope(y):
    n = len(y)
    x = list(range(n))
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = sum((xi - mx) ** 2 for xi in x)
    return num / den if den else 0.0


def rolling_avg(y, w=7):
    out = []
    for i in range(len(y)):
        lo = max(0, i - w + 1)
        out.append(statistics.mean(y[lo:i + 1]))
    return out


def decode(weights, expected_loss_kg_wk, flags, unit="kg"):
    n = len(weights)
    kgb = 0.4536 if unit == "lb" else 1.0
    w_kg = [v * kgb for v in weights]

    slope_day = linreg_slope(w_kg)
    slope_wk = slope_day * 7
    expected = -expected_loss_kg_wk  # negative = losing

    # noise band from the residuals of the last 7 days vs their mean
    last7 = w_kg[-7:]
    noise = statistics.pstdev(last7) if len(last7) > 1 else 0.0

    # water budget from flags
    water_kg = sum(WATER_FLAGS[f]["kg"] for f in flags if f in WATER_FLAGS and WATER_FLAGS[f]["kg"] > 0)

    # signal-to-noise: is the trend distinguishable from flatness?
    trend_over_noise = abs(slope_wk * (n / 7)) / max(noise, 0.05)

    # plateau test on the SMOOTHED series' last 14 days
    ra = rolling_avg(w_kg)
    recent = ra[-14:] if n >= 14 else ra
    recent_slope_wk = linreg_slope(recent) * 7

    flat = abs(recent_slope_wk) < 0.08  # < 80 g/week = flat
    losing = recent_slope_wk < -0.08
    gaining = recent_slope_wk > 0.08

    if flags and "weekend-overshoot" in flags and flat:
        verdict = "LOG BROKEN"
        why = ("flat trend + known weekend overshoot: the deficit arithmetic is broken, "
               "not the metabolism. 14 days of honest 7-day logging before any change.")
    elif n < 14:
        verdict = "INCONCLUSIVE"
        why = f"only {n} days — water masks last 1-2 weeks; keep logging, rerun at day 14+"
    elif flat and water_kg > 0.4:
        verdict = "NOT A PLATEAU (masked)"
        why = (f"smoothed trend is flat by {abs(recent_slope_wk):.2f} kg/wk, but flags account for "
               f"~{water_kg:.1f} kg of water. Expected rate {expected:.2f} kg/wk is hidden under it. "
               "Change nothing for 7 days; judge the rolling average only.")
    elif flat and water_kg <= 0.4:
        verdict = "TRUE PLATEAU"
        why = (f"smoothed trend flat ({recent_slope_wk:+.2f} kg/wk) for {min(14, n)}+ days with no "
               "water flags to explain it. Audit log -> recompute TDEE -> NEAT -> then trim 100-200 kcal.")
    elif losing:
        verdict = "NOT A PLATEAU"
        why = (f"smoothed trend {recent_slope_wk:+.2f} kg/wk — fat is still leaving. Raw-day flatness "
               "is water noise (±%.1f kg band). Keep executing." % noise)
    else:  # gaining
        verdict = "GAINING — check the log"
        why = (f"smoothed trend {recent_slope_wk:+.2f} kg/wk upward. Either surplus creep (weekends?) "
               "or a big water flag; if flags present, wait 7 days before reacting.")

    weeks = [w_kg[i:i + 7] for i in range(0, n, 7)]
    week_means = [statistics.mean(x) for x in weeks if len(x) == 7]

    plan = {
        "NOT A PLATEAU": [
            "Change nothing for 7 days.",
            "Weigh daily, same conditions; judge only the 7-day rolling average.",
            "Expect the whoosh when flagged water clears.",
        ],
        "NOT A PLATEAU (masked)": [
            "Change nothing for 7 days — the mask resolves on its own schedule.",
            "Judge only the rolling average, never a single day.",
            "If sodium/training flagged: whoosh typically in 2-7 days.",
        ],
        "TRUE PLATEAU": [
            "1) Audit the food log 2 weeks — re-weigh portions; creep is 10-20%.",
            "2) Recompute TDEE at CURRENT weight (engine shrank with you).",
            "3) Add NEAT (steps) before cutting calories.",
            "4) Then trim 100-200 kcal OR take a 1-2 week maintenance diet break.",
            "5) Track waist/photos/gym lifts — recomposition hides fat loss.",
        ],
        "LOG BROKEN": [
            "14 days of honest logging including weekends.",
            "Daily weighing is fine — the trend, not the day, is the unit.",
            "Re-run decoder on clean data before touching calories.",
        ],
        "GAINING — check the log": [
            "Find the surplus (weekend arithmetic first).",
            "If water flags present, wait 7 days; re-run.",
        ],
        "INCONCLUSIVE": [
            "Keep daily weighing; re-run with >=14 days.",
        ],
    }.get(verdict, [])

    return {
        "days_logged": n,
        "unit": unit,
        "trend_kg_per_week": round(slope_wk, 3),
        "recent_smoothed_trend_kg_per_week": round(recent_slope_wk, 3),
        "expected_kg_per_week": round(expected, 3),
        "noise_band_kg": round(noise, 2),
        "trend_over_noise": round(trend_over_noise, 2),
        "water_budget_kg_from_flags": round(water_kg, 2),
        "flags": flags,
        "week_means_kg": [round(x, 2) for x in week_means],
        "verdict": verdict,
        "why": why,
        "action_plan": plan,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weights", required=True, help="comma-separated daily weights")
    ap.add_argument("--expected-loss", type=float, required=True,
                    help="expected loss rate per week in the weight unit (kg or lb)")
    ap.add_argument("--unit", default="kg", choices=["kg", "lb"])
    ap.add_argument("--flag", action="append", default=[],
                    choices=list(WATER_FLAGS), dest="flags")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    weights = parse_series(args.weights)
    exp_kg = args.expected_loss * (0.4536 if args.unit == "lb" else 1.0)

    r = decode(weights, exp_kg, args.flags, args.unit)
    # report expected rate back in user unit
    r["expected_per_week_user_unit"] = round(args.expected_loss, 2)
    if args.json:
        print(json.dumps(r, indent=2))
        return 0

    print(f"\n=== Plateau Decode ({r['days_logged']} days, {r['unit']}) ===")
    print(f"  full-series trend:     {r['trend_kg_per_week']:+.2f} kg/wk")
    print(f"  recent smoothed trend: {r['recent_smoothed_trend_kg_per_week']:+.2f} kg/wk (last 14d rolling avg)")
    print(f"  expected from deficit: {r['expected_kg_per_week']:+.2f} kg/wk")
    print(f"  daily noise band:      ±{r['noise_band_kg']:.2f} kg")
    print(f"  trend/noise ratio:     {r['trend_over_noise']:.1f}x (>2 = signal, not noise)")
    if r["flags"]:
        print(f"  flags:                 {', '.join(r['flags'])} -> water budget ~{r['water_budget_kg_from_flags']:.1f} kg")
        for f in r["flags"]:
            print(f"    - {f}: {WATER_FLAGS[f]['why']}")
    if r["week_means_kg"]:
        print("  weekly means (kg):     " + " -> ".join(f"{x:+.1f}" for x in r["week_means_kg"]))
    print(f"\n  VERDICT: {r['verdict']}")
    print(f"  {r['why']}")
    print("\n  Action plan:")
    for step in r["action_plan"]:
        print(f"   - {step}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
