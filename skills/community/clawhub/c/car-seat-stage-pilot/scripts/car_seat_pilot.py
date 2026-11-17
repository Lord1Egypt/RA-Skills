#!/usr/bin/env python3
"""car-seat-stage-pilot: stage engine for child car-seat safety.

Pure-stdlib. Converts a child's birthday (or exact age in months) plus
measurements into: rear-facing verdict, seat-type stage, harness/belt
guidance, next-transition estimate, and lifetime stage timeline.

Usage:
  python3 car_seat_pilot.py --birthday 2024-03-15 --weight-lb 24 --height-in 31
  python3 car_seat_pilot.py --months 9 --weight-lb 20
  python3 car_seat_pilot.py --birthday 2019-06-01 --weight-lb 42 --height-in 41 --forward-only
  python3 car_seat_pilot.py --months 100 --height-in 54 --belt-fit
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys

TODAY = dt.date.today()
AVG_MONTH_DAYS = 30.4375

# ---------------------------------------------------------------- constants

RF_MIN_MONTHS_BEST = 24      # AAP: rear-facing at least to age 2, longer if seat allows
BOOSTER_MIN_MONTHS = 48      # booster typically from ~4 y AND 40 lb
BELT_FIT_MIN_HEIGHT_IN = 57  # 4'9" readiness signal
BACK_SEAT_UNTIL_AGE = 13

# typical convertible seat: (rf_w_max, rf_h_max, ff_w_max, ff_h_max)
SEAT_LIMITS = {
    "typical-convertible": (40, 49, 65, 49),
    "extended-rear-facing": (50, 49, 65, 49),
}

BELT_FIT_STEPS = [
    "Shoulder belt lies across the middle of the chest and shoulder - not on the neck or face.",
    "Lap belt lies low and snug across the top of the thighs - not the stomach.",
    "Child's back and bottom sit flat against the vehicle seat back, no slouching.",
    "Knees bend naturally at the edge of the seat while the back stays against the seat back.",
    "Child can stay seated like this for the WHOLE ride without slouching.",
]


def months_between(d0: dt.date, d1: dt.date) -> int:
    m = (d1.year - d0.year) * 12 + (d1.month - d0.month)
    if d1.day < d0.day:
        m -= 1
    return m


def add_months(birthday: dt.date, months: float) -> dt.date:
    return birthday + dt.timedelta(days=AVG_MONTH_DAYS * months)


# ---------------------------------------------------------------- stage engine

def stage_at(age_months: int, weight_lb=None, height_in=None,
             seat_key="typical-convertible") -> dict:
    """Classify current stage + rules. Returns dict(position, seat, harness, rules, warnings)."""
    w, h = weight_lb, height_in
    rf_w, rf_h, ff_w, ff_h = SEAT_LIMITS[seat_key]
    rules, warns = [], []

    # Stage 1: rear-facing
    if age_months < RF_MIN_MONTHS_BEST or (w is not None and w < 22):
        rules.append("Best practice (AAP/NHTSA): ride REAR-FACING as long as possible - "
                     "at minimum until age 2 OR until the seat's RF limits are maxed out.")
        rules.append("RF harness straps must sit at or BELOW shoulder level.")
        rules.append("Chest clip at armpit level; straps snug (no slack if you pinch them).")
        rules.append("Recline per the seat's level indicator; no added products under the child.")
        if w is not None and w >= rf_w:
            warns.append(f"{w} lb meets/exceeds the {rf_w} lb RF weight limit of a typical "
                         f"convertible - keep RF only in an extended-RF seat (to {SEAT_LIMITS['extended-rear-facing'][0]} lb).")
        if h is not None and h >= rf_h:
            warns.append(f"{h} in meets/exceeds the {rf_h} in RF height cap of a typical seat; "
                         "most manuals also say outgrown RF when head is within 1 in of shell top.")
        return {"position": "rear-facing",
                "seat": "rear-facing infant carrier or convertible installed RF",
                "harness": "5-point harness",
                "rules": rules, "warnings": warns}

    # Stage 2: forward-facing + harness
    if age_months < BOOSTER_MIN_MONTHS or (w is not None and w < 40):
        rules.append("Forward-facing with the 5-point internal harness until at least age 4 AND "
                     "40 lb; harnesses rated to 65-90 lb - max it out before booster.")
        rules.append("FF harness straps must sit at or ABOVE shoulder level.")
        rules.append("Top tether REQUIRED when forward-facing (it anchors the seat's head path).")
        rules.append("Install with seat belt OR lower anchors - not both unless the manual allows; "
                     "check the lower-anchor weight cap (child+seat, often 65 lb).")
        if w is not None and w >= ff_w:
            warns.append(f"{w} lb meets/exceeds the {ff_w} lb harness limit - transition to a "
                         "belt-positioning booster (keep the harness longer via a higher-limit seat if possible).")
        if h is not None and h >= ff_h:
            warns.append(f"{h} in meets/exceeds the {ff_h} in standing-height cap - check the "
                         "manual's shoulder-slot limit for harness use.")
        return {"position": "forward-facing",
                "seat": "convertible or combination seat installed FF",
                "harness": "5-point harness + top tether",
                "rules": rules, "warnings": warns}

    # Stage 3: booster
    rules.append("Booster with lap-AND-shoulder belt only. Never a lap-only belt.")
    rules.append("Stay in the booster until the adult belt passes the 5-step fit test - "
                 f"usually 4'9\" ({BELT_FIT_MIN_HEIGHT_IN} in) AND the maturity to sit properly, typically age 8-12.")
    rules.append("High-back booster first (better belt geometry + head support); backless OK later "
                 "if the vehicle seat has a headrest.")
    if h is not None and h >= BELT_FIT_MIN_HEIGHT_IN:
        rules.append("Height >= 4'9\": run the 5-step belt-fit test now and every 6 months.")
    return {"position": "forward-facing",
            "seat": "belt-positioning booster",
            "harness": "vehicle lap+shoulder belt",
            "rules": rules, "warnings": warns}


# ---------------------------------------------------------------- projections

def _date_for(current, limit, rate_per_month) -> dt.date:
    """Date when `current` reaches `limit` growing at rate/month (clamped: now if already past)."""
    if current is None or current >= limit or rate_per_month <= 0:
        return TODAY
    return TODAY + dt.timedelta(days=AVG_MONTH_DAYS * ((limit - current) / rate_per_month))


def growth_rates(age_months: int) -> tuple[float, float]:
    """(lb/month, in/month) crude growth model by age."""
    if age_months < 12:
        return 1.0, 0.5
    if age_months < 24:
        return 0.5, 0.4
    return 0.25, 0.2


def next_transition(birthday: dt.date, age_months: int, weight_lb, height_in,
                    seat_key="typical-convertible") -> dict | None:
    stage = stage_at(age_months, weight_lb, height_in, seat_key)
    w_rate, h_rate = growth_rates(age_months)
    rf_w, rf_h, ff_w, ff_h = SEAT_LIMITS[seat_key]
    candidates = []  # (date, label, driver)

    if stage["position"] == "rear-facing":
        candidates.append((_date_for(weight_lb, rf_w, w_rate),
                           f"RF weight limit {rf_w} lb reached", "weight"))
        candidates.append((_date_for(height_in, rf_h, h_rate),
                           f"RF height limit {rf_h} in reached", "height"))
        floor = add_months(birthday, RF_MIN_MONTHS_BEST)
        if floor >= TODAY:
            candidates.append((floor,
                               "Age-2 RF floor (turn earlier ONLY if seat limits maxed out first)",
                               "age"))
    elif "harness" in stage["harness"]:
        candidates.append((_date_for(weight_lb, ff_w, w_rate),
                           f"Harness weight limit {ff_w} lb reached", "weight"))
        candidates.append((_date_for(height_in, ff_h, h_rate),
                           f"Harness height limit {ff_h} in reached", "height"))
        win = add_months(birthday, BOOSTER_MIN_MONTHS)
        if win >= TODAY:
            candidates.append((win, "Booster window opens (age ~4 + 40 lb)", "age"))
    else:
        candidates.append((_date_for(height_in, BELT_FIT_MIN_HEIGHT_IN, h_rate),
                           f"4'9\" belt-fit readiness ({BELT_FIT_MIN_HEIGHT_IN} in)", "height"))
        win = add_months(birthday, 96)
        if win >= TODAY:
            candidates.append((win, "Adult-belt window opens - run 5-step belt-fit test", "age"))

    future = [c for c in candidates if c[0] >= TODAY]
    if not future:
        return None
    d, label, driver = min(future, key=lambda c: c[0])
    return {"date": d.isoformat(), "what": label, "driven_by": driver,
            "days_from_now": (d - TODAY).days}


def timeline(birthday: dt.date) -> list[dict]:
    out = []

    def add(mo: float, event: str, detail: str = ""):
        out.append({"date": add_months(birthday, mo).isoformat(),
                    "age_months": int(mo), "event": event, "detail": detail})

    add(12, "Infant-carrier outgrow check",
        "Head within 1 in of shell top -> move to convertible (still rear-facing).")
    add(RF_MIN_MONTHS_BEST, "Rear-facing minimum (best practice)",
        "Age 2 is the FLOOR for turning, not the goal - keep RF to the seat's max limits.")
    add(48, "Forward-facing harness stage (if not already)",
        "FF + 5-point harness + top tether; booster not yet unless limits force it.")
    add(96, "Booster stage (typical)",
        "Belt-positioning booster until the 5-step belt-fit test passes.")
    add(108, "Belt-fit test window",
        "4'9\" + mature sitting = adult belt in the back seat.")
    add(BACK_SEAT_UNTIL_AGE * 12, "Back seat until 13",
        "All children under 13 ride in the back seat.")
    return out


# ---------------------------------------------------------------- verdict + render

def build_verdict(birthday: dt.date | None, months: int, weight_lb, height_in,
                  forward_only=False, belt_fit=False) -> dict:
    notes = []
    if birthday is None:
        birthday = TODAY - dt.timedelta(days=AVG_MONTH_DAYS * months)
    age_months = months_between(birthday, TODAY)
    if age_months < 0:
        age_months = 0
        notes.append("Birthday is in the future - age clamped to 0 months.")
    if forward_only:
        notes.append("--forward-only: RF math skipped; assume FF harness stage or later.")

    stage = stage_at(age_months, weight_lb, height_in)
    if forward_only and stage["position"] == "rear-facing":
        # re-run with age pushed past RF floor
        stage = stage_at(max(age_months, RF_MIN_MONTHS_BEST), weight_lb, height_in)

    rf_required = age_months < RF_MIN_MONTHS_BEST
    rf_now = stage["position"] == "rear-facing"

    v = {
        "birthday": birthday.isoformat(),
        "today": TODAY.isoformat(),
        "age_months": age_months,
        "weight_lb": weight_lb,
        "height_in": height_in,
        "position_now": stage["position"],
        "seat_now": stage["seat"],
        "harness_now": stage["harness"],
        "rear_facing_ok": rf_now,
        "rear_facing_required_by_age": rf_required,
        "rules": stage["rules"],
        "warnings": stage["warnings"],
        "next_transition": next_transition(birthday, age_months, weight_lb, height_in),
        "timeline": timeline(birthday),
        "belt_fit_checklist": BELT_FIT_STEPS if (belt_fit or stage["harness"] == "vehicle lap+shoulder belt") else [],
        "notes": notes,
        "disclaimer": ("Basis: AAP 2018 policy, NHTSA, Safe Kids guidance. Informational use - "
                       "your car-seat manual and state law supersede this tool."),
    }
    return v


def render(v: dict) -> str:
    L = []
    bar = "=" * 64
    L += [bar, "CHILD CAR-SEAT STAGE PILOT - verdict", bar]
    L.append(f"Age: {v['age_months']} months   (birthday {v['birthday']})")
    if v["weight_lb"] is not None:
        L.append(f"Weight: {v['weight_lb']} lb")
    if v["height_in"] is not None:
        L.append(f"Height: {v['height_in']} in")
    L.append("")
    L.append(f"POSITION NOW: {v['position_now'].upper()}")
    L.append(f"SEAT NOW:     {v['seat_now']}")
    L.append(f"HARNESS NOW:  {v['harness_now']}")
    if v["rear_facing_required_by_age"]:
        if v["rear_facing_ok"]:
            L.append("-> OK: child under 2 y is riding rear-facing as recommended.")
        else:
            L.append("!! STOP: child under 2 y is set up forward-facing -")
            L.append("   turn the seat back around unless a seat limit forces the switch.")
    for w in v["warnings"]:
        L.append(f"WARNING: {w}")
    L.append("")
    L.append("TOP RULES:")
    for i, r in enumerate(v["rules"], 1):
        L.append(f"  {i}. {r}")
    nt = v["next_transition"]
    if nt:
        L.append("")
        L.append(f"NEXT TRANSITION: {nt['what']}")
        L.append(f"  on/before {nt['date']} (in {nt['days_from_now']} days) - driven by {nt['driven_by']}")
    if v["belt_fit_checklist"]:
        L.append("")
        L.append("5-STEP BELT-FIT TEST (ALL must pass before leaving the booster):")
        for i, s in enumerate(v["belt_fit_checklist"], 1):
            L.append(f"  [ ] {i}. {s}")
    if v["notes"]:
        L.append("")
        for n in v["notes"]:
            L.append(f"NOTE: {n}")
    L.append("")
    L.append("PROJECTED TIMELINE:")
    for m in v["timeline"]:
        L.append(f"  {m['date']}  age {m['age_months']:>3} mo  {m['event']}")
        if m["detail"]:
            L.append(f"       {m['detail']}")
    L.append("")
    L.append(v["disclaimer"])
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description="Child car-seat stage verdict engine")
    p.add_argument("--birthday", help="YYYY-MM-DD")
    p.add_argument("--months", type=int, help="age in months (if no birthday given)")
    p.add_argument("--weight-lb", type=float)
    p.add_argument("--height-in", type=float)
    p.add_argument("--seat", choices=sorted(SEAT_LIMITS), default="typical-convertible")
    p.add_argument("--forward-only", action="store_true",
                   help="skip RF math (child already FF); harness/booster/belt stages only")
    p.add_argument("--belt-fit", action="store_true", help="always print the 5-step belt-fit test")
    p.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = p.parse_args(argv)

    if not args.birthday and args.months is None:
        p.error("need --birthday YYYY-MM-DD or --months N")

    birthday = dt.date.fromisoformat(args.birthday) if args.birthday else None
    v = build_verdict(birthday, args.months or 0, args.weight_lb, args.height_in,
                      args.forward_only, args.belt_fit)
    if args.json:
        print(json.dumps(v, indent=2))
    else:
        print(render(v))


if __name__ == "__main__":
    main(sys.argv[1:])
