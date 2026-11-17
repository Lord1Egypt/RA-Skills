#!/usr/bin/env python3
"""Appliance Energy Audit — find out what each appliance really costs you.

Commands:
  library                 list built-in appliance presets (typical watts/duty)
  estimate                quick cost estimate for one appliance
  audit                   full home audit: ranked table + vampire loads + totals
  calibrate               reconcile model vs your actual bill kWh
  replace                 what-if: old appliance vs efficient replacement, payback
  example                 run a sample audit

Stdlib only. All money values in whatever currency your rate uses ($ assumed).
"""

import argparse
import json
import sys

HOURS_PER_MONTH = 730.0  # 24 * 365 / 12 — the standard energy-audit convention

# ---------------------------------------------------------------------------
# Built-in appliance library.
#   watts      = nameplate/typic draw when active
#   duty       = fraction of "on" time the device actually draws (compressors cycle)
#   standby_w  = draw when idle/off but plugged in
#   hours_day  = default active hours per day if user gives none
# ---------------------------------------------------------------------------
LIBRARY = {
    "fridge":          {"watts": 150,   "duty": 0.35, "standby_w": 0,   "hours_day": 24, "category": "cooling"},
    "freezer":         {"watts": 200,   "duty": 0.40, "standby_w": 0,   "hours_day": 24, "category": "cooling"},
    "chest-freezer":   {"watts": 180,   "duty": 0.35, "standby_w": 0,   "hours_day": 24, "category": "cooling"},
    "electric-oven":   {"watts": 2400,  "duty": 0.60, "standby_w": 3,   "hours_day": 0.5, "category": "cooking"},
    "electric-stove":  {"watts": 2000,  "duty": 0.50, "standby_w": 0,   "hours_day": 0.5, "category": "cooking"},
    "microwave":       {"watts": 1100,  "duty": 1.0,  "standby_w": 3,   "hours_day": 0.2, "category": "cooking"},
    "dishwasher":      {"watts": 1300,  "duty": 1.0,  "standby_w": 2,   "hours_day": 0.5, "category": "kitchen"},
    "electric-kettle": {"watts": 2000,  "duty": 1.0,  "standby_w": 0,   "hours_day": 0.1, "category": "kitchen"},
    "coffee-maker":    {"watts": 1000,  "duty": 1.0,  "standby_w": 1,   "hours_day": 0.3, "category": "kitchen"},
    "toaster":         {"watts": 1100,  "duty": 1.0,  "standby_w": 0,   "hours_day": 0.1, "category": "kitchen"},
    "clothes-washer":  {"watts": 500,   "duty": 1.0,  "standby_w": 1,   "hours_day": 0.3, "category": "laundry"},
    "electric-dryer":  {"watts": 3000,  "duty": 1.0,  "standby_w": 1,   "hours_day": 0.4, "category": "laundry"},
    "heat-pump-dryer": {"watts": 900,   "duty": 1.0,  "standby_w": 1,   "hours_day": 0.5, "category": "laundry"},
    "water-heater":    {"watts": 4500,  "duty": 0.20, "standby_w": 0,   "hours_day": 24, "category": "water"},
    "heat-pump-water": {"watts": 500,   "duty": 0.35, "standby_w": 0,   "hours_day": 24, "category": "water"},
    "led-bulb":        {"watts": 9,     "duty": 1.0,  "standby_w": 0,   "hours_day": 5,  "category": "lighting"},
    "cfl-bulb":        {"watts": 14,    "duty": 1.0,  "standby_w": 0,   "hours_day": 5,  "category": "lighting"},
    "incandescent":    {"watts": 60,    "duty": 1.0,  "standby_w": 0,   "hours_day": 5,  "category": "lighting"},
    "halogen-floor":   {"watts": 300,   "duty": 1.0,  "standby_w": 0,   "hours_day": 4,  "category": "lighting"},
    "tv-led-55":       {"watts": 100,   "duty": 1.0,  "standby_w": 1,   "hours_day": 5,  "category": "entertainment"},
    "tv-oled-55":      {"watts": 150,   "duty": 1.0,  "standby_w": 1,   "hours_day": 5,  "category": "entertainment"},
    "game-console":    {"watts": 160,   "duty": 1.0,  "standby_w": 8,   "hours_day": 2,  "category": "entertainment"},
    "desktop-pc":      {"watts": 200,   "duty": 1.0,  "standby_w": 3,   "hours_day": 6,  "category": "computing"},
    "gaming-pc":       {"watts": 450,   "duty": 1.0,  "standby_w": 4,   "hours_day": 4,  "category": "computing"},
    "laptop":          {"watts": 60,    "duty": 1.0,  "standby_w": 1,   "hours_day": 8,  "category": "computing"},
    "monitor-27":      {"watts": 40,    "duty": 1.0,  "standby_w": 1,   "hours_day": 6,  "category": "computing"},
    "wifi-router":     {"watts": 10,    "duty": 1.0,  "standby_w": 6,   "hours_day": 24, "category": "network"},
    "modem":           {"watts": 9,     "duty": 1.0,  "standby_w": 5,   "hours_day": 24, "category": "network"},
    "mesh-node":       {"watts": 6,     "duty": 1.0,  "standby_w": 4,   "hours_day": 24, "category": "network"},
    "smart-speaker":   {"watts": 3,     "duty": 1.0,  "standby_w": 2,   "hours_day": 24, "category": "network"},
    "ac-window-12k":   {"watts": 1200,  "duty": 0.60, "standby_w": 2,   "hours_day": 8,  "category": "heating-cooling"},
    "ac-central-3ton": {"watts": 3500,  "duty": 0.50, "standby_w": 5,   "hours_day": 8,  "category": "heating-cooling"},
    "mini-split-12k":  {"watts": 900,   "duty": 0.55, "standby_w": 3,   "hours_day": 8,  "category": "heating-cooling"},
    "space-heater":    {"watts": 1500,  "duty": 0.70, "standby_w": 0,   "hours_day": 4,  "category": "heating-cooling"},
    "ceiling-fan":     {"watts": 60,    "duty": 1.0,  "standby_w": 0,   "hours_day": 8,  "category": "heating-cooling"},
    "box-fan":         {"watts": 55,    "duty": 1.0,  "standby_w": 0,   "hours_day": 8,  "category": "heating-cooling"},
    "dehumidifier":    {"watts": 300,   "duty": 0.50, "standby_w": 1,   "hours_day": 12, "category": "heating-cooling"},
    "air-purifier":    {"watts": 45,    "duty": 1.0,  "standby_w": 1,   "hours_day": 12, "category": "heating-cooling"},
    "treadmill":       {"watts": 900,   "duty": 1.0,  "standby_w": 6,   "hours_day": 0.5, "category": "misc"},
    "fish-tank":       {"watts": 120,   "duty": 1.0,  "standby_w": 0,   "hours_day": 24, "category": "misc"},
    "garage-opener":   {"watts": 400,   "duty": 1.0,  "standby_w": 4,   "hours_day": 0.1, "category": "misc"},
    "ev-charger-7kw":  {"watts": 7000,  "duty": 1.0,  "standby_w": 2,   "hours_day": 2,  "category": "vehicle"},
    "pool-pump":       {"watts": 1100,  "duty": 1.0,  "standby_w": 0,   "hours_day": 6,  "category": "misc"},
    "hot-tub":         {"watts": 1500,  "duty": 0.30, "standby_w": 0,   "hours_day": 24, "category": "misc"},
}

