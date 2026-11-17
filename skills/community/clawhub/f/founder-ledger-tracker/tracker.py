#!/usr/bin/env python3
"""founder-ledger-tracker: a dependency-free goal + budget-guard reminder tool.

Tracks a numeric goal (e.g. "first $1 revenue") and an optional date-based
deadline plus daily spend cap in a single local JSON state file. No network
access, no secrets, no daemon or cron logic: every invocation is one
deterministic command that the calling agent decides when to run.
"""
import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

DEFAULT_STATE = ".founder-ledger-tracker.json"
SOFT_CAP_RATIO = 0.8
SOFT_DEADLINE_DAYS = 3


def _load_state(path):
    p = Path(path)
    if not p.exists():
        print(f"error: state file not found: {path}", file=sys.stderr)
        sys.exit(2)
    return json.loads(p.read_text())


def _save_state(path, state):
    Path(path).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def _parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def cmd_init(args):
    p = Path(args.state)
    if p.exists() and not args.force:
        print(
            f"error: state file already exists: {args.state} (use --force to overwrite)",
            file=sys.stderr,
        )
        return 1
    state = {
        "goal_name": args.goal_name,
        "goal_target": args.goal_target,
        "goal_current": args.goal_current,
        "deadline": args.deadline,
        "daily_cap": args.daily_cap,
        "spent_today": args.spent_today,
    }
    _save_state(args.state, state)
    print(f"initialized {args.state}")
    return 0


def _evaluate(state, today):
    """Return (exit_code, reasons) — exit_code is the worst of goal/budget checks."""
    code = 0
    reasons = []

    deadline = state.get("deadline")
    if deadline:
        d = _parse_date(deadline)
        days_left = (d - today).days
        if days_left < 0:
            code = max(code, 2)
            reasons.append(f"deadline {deadline} has passed ({-days_left}d ago)")
        elif days_left <= SOFT_DEADLINE_DAYS:
            code = max(code, 1)
            reasons.append(f"deadline {deadline} in {days_left}d")

    daily_cap = state.get("daily_cap")
    spent = state.get("spent_today")
    if daily_cap is not None and spent is not None:
        if spent >= daily_cap:
            code = max(code, 2)
            reasons.append(f"spend {spent} hit cap {daily_cap}")
        elif spent >= SOFT_CAP_RATIO * daily_cap:
            code = max(code, 1)
            reasons.append(f"spend {spent} at {spent / daily_cap:.0%} of cap {daily_cap}")

    goal_target = state.get("goal_target")
    goal_current = state.get("goal_current")
    goal_name = state.get("goal_name")
    if goal_target is not None and goal_current is not None and goal_current >= goal_target:
        reasons.append(f"goal '{goal_name}' reached: {goal_current}/{goal_target}")

    return code, reasons


def _reminder_text(state, code, reasons):
    goal_name = state.get("goal_name", "goal")
    if not reasons:
        return f"{goal_name}: on track, no triggers."
    prefix = {0: "info", 1: "reminder", 2: "alert"}[code]
    return f"[{prefix}] {goal_name}: " + "; ".join(reasons)


def cmd_check(args):
    state = _load_state(args.state)
    if args.spent is not None:
        state["spent_today"] = args.spent
        _save_state(args.state, state)
    if args.goal_current is not None:
        state["goal_current"] = args.goal_current
        _save_state(args.state, state)
    today = _parse_date(args.today) if args.today else date.today()
    code, reasons = _evaluate(state, today)
    print(_reminder_text(state, code, reasons))
    return code


def cmd_reminder_text(args):
    state = _load_state(args.state)
    today = _parse_date(args.today) if args.today else date.today()
    code, reasons = _evaluate(state, today)
    print(_reminder_text(state, code, reasons))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tracker.py",
        description="Goal + budget-guard reminders. No network, no secrets, no daemon.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create a new local state file")
    p_init.add_argument("--state", default=DEFAULT_STATE)
    p_init.add_argument("--goal-name", required=True)
    p_init.add_argument("--goal-target", type=float, required=True)
    p_init.add_argument("--goal-current", type=float, default=0.0)
    p_init.add_argument("--deadline", default=None, help="YYYY-MM-DD")
    p_init.add_argument("--daily-cap", type=float, default=None)
    p_init.add_argument("--spent-today", type=float, default=0.0)
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_check = sub.add_parser("check", help="evaluate triggers; exit 0/1/2")
    p_check.add_argument("--state", default=DEFAULT_STATE)
    p_check.add_argument("--spent", type=float, default=None, help="update spent_today before checking")
    p_check.add_argument(
        "--goal-current", type=float, default=None, help="update goal_current before checking"
    )
    p_check.add_argument("--today", default=None, help="YYYY-MM-DD override, for testing")
    p_check.set_defaults(func=cmd_check)

    p_rt = sub.add_parser(
        "reminder-text", help="print the one-line reminder without mutating state; always exits 0"
    )
    p_rt.add_argument("--state", default=DEFAULT_STATE)
    p_rt.add_argument("--today", default=None)
    p_rt.set_defaults(func=cmd_reminder_text)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
