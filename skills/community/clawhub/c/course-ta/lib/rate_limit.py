#!/usr/bin/env python3
"""
rate_limit.py — Per-user rate limit checker/updater for course-ta skill.

Usage:
    python3 rate_limit.py check <userId> [--state <path>] [--max-hour N] [--max-day N] [--config <path>]
    python3 rate_limit.py record <userId> [--state <path>]

Privileged users defined in course-ta.json under "privileged_users" get their
own max_hour and max_day limits, overriding the defaults.

Exit codes:
    0 = allowed
    1 = rate limited (prints reason to stdout as JSON)
    2 = error

Stdout (JSON):
    {"allowed": true/false, "reason": "...", "count_hour": N, "count_day": N}
"""

import json
import sys
import time
import os
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import RATE_LIMIT_STATE, COURSE_TA_CONFIG

DEFAULT_STATE = RATE_LIMIT_STATE
DEFAULT_CONFIG = COURSE_TA_CONFIG
DEFAULT_MAX_HOUR = 20
DEFAULT_MAX_DAY = 60


def get_user_limits(user_id: str, config_path: Path, default_max_hour: int, default_max_day: int):
    """Return (max_hour, max_day) for a user, respecting privileged_users in config."""
    try:
        config = json.loads(config_path.read_text())
        privileged = config.get("privileged_users", {})
        if user_id in privileged:
            entry = privileged[user_id]
            return entry.get("max_hour", default_max_hour), entry.get("max_day", default_max_day)
    except Exception:
        pass
    return default_max_hour, default_max_day

def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}
    return {}

def save_state(path: Path, state: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))

def clean_old(timestamps: list, now: float) -> list:
    """Keep only last 24h of timestamps."""
    cutoff = now - 86400
    return [t for t in timestamps if t > cutoff]

def count_in_window(timestamps: list, now: float, window: int) -> int:
    cutoff = now - window
    return sum(1 for t in timestamps if t > cutoff)

def check(user_id: str, state_path: Path, max_hour: int, max_day: int, config_path: Path = DEFAULT_CONFIG):
    # Check privileged_users for custom limits
    max_hour, max_day = get_user_limits(user_id, config_path, max_hour, max_day)

    state = load_state(state_path)
    now = time.time()
    user_data = state.get(user_id, {"messages": []})
    msgs = clean_old(user_data.get("messages", []), now)

    count_hour = count_in_window(msgs, now, 3600)
    count_day  = count_in_window(msgs, now, 86400)

    if count_hour >= max_hour:
        result = {
            "allowed": False,
            "reason": f"hourly limit ({max_hour} messages/hour)",
            "count_hour": count_hour,
            "count_day": count_day
        }
    elif count_day >= max_day:
        result = {
            "allowed": False,
            "reason": f"daily limit ({max_day} messages/day)",
            "count_hour": count_hour,
            "count_day": count_day
        }
    else:
        result = {
            "allowed": True,
            "reason": "ok",
            "count_hour": count_hour,
            "count_day": count_day
        }

    print(json.dumps(result))
    sys.exit(0 if result["allowed"] else 1)

def record(user_id: str, state_path: Path):
    state = load_state(state_path)
    now = time.time()
    user_data = state.get(user_id, {"messages": []})
    msgs = clean_old(user_data.get("messages", []), now)
    msgs.append(now)
    state[user_id] = {"messages": msgs}
    save_state(state_path, state)
    print(json.dumps({"recorded": True, "count_hour": count_in_window(msgs, now, 3600)}))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["check", "record"])
    parser.add_argument("user_id")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--max-hour", type=int, default=DEFAULT_MAX_HOUR)
    parser.add_argument("--max-day", type=int, default=DEFAULT_MAX_DAY)
    args = parser.parse_args()

    if args.action == "check":
        check(args.user_id, args.state, args.max_hour, args.max_day, args.config)
    elif args.action == "record":
        record(args.user_id, args.state)

if __name__ == "__main__":
    main()