# Tiered rate tables: list of (up_to_kwh_monthly_or_None, price_per_kwh), last tier must be None.
DEFAULT_RATE = 0.17


def resolve_appliance(spec):
    """Fill an appliance spec dict with library defaults. Returns normalized dict."""
    out = {
        "name": spec.get("name", "unnamed"),
        "watts": None, "duty": 1.0, "standby_w": 0.0,
        "hours_day": None, "qty": int(spec.get("qty", 1) or 1),
        "category": spec.get("category", "custom"),
        "preset": spec.get("preset"),
    }
    preset = spec.get("preset")
    if preset is not None:
        if preset not in LIBRARY:
            raise ValueError("unknown preset '%s' (run: library)" % preset)
        lib = LIBRARY[preset]
        out.update({
            "watts": spec.get("watts", lib["watts"]),
            "duty": float(spec.get("duty", lib["duty"])),
            "standby_w": float(spec.get("standby_w", lib["standby_w"])),
            "hours_day": spec.get("hours_day", lib["hours_day"]),
            "category": spec.get("category", lib["category"]),
        })
    else:
        if spec.get("watts") is None:
            raise ValueError("appliance '%s' needs watts or preset" % out["name"])
        out["watts"] = float(spec["watts"])
        out["duty"] = float(spec.get("duty", 1.0))
        out["standby_w"] = float(spec.get("standby_w", 0.0))
        out["hours_day"] = spec.get("hours_day", 4.0)
    if out["hours_day"] is None:
        out["hours_day"] = 4.0
    out["hours_day"] = float(out["hours_day"])
    out["qty"] = max(1, out["qty"])
    if out["watts"] <= 0:
        raise ValueError("appliance '%s': watts must be > 0" % out["name"])
    if not (0.0 < out["duty"] <= 1.0):
        raise ValueError("appliance '%s': duty must be in (0, 1]" % out["name"])
    if not (0 <= out["hours_day"] <= 24):
        raise ValueError("appliance '%s': hours_day must be 0..24" % out["name"])
    if out["standby_w"] < 0:
        raise ValueError("appliance '%s': standby_w must be >= 0" % out["name"])
    return out


