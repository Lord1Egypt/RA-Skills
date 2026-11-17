#!/usr/bin/env python3
"""nap_navigator.py — wake-window timing instrument for infant/toddler naps.

Offline, stdlib-only. State: nap_state.json beside the script (or --state).
Commands: log | now | projections | drift | report
NOT MEDICAL ADVICE. Safe-sleep footer per AAP is printed with every plan.
"""
import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_STATE = Path(__file__).resolve().parent / "nap_state.json"

# age weeks lo, hi | window min/max (min) | naps label, naps_max | typical nap (min lo,hi)
# | bedtime band (min from midnight lo,hi) | typical night h | note
BANDS = [
    dict(lo=0, hi=6, wmin=45, wmax=70, naps="5-6 (chaotic)", nmax=6, nap=(40, 90),
         bed=(1230, 1320), night=9.0, note="PATTERN-SEEKING, NOT SCHEDULING — circadian rhythm not yet online"),
    dict(lo=6, hi=12, wmin=60, wmax=90, naps="4-5", nmax=5, nap=(45, 105),
         bed=(1170, 1260), night=9.5, note="rhythm begins; morning nap starts to anchor ~9:00"),
    dict(lo=13, hi=21, wmin=75, wmax=120, naps="4->3", nmax=4, nap=(45, 120),
         bed=(1140, 1200), night=10.0, note="naps 1-2 restorative; 3-4 are catnaps"),
    dict(lo=22, hi=30, wmin=120, wmax=165, naps="3", nmax=3, nap=(45, 90),
         bed=(1110, 1170), night=10.5, note="cap nap 3 ~45 min if it threatens bedtime"),
    dict(lo=31, hi=43, wmin=150, wmax=180, naps="3->2", nmax=3, nap=(45, 120),
         bed=(1110, 1170), night=11.0, note="3->2 TRANSITION ZONE (7-10 mo); check drift before dropping"),
    dict(lo=44, hi=60, wmin=165, wmax=210, naps="2", nmax=2, nap=(60, 120),
         bed=(1110, 1170), night=11.0, note="stable 2-nap balance point"),
    dict(lo=61, hi=78, wmin=180, wmax=240, naps="2->1", nmax=2, nap=(90, 150),
         bed=(1140, 1200), night=11.0, note="2->1 TRANSITION (avg ~15.5 mo)"),
    dict(lo=79, hi=104, wmin=270, wmax=330, naps="1", nmax=1, nap=(90, 150),
         bed=(1140, 1200), night=11.0, note="single midday nap"),
    dict(lo=105, hi=156, wmin=300, wmax=360, naps="1 (or none)", nmax=1, nap=(60, 120),
         bed=(1140, 1260), night=11.0, note="keep quiet time after the nap drops"),
]

CUES = ["yawning", "pink eyebrows", "gaze aversion", "fist to ear/mouth (past hunger)",
        "rubbing eyes/ears", "decreased activity, quieter", "slower sucking"]
RED_CUES = ["arching back", "fussiness spike", "hyper/wired state (cortex won)"]
FOOTER = ("SAFE SLEEP (AAP): back to sleep | firm flat bare crib | nothing in the sleep space "
          "| no weighted items/hats | room ~20-22C | room-share >= 6 months.\n"
          "NOT MEDICAL ADVICE — snoring, breathing pauses, pain wakes, or poor-weight-gain "
          "sleep disruption -> pediatrician, not this tool.")


