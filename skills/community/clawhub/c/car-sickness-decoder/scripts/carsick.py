#!/usr/bin/env python3
"""carsick.py — car/motion sickness triage, trip protocol, weight-banded dosing, log analysis.

Subcommands:
  triage   classify the pattern (classic / migraine-suspect / conditioned / red flags)
  plan     build the seating/gaze/food/cadence protocol for a trip
  dose     OTC antiemetic dosing by weight with hard gates
  log      episode CSV analyzer (date,seat,activity,hour,duration,severity)

Offline, stdlib only. Educational: a pediatrician owns medical decisions.
"""
import argparse
import csv
import re
from collections import Counter, defaultdict

FOOTER = ("\nEDUCATIONAL — not a substitute for a pediatrician. Label bands "
          "as published by manufacturers; follow the package and your doctor "
          "when they disagree with this tool.\n")

# ------------------------------------------------------------------- triage

CLASSIC_CLUES = {
    "pale": 2, "sweaty": 2, "cold sweat": 2, "nausea": 2, "queasy": 2,
    "drool": 1, "vomit": 1, "winding": 2, "curvy": 2, "backroad": 1,
    "resolves after stop": 3, "fine after stop": 3, "resolves": 2,
    "fine on highway": 1, "stop and go": 1, "resolves after stopping": 3,
}
MIGRAINE_CLUES = {
    "headache": 3, "head pain": 3, "light sensitive": 2, "photophobia": 3,
    "noise sensitive": 2, "phonophobia": 3, "spinning": 2, "vertigo": 3,
    "at rest": 2, "family migraine": 2, "migraine": 2,
}
CONDITIONED_CLUES = {
    "before the trip": 3, "before leaving": 3, "driveway": 3, "at the mention": 3,
    "anticipat": 3, "anxious": 2, "anxiety": 2, "worry": 1, "only some drivers": 1,
}
RED_FLAGS = {
    "hearing loss": 5, "ringing": 3, "tinnitus": 4, "ear fullness": 2,
    "imbalance": 4, "walking into": 4, "ataxia": 5, "severe headache": 5,
    "worst headache": 5, "vomiting >2h": 4, "vomiting over 2 hours": 4,
    "dehydrat": 4, "after concussion": 5, "after head injury": 5,
    "neuro": 3, "slurred": 4, "double vision": 4,
}


def triage(age, symptoms, since, on_trips_only, frequency):
    text = (symptoms or "").lower()
    def score(table):
        return sum(v for k, v in table.items() if k in text)
    classic, mig, cond = score(CLASSIC_CLUES), score(MIGRAINE_CLUES), score(CONDITIONED_CLUES)
    flags = [k for k in RED_FLAGS if k in text]
    print("CAR-SICKNESS TRIAGE")
    print("═" * 62)
    print(f"Age {age if age else '?'} | pattern since: {since or '?'} | "
          f"episodes: {frequency or '?'} | on-trips-only: {on_trips_only}")
    print(f"Scores — classic {classic}, migraine-suspect {mig}, conditioned {cond}")
    print("─" * 62)
    if flags:
        print("🚩 RED FLAG(S) DETECTED:", ", ".join(flags))
        print("   → DOCTOR NOW / same-day. These are not 'just carsickness' signs;")
        print("     stop triaging and escalate. Do not give another motion-sickness dose.")
        print(FOOTER)
        return
    if age is not None and age < 2:
        print(f"AGE GATE: under 2 — motion-sickness antihistamines are NOT for this age.")
        print("   Non-drug protocol only (front gaze, nap timing, smooth driving).")
        print("   Frequent episodes under 2 → pediatrician visit.")
    candidates = [("CLASSIC KINETOSIS", classic), ("MIGRAINE-SUSPECT", mig),
                  ("CONDITIONED/ANTICIPATORY", cond)]
    top, pts = max(candidates, key=lambda c: c[1])
    if pts == 0:
        print("Not enough clues. Typical classic picture: pale+sweaty+nausea on winding")
        print("roads that resolves within 30 min of stopping, age 2–12, trips only.")
        verdict = "UNCLEAR — re-run with more symptom detail"
    elif top == "CLASSIC KINETOSIS" and classic >= mig and classic >= cond:
        verdict = top
        print(f"VERDICT: {verdict} (score {pts})")
        print("   Sensory-mismatch picture. Management: trip protocol (`plan`) ±")
        print("   pre-trip antihistamine 30–60 min before departure (`dose`).")
    elif top == "MIGRAINE-SUSPECT":
        verdict = top
        print(f"VERDICT: {verdict} (score {pts})")
        print("   Headache/vertigo features present. See the pediatrician — vestibular")
        print("   migraine is common in school-age kids and treatable. The behavioral")
        print("   protocol still reduces load in the meantime.")
    else:
        verdict = top
        print(f"VERDICT: {verdict} (score {pts})")
        print("   Nausea starts before motion — conditioned response. Plan: calm")
        print("   framing, graded short drives to fun destinations, no drama at cleanup.")
        print("   Meds usually unnecessary; don't cement the 'sick passenger' identity.")
    if on_trips_only and on_trips_only.lower().startswith("n") and classic > 0:
        print("NOTE: episodes NOT confined to trips + nausea pattern → widen the")
        print("differential with a doctor (reflux, cyclic vomiting, abdominal migraine).")
    print(FOOTER)