def monthly_kwh(app):
    """kWh in an average month for one appliance (qty included)."""
    active_hours = app["hours_day"] * 30.0 * app["duty"]
    idle_hours = max(0.0, (24.0 - app["hours_day"]) * 30.0)
    kwh = (app["watts"] * active_hours + app["standby_w"] * idle_hours) / 1000.0
    return kwh * app["qty"]


def standby_kwh(app):
    """kWh/month drawn purely in standby/idle hours (qty included)."""
    idle_hours = max(0.0, (24.0 - app["hours_day"]) * 30.0)
    return app["standby_w"] * idle_hours / 1000.0 * app["qty"]


def tiered_cost(total_kwh, tiers):
    """Cost under a tiered rate structure. tiers = [(limit_kwh_or_None, rate), ...]."""
    cost, remaining = 0.0, total_kwh
    prev_limit = 0.0
    for limit, rate in tiers:
        if limit is None:
            span = remaining
        else:
            span = min(remaining, max(0.0, limit - prev_limit))
        cost += span * rate
        remaining -= span
        if limit is not None:
            prev_limit = limit
        if remaining <= 0:
            break
    return cost


def flat_or_tiered_rate(total_kwh, rate, tiers):
    if tiers:
        return tiered_cost(total_kwh, tiers)
    return total_kwh * rate


def build_audit(specs, rate=DEFAULT_RATE, tiers=None):
    """Full audit: per-appliance rows, ranked by monthly cost."""
    rows = []
    for spec in specs:
        app = resolve_appliance(spec)
        kwh = monthly_kwh(app)
        # marginal cost of THIS appliance at its cumulative position is complex;
        # use average-rate-at-total for ranking instead (see references doc).
        rows.append({
            "name": app["name"], "preset": app.get("preset"),
            "category": app["category"], "qty": app["qty"],
            "watts": app["watts"], "duty": app["duty"],
            "hours_day": app["hours_day"], "standby_w": app["standby_w"],
            "kwh_month": round(kwh, 2),
            "vampire_kwh_month": round(standby_kwh(app), 2),
        })
    total_kwh = sum(r["kwh_month"] for r in rows)
    avg_rate = flat_or_tiered_rate(total_kwh, rate, tiers) / total_kwh if total_kwh else rate
    for r in rows:
        r["cost_month"] = round(r["kwh_month"] * avg_rate, 2)
        r["cost_year"] = round(r["cost_month"] * 12, 2)
        r["share_pct"] = round(100.0 * r["kwh_month"] / total_kwh, 1) if total_kwh else 0.0
    rows.sort(key=lambda r: r["cost_month"], reverse=True)
    total_cost = flat_or_tiered_rate(total_kwh, rate, tiers)
    vampire_kwh = sum(r["vampire_kwh_month"] for r in rows)
    return {
        "rows": rows,
        "total_kwh_month": round(total_kwh, 1),
        "total_cost_month": round(total_cost, 2),
        "total_cost_year": round(total_cost * 12, 2),
        "effective_rate": round(avg_rate, 4),
        "vampire_kwh_month": round(vampire_kwh, 1),
        "vampire_cost_month": round(vampire_kwh * avg_rate, 2),
    }


