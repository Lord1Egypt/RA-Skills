#!/usr/bin/env python3
"""Garage door safety audit + spring cycle-life forecaster.

Commands:
  init   --installed YEAR --openings N [--rating CYCLES] [--today DATE]
  audit  (12-point interactive checklist -> saves results)
  log-test --test reverse_2x4|photo_eye|hand_balance --result pass|fail
  status (spring life %, replace-by date, open safety issues)
Registry: garage_door.json next to this script (or --registry PATH).
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DEFAULT_RATING = 10000

CHECKLIST = [
    ("reverse_2x4", "2x4 contact-reverse test: door touches board and reverses within 2s"),
    ("photo_eye", "Photo-eye sweep with broomstick (never a hand): immediate reversal"),
    ("hand_balance", "Opener disengaged: door lifts one-handed, stays at half-open"),
    ("manual_release", "Manual release practiced by each driving adult (door CLOSED)"),
    ("wall_button", "Wall button >= 1.5 m high, in sight of door, out of child reach"),
    ("opener_age", "Opener post-1993 (photo-eyes) and post-1996 (rolling-code remote)"),
    ("keypad_code", "Keypad code is 6-digit random, changed at move-in"),
    ("remote_hygiene", "No remotes stored in cars parked on driveway; vacation lock known"),
    ("rollers_hinges", "Rollers/hinges: no play, no screaming, no visibly worn rollers"),
    ("tracks", "Tracks aligned: no rub marks on door edges, bolts tight"),
    ("lubrication", "Hinges/rollers/spring coils lubed in last 6 months (lithium/silicone)"),
    ("springs_visual", "Springs visually intact: no gaps, kinks, or rust (else PRO NOW)"),
]


def load(registry: Path) -> dict:
    if registry.exists():
        return json.loads(registry.read_text())
    return {}


def save(registry: Path, data: dict) -> None:
    registry.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def parse_date(s: str) -> date:
    return date.fromisoformat(s) if s else date.today()


def cmd_init(args, registry: Path) -> None:
    installed = date(args.installed, 1, 1)
    data = load(registry)
    data.update({
        "installed_year": args.installed,
        "installed_date": installed.isoformat(),
        "openings_per_day": args.openings,
        "spring_rating_cycles": args.rating,
        "tests": data.get("tests", []),
        "audit_runs": data.get("audit_runs", []),
    })
    save(registry, data)
    print(f"Door registered: installed {args.installed}, "
          f"{args.rating:,}-cycle springs, ~{args.openings} openings/day.")
    print(f"Registry: {registry}")


def spring_math(data: dict, today: date) -> dict:
    installed = date.fromisoformat(data["installed_date"])
    years = max((today - installed).days / 365.25, 0.0)
    per_year = data["openings_per_day"] * 365.25
    cycles_used = years * per_year
    rating = data["spring_rating_cycles"]
    remaining = max(rating - cycles_used, 0.0)
    pct = 100.0 * remaining / rating
    life_years = rating / per_year if per_year else 0.0
    replace_by = installed + timedelta(days=life_years * 365.25)
    return {
        "cycles_used": cycles_used, "rating": rating, "remaining": remaining,
        "pct": pct, "replace_by": replace_by, "years_in_service": years,
    }


def verdict_for(m: dict) -> tuple:
    if m["pct"] <= 0:
        return "REPLACE SPRINGS NOW", "Cycle rating exceeded - failure probability high. Replace BOTH springs (they age together). Torsion = pro only."
    if m["pct"] < 10:
        return "REPLACE THIS SEASON", "Under 10% spring life left. Schedule on your terms, not the 7PM crash-and-stuck."
    if m["pct"] < 20:
        return "SCHEDULE REPLACEMENT", "Under 20% left. Book a paired-spring visit; add rollers if original."
    return "OK", "Spring life healthy per cycle model. Keep quarterly reverse tests."


def cmd_audit(args, registry: Path) -> None:
    data = load(registry)
    if "installed_year" not in data:
        sys.exit("Run `init` first (no door registered).")
    print("12-point garage door safety audit. Enter: p=pass f=fail s=skip Enter=skip\n")
    results = {}
    for key, text in CHECKLIST:
        ans = input(f"  [{key}] {text}\n    > ").strip().lower()
        results[key] = {"p": "pass", "f": "fail"}.get(ans, "skip")
    run = {"date": date.today().isoformat(), "results": results}
    data.setdefault("audit_runs", []).append(run)
    data.setdefault("tests", []).extend(
        {"test": k, "result": v, "date": run["date"]} for k, v in results.items()
    )
    save(registry, data)
    fails = [k for k, v in results.items() if v == "fail"]
    print(f"\nAudit saved: {sum(1 for v in results.values() if v=='pass')}/12 pass, "
          f"{len(fails)} fail.")
    if fails:
        print("FAILED items:", ", ".join(fails))
        if "reverse_2x4" in fails or "photo_eye" in fails:
            print("!! Reverse-system failure: door is a crush hazard. Adjust down-force/limit,")
            print("   clean photo-eyes, retest. Pre-1993 opener -> replace opener.")


def cmd_log(args, registry: Path) -> None:
    data = load(registry)
    data.setdefault("tests", []).append(
        {"test": args.test, "result": args.result, "date": date.today().isoformat()}
    )
    save(registry, data)
    print(f"Logged {args.test} = {args.result} on {date.today()}.")
    if args.result == "fail" and args.test in ("reverse_2x4", "photo_eye"):
        print("!! Reverse-system FAIL: treat door as crush hazard until fixed and retested.")


def cmd_status(args, registry: Path) -> None:
    data = load(registry)
    if "installed_year" not in data:
        sys.exit("Run `init` first (no door registered).")
    today = parse_date(args.today)
    m = spring_math(data, today)
    verdict, advice = verdict_for(m)
    print(f"Installed: {data['installed_year']} | Openings/day: {data['openings_per_day']} "
          f"| Rating: {m['rating']:,} cycles")
    print(f"Cycles used: ~{m['cycles_used']:,.0f} ({m['years_in_service']:.1f} yrs) "
          f"-> remaining {m['pct']:.0f}%")
    print(f"Modeled replace-by date: {m['replace_by'].isoformat()}")
    print(f"Verdict: {verdict}\n  {advice}")
    open_fails = {}
    for t in data.get("tests", []):
        if t["result"] == "fail":
            prev = open_fails.get(t["test"])
            if prev is None or t["date"] > prev:
                open_fails[t["test"]] = t["date"]
    if open_fails:
        print("\nOpen safety issues (no passing retest since):")
        for k, d in sorted(open_fails.items(), key=lambda kv: kv[1], reverse=True):
            print(f"  - {k}: FAIL on {d}")
    else:
        print("\nNo open safety issues in test log.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", default=str(Path(__file__).parent / "garage_door.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="register the door")
    p.add_argument("--installed", type=int, required=True, help="install year")
    p, = [p]
    p.add_argument("--openings", type=float, required=True, help="open+close cycles per day")
    p.add_argument("--rating", type=int, default=DEFAULT_RATING, help="spring cycle rating")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("audit", help="12-point interactive checklist")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("log-test", help="log one test result")
    p.add_argument("--test", required=True,
                   choices=["reverse_2x4", "photo_eye", "hand_balance", "manual_release"])
    p.add_argument("--result", required=True, choices=["pass", "fail"])
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("status", help="spring life + open issues")
    p.add_argument("--today", default=None, help="override date YYYY-MM-DD")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args, Path(args.registry))


if __name__ == "__main__":
    main()
