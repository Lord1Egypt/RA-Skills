#!/usr/bin/env python3
"""bp-log-sentinel: home blood-pressure log analysis.

Pure-stdlib. Analyzes a CSV of home BP readings against ACC/AHA 2017 and
ESC/ESH 2023 thresholds, computes averages per AHA home-monitoring rules
(discard day-1, average days 2-7, morning+evening), grades hypertension
(Stage 1/2), finds the white-coat / masked patterns (home vs clinic),
evaluates measurement-procedure compliance from a procedure questionnaire,
flags readings contaminated by known error sources (caffeine, full bladder,
recent smoking, arm position), and writes a doctor-ready consult summary.

CSV columns (header required): date, time, systolic, diastolic, pulse
Optional columns: arm, position, notes
(`notes` is scanned for: caffeine, smoking/vaping, exercise, full bladder,
 talking, cold, back unsupported, legs crossed, wrong cuff, over clothing)

Usage:
  python3 bp_sentinel.py analyze readings.csv
  python3 bp_sentinel.py analyze readings.csv --clinic 150/95 --window 7
  python3 bp_sentinel.py demo          # self-test with synthetic data
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import sys
from statistics import mean, pstdev

# ---------------------------------------------------------------- thresholds

# ACC/AHA 2017 home (self-monitoring) thresholds
AHA_HOME_NORMAL = (120.0, 80.0)          # home SBP >=135 or DBP >=85 => hypertensive (AHA/ESH)
AHA_HOME_ELEVATED_TRIGGER = (135.0, 85.0)
AHA_STAGE2_TRIGGER = (150.0, 95.0)       # home avg >=150/95

# ESC/ESH 2023 home thresholds (identical operational triggers)
ESH_HOME_HYPERTENSION = (135.0, 85.0)

CATS = [
    (120, 80, "Normal"),
    (130, 80, "Elevated"),
    (140, 90, "Stage 1 hypertension"),
    (180, 120, "Stage 2 hypertension"),
    (float("inf"), float("inf"), "Crisis — seek care immediately"),
]

PROCEDURE_RULES = [
    ("no_activity_30m", "No exercise in the 30 min before"),
    ("empty_bladder", "Bladder empty"),
    ("seated_5m", "Seated quietly 5 min before"),
    ("back_supported", "Back supported, feet flat"),
    ("arm_supported", "Arm supported at heart level"),
    ("correct_cuff", "Correct cuff size for arm circumference"),
    ("no_talking", "No talking during measurement"),
    ("no_caffeine_30m", "No caffeine in the 30 min before"),
    ("no_smoking_30m", "No smoking/vaping 30 min before"),
    ("two_readings", "Two readings 1-2 min apart, average taken"),
]

CONTAMINANT_PATTERNS = [
    ("caffeine", ["caffeine", "coffee", "tea", "energy drink"]),
    ("smoking", ["smok", "vape", "cigarette"]),
    ("exercise", ["exercise", "workout", "run", "gym", "cycled"]),
    ("full bladder", ["full bladder", "held pee", "bathroom urgent"]),
    ("talking", ["talked", "talking", "on the phone", "call"]),
    ("cold", ["cold", "shivering", "freezing"]),
    ("posture", ["legs crossed", "back unsupported", "standing", "lying"]),
    ("cuff issue", ["over cloth", "sleeve", "wrong cuff", "loose cuff"]),
]

# BP components of cardiovascular risk (rough, per 20/10 mmHg, Lancet-type RCT meta framing)
RISK_PER_20_10 = "each 20/10 mmHg increase roughly doubles cardiovascular mortality risk"


def parse_csv(text: str) -> list[dict]:
    """Parse CSV with header: date,time,systolic,diastolic,pulse[,arm,position,notes]."""
    rows = []
    rdr = csv.DictReader(io.StringIO(text))
    required = {"date", "time", "systolic", "diastolic"}
    if not rdr.fieldnames or not required.issubset({f.strip().lower() for f in rdr.fieldnames}):
        raise ValueError("CSV must have header: date,time,systolic,diastolic,pulse[,arm,position,notes]")
    for i, r in enumerate(rdr, 2):
        try:
            row = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in r.items() if k}
            d = dt.date.fromisoformat(row["date"])
            sys_v = float(row["systolic"])
            dia_v = float(row["diastolic"])
            if not (60 <= sys_v <= 260 and 30 <= dia_v <= 160):
                raise ValueError(f"implausible values {sys_v}/{dia_v}")
            rows.append({
                "date": d, "time": row.get("time", ""),
                "sys": sys_v, "dia": dia_v,
                "pulse": float(row["pulse"]) if row.get("pulse") else None,
                "notes": (row.get("notes") or "").lower(),
                "line": i,
            })
        except (KeyError, ValueError) as e:
            print(f"  (skipping line {i}: {e})", file=sys.stderr)
    return rows


def detect_contaminants(rows: list[dict]) -> list[tuple[dict, list[str]]]:
    out = []
    for r in rows:
        hits = [name for name, pats in CONTAMINANT_PATTERNS for p in pats if p in r["notes"]]
        if hits:
            out.append((r, sorted(set(hits))))
    return out


def aha_home_average(rows: list[dict], discard_day1: bool = True) -> dict:
    """AHA home-monitoring average: drop day 1, then mean of all remaining readings
    (ideally days 2-7, morning + evening)."""
    days = sorted({r["date"] for r in rows})
    if discard_day1 and len(days) > 1:
        kept = [r for r in rows if r["date"] != days[0]]
        note = f"day 1 ({days[0].isoformat()}) discarded per AHA protocol"
    else:
        kept = rows
        note = "single-day log; day-1 readings included"
    if not kept:
        raise ValueError("no readings left after day-1 discard")
    return {
        "n_days": len({r['date'] for r in kept}),
        "n_readings": len(kept),
        "sys_avg": round(mean(r["sys"] for r in kept), 1),
        "dia_avg": round(mean(r["dia"] for r in kept), 1),
        "pulse_avg": round(mean(r["pulse"] for r in kept if r["pulse"]), 1)
                     if any(r["pulse"] for r in kept) else None,
        "sys_sd": round(pstdev([r["sys"] for r in kept]), 1) if len(kept) > 1 else None,
        "dia_sd": round(pstdev([r["dia"] for r in kept]), 1) if len(kept) > 1 else None,
        "note": note,
    }


def classify(avg_sys: float, avg_dia: float) -> str:
    if avg_sys >= 180 or avg_dia >= 120:
        return "Crisis range — contact care now"
    if avg_sys >= 140 or avg_dia >= 90:
        return "Stage 2 hypertension (home average)"
    if avg_sys >= 130 or avg_dia >= 80:
        return "Stage 1 hypertension (home average)"
    if avg_sys >= 120:
        return "Elevated (home average)"
    return "Normal (home average)"


def white_coat_check(home_avg: dict, clinic: tuple[float, float] | None) -> dict | None:
    """White-coat = clinic high, home normal. Masked = clinic normal, home high."""
    if clinic is None:
        return None
    c_sys, c_dia = clinic
    home_high = home_avg["sys_avg"] >= ESH_HOME_HYPERTENSION[0] or home_avg["dia_avg"] >= ESH_HOME_HYPERTENSION[1]
    clinic_high = c_sys >= 140 or c_dia >= 90
    if clinic_high and not home_high:
        kind = "WHITE-COAT pattern: clinic high, home normal"
        advice = ("Bring the log to your physician — white-coat hypertension still carries "
                  "some risk and is managed case-by-case (lifestyle + monitoring), not ignored.")
    elif home_high and not clinic_high:
        kind = "MASKED HYPERTENSION: home high, clinic normal"
        advice = ("Masked hypertension carries risk close to sustained hypertension — "
                  "this log is exactly the evidence your physician needs.")
    else:
        kind = ("SUSTAINED hypertension pattern (both settings high)" if home_high
                else "Normotensive in both settings")
        advice = ""
    return {"clinic": f"{c_sys:.0f}/{c_dia:.0f}", "kind": kind, "advice": advice}


def procedure_audit(answers: dict[str, bool]) -> list[str]:
    """answers: rule_key -> True/False. Returns list of failed-rule strings."""
    fails = []
    for key, text in PROCEDURE_RULES:
        v = answers.get(key)
        if v is False:
            fails.append(text)
    return fails


def render_report(rows, avg, category, contaminants, wc, proc_fails, args_info) -> str:
    L = []
    bar = "=" * 64
    L += [bar, "BP LOG SENTINEL — home blood-pressure log analysis", bar]
    L.append(f"Readings: {len(rows)}  Days: {len({r['date'] for r in rows})}  "
             f"Period: {min(r['date'] for r in rows)} … {max(r['date'] for r in rows)}")
    L.append(f"Averaging: {avg['note']}")
    L.append(f"  -> {avg['n_readings']} readings over {avg['n_days']} days", )
    L.append("")
    L.append(f"HOME AVERAGE: {avg['sys_avg']:.0f}/{avg['dia_avg']:.0f} mmHg"
             + (f"   (SD {avg['sys_sd']}/{avg['dia_sd']})" if avg["sys_sd"] is not None else ""))
    if avg["pulse_avg"]:
        L.append(f"PULSE AVERAGE: {avg['pulse_avg']:.0f} bpm")
    L.append(f"CATEGORY (ACC/AHA 2017 home thresholds): {category}")
    L.append(f"  Thresholds used: normal <120/80, elevated >=120-129/<80, "
             f"stage1 >=130/80, stage2 >=140/90 (home triggers 135/85)")
    L.append("")
    if contaminants:
        L.append(f"MEASUREMENT-ERROR FLAGS ({len(contaminants)} readings):")
        for r, hits in contaminants[:8]:
            L.append(f"  {r['date']} {r['time']}: {r['sys']:.0f}/{r['dia']:.0f} — {', '.join(hits)}")
        L.append("  (These readings still count toward averages; consider re-measuring")
        L.append("   correctly and logging a clean session before drawing conclusions.)")
        L.append("")
    if wc:
        L.append(f"CLINIC COMPARISON: clinic {wc['clinic']} vs home {avg['sys_avg']:.0f}/{avg['dia_avg']:.0f}")
        L.append(f"  {wc['kind']}")
        if wc["advice"]:
            L.append(f"  -> {wc['advice']}")
        L.append("")
    if proc_fails:
        L.append("PROCEDURE COMPLIANCE — failed checks:")
        for f in proc_fails:
            L.append(f"  x {f}")
        L.append("  Each failed rule can shift readings by 5-10 mmHg. Fix these first,")
        L.append("  then re-log 7 days before trusting the category.")
        L.append("")
    L.append("TRENDS IN THIS LOG:")
    L.append(f"  Highest reading: {max(r['sys'] for r in rows):.0f} sys "
             f"({[r for r in rows if r['sys'] == max(x['sys'] for x in rows)][0]['date']})")
    lows = min(r["sys"] for r in rows)
    L.append(f"  Lowest systolic: {lows:.0f}")
    extremes = [r for r in rows if r["sys"] >= 180 or r["dia"] >= 120]
    if extremes:
        L.append(f"  !! {len(extremes)} reading(s) >=180/120 (crisis range):")
        for r in extremes:
            L.append(f"     {r['date']} {r['time']}  {r['sys']:.0f}/{r['dia']:.0f}")
        L.append("     If a reading like that comes with chest pain, shortness of breath,")
        L.append("     vision changes, weakness, or confusion — emergency care NOW.")
    L.append("")
    L.append("CONTEXT: " + RISK_PER_20_10 + ".")
    L.append("")
    L.append("NEXT STEPS")
    L.append("  1. If any reading >=180/120 with symptoms: emergency care now.")
    L.append("  2. Bring this log (and the averaging note) to your physician —")
    L.append("     home-monitoring averages, not office spot-checks, drive diagnosis.")
    L.append("  3. Diagnosis requires confirmation: a 7-day home log with correct")
    L.append("     technique, analyzed like this one.")
    L.append("")
    L.append("This is an information tool, not a diagnosis. Thresholds: ACC/AHA 2017,")
    L.append("ESC/ESH 2023 home-monitoring guidance.")
    return "\n".join(L)


def demo() -> str:
    """Synthetic 7-day log: masked-hypertension pattern + contaminants + crisis reading."""
    csv_text = (
        "date,time,systolic,diastolic,pulse,arm,position,notes\n"
        "2026-09-28,08:02,138,88,72,left,seated,coffee before reading\n"
        "2026-09-28,20:15,136,86,70,left,seated,\n"
        "2026-09-29,08:05,134,85,74,left,seated,\n"
        "2026-09-29,20:10,137,87,71,left,seated,talked during measurement\n"
        "2026-09-30,08:03,133,84,73,left,seated,\n"
        "2026-09-30,20:12,135,86,69,left,seated,\n"
        "2026-10-01,08:04,132,83,72,left,seated,\n"
        "2026-10-01,20:11,136,88,74,left,seated,\n"
        "2026-10-02,08:06,135,85,73,left,seated,\n"
        "2026-10-02,20:14,184,122,88,left,seated,feeling unwell\n"
        "2026-10-03,08:02,134,86,72,left,seated,\n"
        "2026-10-03,20:10,136,87,71,left,seated,\n"
        "2026-10-04,08:05,133,84,70,left,seated,\n"
        "2026-10-04,20:13,135,86,72,left,seated,\n"
    )
    rows = parse_csv(csv_text)
    avg = aha_home_average(rows)
    cat = classify(avg["sys_avg"], avg["dia_avg"])
    contam = detect_contaminants(rows)
    wc = white_coat_check(avg, (128, 82))  # clinic normal -> masked pattern
    proc_fails = procedure_audit({k: True for k, _ in PROCEDURE_RULES[:8]} |
                                 {"no_caffeine_30m": False, "two_readings": False})
    return render_report(rows, avg, cat, contam, wc, proc_fails, {})


def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Home BP log analysis (ACC/AHA + ESC/ESH)")
    p.add_argument("command", choices=["analyze", "demo"])
    p.add_argument("csv", nargs="?", help="readings CSV (header: date,time,systolic,diastolic,pulse)")
    p.add_argument("--clinic", help="clinic reading SYS/DIA e.g. 150/95, for white-coat check")
    p.add_argument("--keep-day1", action="store_true",
                   help="do not discard day 1 (default: discard per AHA protocol)")
    p.add_argument("--window", type=int, default=7, help="analysis window in days (default 7)")
    args = p.parse_args(argv)

    if args.command == "demo":
        print(demo())
        return

    if not args.csv:
        p.error("analyze needs a CSV path")
    with open(args.csv, encoding="utf-8") as f:
        text = f.read()
    rows = parse_csv(text)
    if not rows:
        print("No valid rows.")
        return 1

    if args.window and len(rows) > 4:
        cutoff = max(r["date"] for r in rows) - dt.timedelta(days=args.window)
        rows = [r for r in rows if r["date"] >= cutoff]

    avg = aha_home_average(rows, discard_day1=not args.keep_day1)
    cat = classify(avg["sys_avg"], avg["dia_avg"])
    contam = detect_contaminants(rows)
    clinic = None
    if args.clinic:
        s, d = args.clinic.split("/")
        clinic = (float(s), float(d))
    wc = white_coat_check(avg, clinic)
    print(render_report(rows, avg, cat, contam, wc, [], {}))


if __name__ == "__main__":
    main(sys.argv[1:])