# -------------------------------------------------------------------- plan

def plan(age, trip_hours, winding, night, boostered, history):
    print(f"TRIP PROTOCOL — {trip_hours:g} h drive"
          + (" (winding)" if winding else "")
          + (" (night)" if night else ""))
    print("═" * 62)
    steps = []
    seat = ("Center rear seat (clearest forward view, least head roll)" if age and age < 13
            else "Front passenger seat (reclined slightly, eyes on the road)")
    if age and age < 13 and not boostered:
        seat += " — on a booster so the horizon line is visible"
    steps.append(("SEAT", seat))
    steps.append(("GAZE RULE", "Eyes forward at the horizon the whole drive. NO books, "
                  "tablets, phones, handheld games. Audio books and music are fine — "
                  "ears don't conflict, eyes do."))
    steps.append(("TIMING", ("Drive during nap/night — sleep is immunity."
                  if night else
                  "If possible shift departure into nap window; announce the plan the day before.")))
    cadence = max(30 if winding else 45, min(90, int(trip_hours * 60 / max(1, int(trip_hours * 1.2)))))
    steps.append(("STOP CADENCE",
                  f"Stop every {45 if not winding else 30}–{60} min: 5 minutes walking, "
                  "cool air. Winding roads = shorter intervals."))
    steps.append(("FOOD", "Light carbs 30–60 min before (crackers, toast, banana); avoid "
                  "greasy/acidic/heavy. Cold-water sips en route. Ginger chew/drink "
                  "0.5–1 g 30 min before (best-evidenced non-drug option)."))
    steps.append(("CABIN", "Cool airflow at the face; no strong smells (air freshener out, "
                  "food wrappers out); loose clothing; sour candy as rescue comfort."))
    steps.append(("DRIVING", "Smooth inputs: early braking, wide lines on curves, announce "
                  "turns. Late braking and jerky lane changes are the top driver-side triggers."))
    if history:
        steps.append(("PRE-MED", "Given the history, consider an OTC antihistamine "
                      "30–60 min BEFORE departure (run `dose` for the weight-banded "
                      "number). Never wait for nausea — these prevent, they don't rescue."))
    steps.append(("RESCUE (mid-episode)", "Stop safely → walk 5 min → cool air on face → "
                  "small cold sips → sour candy. No pills once vomiting started. "
                  "Sleep = finish line. Cleanup without commentary."))
    for i, (title, body) in enumerate(steps, 1):
        print(f"[{i}] {title}: {body}")
    print()
    print("Night dosing note: if the pediatrician agrees, a bedtime-dose antihistamine "
          "on a night drive doubles as sleep aid — but that's a doctor conversation.")
    print(FOOTER)


# -------------------------------------------------------------------- dose

MEDS = {
    "dimenhydrinate": {
        "label": "dimenhydrinate (Dramamine)",
        "bands": [(2, 6, 12.5, 25, 75), (6, 12, 25, 50, 150), (12, 200, 50, 100, 400)],
        "every": "6–8 h", "min_age": 2, "note": "Duration 4–6 h — plan the second dose "
        "for long drives. Drowsiness is the main effect (useful at night)."},
    "diphenhydramine": {
        "label": "diphenhydramine (Benadryl)",
        "bands": [(2, 6, 12.5, 25, 75), (6, 12, 25, 50, 150), (12, 200, 50, 100, 400)],
        "every": "6 h", "min_age": 2, "note": "More sedating per mg; same pre-trip timing."},
    "meclizine": {
        "label": "meclizine (Bonine)",
        "bands": [(12, 200, 25, 50, 50)],
        "every": "24 h", "min_age": 12, "note": "Less sedating, 24 h duration — good for "
        "all-day trips. Not labeled for children under 12."},
}


