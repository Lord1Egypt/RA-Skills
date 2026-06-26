#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from codex_profile_runtime import append_event, backup_file, load_json, write_json

DEFAULT_STATE_DIR = Path("/home/node/.openclaw")


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign a Codex authProfileOverride to a session")
    parser.add_argument("session_key", help="Session key to patch")
    parser.add_argument("profile_id", help="Codex profile id to assign")
    parser.add_argument("--config", required=True, help="Config path used to resolve agent and event log")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="OpenClaw state directory")
    parser.add_argument("--source", help="Override authProfileOverrideSource")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    config = load_json(Path(args.config))
    state_dir = Path(args.state_dir)
    agent = config.get("agent", "main")
    source = args.source or config.get("switchSource", "manual")
    sessions_path = state_dir / "agents" / agent / "sessions" / "sessions.json"
    event_log_path = Path(config.get("eventLogPath", "state/codex-profile-broker-events.jsonl"))

    sessions = load_json(sessions_path)
    entry = sessions.get(args.session_key)
    if not isinstance(entry, dict):
        raise SystemExit(f"Session not found: {args.session_key}")

    old_profile_id = entry.get("authProfileOverride")
    backup_path = backup_file(sessions_path)
    entry["authProfileOverride"] = args.profile_id
    entry["authProfileOverrideSource"] = source
    entry["updatedAt"] = int(time.time() * 1000)
    write_json(sessions_path, sessions)

    event = {
        "timestamp": int(time.time()),
        "sessionKey": args.session_key,
        "oldProfileId": old_profile_id,
        "newProfileId": args.profile_id,
        "source": source,
        "backup": str(backup_path),
    }
    append_event(event_log_path, event)

    payload = {
        "sessionKey": args.session_key,
        "oldProfileId": old_profile_id,
        "newProfileId": args.profile_id,
        "source": source,
        "backup": str(backup_path),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
