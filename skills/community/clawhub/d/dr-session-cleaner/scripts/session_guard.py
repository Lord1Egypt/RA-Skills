#!/usr/bin/env python3
"""Session Guard – monitor OpenClaw sessions and alert when context usage is high."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict

GUARD_DIR = Path("~/.openclaw/session-guard").expanduser()
DEFAULT_STATE = Path(os.environ.get("SESSION_GUARD_STATE", str(GUARD_DIR / "state.json"))).expanduser()
DEFAULT_THRESHOLD = float(os.environ.get("SESSION_GUARD_THRESHOLD", "0.8"))
DEFAULT_TARGET = os.environ.get("SESSION_GUARD_TARGET", "")
DEFAULT_CHANNEL = os.environ.get("SESSION_GUARD_CHANNEL", "discord")
DEFAULT_COOLDOWN_MIN = int(os.environ.get("SESSION_GUARD_COOLDOWN_MIN", "60"))
DEFAULT_AGENT = os.environ.get("SESSION_GUARD_AGENT", "main")


def run(cmd: list[str], *, expect_json: bool = False) -> Any:
    """Run a shell command and optionally parse JSON."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - surface error
        print(f"[session-guard] command failed: {' '.join(cmd)}", file=sys.stderr)
        print(exc.stdout, file=sys.stderr)
        print(exc.stderr, file=sys.stderr)
        raise
    if expect_json:
        return json.loads(result.stdout or "{}")
    return result.stdout


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"notified": {}}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {"notified": {}}


def save_state(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")
        tmp_name = handle.name
    os.chmod(tmp_name, 0o600)
    Path(tmp_name).replace(path)


def is_guard_file(path: Path) -> bool:
    try:
        return path.expanduser().resolve().is_relative_to(GUARD_DIR.resolve())
    except (OSError, ValueError):
        return False


def format_message(session: Dict[str, Any]) -> str:
    key = session.get("key", "(unknown)")
    session_id = session.get("sessionId", "?")
    total = session.get("totalTokens", 0)
    context = session.get("contextTokens", 0)
    ratio = (total / context * 100) if context else 0
    return (
        "⚠️ Session Guard alert\n"
        f"Session **{key}** is at {ratio:.1f}% ({total:,}/{context:,} tokens).\n\n"
        "This monitor is alert-only. Inspect the session before deciding on a separate, approved recovery action.\n"
        f"Session identifier: `{session_id}`"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor OpenClaw sessions and alert when usage is high")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Message target, e.g. user:270... (required)")
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="Channel name (default: discord)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Ratio (0-1) before alert")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="State file path")
    parser.add_argument("--cooldown-min", type=int, default=DEFAULT_COOLDOWN_MIN, help="Minutes before re-alerting the same session")
    parser.add_argument("--agent", default=DEFAULT_AGENT, help="Agent id (for logging only)")
    args = parser.parse_args()

    if not args.target:
        print("SESSION_GUARD_TARGET or --target is required", file=sys.stderr)
        return 2
    if args.channel != "discord":
        print("--channel must be discord", file=sys.stderr)
        return 2
    if not re.fullmatch(r"user:[0-9]{5,30}", args.target):
        print("--target must be a Discord immutable DM target", file=sys.stderr)
        return 2
    if not 0 < args.threshold < 1:
        print("--threshold must be greater than 0 and less than 1", file=sys.stderr)
        return 2
    if args.cooldown_min < 0:
        print("--cooldown-min must be non-negative", file=sys.stderr)
        return 2
    if not is_guard_file(args.state):
        print("--state must be inside ~/.openclaw/session-guard", file=sys.stderr)
        return 2

    data = run(["openclaw", "sessions", "--json"], expect_json=True)
    sessions = data.get("sessions", [])
    threshold_ratio = args.threshold
    state = load_state(args.state)
    notified: Dict[str, Dict[str, Any]] = state.setdefault("notified", {})
    now = time.time()
    cooldown_seconds = args.cooldown_min * 60

    triggered = []
    still_high_keys = set()

    for session in sessions:
        context_tokens = session.get("contextTokens")
        total_tokens = session.get("totalTokens")
        if not context_tokens:
            continue
        ratio = (total_tokens or 0) / context_tokens
        if ratio >= threshold_ratio:
            key = session.get("key", "")
            still_high_keys.add(key)
            last = notified.get(key)
            if last and now - last.get("timestamp", 0) < cooldown_seconds:
                continue  # already warned recently
            message = format_message(session)
            run([
                "openclaw",
                "message",
                "send",
                "--channel",
                args.channel,
                "--target",
                args.target,
                "--message",
                message,
            ])
            notified[key] = {
                "timestamp": now,
                "sessionId": session.get("sessionId"),
                "totalTokens": total_tokens,
                "contextTokens": context_tokens,
            }
            triggered.append(key)

    # Drop entries that are no longer high
    for key in list(notified.keys()):
        if key not in still_high_keys:
            notified.pop(key, None)

    save_state(args.state, state)

    if triggered:
        print(f"[session-guard] alerted on: {', '.join(triggered)}")
    else:
        print("[session-guard] no sessions above threshold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
