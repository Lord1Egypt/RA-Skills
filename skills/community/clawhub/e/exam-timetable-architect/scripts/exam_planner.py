#!/usr/bin/env python3
"""Exam Timetable Architect — priority-ranked, spaced, load-capped study plans.

Schedules topics backwards from exam dates with expanding-interval reviews
(+1/+3/+7/+14 days, clamped pre-exam), caps days at declared available hours,
runs honest feasibility math, and re-plans from today when life happens.

Commands: init, exam, topic, plan, today, done, progress, replan, drop.
Stdlib only. Store: exam_plan.json (override with --store).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "exam_plan.json"
REVIEW_LADDER = [1, 3, 7, 14]      # days after first study
REVIEW_COST = 0.25                 # fraction of first-study hours
UNIT_MINUTES = 60                  # 50 study + 10 break = 1h wall clock


def load(store: Path) -> dict:
    if not store.exists():
        sys.exit(f"No plan at {store}. Run `init` first.")
    return json.loads(store.read_text())


def save(store: Path, d: dict) -> None:
    store.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def d(s: str) -> date:
    return datetime.fromisoformat(s).date()


def today() -> date:
    return date.today()


# ------------------------------------------------------------------ setup
def cmd_init(args) -> None:
    if args.store.exists() and not args.force:
        sys.exit(f"{args.store} exists (use --force to reset).")
    data = {
        "start": args.start or today().isoformat(),
        "daily_hours": args.hours,
        "created": today().isoformat(),
        "exams": {},       # name -> {date, weight}
        "topics": [],      # {id, exam, name, difficulty, weakness, hours, pin, dropped, first_done, reviews_done}
        "schedule": [],    # {id, date, kind: study|review, topic_id, hours, done}
        "next_topic": 1,
    }
    save(args.store, data)
    print(f"Plan starts {data['start']}, {args.hours}h/day available.")


def cmd_exam(args) -> None:
    data = load(args.store)
    if args.add:
        name, _, dstr = args.add.rpartition("=")
        data["exams"][name.strip()] = {"date": dstr, "weight": args.weight}
        save(args.store, data)
        days = (d(dstr) - today()).days
        print(f'Exam "{name.strip()}" on {dstr} (weight {args.weight}) — {days} days away.')
    elif args.list:
        for name, e in sorted(data["exams"].items(), key=lambda kv: kv[1]["date"]):
            print(f"  {e['date']}  w={e['weight']:<3}  {name}")


def cmd_topic(args) -> None:
    data = load(args.store)
    if args.add:
        # format: "exam|name" with flags
        name = args.add
        exam = args.exam
        if exam not in data["exams"]:
            sys.exit(f'Unknown exam "{exam}". Add it first with `exam add`.')
        tid = data["next_topic"]
        data["next_topic"] += 1
        data["topics"].append({
            "id": tid, "exam": exam, "name": name,
            "difficulty": args.difficulty, "weakness": args.weakness,
            "hours": args.hours_, "pin": args.pin, "dropped": False,
            "first_done": None, "reviews_done": [],
        })
        save(args.store, data)
        pri = priority(data, data["topics"][-1])
        print(f"Topic t{tid}: {name} ({exam}) — priority {pri:.1f}")
    elif args.list:
        ts = sorted((t for t in data["topics"] if not t["dropped"]),
                    key=lambda t: -priority(data, t))
        for t in ts:
            status = "✅" if t["first_done"] else "  "
            print(f"  {status} t{t['id']:<3} pri={priority(data, t):5.1f} "
                  f"{t['hours']}h  {t['exam'][:12]:<12} {t['name']}")


def priority(data: dict, t: dict) -> float:
    e = data["exams"][t["exam"]]
    days_to = (d(e["date"]) - today()).days
    proximity = 1 + 3 * max(0, 28 - days_to) / 28
    w = e["weight"] / 50.0  # 50 = typical full weight
    return round(w * proximity * t["weakness"] * t["difficulty"], 1)


# ------------------------------------------------------------------ planner
def required_hours(data: dict) -> float:
    req = 0.0
    for t in data["topics"]:
        if t["dropped"] or t["first_done"]:
            continue
        exam = d(data["exams"][t["exam"]]["date"])
        days_avail = max(1, (exam - today()).days)
        n_rev = sum(1 for g in REVIEW_LADDER if g <= days_avail - 1)
        req += t["hours"] * (1 + n_rev * REVIEW_COST)
    # reviews still owed for studied topics
    for t in data["topics"]:
        if t["dropped"] or not t["first_done"]:
            continue
        exam = d(data["exams"][t["exam"]]["date"])
        days_avail = max(0, (exam - today()).days)
        owed = sum(1 for g in REVIEW_LADDER
                   if g not in [int(x) for x in t["reviews_done"]]
                   and (d(t["first_done"]) + timedelta(days=g)) <= exam
                   and (d(t["first_done"]) + timedelta(days=g)) >= today())
        req += t["hours"] * REVIEW_COST * owed
    return req


def available_hours(data: dict) -> float:
    last_exam = max(d(e["date"]) for e in data["exams"].values()) if data["exams"] else today()
    days = max(0, (last_exam - today()).days + 1)
    return days * data["daily_hours"]


def cmd_plan(args) -> None:
    data = load(args.store)
    if not data["exams"]:
        sys.exit("Add exams first (`exam add \"Name=YYYY-MM-DD\"`).")

    req, avail = required_hours(data), available_hours(data)
    print(f"Feasibility: need {req:.1f}h, have {avail:.1f}h "
          f"({data['daily_hours']}h/day × days to last exam)")
    if req > avail:
        print(f"⚠ OVER CAPACITY by {req-avail:.1f}h — suggested cuts, in order:")
        low = sorted((t for t in data["topics"] if not t["dropped"]),
                     key=lambda t: priority(data, t))
        for t in low[:5]:
            print(f"  - drop t{t['id']} \"{t['name']}\" "
                  f"(pri {priority(data, t)}, saves {t['hours']*(1+len(REVIEW_LADDER)*REVIEW_COST):.1f}h)")
        print("  - or: `plan --no-14` to drop the +14d review tier")
        print("  - or: raise --hours at init (unsustainable above 6h/day)")
        if not args.force:
            return

    data["schedule"] = [b for b in data["schedule"] if b["done"]]  # keep history
    days_load: dict[str, float] = {}
    for b in data["schedule"]:
        if b["date"] >= today().isoformat():
            days_load[b["date"]] = days_load.get(b["date"], 0) + b["hours"]

    def place(tid: int, tname: str, exam_name: str, kind: str, hours: float,
              not_before: date, deadline: date, suffix: str) -> dict | None:
        """Earliest day >= not_before with capacity; compress to eve if full."""
        cur = max(not_before, today())
        while cur < deadline:
            if days_load.get(cur.isoformat(), 0) + hours <= data["daily_hours"]:
                break
            cur += timedelta(days=1)
        else:
            cur = deadline  # compress to exam eve
        blk = {"id": f"t{tid}-{suffix}", "date": cur.isoformat(), "kind": kind,
               "topic": tid, "topic_name": tname, "exam": exam_name,
               "hours": hours, "done": False}
        days_load[cur.isoformat()] = days_load.get(cur.isoformat(), 0) + hours
        return blk

    placed = []
    # Phase 1: first-study blocks in priority order (pins first).
    # Topics taller than a day's capacity are chunked across consecutive days.
    active = [t for t in data["topics"] if not t["dropped"] and not t["first_done"]]
    active.sort(key=lambda t: (0 if t["pin"] else 1, -priority(data, t)))
    study_dates: dict[int, date] = {}
    seq = 0

    def place_chunked(t: dict, kind: str, hours: float, not_before: date,
                      deadline: date) -> date | None:
        """Place hours possibly split across days; returns last (completion) date."""
        nonlocal seq
        remaining, cur_min, last = hours, not_before, None
        while remaining > 1e-9:
            chunk = round(min(remaining, data["daily_hours"]), 2)
            blk = place(t["id"], t["name"], t["exam"], kind, chunk,
                        cur_min, deadline, f"{'s' if kind == 'study' else 'r'}{seq}")
            seq += 1
            if not blk:
                break
            placed.append(blk)
            last = d(blk["date"])
            cur_min = last + timedelta(days=1)
            remaining = round(remaining - chunk, 2)
        return last

    for t in active:
        exam = d(data["exams"][t["exam"]]["date"])
        last = place_chunked(t, "study", t["hours"], today(), exam)
        if last:
            study_dates[t["id"]] = last
    # Phase 2: reviews, spaced from each study block's ACTUAL completion date.
    ladder = REVIEW_LADDER if not args.no_14 else REVIEW_LADDER[:-1]
    for t in data["topics"]:
        if t["dropped"]:
            continue
        exam = d(data["exams"][t["exam"]]["date"])
        first = d(t["first_done"]) if t["first_done"] else study_dates.get(t["id"])
        if first is None:
            continue  # study couldn't be placed at all
        done_g = [int(x) for x in t["reviews_done"]]
        for g in ladder:
            if g in done_g:
                continue
            target = first + timedelta(days=g)
            if target > exam or target < today():
                continue
            place_chunked(t, "review", round(t["hours"] * REVIEW_COST, 2),
                          target, exam)
    data["schedule"] = [b for b in data["schedule"] if b["done"]] + placed
    save(args.store, data)
    # print day map
    by_day: dict[str, list] = {}
    for b in data["schedule"]:
        if not b["done"]:
            by_day.setdefault(b["date"], []).append(b)
    for day in sorted(by_day):
        hrs = sum(b["hours"] for b in by_day[day])
        print(f"\n{day} ({d(day).strftime('%a')}) — {hrs:.1f}h")
        for b in sorted(by_day[day], key=lambda x: -x["hours"]):
            mark = "🔁" if b["kind"] == "review" else "📖"
            print(f"   {mark} [{b['id']}] {b['hours']:.1f}h {b['topic_name'][:52]}")


def cmd_today(args) -> None:
    data = load(args.store)
    blocks = [b for b in data["schedule"]
              if not b["done"] and d(b["date"]) <= today()]
    if not blocks:
        print("Nothing scheduled today (or overdue). Run `plan` if you haven't.")
        return
    blocks.sort(key=lambda b: (b["kind"] != "review", -b["hours"]))  # reviews first
    print(f"Today ({today().isoformat()}) — {sum(b['hours'] for b in blocks):.1f}h")
    for i, b in enumerate(blocks, 1):
        mark = "🔁" if b["kind"] == "review" else "📖"
        print(f"  {i}. {mark} [{b['id']}] {b['hours']:.1f}h {b['topic_name']}")
        if b["kind"] == "review":
            print(f"      recall first (closed book), then check notes")
    print("\nUnits: 50min study + 10min break. Long break after 3 units.")


def cmd_done(args) -> None:
    data = load(args.store)
    b = next((b for b in data["schedule"] if b["id"] == args.block_id), None)
    if not b:
        sys.exit(f"No block '{args.block_id}'. See `today` / `plan`.")
    b["done"] = True
    t = next(t for t in data["topics"] if t["id"] == b["topic"])
    if b["kind"] == "study":
        t["first_done"] = b["date"]
    else:
        # record which ladder rung this review satisfied (nearest gap)
        gaps = [((d(b["date"]) - d(t["first_done"])).days, g) for g in REVIEW_LADDER]
        nearest = min(gaps, key=lambda x: abs(x[0] - x[1]))[1]
        t["reviews_done"].append(nearest)
    save(args.store, data)
    print(f"✅ [{b['id']}] {b['topic_name']} — done.")


def cmd_progress(args) -> None:
    data = load(args.store)
    active = [t for t in data["topics"] if not t["dropped"]]
    studied = [t for t in active if t["first_done"]]
    cov = len(studied) / len(active) * 100 if active else 0
    total_rev = sum(sum(1 for g in REVIEW_LADDER
                        if (d(t["first_done"]) + timedelta(days=g)) <= d(data["exams"][t["exam"]]["date"]))
                    for t in studied)
    done_rev = sum(len(t["reviews_done"]) for t in studied)
    reinf = done_rev / total_rev * 100 if total_rev else 0
    hours_done = sum(b["hours"] for b in data["schedule"] if b["done"])
    hours_left = sum(b["hours"] for b in data["schedule"] if not b["done"])
    print(f"Coverage:       {cov:5.1f}%  ({len(studied)}/{len(active)} topics first-studied)")
    print(f"Reinforcement:  {reinf:5.1f}%  ({done_rev}/{total_rev} scheduled reviews done)")
    print(f"Hours: done {hours_done:.1f} · remaining {hours_left:.1f}")
    overdue = [b for b in data["schedule"] if not b["done"] and d(b["date"]) < today()]
    if overdue:
        print(f"⚠ {len(overdue)} overdue blocks — run `replan` to re-space from today.")


def cmd_replan(args) -> None:
    data = load(args.store)
    dropped_future = [b for b in data["schedule"] if not b["done"]]
    data["schedule"] = [b for b in data["schedule"] if b["done"]]
    save(args.store, data)
    print(f"Dropped {len(dropped_future)} future blocks; rebuilding from today.")
    cmd_plan(args)


def cmd_drop(args) -> None:
    data = load(args.store)
    t = next((t for t in data["topics"] if t["id"] == args.topic_id), None)
    if not t:
        sys.exit(f"No topic t{args.topic_id}")
    t["dropped"] = True
    data["schedule"] = [b for b in data["schedule"]
                        if b["done"] or b["topic"] != t["id"]]
    save(args.store, data)
    print(f"Dropped \"{t['name']}\" and its future blocks.")


# ------------------------------------------------------------------ cli
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", default=str(DEFAULT_STORE))
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init")
    sp.add_argument("--hours", type=float, required=True, help="daily study hours")
    sp.add_argument("--start", default=None)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(fn=cmd_init)

    sp = sub.add_parser("exam")
    sp.add_argument("--add", metavar='"Name=YYYY-MM-DD"')
    sp.add_argument("--weight", type=float, default=50)
    sp.add_argument("--list", action="store_true")
    sp.set_defaults(fn=cmd_exam)

    sp = sub.add_parser("topic")
    sp.add_argument("--add", metavar="NAME")
    sp.add_argument("--exam", default=None)
    sp.add_argument("--difficulty", type=int, default=3, choices=range(1, 6))
    sp.add_argument("--weakness", type=int, default=3, choices=range(1, 6))
    sp.add_argument("--hours", dest="hours_", type=float, default=2.0)
    sp.add_argument("--pin", action="store_true")
    sp.add_argument("--list", action="store_true")
    sp.set_defaults(fn=cmd_topic)

    sp = sub.add_parser("plan")
    sp.add_argument("--no-14", action="store_true", help="drop +14d review tier")
    sp.add_argument("--force", action="store_true", help="build even if over capacity")
    sp.set_defaults(fn=cmd_plan)

    sp = sub.add_parser("today")
    sp.set_defaults(fn=cmd_today)
    sp = sub.add_parser("done")
    sp.add_argument("block_id")
    sp.set_defaults(fn=cmd_done)
    sp = sub.add_parser("progress")
    sp.set_defaults(fn=cmd_progress)
    sp = sub.add_parser("replan")
    sp.add_argument("--no-14", action="store_true")
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(fn=cmd_replan)
    sp = sub.add_parser("drop")
    sp.add_argument("topic_id", type=int)
    sp.set_defaults(fn=cmd_drop)

    args = p.parse_args()
    args.store = Path(args.store)
    args.fn(args)


if __name__ == "__main__":
    main()
