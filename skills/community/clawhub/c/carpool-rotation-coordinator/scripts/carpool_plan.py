#!/usr/bin/env python3
"""Carpool Rotation Coordinator — fair school-run scheduling.

Seat-credit fairness model: each occupied seat a driver supplies is credit;
each ride a kid consumes is debt. The scheduler always picks the
lowest-balance eligible driver, so load provably spreads.

Commands:
  plan   Generate N weeks of schedule + fairness audit + optional cost split.
  audit  Print only the projected fairness audit (no calendar).

stdlib only.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta

WEEKDAY_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
BAND = 0.15  # +/- 15% of family demand = fairness tolerance


def load_registry(path):
    with open(path, encoding="utf-8") as f:
        reg = json.load(f)
    fams = {k["family"] for k in reg["kids"]} | {d["family"] for d in reg["drivers"]}
    for f in fams:
        if not any(d["family"] == f for d in reg["drivers"]):
            raise SystemExit(f"family {f} has kids but no driver entry")
    return reg


def school_days(start_iso, weeks, blackouts):
    d0 = date.fromisoformat(start_iso)
    # align to next Monday
    d0 += timedelta(days=(7 - d0.weekday()) % 7)
    days = []
    d = d0
    while len(days) < weeks * 5:
        if d.weekday() < 5 and d.isoformat() not in blackouts:
            days.append(d)
        d += timedelta(days=1)
    return days


def plan(reg, weeks):
    days = school_days(reg["start"], weeks, set(reg.get("blackouts", [])))
    trips = reg.get("trips", ["AM", "PM"])
    drivers = reg["drivers"]
    kids = reg["kids"]
    absent = {}
    for k in kids:
        for a in k.get("absent", []):
            absent.setdefault(a, []).append(k["name"])

    balance = {k["family"]: 0.0 for k in kids}          # credit - debt
    drive_days = {d["family"]: 0 for d in drivers}
    seats_given = {d["family"]: 0 for d in drivers}
    seats_taken = {k["family"]: 0.0 for k in kids}
    schedule = []
    rr = 0  # round-robin pointer for ties

    for day in days:
        riders = [k for k in kids if k["name"] not in absent.get(day.isoformat(), [])]
        n_ride = len(riders)
        n_booster = sum(1 for k in riders if k.get("booster"))
        wd = WEEKDAY_ABBR[day.weekday()]
        row = {"date": day.isoformat(), "weekday": wd, "trips": {}}
        for trip in trips:
            cands = [d for d in drivers
                     if wd in d["weekdays"]
                     and d["seats"] >= n_ride
                     and d["boosters"] >= n_booster]
            if not cands:
                row["trips"][trip] = "UNCOVERED"
                continue
            cands.sort(key=lambda d: (round(balance[d["family"]], 1),
                                      drive_days[d["family"]]))
            best = (round(balance[cands[0]["family"]], 1),
                    drive_days[cands[0]["family"]])
            tied = [d for d in cands
                    if (round(balance[d["family"]], 1),
                        drive_days[d["family"]]) == best]
            pick = tied[rr % len(tied)]
            rr += 1
            fam = pick["family"]
            balance[fam] += n_ride          # credit: seats supplied
            seats_given[fam] += n_ride
            drive_days[fam] += 1
            for k in riders:                 # debt: seats consumed
                balance[k["family"]] -= 1
                seats_taken[k["family"]] += 1
            row["trips"][trip] = pick["name"]
        schedule.append(row)
    return schedule, balance, drive_days, seats_given, seats_taken, n_ride


def audit_table(reg, weeks, balance, drive_days, seats_given, seats_taken, total_trips):
    fams = sorted({k["family"] for k in reg["kids"]})
    kids_by_fam = {f: [k for k in reg["kids"] if k["family"] == f] for f in fams}
    print(f"\nFAIRNESS AUDIT over {weeks} weeks ({total_trips} school days)")
    print(f"{'family':<12} {'drives':>6} {'seats+':>7} {'seats-':>7} "
          f"{'balance':>8} {'tol':>6}  verdict")
    drift = []
    for f in fams:
        tol = max(2.0, BAND * seats_taken[f]) if seats_taken[f] else 2.0
        verdict = "FAIR" if abs(balance[f]) <= tol else "DRIFTING"
        if verdict != "FAIR":
            drift.append(f)
        print(f"{f:<12} {drive_days.get(f,0):>6} {seats_given.get(f,0):>7} "
              f"{int(seats_taken[f]):>7} {balance[f]:>8.1f} {tol:>6.1f}  {verdict}")
    if drift:
        print("Correction: give next uncovered/contestable days to: "
              + ", ".join(f"{f} (balance {balance[f]:+.0f})" for f in drift))
    else:
        print("All families inside the +/-15% band.")


def cost_split(reg, balance, seats_taken, cost_per_km, km_one_way, days_n):
    trips_per_day = len(reg.get("trips", ["AM", "PM"]))
    total_cost = 2 * km_one_way * cost_per_km * trips_per_day * days_n
    per_seat = total_cost / max(sum(seats_taken.values()), 1)
    print(f"\nCOST SPLIT (route {km_one_way} km ow, {cost_per_km:.2f}/km, "
          f"{days_n} days): total {total_cost:.2f}")
    paid = {}
    for f, st in seats_taken.items():
        paid[f] = st * per_seat
    # net: family owes its seat-share; drivers were 'reimbursed' via balance
    flows = []
    for f, b in balance.items():
        flows.append((f, b * per_seat))  # positive = over-contributed
    debtors = sorted([x for x in flows if x[1] < -0.01], key=lambda x: x[1])
    creditors = sorted([x for x in flows if x[1] > 0.01], key=lambda x: -x[1])
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        df, damt = debtors[i]
        cf, camt = creditors[j]
        move = min(-damt, camt)
        print(f"  {df} pays {cf}: {move:8.2f}")
        debtors[i] = (df, damt + move)
        creditors[j] = (cf, camt - move)
        if abs(debtors[i][1]) < 0.01:
            i += 1
        if abs(creditors[j][1]) < 0.01:
            j += 1


def cmd_plan(a):
    reg = load_registry(a.registry)
    (schedule, balance, drive_days, seats_given, seats_taken,
     _) = plan(reg, a.weeks)
    print(f"Carpool: {reg.get('name','(unnamed)')}  weeks={a.weeks}  "
          f"start={reg['start']}")
    print(f"{'date':<12}{'wd':<5}" +
          "".join(f"{t:<12}" for t in reg.get("trips", ["AM", "PM"])))
    uncovered = 0
    for row in schedule:
        cells = []
        for t, who in row["trips"].items():
            cells.append(who)
            if who == "UNCOVERED":
                uncovered += 1
        print(f"{row['date']:<12}{row['weekday']:<5}" +
              "".join(f"{c:<12}" for c in cells))
    audit_table(reg, a.weeks, balance, drive_days, seats_given,
                seats_taken, len(schedule))
    if uncovered:
        print(f"\nWARNING: {uncovered} trip(s) UNCOVERED - widen weekday "
              f"availability or add a driver.")
    if a.cost_per_km:
        cost_split(reg, balance, seats_taken, a.cost_per_km, a.km_one_way,
                   len(schedule))
    return 0 if uncovered == 0 else 2


def cmd_audit(a):
    reg = load_registry(a.registry)
    (_, balance, drive_days, seats_given, seats_taken,
     _) = plan(reg, a.weeks)
    audit_table(reg, a.weeks, balance, drive_days, seats_given,
                seats_taken, a.weeks * 5)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("registry")
    pl.add_argument("--weeks", type=int, default=12)
    pl.add_argument("--cost-per-km", type=float)
    pl.add_argument("--km-one-way", type=float, default=5.0)
    pl.set_defaults(fn=cmd_plan)
    au = sub.add_parser("audit")
    au.add_argument("registry")
    au.add_argument("--weeks", type=int, default=12)
    au.set_defaults(fn=cmd_audit)
    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
