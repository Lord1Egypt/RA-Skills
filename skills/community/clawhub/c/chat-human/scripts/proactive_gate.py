#!/usr/bin/env python3
"""
Runtime-agnostic probabilistic & silence-decay gate for proactive IM outreach.

Designed for scheduled task or heartbeat hooks:
- Reads optional JSON metadata (`{"jobId","cron","coalescedCount"}`) from stdin when piped.
- Exit code 0: Wake admitted! Emits state metadata only (`<proactive_tick ... />` or JSON)
  with ZERO canned message templates so the agent composes from live context.
- Exit code 3: Quiet hours active; silently skip without waking the model.
- Exit code 4: Cooldown, daily cap, or probability roll missed; silently skip.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import random
import sys
from typing import Any, Dict, Sequence, Tuple

DEFAULT_MIN_COOLDOWN_SECONDS = 45 * 60
DEFAULT_DAILY_MAX = 6
DEFAULT_BASE_PROB_15M = 0.22
DEFAULT_BASE_PROB_30M = 0.38


def default_state_path() -> pathlib.Path:
    return pathlib.Path(".tmp") / "proactive_gate_state.json"


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_quiet_hours(spec: str) -> Tuple[int, int]:
    """Parse `HH:MM-HH:MM` into (start_minutes, end_minutes)."""
    parts = spec.strip().split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid quiet-hours format {spec!r}; expected HH:MM-HH:MM")
    start_h, start_m = (int(x) for x in parts[0].split(":"))
    end_h, end_m = (int(x) for x in parts[1].split(":"))
    return start_h * 60 + start_m, end_h * 60 + end_m


def in_quiet_window(now: dt.datetime, window: Tuple[int, int]) -> bool:
    start_min, end_min = window
    cur = now.hour * 60 + now.minute
    if start_min <= end_min:
        return start_min <= cur < end_min
    return cur >= start_min or cur < end_min


def read_cron_stdin() -> Dict[str, Any]:
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return {}
        raw = sys.stdin.read()
        if not raw or not raw.strip():
            return {}
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def load_state(path: pathlib.Path) -> Dict[str, Any]:
    empty = {
        "last_triggered_ts": 0.0,
        "last_user_reply_ts": 0.0,
        "unanswered_streak": 0,
        "daily_date": "",
        "daily_count": 0,
        "history": [],
    }
    if not path.exists():
        return empty
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else empty
    except Exception:
        return empty


def save_state(path: pathlib.Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_time_bucket(now: dt.datetime) -> str:
    h = now.hour
    if 6 <= h < 12:
        return "morning"
    if 12 <= h < 17:
        return "afternoon"
    if 17 <= h < 21:
        return "evening"
    return "late_night"


def compute_dynamic_probability(
    base_prob: float,
    seconds_since_last_trigger: float,
    unanswered_streak: int,
    coalesced_count: int = 1,
) -> float:
    """
    Hybrid outreach probability:
    - Rises gently after 1.5+ hours of silence so outreach feels organic rather than metronomic.
    - Decays sharply when consecutive proactive messages go unanswered (silence decay).
    """
    prob = base_prob
    hours_since = seconds_since_last_trigger / 3600.0 if seconds_since_last_trigger > 0 else 2.0
    if hours_since > 1.5:
        prob = min(0.65, base_prob * (1.0 + 0.20 * min(hours_since - 1.5, 4.0)))
    if coalesced_count > 1:
        prob = min(0.70, prob * (1.0 + 0.08 * min(coalesced_count - 1, 3)))

    if unanswered_streak >= 3:
        prob *= 0.15
    elif unanswered_streak == 2:
        prob *= 0.45
    elif unanswered_streak == 1:
        prob *= 0.80

    return max(0.02, min(0.85, prob))


def cmd_check(args: argparse.Namespace) -> int:
    stdin_payload = {} if args.no_stdin else read_cron_stdin()
    coalesced_count = int(stdin_payload.get("coalescedCount") or 1)
    job_id = str(stdin_payload.get("jobId") or "")

    now = now_local()
    now_ts = now.timestamp()
    today_str = now.strftime("%Y-%m-%d")
    quiet_window = parse_quiet_hours(args.quiet_hours)

    state = load_state(args.state_file)
    if state.get("daily_date") != today_str:
        state["daily_date"] = today_str
        state["daily_count"] = 0

    if not args.ignore_quiet and in_quiet_window(now, quiet_window):
        print(
            json.dumps({"ok": False, "reason": "quiet_hours", "local_time": now.strftime("%H:%M"), "job_id": job_id}),
            file=sys.stderr,
        )
        return 3

    daily_count = int(state.get("daily_count", 0))
    if daily_count >= args.daily_max and not args.force:
        print(
            json.dumps({"ok": False, "reason": "daily_cap_reached", "daily_count": daily_count, "daily_max": args.daily_max}),
            file=sys.stderr,
        )
        return 4

    last_ts = float(state.get("last_triggered_ts", 0.0))
    elapsed = now_ts - last_ts if last_ts > 0 else float("inf")
    if elapsed < args.min_cooldown and not args.force:
        print(
            json.dumps({"ok": False, "reason": "cooldown", "elapsed_seconds": round(elapsed, 1), "min_cooldown": args.min_cooldown}),
            file=sys.stderr,
        )
        return 4

    base_prob = args.prob if args.prob is not None else (DEFAULT_BASE_PROB_15M if args.interval <= 15 else DEFAULT_BASE_PROB_30M)
    unanswered = int(state.get("unanswered_streak", 0))
    eff_prob = 1.0 if args.force else compute_dynamic_probability(base_prob, elapsed, unanswered, coalesced_count)

    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    roll = rng.random()

    if roll >= eff_prob:
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "probability_miss",
                    "roll": round(roll, 4),
                    "effective_prob": round(eff_prob, 4),
                    "unanswered_streak": unanswered,
                }
            ),
            file=sys.stderr,
        )
        return 4

    bucket = get_time_bucket(now)
    next_daily = daily_count + 1

    if not args.dry_run:
        state["last_triggered_ts"] = now_ts
        state["daily_count"] = next_daily
        state["unanswered_streak"] = unanswered + 1
        history = list(state.get("history", []))
        history.append(
            {
                "iso": now.isoformat(timespec="seconds"),
                "job_id": job_id,
                "coalesced_count": coalesced_count,
                "bucket": bucket,
                "roll": round(roll, 4),
                "effective_prob": round(eff_prob, 4),
            }
        )
        state["history"] = history[-20:]
        save_state(args.state_file, state)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "ok": True,
                    "time": now.strftime("%H:%M"),
                    "bucket": bucket,
                    "unanswered_streak": unanswered,
                    "coalesced": coalesced_count,
                    "daily": f"{next_daily}/{args.daily_max}",
                    "roll": round(roll, 4),
                    "effective_prob": round(eff_prob, 4),
                },
                ensure_ascii=False,
            )
        )
    else:
        print(
            f'<proactive_tick time="{now.strftime("%H:%M")}" bucket="{bucket}" '
            f'unanswered_streak="{unanswered}" coalesced="{coalesced_count}" '
            f'daily="{next_daily}/{args.daily_max}" roll="{roll:.2f}/{eff_prob:.2f}" />'
        )
    return 0


def cmd_ack_user(args: argparse.Namespace) -> int:
    state = load_state(args.state_file)
    state["last_user_reply_ts"] = now_local().timestamp()
    state["unanswered_streak"] = 0
    save_state(args.state_file, state)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = load_state(args.state_file)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Probabilistic & silence-decay gate for proactive IM wakes.")
    parser.add_argument("--state-file", type=pathlib.Path, default=default_state_path(), help="Path to JSON state file")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Evaluate gate for the current scheduler tick")
    p_check.add_argument("--interval", type=int, default=15, help="Scheduler interval in minutes (default: 15)")
    p_check.add_argument("--prob", type=float, default=None, help="Explicit base probability (0..1)")
    p_check.add_argument("--min-cooldown", type=int, default=DEFAULT_MIN_COOLDOWN_SECONDS, help="Minimum seconds between triggers")
    p_check.add_argument("--daily-max", type=int, default=DEFAULT_DAILY_MAX, help="Maximum triggers per local day")
    p_check.add_argument("--quiet-hours", type=str, default="01:30-10:00", help="Local quiet window HH:MM-HH:MM")
    p_check.add_argument("--ignore-quiet", action="store_true", help="Bypass quiet-hours check")
    p_check.add_argument("--force", action="store_true", help="Force trigger regardless of probability/cooldown")
    p_check.add_argument("--dry-run", action="store_true", help="Evaluate without mutating state file")
    p_check.add_argument("--no-stdin", action="store_true", help="Ignore piped stdin")
    p_check.add_argument("--seed", type=int, default=None, help="Deterministic RNG seed for testing")
    p_check.add_argument("--format", choices=("xml", "json"), default="xml", help="Output tick format")
    p_check.set_defaults(func=cmd_check)

    p_ack = sub.add_parser("ack-user", help="Reset unanswered streak when user replies")
    p_ack.set_defaults(func=cmd_ack_user)

    p_status = sub.add_parser("status", help="Print current JSON state")
    p_status.set_defaults(func=cmd_status)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
