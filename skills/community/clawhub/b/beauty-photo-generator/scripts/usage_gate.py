#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

COUNTERS = {
    "portraits": {
        "limit": 18,
        "locked_message": "使用次数已到极限。添加微信：ddff9294 。 点赞转发公众号即可永久解锁次数❤",
    },
    "reference-sheet": {
        "limit": 8,
        "locked_message": "使用次数已到极限。添加微信：ddff9294 。 点赞转发公众号即可永久解锁次数❤",
    },
}


def state_path() -> Path:
    state_dir = Path.home() / ".codex" / "skill-state" / "beauty-generator"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "usage.json"


def load_state() -> dict:
    path = state_path()
    if not path.exists():
        return {name: 0 for name in COUNTERS}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {name: 0 for name in COUNTERS}

    state = {}
    for name in COUNTERS:
        used = data.get(name, 0)
        if not isinstance(used, int) or used < 0:
            used = 0
        state[name] = used
    return state


def save_state(state: dict) -> None:
    path = state_path()
    path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_payload(target: str, allowed: bool, used: int) -> dict:
    counter = COUNTERS[target]
    limit = counter["limit"]
    remaining = max(limit - used, 0)
    return {
        "target": target,
        "allowed": allowed,
        "used": used,
        "limit": limit,
        "remaining": remaining,
        "message": "" if allowed else counter["locked_message"],
    }


def cmd_status(target: str) -> int:
    state = load_state()
    used = state[target]
    allowed = used < COUNTERS[target]["limit"]
    print(json.dumps(build_payload(target, allowed, used), ensure_ascii=False))
    return 0


def cmd_consume(target: str) -> int:
    state = load_state()
    used = state[target]
    if used >= COUNTERS[target]["limit"]:
        print(json.dumps(build_payload(target, False, used), ensure_ascii=False))
        return 0

    used += 1
    state[target] = used
    save_state(state)
    print(json.dumps(build_payload(target, True, used), ensure_ascii=False))
    return 0


def cmd_reset(target: str | None) -> int:
    state = load_state()
    if target is None:
        state = {name: 0 for name in COUNTERS}
        print(json.dumps({"reset": "all", "targets": state}, ensure_ascii=False))
    else:
        state[target] = 0
        print(json.dumps(build_payload(target, True, 0), ensure_ascii=False))
    save_state(state)
    return 0


def parse_args() -> tuple[str, str | None]:
    parser = argparse.ArgumentParser(description="Usage gate for the beauty-generator skill")
    parser.add_argument(
        "parts",
        nargs="+",
        help="Either '<command>' for portrait usage, or '<target> <command>'",
    )
    args = parser.parse_args()

    if len(args.parts) == 1:
        target = "portraits"
        command = args.parts[0]
    elif len(args.parts) == 2:
        target, command = args.parts
    else:
        parser.error("Use '<command>' or '<target> <command>'")

    if target not in COUNTERS:
        parser.error(f"Unknown target: {target}")
    if command not in {"status", "consume", "reset"}:
        parser.error(f"Unknown command: {command}")
    return target, command


def main() -> int:
    target, command = parse_args()

    if command == "status":
        return cmd_status(target)
    if command == "consume":
        return cmd_consume(target)
    return cmd_reset(target)


if __name__ == "__main__":
    raise SystemExit(main())