def hm2m(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def m2hm(m):
    m = int(round(m))
    return f"{(m // 60) % 24:02d}:{m % 60:02d}"


def band_for(age_weeks):
    for b in BANDS:
        if b["lo"] <= age_weeks < b["hi"]:
            return b
    return BANDS[-1]


def load(state):
    if Path(state).exists():
        return json.loads(Path(state).read_text())
    return {"anchor": None, "entries": []}


def save(st, state):
    Path(state).write_text(json.dumps(st, indent=2))


def age_weeks_at(st, d):
    a = st.get("anchor")
    if not a:
        return None
    days = (d - date.fromisoformat(a["date"])).days
    return a["age_weeks"] + days / 7.0


def last_wake(st):
    wakes = [e for e in st["entries"] if "wake" in e]
    if not wakes:
        return None, None
    w = max(wakes, key=lambda e: (e["date"], e["wake"]))
    return w["date"], hm2m(w["wake"])


# ---------------------------------------------------------------- commands
def cmd_log(a, st, state):
    d = a.date or date.today().isoformat()
    if a.age_weeks is not None:
        st["anchor"] = {"date": d, "age_weeks": a.age_weeks}
        print(f"anchor set: {a.age_weeks} weeks on {d}")
    e = {"date": d}
    if a.wake:
        e["wake"] = a.wake
    if a.nap_start:
        e["nap_start"] = a.nap_start
    if a.nap_end:
        e["nap_end"] = a.nap_end
    if len(e) == 1:
        sys.exit("nothing to log: give --wake and/or --nap-start/--nap-end")
    st["entries"].append(e)
    save(st, state)
    age = age_weeks_at(st, date.fromisoformat(d))
    print(f"logged {e} | entries={len(st['entries'])}"
          + (f" | age now ~{age:.1f}w" if age else ""))


def cmd_now(a, st, state):
    d, w = last_wake(st)
    if w is None:
        sys.exit("no wake logged yet: log --age-weeks N --wake HH:MM")
    age = age_weeks_at(st, date.fromisoformat(d))
    if age is None:
        sys.exit("no anchor age: log --age-weeks once")
    b = band_for(age)
    now_m = datetime.now().hour * 60 + datetime.now().minute
    print(f"age ~{age:.1f} weeks | band {b['lo']}-{b['hi']}w | {b['naps']} naps/day | {b['note']}")
    print(f"last wake {d} {m2hm(w)}")
    print(f"window: {m2hm(w + b['wmin'])}-{m2hm(w + b['wmax'])} "
          f"(ideal start {m2hm(w + (b['wmin'] + b['wmax']) // 2)})")
    print("watch for: " + ", ".join(CUES[:5]))
    if now_m > w + b["wmax"] and now_m - w < 6 * 60:
        print("!! PAST WINDOW — second-wind risk. Settle now; if bedtime is near, pull it 15-20 min EARLIER.")
    print(FOOTER)


def cmd_projections(a, st, state):
    d, w = last_wake(st)
    if w is None:
        sys.exit("no wake logged yet")
    age = age_weeks_at(st, date.fromisoformat(d))
    if age is None:
        sys.exit("no anchor age: log --age-weeks once")
    b0 = band_for(age)
    print(f"PROJECTION from {d} {m2hm(w)} | age ~{age:.1f}w | {b0['naps']} naps/day")
    print(f"note: {b0['note']}\n")
    wake = w
    placed_naps = 0
    ot = False
    horizon_end = 24 * 60 + hm2m("12:00")  # stop ~noon tomorrow
    for i in range(b0["nmax"] + 1):
        age_i = age + i * 0.25
        b = band_for(age_i)
        mid = (b["wmin"] + b["wmax"]) // 2
        nap_start = wake + mid
        bed_lo, bed_hi = b["bed"]
        if placed_naps >= b["nmax"] or nap_start > bed_lo - 90:
            gap = b["wmax"]
            bedtime = wake + gap
            flag = ""
            if bedtime > bed_hi:
                bedtime = bed_hi
                flag = "  <- OVERTIRED RISK: pull previous nap shorter / bedtime 15-20 min earlier"
                ot = True
            print(f"  BEDTIME {m2hm(bedtime)} (window {m2hm(bed_lo)}-{m2hm(bed_hi)}) "
                  f"awake stretch {m2hm(wake)}->{m2hm(bedtime)} = {(bedtime - wake) / 60:.1f}h{flag}")
            mw = bedtime + b["night"] * 60
            print(f"  est. morning wake {m2hm(mw)} (typical night {b['night']}h)")
            break
        nap_len = (b["nap"][0] + b["nap"][1]) // 2
        warn = ""
        if mid > b["wmax"]:
            warn = "  <- window over max"
        print(f"  nap {placed_naps + 1}: {m2hm(nap_start)}-{m2hm(nap_start + nap_len)} "
              f"(~{nap_len} min, window {m2hm(wake + b['wmin'])}-{m2hm(wake + b['wmax'])}){warn}")
        placed_naps += 1
        wake = nap_start + nap_len
        if wake > horizon_end:
            break
    if ot:
        print("\n!! Day runs long: the fix is an EARLIER bedtime, never more stimulation "
              "(cortisol second wind keeps tired babies awake).")
    print("\ncues to act on: " + ", ".join(CUES))
    print("past-max red flags: " + ", ".join(RED_CUES))
    print("\n" + FOOTER)


def _slope(pts):
    """least-squares slope (min/day) for [(day_index, minutes)]"""
    n = len(pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    return (sum((x - mx) * (y - my) for x, y in pts) / den) if den else 0.0


def cmd_drift(a, st, state):
    days = {}
    for e in st["entries"]:
        if "nap_start" in e:
            days.setdefault(e["date"], []).append(hm2m(e["nap_start"]))
    if not days:
        sys.exit("no nap starts logged: log --nap-start HH:MM [--nap-end HH:MM]")
    dates = sorted(days)
    if len(dates) < 3:
        sys.exit(f"only {len(dates)} day(s) with naps — need >=3 (7+ for a real verdict)")
    d0 = date.fromisoformat(dates[0])
    slots = {}
    for d in dates:
        for i, s in enumerate(sorted(days[d])):
            slots.setdefault(i, []).append(((date.fromisoformat(d) - d0).days, s))
    print(f"DRIFT over {len(dates)} days ({dates[0]} .. {dates[-1]})")
    any_creep = False
    for i in sorted(slots):
        pts = slots[i]
        if len(pts) < 3:
            continue
        per_week = _slope(pts) * 7
        if per_week > 10:
            v = f"CREEPING +{per_week:.0f} min/wk — watch for nap transition"
            any_creep = True
        elif per_week > 5:
            v = f"slight creep +{per_week:.0f} min/wk — keep watching"
            any_creep = True
        elif per_week < -10:
            v = f"REGRESSION {per_week:.0f} min/wk (earlier) — check morning light / bedtime placement"
        else:
            v = "STABLE"
        avg = sum(p[1] for p in pts) / len(pts)
        print(f"  nap {i + 1}: avg start {m2hm(avg)}  slope {per_week:+.1f} min/wk  -> {v}")
    if any_creep:
        print("\ntransition signals checklist: nap refused >=5 non-illness days? other naps "
              "shortening/lengthening? night wakes with no other cause? All three = transition.")
    print("regressions need 3-5 consecutive days before concluding anything. Watch the baby, not the clock.")


def cmd_report(a, st, state):
    days = {}
    for e in st["entries"]:
        days.setdefault(e["date"], []).append(e)
    dates = sorted(days)[-7:]
    if not dates:
        sys.exit("nothing logged yet")
    age = age_weeks_at(st, date.fromisoformat(dates[-1]))
    b = band_for(age) if age is not None else BANDS[0]
    print(f"7-DAY REPORT | age ~{age:.1f}w | band expects {b['naps']} naps\n")
    for d in dates:
        es = days[d]
        naps = [(hm2m(e["nap_start"]), hm2m(e["nap_end"]))
                for e in es if "nap_start" in e and "nap_end" in e]
        total = sum(end - start for start, end in naps)
        wakes = [e["wake"] for e in es if "wake" in e]
        partial = len(naps) < 2 and b["nmax"] >= 2
        tag = "PARTIAL" if partial else "ok"
        detail = " ".join(f"{m2hm(s)}-{m2hm(e)}" for s, e in naps) or "(no complete naps logged)"
        print(f"  {d} [{tag}] naps={len(naps)} total={total // 60}h{total % 60:02d}m | {detail}"
              + (f" | wakes: {', '.join(wakes)}" if wakes else ""))
    print("\n" + FOOTER)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", default=str(DEFAULT_STATE))
    sub = p.add_subparsers(dest="cmd", required=True)
    lg = sub.add_parser("log")
    lg.add_argument("--age-weeks", type=float)
    lg.add_argument("--wake")
    lg.add_argument("--nap-start")
    lg.add_argument("--nap-end")
    lg.add_argument("--date", help="YYYY-MM-DD for backfill")
    sub.add_parser("now")
    sub.add_parser("projections")
    dr = sub.add_parser("drift")
    dr.add_argument("--clean", action="store_true", help="exclude PARTIAL days (<2 naps)")
    sub.add_parser("report")
    a = p.parse_args()
    st = load(a.state)
    {"log": cmd_log, "now": cmd_now, "projections": cmd_projections,
     "drift": cmd_drift, "report": cmd_report}[a.cmd](a, st, a.state)


if __name__ == "__main__":
    main()
