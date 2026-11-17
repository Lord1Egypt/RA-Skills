#!/usr/bin/env python3
"""Car Battery Cold-Start Doctor — SOC from resting voltage, cold derate,
age fade, predicted no-start temperature, verdict + failure-signature
triage and protocols. Pure stdlib.

Examples:
    python3 battery_doctor.py --resting-v 12.1 --temp-c -5 --age-years 5 --cca-rated 550
    python3 battery_doctor.py --age-years 6 --temp-c -12 --cca-rated 520 --no-meter
    python3 battery_doctor.py --resting-v 12.55 --temp-c 10 --age-years 3 --cca-rated 600 --design-low-c -25
"""
import argparse
import json
import math

ENGINE_CLASS = {
    # demand baseline = typical OEM CCA spec x0.8 (the -18C requirement with margin)
    "4cyl-gas": 320, "6cyl-gas": 440, "8cyl-gas": 520,
    "truck-v8": 600, "4cyl-diesel": 640, "6cyl-diesel": 800,
}

# resting V -> SOC fraction (12V lead-acid, ~25C)
SOC_TABLE = [
    (12.7, 1.00), (12.5, 0.85), (12.4, 0.75), (12.3, 0.65),
    (12.2, 0.50), (12.1, 0.40), (12.0, 0.25), (11.9, 0.10), (11.4, 0.0),
]


def soc_from_voltage(v):
    if v >= SOC_TABLE[0][0]:
        return 1.0
    if v <= SOC_TABLE[-1][0]:
        return 0.0
    for (hi, shi), (lo, slo) in zip(SOC_TABLE, SOC_TABLE[1:]):
        if lo <= v <= hi:
            t = (v - lo) / (hi - lo)
            return slo + t * (shi - slo)
    return 0.0


def cold_factor(t_c):
    """Deliverable-current fraction vs temperature, anchored so CCA
    rating (deliverable at -18C) = 100%. Above -18C you get MORE than
    rating; far below, less. Ticks all the right physical boxes:
    ~1.4x at 0C, ~2.0x at +27C, ~0.75x at -30C relative to rating."""
    r = 1.0 + 0.022 * (t_c + 18.0)          # linear core
    if t_c < -18.0:
        r -= 0.004 * (-18.0 - t_c) ** 1.5 / 3.0  # extra collapse below spec
    return max(0.3, r)


def demand_mult(t_c):
    """Cranking demand multiplier from cold oil viscosity (1.0 at 18C)."""
    return 1.0 + 0.55 * max(0.0, (18.0 - t_c) / 36.0)  # 1.55 at -18C


def age_factor(years, climate="average"):
    per_year = {"average": 0.06, "hot": 0.09, "gentle": 0.045}[climate]
    return max(0.0, 1.0 - per_year * years)


def fails_to_start(t_c, cca, age_f, baseline_cca):
    """Demand baseline is stated at -18C (CCA conditions); rescale to T."""
    demand_at_t = baseline_cca * demand_mult(t_c) / demand_mult(-18.0)
    supply = cca * age_f * cold_factor(t_c)
    return supply < demand_at_t, supply, demand_at_t


def no_start_temp(cca, age_f, baseline_cca):
    """Temperature below which the car fails to start (None = starts even at -45C)."""
    lo, hi = -45.0, 30.0  # invariant: lo = fails, hi = starts
    if not fails_to_start(lo, cca, age_f, baseline_cca)[0]:
        return None  # starts everywhere in range
    if fails_to_start(hi, cca, age_f, baseline_cca)[0]:
        return hi  # fails even warm -> marginal at any temperature
    for _ in range(50):
        mid = (lo + hi) / 2
        fail, _, _ = fails_to_start(mid, cca, age_f, baseline_cca)
        if fail:
            lo = mid
        else:
            hi = mid
    return round(hi, 1)  # below this line it fails


