#!/usr/bin/env python3
"""feast.py — backward-schedule a multi-dish meal from serve time.

Subcommands:
  example  write a sample dishes.json
  plan     backward-schedule dishes against oven shelves/burners + serve time

Model: every dish must be READY (cook + rest done) by serve time. A dish's
hold_min is how long it stays good after resting — i.e. how much EARLIER
than serve it may finish. The solver places each dish at the LATEST start
that fits, sliding earlier only within its hold slack.

Stdlib only. Times HH:MM; durations in minutes.
"""
import argparse
import json
import sys
from pathlib import Path


def hms(mins):
    mins = round(mins)
    return "%02d:%02d" % (mins // 60, mins % 60)


def parse_hhmm(s):
    h, m = s.strip().split(":")
    return int(h) * 60 + int(m)


SAMPLE = [
    {"name": "Roast turkey 14lb", "prep_min": 30, "cook_min": 180,
     "rest_min": 45, "equipment": "oven", "temp_f": 350, "hold_min": 30,
     "shelves": 2},
    {"name": "Stuffing casserole", "prep_min": 15, "cook_min": 35,
     "rest_min": 10, "equipment": "oven", "temp_f": 375, "hold_min": 60,
     "shelves": 1},
    {"name": "Popovers", "prep_min": 10, "cook_min": 20, "rest_min": 2,
     "equipment": "oven", "temp_f": 450, "hold_min": 5, "shelves": 1},
    {"name": "Mashed potatoes", "prep_min": 25, "cook_min": 30,
     "rest_min": 0, "equipment": "burner", "hold_min": 30},
    {"name": "Gravy (from drippings)", "prep_min": 5, "cook_min": 15,
     "rest_min": 0, "equipment": "burner", "hold_min": 60},
]


def cmd_example(args):
    Path(args.out).write_text(json.dumps(SAMPLE, indent=2) + "\n")
    print("Wrote %d sample dishes -> %s" % (len(SAMPLE), args.out))
    print("Then: python3 %s plan --serve 19:00 --dishes %s" % (sys.argv[0], args.out))
    return 0


def fits_oven(windows, start, dur, temp, shelves, capacity, eps=25):
    """Can (start, dur, temp, shelves) coexist with existing oven windows?"""
    for (s, e, t, sh, n) in windows:
        if start < e and s < start + dur:  # overlaps an existing window
            if temp is not None and t is not None and abs(temp - t) > eps:
                return False
            if sh + shelves > capacity:
                return False
    return True


def place(dish, serve, oven_windows, burner_windows, shelves, burners):
    """Place one dish as late as possible within [start0-hold, start0].
    Returns placement dict or None."""
    cook = dish["cook_min"]
    rest = dish.get("rest_min", 0)
    hold = dish.get("hold_min", 30)
    prep = dish["prep_min"]
    eq = dish.get("equipment", "counter")
    temp = dish.get("temp_f")
    shl = dish.get("shelves", 1)

    start0 = serve - rest - cook          # finish exactly at serve
    floor = start0 - hold                 # earliest allowed start
    if floor < 0:
        floor = 0

    if eq == "oven":
        s = start0
        while s >= floor:
            if fits_oven(oven_windows, s, cook, temp, shl, shelves):
                oven_windows.append((s, s + cook, temp, shl, dish["name"]))
                return {"start": s, "end": s + cook, "eq": "oven", "temp": temp,
                        "shelves": shl, "rest": rest, "hold": hold, "prep": prep}
            s -= 5
        return None
    if eq == "burner":
        s = start0
        while s >= floor:
            used = sum(1 for (bs, be, _bn) in burner_windows
                       if s < be and bs < s + cook)
            if used < burners:
                burner_windows.append((s, s + cook, dish["name"]))
                return {"start": s, "end": s + cook, "eq": "burner", "temp": None,
                        "shelves": 0, "rest": rest, "hold": hold, "prep": prep}
            s -= 5
        return None
    # counter / no shared equipment
    return {"start": start0, "end": start0 + cook, "eq": "counter", "temp": None,
            "shelves": 0, "rest": rest, "hold": hold, "prep": prep}


def schedule(dishes, serve, shelves, burners, max_passes=8):
    """Retry-priority backward scheduler.

    Pass 1 places dishes longest-cook-first at their latest feasible start.
    Dishes that fail get priority next pass (placed first), which lets them
    claim their ideal slot while longer dishes slide earlier into their own
    hold slack. Returns (plan, warnings, day_ahead).
    """
    day_ahead = [d for d in dishes if d.get("make_ahead")]
    day_of = [d for d in dishes if not d.get("make_ahead")]
    base = sorted(day_of, key=lambda d: -(d["cook_min"] + d.get("rest_min", 0)))

    order = list(base)
    plan = {}
    failed_last = []
    for _p in range(max_passes):
        oven_windows, burner_windows = [], []
        plan, failed = {}, []
        for d in order:
            p = place(d, serve, oven_windows, burner_windows, shelves, burners)
            if p is None:
                failed.append(d)
            else:
                p["prep_start"] = p["start"] - d["prep_min"]
                plan[d["name"]] = p
        if not failed:
            failed_last = []
            break
        # give failures priority next pass, keeping duration order within groups
        failed_sorted = sorted(failed, key=lambda d: -(d["cook_min"] + d.get("rest_min", 0)))
        order = failed_sorted + [d for d in base if d not in failed]
        failed_last = failed

    warnings = []
    if failed_last:
        for d in failed_last:
            warnings.append("INFEASIBLE: '%s' cannot fit by %s — make it ahead, "
                            "raise --shelves, or serve later" % (d["name"], hms(serve)))

    # hold slack consumed (wait time after dish is ready)
    for p in plan.values():
        p["hold_used"] = max(0, serve - (p["end"] + p["rest"]))

    # hands-busy audit: pairwise prep overlap
    preps = sorted((p["prep_start"], p["prep_start"] + p["prep"], n)
                   for n, p in plan.items())
    for i in range(len(preps) - 1):
        s1, e1, n1 = preps[i]
        s2, e2, n2 = preps[i + 1]
        if s2 < e1:
            warnings.append(
                "HANDS CONFLICT: prep '%s' (%s-%s) overlaps '%s' (%s-%s) by %d min "
                "— start '%s' earlier" % (n1, hms(s1), hms(e1), n2, hms(s2), hms(e2),
                                          e1 - s2, n1))
    return plan, warnings, day_ahead


def render(plan, serve, warnings, day_ahead, burners):
    out = ["== TIMELINE =="]
    events = []
    for n, p in plan.items():
        events.append((p["prep_start"], 0, "PREP    %s (%d min, hands-on)" % (n, p["prep"])))
        if p["eq"] == "oven":
            temp = ("%dF" % p["temp"]) if p["temp"] else "any"
            events.append((p["start"], 1, "%-28s -> OVEN @ %-4s (%d shelf)" % (n, temp, p["shelves"])))
        elif p["eq"] == "burner":
            events.append((p["start"], 1, "%-28s -> BURNER" % n))
        else:
            events.append((p["start"], 1, "%-28s -> COUNTER" % n))
        if p["rest"] > 0:
            events.append((p["end"], 2, "%-28s OUT — rest %d min" % (n, p["rest"])))
        else:
            events.append((p["end"], 2, "%-28s done" % n))
        events.append((p["end"] + p["rest"], 3, "%-28s READY (waits %d of %d min hold)"
                      % (n, p["hold_used"], p["hold"])))
    events.append((serve, 4, "SERVE   *** everything to the table ***"))
    events.sort(key=lambda x: (x[0], x[1]))
    for t, _prio, line in events:
        out.append("%s  %s" % (hms(t), line))

    if day_ahead:
        out += ["", "== DAY BEFORE (make-ahead) =="]
        out += ["- %s (cook %d min)" % (d["name"], d["cook_min"]) for d in day_ahead]

    out += ["", "== WARNINGS =="]
    out += ["! " + w for w in warnings] or ["None — resources fit, hands-on work never overlaps."]

    ready = sorted(plan.items(), key=lambda kv: kv[1]["hold_used"], reverse=True)
    if ready and ready[0][1]["hold_used"] > 0:
        n, p = ready[0]
        out.append("Tightest dish: '%s' — waits %d min after resting, %d min of "
                   "hold left. Protect it." % (n, p["hold_used"], p["hold"] - p["hold_used"]))
    return "\n".join(out)


def cmd_plan(args):
    dishes = json.loads(Path(args.dishes).read_text())
    shelves, burners = args.shelves, args.burners
    now = parse_hhmm(args.now) if args.now else None

    if args.serve:
        serve = parse_hhmm(args.serve)
        plan, warnings, day_ahead = schedule(dishes, serve, shelves, burners)
        hard = [w for w in warnings if w.startswith("INFEASIBLE")]
        if now is not None and not hard:
            first_prep = min((p["prep_start"] for p in plan.values()), default=serve)
            if first_prep < now:
                warnings.append("INFEASIBLE from now=%s: first prep needed at %s — "
                                "serve later or make dishes ahead" % (hms(now), hms(first_prep)))
        print("Plan for SERVE = %s   (oven %d shelves, %d burners)\n"
              % (hms(serve), shelves, burners))
        print(render(plan, serve, warnings, day_ahead, burners))
        return 0

    if now is None:
        print("Give --serve HH:MM, or --now HH:MM for earliest-serve search.")
        return 2

    cand, found = now, None
    for _ in range(120):  # up to +10h in 5-min steps
        plan, warnings, _da = schedule(dishes, cand, shelves, burners)
        if not [w for w in warnings if w.startswith("INFEASIBLE")]:
            first_prep = min((p["prep_start"] for p in plan.values()), default=cand)
            if first_prep >= now:
                found = (cand, plan, warnings, _da)
                break
        cand += 5
    if found is None:
        plan, warnings, _da = schedule(dishes, cand, shelves, burners)
        blockers = [w.split("'")[1] for w in warnings if w.startswith("INFEASIBLE")]
        print("No feasible serve within +10h. Blocked by: %s — make it ahead, "
              "drop it, or raise --shelves." % ", ".join(blockers or ["?"]))
        return 1
    serve, plan, warnings, day_ahead = found
    print("Earliest feasible SERVE = %s (from now = %s)\n" % (hms(serve), hms(now)))
    print(render(plan, serve, warnings, day_ahead, burners))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Backward-schedule a multi-dish meal.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ex = sub.add_parser("example", help="write a sample dishes.json")
    ex.add_argument("--out", default="dishes.json")
    ex.set_defaults(func=cmd_example)

    pl = sub.add_parser("plan", help="backward-schedule the meal")
    pl.add_argument("--dishes", required=True)
    pl.add_argument("--serve", help="HH:MM serve time (omit with --now to search)")
    pl.add_argument("--now", help="current HH:MM for feasibility / search")
    pl.add_argument("--shelves", type=int, default=3,
                    help="oven rack slots (a 14lb bird eats ~2)")
    pl.add_argument("--burners", type=int, default=4)
    pl.set_defaults(func=cmd_plan)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