def dose(age, weight, med):
    m = MEDS[med]
    print(f"MOTION-SICKNESS DOSING — {m['label']}, "
          f"{age if age else '?'} y, {weight if weight else '?'} kg")
    print("═" * 62)
    if age is not None and age < m["min_age"]:
        print(f"✖ AGE GATE: {med} is not for under {m['min_age']} y"
              + (" — no motion-sickness antihistamines under 2 at all." if m["min_age"] == 2 else "."))
        print("  Non-med arm only: front gaze + horizon, center rear seat, nap timing,")
        print("  ginger 30 min before, stops every 30–45 min. Frequent episodes → pediatrician.")
        print(FOOTER)
        return
    band = next((b for b in m["bands"]
                 if (age is None or b[0] <= age < b[1])), None)
    if band is None:
        print("No band resolves — check age input.")
        return
    lo_a, hi_a, lo, hi, mx = band
    print(f"Label band {lo_a}–{hi_a} y: {lo:g}–{hi:g} mg per dose, max {mx:g} mg/day")
    # weight sanity: typical child weight for age (rough 2-12y: ~ age*2+9 kg)
    if weight is not None and age is not None and 2 <= age <= 12:
        typical = age * 2 + 9
        note = (f"Weight check: {weight:g} kg vs ~{typical} kg typical for {age} y — "
                + ("well below typical: start at the LOW end of the band."
                   if weight < typical * 0.85 else
                   "above typical: the band's low end is still the safe start; "
                   "don't jump to the max without a doctor."
                   if weight > typical * 1.25 else "in line; band applies as printed."))
        print(f"  {note}")
    start = lo if (weight is not None and age is not None and 2 <= age <= 12
                   and weight < (age * 2 + 9) * 0.85) else (lo + hi) / 2 if hi - lo >= 25 else lo
    start = round(start * 2) / 2
    tag = "low-end start" if start <= lo else "mid-band start"
    print(f"DOSE: {start:g} mg ({tag}), 30–60 min BEFORE departure")
    print(f"      repeat every {m['every']}, MAX {mx:g} mg/day")
    print("GATES: never combine with other antihistamines/cold meds · check with the "
          "pediatrician for regular use · once vomiting has started, pills won't stay down.")
    print(f"NOTE: {m['note']}")
    print("Non-med arm runs in parallel: gaze rule, seat, ginger, cadence (`plan`).")
    print(FOOTER)


# --------------------------------------------------------------------- log

def log_analyze(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip() or row[0].lower().startswith("date"):
                continue
            try:
                rows.append({"date": row[0], "seat": (row[1] if len(row) > 1 else "").strip(),
                             "activity": (row[2] if len(row) > 2 else "").strip(),
                             "hour": (row[3] if len(row) > 3 else "").strip(),
                             "severity": (row[4] if len(row) > 4 else "").strip()})
            except IndexError:
                continue
    if not rows:
        print("No parsable rows (expected: date,seat,activity,hour,duration/severity).")
        return 1
    print(f"EPISODE LOG — {len(rows)} episodes")
    print("═" * 62)
    for field, label in (("seat", "SEAT"), ("activity", "ACTIVITY"), ("hour", "HOUR")):
        c = Counter(r[field].lower() for r in rows if r[field])
        if c:
            top = ", ".join(f"{k} ×{v}" for k, v in c.most_common(4))
            print(f"{label}: {top}")
    try:
        sev = [float(re.sub(r"[^\d.]", "", r["severity"])) for r in rows
               if re.sub(r"[^\d.]", "", r["severity"])]
        if sev:
            print(f"Severity: avg {sum(sev) / len(sev):.1f}, max {max(sev):.0f} "
                  f"over {len(sev)} rated episodes")
    except ValueError:
        pass
    print("─" * 62)
    print("Reading: dominant seat/activity/hour = your trigger conditions. If episodes")
    print("cluster on one seat/activity, the protocol writes itself (change that one")
    print("variable first). If severity trends up or episodes spread to new conditions,")
    print("re-run `triage` and consider the pediatrician.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("triage")
    p.add_argument("--age", type=int, default=None)
    p.add_argument("--symptoms", required=True)
    p.add_argument("--since", default="")
    p.add_argument("--on-trips-only", default="yes")
    p.add_argument("--frequency", default="")

    p = sub.add_parser("plan")
    p.add_argument("--age", type=int, default=None)
    p.add_argument("--trip-hours", type=float, required=True)
    p.add_argument("--winding", action="store_true")
    p.add_argument("--night", action="store_true")
    p.add_argument("--boostered", action="store_true")
    p.add_argument("--history", action="store_true",
                   help="known carsick passenger — include pre-med guidance")

    p = sub.add_parser("dose")
    p.add_argument("--age", type=int, default=None)
    p.add_argument("--weight", type=float, default=None)
    p.add_argument("--med", default="dimenhydrinate", choices=list(MEDS))

    p = sub.add_parser("log")
    p.add_argument("--csv", required=True)

    a = ap.parse_args()
    if a.cmd == "triage":
        triage(a.age, a.symptoms, a.since, a.on_trips_only, a.frequency)
    elif a.cmd == "plan":
        plan(a.age, a.trip_hours, a.winding, a.night, a.boostered, a.history)
    elif a.cmd == "dose":
        dose(a.age, a.weight, a.med)
    elif a.cmd == "log":
        raise SystemExit(log_analyze(a.csv) or 0)


if __name__ == "__main__":
    main()