def calibrate(audit, actual_kwh):
    """Compare model total vs the bill; return gap analysis."""
    model = audit["total_kwh_month"]
    gap = actual_kwh - model
    top_share = audit["rows"][0]["share_pct"] if audit["rows"] else 0.0
    if abs(gap) / actual_kwh < 0.05:
        verdict = "matched"
        hint = "Model is within 5% of your bill — trust the per-appliance breakdown."
    elif gap > 0:
        verdict = "undercounted"
        hint = ("Your bill shows %.0f kWh more than the model. Look for: heating/cooling "
                "run-time far above the hours you entered, an old fridge/freezer working "
                "harder than its rating, or devices you forgot to list." % gap)
    else:
        verdict = "overcounted"
        hint = ("Model exceeds your bill by %.0f kWh. Your appliances likely run fewer "
                "hours than assumed — lower hours_day for the biggest rows and re-run." % -gap)
    return {
        "model_kwh": round(model, 1), "bill_kwh": round(actual_kwh, 1),
        "gap_kwh": round(gap, 1), "gap_pct": round(100.0 * gap / actual_kwh, 1),
        "verdict": verdict, "hint": hint,
        "biggest_modeled_share_pct": top_share,
    }


def replace_analysis(old_spec, new_spec, price, rate=DEFAULT_RATE, tiers=None):
    """What-if: replace old with new. Payback in months given purchase price."""
    old = resolve_appliance(old_spec)
    new = resolve_appliance(new_spec)
    old_kwh, new_kwh = monthly_kwh(old), monthly_kwh(new)
    total_kwh = old_kwh  # marginal-rate approximation uses old appliance scale
    marginal = flat_or_tiered_rate(total_kwh, rate, tiers) / total_kwh if total_kwh else rate
    saved_kwh = old_kwh - new_kwh
    saved_month = saved_kwh * marginal
    return {
        "old": {"name": old["name"], "kwh_month": round(old_kwh, 2)},
        "new": {"name": new["name"], "kwh_month": round(new_kwh, 2)},
        "kwh_saved_month": round(saved_kwh, 2),
        "kwh_saved_year": round(saved_kwh * 12, 1),
        "money_saved_month": round(saved_month, 2),
        "money_saved_year": round(saved_month * 12, 2),
        "purchase_price": price,
        "payback_months": round(price / saved_month, 1) if saved_month > 0 else None,
        "worth_it": bool(saved_month > 0 and (price / saved_month) <= 120),
    }


# ----------------------------- output helpers ------------------------------