def main():
    ap = argparse.ArgumentParser(description="12V lead-acid cold-start doctor")
    ap.add_argument("--resting-v", type=float, default=None,
                    help="resting voltage (morning, key off, no surface charge)")
    ap.add_argument("--temp-c", type=float, default=-10, help="current/target temp C")
    ap.add_argument("--age-years", type=float, required=True,
                    help="battery age from case date code")
    ap.add_argument("--cca-rated", type=float, required=True, help="rated CCA on label")
    ap.add_argument("--engine", choices=list(ENGINE_CLASS), default="6cyl-gas",
                    help="engine class for demand baseline")
    ap.add_argument("--climate", choices=["average", "hot", "gentle"], default="average")
    ap.add_argument("--design-low-c", type=float, default=None,
                    help="your local design low temp (e.g. -25)")
    ap.add_argument("--cranking-v", type=float, default=None,
                    help="voltage WHILE cranking if you can catch it")
    ap.add_argument("--no-meter", action="store_true",
                    help="skip voltage analysis; age/temp only")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    baseline = ENGINE_CLASS[a.engine]
    a_f = age_factor(a.age_years, a.climate)
    cf = cold_factor(a.temp_c)
    dm = demand_mult(a.temp_c)
    soc = soc_from_voltage(a.resting_v) if (a.resting_v is not None and not a.no_meter) else None
    # discharged battery can't deliver rated current: scale delivery with SOC
    soc_penalty = (0.5 + 0.5 * soc) if soc is not None else 1.0
    supply = a.cca_rated * a_f * cf * soc_penalty
    _, s_now, demand = fails_to_start(a.temp_c, a.cca_rated * soc_penalty, a_f, baseline)
    supply = s_now
    starts_now = supply >= demand
    nst = no_start_temp(a.cca_rated * soc_penalty, a_f, baseline)

    dead_cell = bool(a.resting_v is not None and not a.no_meter and a.resting_v < 11.0)
    cranking_ok = None
    if a.cranking_v is not None:
        cranking_ok = a.cranking_v >= 10.5

    # verdict ladder
    verdict = "OK"
    reasons = []
    if dead_cell:
        verdict = "REPLACE NOW"; reasons.append("resting voltage < 11.0 V — dead/shorted cell signature")
    elif not starts_now:
        verdict = "REPLACE NOW"; reasons.append(
            f"effective CCA {supply:.0f} < demand {demand:.0f} at {a.temp_c:.0f}C right now")
    elif nst is not None and a.design_low_c is not None and nst >= a.design_low_c + 6:
        verdict = "REPLACE NOW"; reasons.append(
            f"predicted no-start line {nst:.0f}C is above your design low {a.design_low_c:.0f}C "
            "(real world is 5-8C worse than the model)")
    elif (soc is not None and soc < 0.5) or (nst is not None and a.design_low_c is not None
                                             and nst >= a.design_low_c - 2):
        verdict = "WATCH"; reasons.append("marginal for a cold winter — test under load before freeze")
    elif a.age_years >= 5:
        verdict = "WATCH"; reasons.append(f"{a.age_years:.0f} years old — end of typical service life")
    if soc is not None and soc < 0.75 and verdict == "OK":
        verdict = "WATCH"; reasons.append(f"SOC only {soc*100:.0f}% — charge before cold nights")

    triage = [
        ("One click, headlights BRIGHT", "starter solenoid/circuit or cable — NOT the battery"),
        ("Click-click-click, lights DIM", "battery discharged or high-resistance connection"),
        ("Cranks strong, won't fire", "fuel/ignition — battery is fine, don't buy one"),
        ("Cranks slow, slows, stops", "battery exhausted; check alternator 13.8-14.6V running"),
        ("Fine daily, dead after 3 days parked", "parasitic drain (norm <50mA) — not the battery"),
        ("Nothing at all, no lights", "terminals/ground cable or fully dead battery"),
    ]

    if a.json:
        out = {
            "soc": soc, "age_factor": round(a_f, 3), "cold_factor": round(cf, 3),
            "effective_cca_now": round(supply), "demand_cca_now": round(demand),
            "starts_now": starts_now, "no_start_temp_c": nst,
            "verdict": verdict, "reasons": reasons,
            "cranking_voltage_pass": cranking_ok,
        }
        print(json.dumps(out, indent=2))
        return

    W = 62
    print("=" * W)
    print("CAR BATTERY COLD-START DOCTOR (12V lead-acid model)")
    print("=" * W)
    if soc is not None:
        print(f"Resting voltage {a.resting_v:.2f} V  ->  SOC ~{soc*100:.0f}%")
        if dead_cell:
            print("  !! <11.0 V at rest = dead/shorted cell. Replace. Charging won't hold.")
    else:
        print("No resting voltage given — age/temperature coarse mode.")
    print(f"Age {a.age_years:.0f} yr ({a.climate} climate) -> capacity {a_f*100:.0f}%")
    if soc is not None:
        print(f"  delivery penalty for SOC {soc*100:.0f}%: x{soc_penalty:.2f}")
    print(f"At {a.temp_c:.0f} C: deliverable current {cf*100:.0f}% of CCA rating, demand x{dm:.2f} (vs 18C)")
    print(f"Effective CCA now: {supply:.0f}   Demand: {demand:.0f}  "
          f"({'STARTS' if starts_now else 'FAILS'})")
    if a.cranking_v is not None:
        print(f"Cranking voltage {a.cranking_v:.1f} V: "
              f"{'PASS (>=10.5)' if cranking_ok else 'FAIL (<10.5) — weak under load'}")
    if nst is None:
        print("Predicted no-start temp: none within -45..+30 C (healthy).")
    else:
        line = f"Predicted no-start line: {nst:.0f} C"
        if a.design_low_c is not None:
            margin = nst - a.design_low_c
            line += f"   (your design low {a.design_low_c:.0f} C, margin {margin:+.0f} C"
            line += " — real world 5-8C worse)"
        print(line)
    print()
    print(f"VERDICT: {verdict}")
    for r in reasons:
        print(f"  - {r}")
    print()
    print("FAILURE-SIGNATURE TRIAGE (before buying anything):")
    for obs, meaning in triage:
        print(f"  {obs:38s} -> {meaning}")
    print()
    print("PROTOCOLS")
    print("  Jump order: red->dead+, red->donor+, black->donor-,")
    print("             black->dead ENGINE BLOCK metal. Donor running. Reverse to remove.")
    print("  Cold start: loads off, key-on 3s x2 (fuel prime), crank 5s max,")
    print("             rest 30s, 3 attempts max. Then drive 30+ min, not idle.")
    print("=" * W)


if __name__ == "__main__":
    main()
