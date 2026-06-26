#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from codex_profile_runtime import append_event, backup_file, build_usage_rows, choose_best_candidate, collect_profiles, load_json, write_json

DEFAULT_STATE_DIR = Path("/home/node/.openclaw")


def main() -> int:
    parser = argparse.ArgumentParser(description="Switch Codex profile when usage remaining drops below threshold")
    parser.add_argument("--config", required=True, help="Rotation config path")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="OpenClaw state directory")
    parser.add_argument("--session-key", help="Override a single target session key")
    parser.add_argument("--threshold", type=float, help="Override threshold percent")
    parser.add_argument("--timeout", type=int, default=15, help="Per-profile usage timeout")
    parser.add_argument("--apply", action="store_true", help="Apply profile switch when threshold is breached")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    config = load_json(Path(args.config))
    state_dir = Path(args.state_dir)
    agent = config.get("agent", "main")
    threshold = float(args.threshold if args.threshold is not None else config.get("thresholdPercent", 10))
    auth_path = state_dir / "agents" / agent / "agent" / "auth-profiles.json"
    sessions_path = state_dir / "agents" / agent / "sessions" / "sessions.json"
    event_log_path = Path(config.get("eventLogPath", "state/codex-profile-switch-events.jsonl"))
    session_targets = [args.session_key] if args.session_key else list(config.get("sessionTargets") or [])
    switch_source = config.get("switchSource", "auto-threshold")
    switch_on_usage_error = bool(config.get("switchOnUsageError", True))

    auth = load_json(auth_path)
    sessions = load_json(sessions_path)
    profiles = collect_profiles(auth)
    usage_rows = build_usage_rows(profiles, args.timeout)

    session_results: list[dict[str, Any]] = []
    changed = 0
    for session_key in session_targets:
        entry = sessions.get(session_key)
        if not isinstance(entry, dict):
            session_results.append({"sessionKey": session_key, "status": "missing_session"})
            continue
        current_profile_id = entry.get("authProfileOverride")
        current_row = next((row for row in usage_rows if row["profileId"] == current_profile_id), None)
        current_remaining = current_row.get("effectiveRemaining") if current_row else None
        current_error = current_row.get("usage", {}).get("error") if current_row else None if current_row else None
        result = {
            "sessionKey": session_key,
            "currentProfileId": current_profile_id,
            "currentRemaining": current_remaining,
            "currentError": current_error,
            "threshold": threshold,
            "status": "ok",
        }
        switch_reason = None
        if current_error and switch_on_usage_error:
            switch_reason = "current_profile_usage_error"
        elif current_remaining is None:
            result["status"] = "unknown_current_usage"
            session_results.append(result)
            continue
        elif current_remaining > threshold:
            result["status"] = "within_threshold"
            session_results.append(result)
            continue
        else:
            switch_reason = "remaining_below_threshold"

        candidate = choose_best_candidate(usage_rows, current_profile_id, threshold)
        if not candidate:
            result["status"] = "no_candidate_available"
            session_results.append(result)
            continue

        result["status"] = "switch_recommended"
        result["nextProfileId"] = candidate["profileId"]
        result["nextRemaining"] = candidate["effectiveRemaining"]
        result["reason"] = switch_reason

        if args.apply:
            backup_path = backup_file(sessions_path)
            entry["authProfileOverride"] = candidate["profileId"]
            entry["authProfileOverrideSource"] = switch_source
            entry["updatedAt"] = int(time.time() * 1000)
            write_json(sessions_path, sessions)
            event = {
                "timestamp": int(time.time()),
                "sessionKey": session_key,
                "oldProfileId": current_profile_id,
                "oldRemaining": current_remaining,
                "newProfileId": candidate["profileId"],
                "newRemaining": candidate["effectiveRemaining"],
                "threshold": threshold,
                "reason": switch_reason,
                "backup": str(backup_path),
            }
            append_event(event_log_path, event)
            result["status"] = "switched"
            result["backup"] = str(backup_path)
            changed += 1
        session_results.append(result)

    payload = {
        "agent": agent,
        "threshold": threshold,
        "profiles": usage_rows,
        "sessions": session_results,
        "changed": changed,
        "apply": args.apply,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