def fmt_table(audit):
    W = (74, 9, 9, 9, 8, 7)
    lines = []
    hdr = "%-*s %*s %*s %*s %*s %*s" % (W[0], "appliance", W[1], "kWh/mo",
                                        W[2], "$/mo", W[3], "$/yr", W[4], "share", W[5], "qty")
    lines.append(hdr)
    lines.append("-" * len(hdr))
    for r in audit["rows"]:
        lines.append("%-*s %*.1f %*.2f %*.2f %*.1f%% %*d" % (
            W[0], r["name"][:W[0]], W[1], r["kwh_month"], W[2], r["cost_month"],
            W[3], r["cost_year"], W[4], r["share_pct"], W[5], r["qty"]))
    lines.append("-" * len(hdr))
    lines.append("%-*s %*.1f %*.2f %*.2f" % (W[0], "TOTAL", W[1], audit["total_kwh_month"],
                                             W[2], audit["total_cost_month"], W[3], audit["total_cost_year"]))
    lines.append("")
    lines.append("Vampire (standby) draw: %.1f kWh/mo ≈ $%.2f/mo — appliances listed "
                 "with standby_w sitting idle." % (audit["vampire_kwh_month"],
                                                   audit["vampire_cost_month"]))
    lines.append("Effective rate used: $%.4f/kWh" % audit["effective_rate"])
    return "\n".join(lines)


def parse_appliance_arg(text):
    """Parse 'name[,preset|watts][,hours_day][,qty][,standby_w]' CLI shorthand."""
    parts = [p.strip() for p in text.split(",") if p.strip() != ""]
    if not parts:
        raise ValueError("empty appliance spec")
    spec = {"name": parts[0]}
    rest = parts[1:]
    if rest and not _is_number(rest[0]):
        spec["preset"] = rest[0]
        rest = rest[1:]
        # with a preset the remaining numbers are hours_day, qty, standby_w
        nums = [_fnum(p) for p in rest]
        if len(nums) > 0:
            spec["hours_day"] = nums[0]
        if len(nums) > 1:
            spec["qty"] = int(nums[1])
        if len(nums) > 2:
            spec["standby_w"] = nums[2]
    else:
        # no preset: first number is watts, then hours_day, qty, standby_w
        nums = [_fnum(p) for p in rest]
        if len(nums) > 0:
            spec["watts"] = nums[0]
        if len(nums) > 1:
            spec["hours_day"] = nums[1]
        if len(nums) > 2:
            spec["qty"] = int(nums[2])
        if len(nums) > 3:
            spec["standby_w"] = nums[3]
    return spec


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _fnum(s):
    v = float(s)
    if v != v or v in (float("inf"), float("-inf")):
        raise ValueError("bad number: %s" % s)
    return v


def _parse_tiers(text):
    """'0.12:500,0.15:1000,0.20:' → [(500,0.12),(1000,0.15),(None,0.20)]"""
    tiers = []
    for chunk in text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        rate_s, sep, limit_s = chunk.partition(":")
        if not sep:
            raise ValueError("each tier needs 'rate:limit' (limit empty = unlimited)")
        rate = _fnum(rate_s)
        limit_s = limit_s.strip()
        limit = None if limit_s in ("", "*") else _fnum(limit_s)
        tiers.append((limit, rate))
    if not tiers or tiers[-1][0] is not None:
        raise ValueError("tiers must end with an unlimited tier, e.g. '0.12:500,0.20:'")
    prev = 0.0
    prev_rate = 0.0
    for limit, rate in tiers:
        if rate <= 0:
            raise ValueError("tier rate must be > 0")
        if rate < prev_rate:
            raise ValueError("tier rates must not decrease")
        prev_rate = rate
        if limit is not None:
            if limit <= prev:
                raise ValueError("tier limits must increase")
            prev = limit
    return tiers


