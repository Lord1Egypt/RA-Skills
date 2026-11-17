#!/usr/bin/env python3
"""Baby Fever Triage — 2 AM decision support for febrile children 0-5 years.

INFORMATIONAL TOOL — NOT A DOCTOR. When output and parental instinct disagree,
the doctor / emergency services win. Never delay emergency care to consult software.
100% local: single fever.json in cwd (or --db).
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

DB = Path("fever.json")
DISCLAIMER = ("[!] Informational support, not medical advice. "
              "If your gut says emergency, it is right — act first.")

# ----------------------------------------------------------------------------
# Dosing rules (mg/kg/dose). Ranges reflect common pediatric guidance.
# ----------------------------------------------------------------------------
DOSE_RANGES = {
    "acetaminophen": {"min": 10, "max": 15, "interval_h": 4, "max_doses_day": 5,
                      "max_mgkg_day": 75, "min_age_months": 1,
                      "names": ["acetaminophen", "paracetamol", "tylenol", "panadol", "efferalgan", "калпол"]},
    "ibuprofen":     {"min": 5,  "max": 10, "interval_h": 6, "max_doses_day": 4,
                      "max_mgkg_day": 40, "min_age_months": 6,
                      "names": ["ibuprofen", "advil", "nurofen", "motrin", "ибупрофен", "нурофен"]},
}
COMMON_CONCS = {  # informational only — ALWAYS read the actual bottle
    "infant drops (US 160mg/5mL)": 32.0,
    "children's syrup (US 160mg/5mL)": 32.0,
    "EU drops 100mg/mL": 100.0,
    "EU syrup 120mg/5mL": 24.0,
    "EU/RU syrup 250mg/5mL": 50.0,
    "ibuprofen suspension 100mg/5mL": 20.0,
    "ibuprofen suspension 200mg/5mL": 40.0,
}

RED_FLAGS = [
    ("non-blanching-rash", "Rash that does NOT fade when pressed with a glass (meningitis sign)"),
    ("inconsolable", "Cannot be consoled by anything for >1 hour, continuous high-pitched cry"),
    ("unresponsive", "Difficult to wake, limp, floppy, or unresponsive"),
    ("grunting", "Grunting with each breath, or noisy strained breathing"),
    ("breathing-fast", "Fast breathing (infant >60/min, 1-4y >40/min) or ribs pulling in"),
    ("blue-lips", "Blue or gray lips, tongue, or face"),
    ("seizure", "Severe convulsion, or first-ever seizure (jerking, eyes rolling)"),
    ("bulging-fontanelle", "Bulging soft spot (fontanelle) in an infant, or unusual stillness"),
    ("neck-stiffness", "Neck stiffness with light hurting the eyes (older children)"),
    ("dehydrated", "No tears, dry mouth, no wet diaper/urine for 8+ hours, sunken eyes"),
    ("refusing-fluids", "Refuses all fluids for 8+ hours or repeated vomiting everything"),
    ("temperature-over-41", "Temperature 41°C / 105.8°F or higher"),
    ("fever-5-days", "Fever has lasted 5 days or more, regardless of how the child looks"),
    ("getting-worse", "Was recovering, now clearly getting worse again (could be secondary infection)"),
]

# Temperature correction: measured route -> estimated core
ROUTE_ADJ = {"rectal": 0.0, "forehead": 0.3, "temporal": 0.3, "axillary": 0.5, "oral": 0.3}


def load(db=None):
    p = Path(db) if db else DB
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {"events": []}
    return {"events": []}


def save(data, db=None):
    p = Path(db) if db else DB
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return p


def ev(data, kind, **fields):
    e = {"kind": kind, "at": dt.datetime.now().isoformat(timespec="minutes"), **fields}
    data.setdefault("events", []).append(e)
    return e


def to_c(temp, unit):
    return temp if unit == "c" else (temp - 32.0) * 5.0 / 9.0


def core_temp(temp, unit, route):
    return to_c(temp, unit) + ROUTE_ADJ.get((route or "").lower(), 0.0)


# ----------------------------------------------------------------------------
# 1) TRIAGE
# ----------------------------------------------------------------------------
def cmd_triage(a):
    c = core_temp(a.temp, a.unit, a.route)
    tier, reasons, rule = triage_core(a.age_months, c, a.responsive, a.drinking)
    print(f"Child: {a.age_months} months | measured {a.temp}°{a.unit.upper()} ({a.route}) "
          f"→ est. core {c:.1f}°C\n")
    bar = {"EMERGENCY-NOW": "!", "SAME-DAY": "*", "HOME-CARE": "-"}.get(tier, "-")
    print(f"[{bar}] VERDICT: {tier}")
    for r in reasons:
        print(f"      reason: {r}")
    print(f"      rule fired: {rule}")
    print()
    if tier == "EMERGENCY-NOW":
        print("→ Call emergency services / go to the ER NOW. Do not dose at home unless")
        print("  instructed by a dispatcher/doctor. Bring the fever log (fever.py handoff).")
    elif tier == "SAME-DAY":
        print("→ See a doctor TODAY (pediatrician or urgent care). Not a wait-until-morning fever.")
        print("  Run the red-flag checklist now: fever.py flags")
    else:
        print("→ Home care usually OK: fluids, rest, weight-based dosing if the child is")
        print("  miserable. Re-check every 2-3h and run flags if anything changes.")
        print("  Dose calculator: fever.py dose --weight-kg W --drug D --conc mg-per-ml:X")
    print(f"\n{DISCLAIMER}")
    return 0


def triage_core(age_months, c, responsive=None, drinking=None):
    """Pure triage logic — returns (tier, reasons, rule). Conservative by design."""
    reasons = []
    if c >= 41.0:
        return "EMERGENCY-NOW", [f"core temp {c:.1f}°C ≥ 41°C — evaluate immediately"], "temp>=41"
    if age_months < 3:
        if c >= 38.0:
            return "EMERGENCY-NOW", [
                f"age {age_months}m < 3 months with core ≥38.0°C (est. {c:.1f}°C)",
                "under 3 months, fever can signal serious bacterial infection with no other signs",
            ], "age<3m+38C"
        return "SAME-DAY", [
            f"age {age_months}m < 3 months — any illness deserves same-day evaluation",
        ], "age<3m-urgent-ish"
    if age_months < 6:
        if c >= 39.0:
            return "SAME-DAY", [
                f"3-6 months with core ≥39.0°C (est. {c:.1f}°C) — should be seen today",
            ], "3-6m+39C"
        reasons.append(f"3-6 months, {c:.1f}°C — see doctor if not clearly improving within 24h")
        return "HOME-CARE", reasons, "3-6m-home"
    # 6m-5y: behavior dominates
    if responsive is False:
        return "EMERGENCY-NOW", ["child is NOT responsive/interactive — that outranks any temperature"], "behavior"
    if responsive is None:
        reasons.append("responsiveness not specified — verify the child interacts normally (smiles, reaches, answers)")
    if drinking is False:
        return "SAME-DAY", ["not drinking fluids — dehydration risk escalates any fever"], "fluids"
    if c >= 39.0:
        reasons.append(f"{c:.1f}°C is high but in an interactive, drinking child >6m this is usually home care")
    else:
        reasons.append(f"{c:.1f}°C with normal behavior — comfort and observe")
    reasons.append("re-check temp & behavior every 2-3h; escalate on any red flag")
    return "HOME-CARE", reasons, "6m-5y-behavior"


# ----------------------------------------------------------------------------
# 2) RED FLAGS
# ----------------------------------------------------------------------------
def cmd_flags(a):
    present = [k for k, _ in RED_FLAGS if getattr(a, k.replace("-", "_"), None)]
    print("Red-flag checklist (any YES = EMERGENCY-NOW regardless of age/temperature):\n")
    for k, desc in RED_FLAGS:
        v = getattr(a, k.replace("-", "_"), None)
        mark = "YES" if v else ("no" if v is False else "? ")
        print(f"  [{mark:>3}] {k:22} {desc}")
    print()
    if present:
        print("VERDICT: EMERGENCY-NOW — red flags present: " + ", ".join(present))
        print("→ Seek emergency care now. Take the handoff summary (fever.py handoff).")
        rc = 2
    else:
        print("No red flags reported. Continue age-based triage (fever.py triage).")
        print("If any appear later, they override everything and mean EMERGENCY-NOW.")
        rc = 0
    print(f"\n{DISCLAIMER}")
    return rc


# ----------------------------------------------------------------------------
# 3) DOSE
# ----------------------------------------------------------------------------
def cmd_dose(a):
    drug = norm_drug(a.drug)
    if not drug:
        print("Unknown drug: %r. Known: acetaminophen/paracetamol/tylenol/panadol, ibuprofen/nurofen/advil" % a.drug)
        return 1
    d = DOSE_RANGES[drug]
    lo, hi = d["min"] * a.weight_kg, d["max"] * a.weight_kg

    print(f"Drug: {drug} | weight: {a.weight_kg} kg\n")
    if a.age_months is not None and a.age_months < d["min_age_months"]:
        if drug == "ibuprofen":
            print("[!] REFUSED: ibuprofen is not for infants under 6 months.")
            print("    Use acetaminophen (if ≥1 month) per doctor's guidance.")
            return 1
        print(f"[!] Under {d['min_age_months']} month(s): dose ONLY if a doctor directed it.")
        if not a.doctor_directed:
            print("    --doctor-directed not set → no dosing advice. Call your pediatrician.")
            return 1
        print("    Proceeding because --doctor-directed is set.\n")

    print(f"Single dose: {lo:.0f}-{hi:.0f} mg  ({d['min']}-{d['max']} mg/kg × {a.weight_kg} kg)")
    print(f"Interval: at least {d['interval_h']}h between doses | max {d['max_doses_day']} doses/24h")
    print(f"Daily ceiling: {d['max_mgkg_day'] * a.weight_kg:.0f} mg/day ({d['max_mgkg_day']} mg/kg/day)\n")

    if a.conc:
        mgml = parse_conc(a.conc)
        if mgml is None:
            print(f"Cannot parse concentration {a.conc!r}. Use: --conc mg-per-ml:100 or --conc 32")
            return 1
        print(f"Product concentration: {mgml} mg/mL")
        print(f"  → give {lo / mgml:.1f} to {hi / mgml:.1f} mL  (measure with the dosing syringe, not a kitchen spoon)")
        print(f"  → a {hi:.0f} mg convenient amount = {hi / mgml:.2f} mL")
    else:
        print("[!] No concentration given — REFUSING to state mL.")
        print("    mL depends on the product: 5 mL can mean anywhere from 120 mg to 500 mg.")
        print("    Read the bottle and pass e.g. --conc mg-per-ml:100 (EU drops) or --conc mg-per-ml:20 (ibuprofen 100mg/5mL)")
        print("    Common: " + "; ".join(f"{k}={v}" for k, v in COMMON_CONCS.items()))

    print(f"\n{DISCLAIMER}")
    return 0


def norm_drug(name):
    n = (name or "").strip().lower()
    for canon, spec in DOSE_RANGES.items():
        if n in spec["names"]:
            return canon
    return None


def parse_conc(s):
    s = s.strip().lower()
    if s.startswith("mg-per-ml:"):
        s = s.split(":", 1)[1]
    try:
        return float(s)
    except ValueError:
        return None


# ----------------------------------------------------------------------------
# 4) SCHEDULER (alternating acetaminophen/ibuprofen)
# ----------------------------------------------------------------------------
def cmd_schedule(a):
    w = a.weight_kg
    drugs = ["acetaminophen", "ibuprofen"] if a.drugs == "both" else [norm_drug(a.drugs) or a.drugs]
    start = dt.datetime.fromisoformat(a.start) if a.start else dt.datetime.now().replace(second=0, microsecond=0)
    end = start + dt.timedelta(hours=a.hours)

    # Per-drug plan: target doses at interval spacing, staggered by half-interval
    plan = []
    for i, drug in enumerate(drugs):
        d = DOSE_RANGES[drug]
        offset = dt.timedelta(hours=d["interval_h"] * i / max(1, len(drugs) - 1)) if len(drugs) > 1 else dt.timedelta()
        t = start + offset
        while t <= end:
            plan.append((t, drug, lo_hi(d, w)))
            t += dt.timedelta(hours=d["interval_h"])

    plan.sort()
    print(f"Alternating schedule for {w} kg, {a.hours}h from {start.strftime('%Y-%m-%d %H:%M')}")
    print(f"Stagger: acetaminophen every 4h, ibuprofen every 6h (each drug keeps its own interval)\n")
    prev = {}
    ok = True
    for t, drug, (lo, hi) in plan:
        bad = ""
        if drug in prev and (t - prev[drug]).total_seconds() < d_interval(drug) * 3600 - 1:
            bad = "  <-- INTERVAL VIOLATION"
            ok = False
        prev[drug] = t
        print(f"  {t.strftime('%H:%M')}  {drug:14} {lo:.0f}-{hi:.0f} mg{bad}")
    # daily max check (per calendar day)
    days = sorted({t.date() for t, _, _ in plan})
    ok_all = True
    for day in days:
        for drug in drugs:
            n = sum(1 for t, dr, _ in plan if dr == drug and t.date() == day)
            cap = DOSE_RANGES[drug]["max_doses_day"]
            flag = "OK" if n <= cap else f"EXCEEDS daily max {cap}!"
            print(f"{drug}: {n} doses on {day} (max {cap}/24h) — {flag}")
            if n > cap:
                ok_all = False
    print()
    ok = ok and ok_all
    if ok:
        print("Intervals verified. Give a dose only if the child needs it — the schedule is a")
        print("ceiling, not a mandate. Log every dose actually given: fever.py log med ...")
    else:
        print("[!] Violations found — do NOT follow blindly; adjust start times.")
    print(f"\n{DISCLAIMER}")
    return 0 if ok else 1


def lo_hi(d, w):
    return d["min"] * w, d["max"] * w


def d_interval(drug):
    return DOSE_RANGES[drug]["interval_h"]


# ----------------------------------------------------------------------------
# 5) LOG
# ----------------------------------------------------------------------------
def cmd_log(a):
    data = load(a.db)
    if a.kind == "temp":
        c = core_temp(a.value, a.unit, a.route)
        e = ev(data, "temp", value_c=c, measured=a.value, unit=a.unit, route=a.route or "unspecified")
        print(f"logged temp {a.value}°{a.unit.upper()} ({a.route or '?'}) → est. core {c:.1f}°C")
    elif a.kind == "med":
        e = ev(data, "med", drug=norm_drug(a.drug) or a.drug, mg=a.mg, note="logged manually")
        print(f"logged {e['drug']} {a.mg} mg")
    elif a.kind == "fluids":
        e = ev(data, "fluids", ml=a.ml)
        print(f"logged fluids {a.ml} mL")
    elif a.kind == "note":
        e = ev(data, "note", text=a.text)
        print("note added")
    save(data, a.db)
    if a.kind == "temp":
        print("Run triage on this reading: fever.py triage --age-months N --temp T --unit c")
    return 0


def cmd_logshow(a):
    data = load(a.db)
    evs = data.get("events", [])
    if not evs:
        print("No events yet. Log: fever.py log temp 38.6 --route axillary")
        return 0
    print(f"Illness course — {len(evs)} events\n" + "-" * 46)
    for e in evs:
        at = e.get("at", "?")
        if e["kind"] == "temp":
            print(f"  {at}  temp {e.get('value_c', 0):.1f}°C core est. ({e.get('route')})")
        elif e["kind"] == "med":
            print(f"  {at}  {e.get('drug')} {e.get('mg')} mg")
        elif e["kind"] == "fluids":
            print(f"  {at}  fluids {e.get('ml')} mL")
        elif e["kind"] == "note":
            print(f"  {at}  note: {e.get('text')}")
    return 0


# ----------------------------------------------------------------------------
# 6) HANDOFF
# ----------------------------------------------------------------------------
def cmd_handoff(a):
    data = load(a.db)
    evs = data.get("events", [])
    temps = [e for e in evs if e["kind"] == "temp"]
    meds = [e for e in evs if e["kind"] == "med"]
    fluids = [e for e in evs if e["kind"] == "fluids"]
    print("=" * 60)
    print("PEDIATRICIAN HANDOFF SUMMARY — generated by baby-fever-triage")
    print(dt.datetime.now().strftime("generated: %Y-%m-%d %H:%M") + f" | {len(evs)} events")
    print("=" * 60)
    if a.age_months is not None:
        print(f"Age: {a.age_months} months   Weight: {a.weight_kg or '?'} kg")
    if temps:
        peak = max(t.get("value_c", 0) for t in temps)
        first, last = temps[0]["at"], temps[-1]["at"]
        print(f"Course: first temp {first} → last {last}")
        print(f"Peak estimated core temp: {peak:.1f}°C ({len(temps)} readings)")
        print("Temp trend:")
        for t in temps:
            print(f"   {t['at']}  {t.get('value_c', 0):.1f}°C ({t.get('route')})")
    else:
        print("No temperatures logged yet.")
    if meds:
        total = {}
        print("Medications given:")
        for m in meds:
            print(f"   {m['at']}  {m['drug']} {m.get('mg')} mg")
            total[m["drug"]] = total.get(m["drug"], 0) + (m.get("mg") or 0)
        print("Totals: " + ", ".join(f"{k} {v:.0f} mg" for k, v in total.items()))
    if fluids:
        tot = sum(f.get("ml", 0) for f in fluids)
        print(f"Fluids logged: {tot} mL across {len(fluids)} entries")
    print("-" * 60)
    print("Questions to ask:")
    print("  1. When can we return to daycare / normal activity?")
    print("  2. Which warning signs mean we should come back?")
    print("  3. Is alternating dosing appropriate for this child? Exact schedule?")
    print("  4. Dose confirmation for current weight (___ kg)?")
    print("=" * 60)
    print(DISCLAIMER)
    return 0


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=None, help="path to fever.json (default ./fever.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("triage", help="age+temp → EMERGENCY-NOW / SAME-DAY / HOME-CARE")
    p.add_argument("--age-months", type=float, required=True)
    p.add_argument("--temp", type=float, required=True)
    p.add_argument("--unit", choices=["c", "f"], default="c")
    p.add_argument("--route", default=None, choices=list(ROUTE_ADJ), help="measurement route (default none/raw)")
    p.add_argument("--responsive", default=None, type=str2bool, help="is the child interactive? yes/no")
    p.add_argument("--drinking", default=None, type=str2bool, help="drinking fluids? yes/no")
    p.set_defaults(fn=cmd_triage)

    p = sub.add_parser("flags", help="14-item red-flag checklist; any YES = EMERGENCY-NOW")
    for k, _ in RED_FLAGS:
        p.add_argument("--" + k, type=str2bool, default=None, help="yes/no")
    p.set_defaults(fn=cmd_flags)

    p = sub.add_parser("dose", help="weight-based dosing (refuses mL without --conc)")
    p.add_argument("--drug", required=True)
    p.add_argument("--weight-kg", type=float, required=True)
    p.add_argument("--age-months", type=float, default=None)
    p.add_argument("--conc", default=None, help="e.g. mg-per-ml:100 or plain number")
    p.add_argument("--doctor-directed", action="store_true")
    p.set_defaults(fn=cmd_dose)

    p = sub.add_parser("schedule", help="safe alternating-dose timeline")
    p.add_argument("--weight-kg", type=float, required=True)
    p.add_argument("--drugs", choices=["both", "acetaminophen", "ibuprofen"], default="both")
    p.add_argument("--start", default=None, help="ISO datetime, e.g. \"2026-09-27 22:00\"")
    p.add_argument("--hours", type=float, default=12)
    p.set_defaults(fn=cmd_schedule)

    p = sub.add_parser("log", help="record temp/med/fluids/note")
    p.add_argument("kind", choices=["temp", "med", "fluids", "note"])
    p.add_argument("value", nargs="?", type=float, help="temp value (or ml for fluids)")
    p.add_argument("--unit", choices=["c", "f"], default="c")
    p.add_argument("--route", default=None, choices=list(ROUTE_ADJ))
    p.add_argument("--drug", default=None)
    p.add_argument("--mg", type=float, default=None)
    p.add_argument("--ml", type=float, default=None)
    p.add_argument("--text", default=None)
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("logshow", help="print illness course")
    p.set_defaults(fn=cmd_logshow)

    p = sub.add_parser("handoff", help="doctor-ready summary")
    p.add_argument("--age-months", type=float, default=None)
    p.add_argument("--weight-kg", type=float, default=None)
    p.set_defaults(fn=cmd_handoff)

    a = ap.parse_args()
    # 'log temp' compat: value positional
    if a.cmd == "log" and a.kind == "fluids" and a.value is not None and a.ml is None:
        a.ml = a.value
    if a.cmd == "log" and a.kind == "note" and a.value is not None and not a.text:
        a.text = str(a.value)
    rc = a.fn(a)
    sys.exit(rc or 0)


def str2bool(v):
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    if s in ("yes", "true", "t", "y", "1"):
        return True
    if s in ("no", "false", "f", "n", "0"):
        return False
    return None


if __name__ == "__main__":
    main()