def load_specs(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        if isinstance(data, dict) and isinstance(data.get("appliances"), list):
            data = data["appliances"]
        else:
            raise ValueError("spec file must be a JSON list of appliances")
    return data


SAMPLE_AUDIT = [
    {"name": "Kitchen fridge (2015)", "preset": "fridge"},
    {"name": "Chest freezer", "preset": "chest-freezer", "hours_day": 24},
    {"name": "Electric dryer", "preset": "electric-dryer", "hours_day": 0.5},
    {"name": "LED bulbs — living room", "preset": "led-bulb", "qty": 8, "hours_day": 4},
    {"name": "Halogen floor lamp", "preset": "halogen-floor"},
    {"name": "OLED TV", "preset": "tv-oled-55", "hours_day": 4},
    {"name": "Game console", "preset": "game-console", "hours_day": 2},
    {"name": "Gaming PC", "preset": "gaming-pc", "hours_day": 3},
    {"name": "WiFi router", "preset": "wifi-router"},
    {"name": "Window AC (bedroom)", "preset": "ac-window-12k", "hours_day": 6},
    {"name": "Electric kettle", "preset": "electric-kettle"},
    {"name": "Microwave", "preset": "microwave"},
    {"name": "Hot water tank", "preset": "water-heater"},
]

# --------------------------------- commands --------------------------------

def cmd_library(args):
    cats = {}
    for name, lib in sorted(LIBRARY.items()):
        cats.setdefault(lib["category"], []).append((name, lib))
    print("%-18s %8s %6s %9s %9s" % ("preset", "watts", "duty", "h/day", "standby_w"))
    print("-" * 56)
    for cat in sorted(cats):
        print("[%s]" % cat)
        for name, lib in cats[cat]:
            print("%-18s %8.0f %6.2f %9.1f %9.1f" % (
                name, lib["watts"], lib["duty"], lib["hours_day"], lib["standby_w"]))
    return 0


def cmd_estimate(args):
    spec = parse_appliance_arg(args.appliance)
    if args.hours is not None:
        spec["hours_day"] = args.hours
    app = resolve_appliance(spec)
    kwh = monthly_kwh(app)
    cost = kwh * args.rate
    print("%s: %.0f W active (duty %.2f), %.1f h/day, qty %d" % (
        app["name"], app["watts"], app["duty"], app["hours_day"], app["qty"]))
    print("  %.1f kWh/month ≈ $%.2f/month ($%.2f/year) at $%.3f/kWh" % (
        kwh, cost, cost * 12, args.rate))
    if app["standby_w"] > 0:
        v = standby_kwh(app)
        print("  standby draw: %.1f kWh/month ≈ $%.2f/month just sitting there" % (v, v * args.rate))
    return 0


def cmd_audit(args):
    specs = load_specs(args.file) if args.file else [parse_appliance_arg(a) for a in args.appliance]
    if not specs:
        print("error: no appliances given (--appliance or --file)", file=sys.stderr)
        return 2
    tiers = _parse_tiers(args.tiers) if args.tiers else None
    audit = build_audit(specs, rate=args.rate, tiers=tiers)
    if args.json:
        print(json.dumps(audit, indent=2))
    else:
        print(fmt_table(audit))
        if audit["vampire_cost_month"] >= 1.0:
            print("→ Smart-power-strip candidates (highest standby first):")
            for r in sorted(audit["rows"], key=lambda r: r["vampire_kwh_month"], reverse=True)[:3]:
                if r["vampire_kwh_month"] > 0:
                    print("   %s — %.1f kWh/mo idle" % (r["name"], r["vampire_kwh_month"]))
    if args.calibrate_to is not None:
        cal = calibrate(audit, args.calibrate_to)
        print("\nCALIBRATION vs bill:")
        print("  model %.0f kWh vs bill %.0f kWh → gap %+.0f kWh (%+.1f%%) [%s]" % (
            cal["model_kwh"], cal["bill_kwh"], cal["gap_kwh"], cal["gap_pct"], cal["verdict"]))
        print("  %s" % cal["hint"])
    return 0


def cmd_calibrate(args):
    specs = load_specs(args.file) if args.file else [parse_appliance_arg(a) for a in args.appliance]
    if not specs:
        print("error: no appliances given", file=sys.stderr)
        return 2
    audit = build_audit(specs, rate=args.rate)
    cal = calibrate(audit, args.bill_kwh)
    if args.json:
        print(json.dumps(cal, indent=2))
    else:
        print("model: %.0f kWh   bill: %.0f kWh" % (cal["model_kwh"], cal["bill_kwh"]))
        print("gap:   %+.0f kWh (%+.1f%%)  → %s" % (cal["gap_kwh"], cal["gap_pct"], cal["verdict"]))
        print(cal["hint"])
    return 0


def cmd_replace(args):
    old = parse_appliance_arg(args.old)
    new = parse_appliance_arg(args.new)
    res = replace_analysis(old, new, args.price, rate=args.rate)
    if args.json:
        print(json.dumps(res, indent=2))
        return 0
    verdict = ("PAYS BACK in %.1f months" % res["payback_months"]) if res["payback_months"] else \
              ("new appliance uses MORE energy" if res["kwh_saved_month"] < 0 else "no savings")
    print("old: %s — %.1f kWh/mo" % (res["old"]["name"], res["old"]["kwh_month"]))
    print("new: %s — %.1f kWh/mo" % (res["new"]["name"], res["new"]["kwh_month"]))
    print("saves %.1f kWh/mo = %.1f kWh/yr ≈ $%.2f/mo ($%.2f/yr)" % (
        res["kwh_saved_month"], res["kwh_saved_year"],
        res["money_saved_month"], res["money_saved_year"]))
    print("price $%.2f → %s" % (res["purchase_price"], verdict))
    return 0


def cmd_example(args):
    audit = build_audit(SAMPLE_AUDIT, rate=DEFAULT_RATE)
    print("Sample home audit (rate $%.2f/kWh):\n" % DEFAULT_RATE)
    print(fmt_table(audit))
    cal = calibrate(audit, 620.0)
    print("\nCALIBRATION vs a $620 kWh bill: gap %+.0f kWh [%s] — %s" % (
        cal["gap_kwh"], cal["verdict"], cal["hint"]))
    rep = replace_analysis(
        {"name": "Halogen floor lamp", "preset": "halogen-floor"},
        {"name": "LED floor lamp", "watts": 22, "hours_day": 4},
        45.0, rate=DEFAULT_RATE)
    print("\nREPLACE example: halogen lamp → $45 LED lamp")
    print("  saves $%.2f/yr, payback %.1f months, worth_it=%s" % (
        rep["money_saved_year"], rep["payback_months"], rep["worth_it"]))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="energy_audit", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("library", help="list appliance presets").set_defaults(fn=cmd_library)

    sp = sub.add_parser("estimate", help="estimate one appliance's cost")
    sp.add_argument("appliance", help="'name[,preset|watts][,hours][,qty][,standby_w]'")
    sp.add_argument("--hours", type=float, default=None)
    sp.add_argument("--rate", type=float, default=DEFAULT_RATE)
    sp.set_defaults(fn=cmd_estimate)

    sp = sub.add_parser("audit", help="full home audit, ranked by cost")
    sp.add_argument("--appliance", "-a", action="append", default=[],
                    help="appliance spec, repeatable")
    sp.add_argument("--file", "-f", help="JSON file with a list of appliances")
    sp.add_argument("--rate", type=float, default=DEFAULT_RATE)
    sp.add_argument("--tiers", help="tiered rates '0.12:500,0.15:1000,0.20:'")
    sp.add_argument("--calibrate-to", type=float, default=None,
                    help="your actual bill kWh/month for gap analysis")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(fn=cmd_audit)

    sp = sub.add_parser("calibrate", help="model vs actual bill")
    sp.add_argument("--appliance", "-a", action="append", default=[])
    sp.add_argument("--file", "-f")
    sp.add_argument("--bill-kwh", type=float, required=True)
    sp.add_argument("--rate", type=float, default=DEFAULT_RATE)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(fn=cmd_calibrate)

    sp = sub.add_parser("replace", help="old vs new appliance, savings + payback")
    sp.add_argument("--old", required=True, help="'name[,preset|watts][,hours][,qty]'")
    sp.add_argument("--new", required=True)
    sp.add_argument("--price", type=float, required=True)
    sp.add_argument("--rate", type=float, default=DEFAULT_RATE)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(fn=cmd_replace)

    sub.add_parser("example", help="sample audit run").set_defaults(fn=cmd_example)

    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
