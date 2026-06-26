#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from codex_profile_runtime import append_event, backup_file, build_usage_rows, choose_best_candidate, collect_profiles, load_json, write_json

DEFAULT_STATE_DIR = Path("/home/node/.openclaw")


def local_profile_issue(profile: dict[str, Any] | None, now_ms: int) -> str | None:
    if not isinstance(profile, dict):
        return "missing_profile_entry"
    token = profile.get("access") or profile.get("token")
    if not token:
        return "missing_token"
    expires = profile.get("expires")
    if isinstance(expires, (int, float)) and expires <= now_ms:
        return "token_expired"
    return None


def choose_local_fallback(profiles: list[dict[str, Any]], current_profile_id: str | None, now_ms: int, excluded: set[str] | None = None) -> dict[str, Any] | None:
    excluded = excluded or set()
    eligible = []
    for profile in profiles:
        if profile["profileId"] == current_profile_id or profile["profileId"] in excluded:
            continue
        if local_profile_issue(profile, now_ms) is None:
            eligible.append(profile)
    if not eligible:
        return None
    eligible.sort(key=lambda item: ((item.get("expires") or 0), item["profileId"]), reverse=True)
    chosen = eligible[0]
    return {
        "profileId": chosen["profileId"],
        "email": chosen.get("email"),
        "accountId": chosen.get("accountId"),
        "usage": {"note": "local_fallback_only"},
        "effectiveRemaining": None,
    }


def evaluate_session(entry: dict[str, Any], usage_rows: list[dict[str, Any]], profiles: list[dict[str, Any]], threshold: float, switch_on_usage_error: bool, now_ms: int) -> dict[str, Any]:
    current_profile_id = entry.get("authProfileOverride")
    current_profile = next((profile for profile in profiles if profile["profileId"] == current_profile_id), None)
    current_local_issue = local_profile_issue(current_profile, now_ms)
    current_row = next((row for row in usage_rows if row["profileId"] == current_profile_id), None)
    current_remaining = current_row.get("effectiveRemaining") if current_row else None
    current_usage_error = current_row.get("usage", {}).get("error") if current_row else None

    result: dict[str, Any] = {
        "currentProfileId": current_profile_id,
        "currentRemaining": current_remaining,
        "currentUsageError": current_usage_error,
        "currentLocalIssue": current_local_issue,
        "status": "healthy",
        "reason": None,
    }

    reason = None
    if current_local_issue:
        reason = current_local_issue
    elif current_usage_error and switch_on_usage_error:
        reason = "current_profile_usage_error"
    elif current_remaining is not None and current_remaining <= threshold:
        reason = "remaining_below_threshold"
    else:
        return result

    candidate = choose_best_candidate(usage_rows, current_profile_id, threshold)
    if not candidate:
        candidate = choose_local_fallback(profiles, current_profile_id, now_ms)
    if candidate:
        result["status"] = "switch_recommended"
        result["reason"] = reason
        result["nextProfileId"] = candidate["profileId"]
        result["nextRemaining"] = candidate.get("effectiveRemaining")
    else:
        result["status"] = "no_candidate_available"
        result["reason"] = reason
    return result


def run_check(config_path: Path, state_dir: Path, usage_rows: list[dict[str, Any]] | None, force_refresh: bool, timeout: int, apply: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    config = load_json(config_path)
    agent = config.get("agent", "main")
    threshold = float(config.get("thresholdPercent", 10))
    switch_on_usage_error = bool(config.get("switchOnUsageError", True))
    sessions_path = state_dir / "agents" / agent / "sessions" / "sessions.json"
    auth_path = state_dir / "agents" / agent / "agent" / "auth-profiles.json"
    event_log_path = Path(config.get("eventLogPath", "state/codex-profile-watchdog-events.jsonl"))
    switch_source = config.get("switchSource", "auto-watchdog")

    sessions = load_json(sessions_path)
    auth = load_json(auth_path)
    profiles = collect_profiles(auth)
    if usage_rows is None or force_refresh:
        usage_rows = build_usage_rows(profiles, timeout)

    changed = 0
    results: list[dict[str, Any]] = []
    now_ms = int(time.time() * 1000)
    for session_key in config.get("sessionTargets") or []:
        entry = sessions.get(session_key)
        if not isinstance(entry, dict):
            results.append({"sessionKey": session_key, "status": "missing_session"})
            continue

        evaluation = evaluate_session(entry, usage_rows, profiles, threshold, switch_on_usage_error, now_ms)
        evaluation["sessionKey"] = session_key
        evaluation["threshold"] = threshold
        if apply and evaluation.get("status") == "switch_recommended":
            backup_path = backup_file(sessions_path)
            old_profile_id = entry.get("authProfileOverride")
            entry["authProfileOverride"] = evaluation["nextProfileId"]
            entry["authProfileOverrideSource"] = switch_source
            entry["updatedAt"] = now_ms
            write_json(sessions_path, sessions)
            append_event(
                event_log_path,
                {
                    "timestamp": int(time.time()),
                    "sessionKey": session_key,
                    "oldProfileId": old_profile_id,
                    "newProfileId": evaluation["nextProfileId"],
                    "reason": evaluation["reason"],
                    "currentRemaining": evaluation.get("currentRemaining"),
                    "nextRemaining": evaluation.get("nextRemaining"),
                    "backup": str(backup_path),
                },
            )
            evaluation["status"] = "switched"
            evaluation["backup"] = str(backup_path)
            changed += 1
        results.append(evaluation)
    return usage_rows, results, changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Periodic Codex profile health watchdog")
    parser.add_argument("--config", required=True, help="Watchdog config path")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR), help="OpenClaw state directory")
    parser.add_argument("--timeout", type=int, default=15, help="Per-profile usage timeout")
    parser.add_argument("--once", action="store_true", help="Run one check and exit")
    parser.add_argument("--apply", action="store_true", help="Apply profile switches")
    parser.add_argument("--json", action="store_true", help="Print JSON output in once mode")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_json(config_path)
    state_dir = Path(args.state_dir)
    interval_seconds = int(config.get("intervalSeconds", 60))
    usage_probe_every_seconds = int(config.get("usageProbeEverySeconds", 60))
    usage_rows: list[dict[str, Any]] | None = None
    last_usage_probe_at = 0.0

    if args.once:
        usage_rows, results, changed = run_check(config_path, state_dir, usage_rows, True, args.timeout, args.apply)
        payload = {
            "mode": "once",
            "usageProbeEverySeconds": usage_probe_every_seconds,
            "intervalSeconds": interval_seconds,
            "profiles": usage_rows,
            "sessions": results,
            "changed": changed,
            "apply": args.apply,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    while True:
        now = time.time()
        force_refresh = usage_rows is None or (now - last_usage_probe_at) >= usage_probe_every_seconds
        usage_rows, results, changed = run_check(config_path, state_dir, usage_rows, force_refresh, args.timeout, args.apply)
        if force_refresh:
            last_usage_probe_at = now
        log_line = {
            "timestamp": int(now),
            "changed": changed,
            "sessions": results,
        }
        print(json.dumps(log_line, ensure_ascii=False), flush=True)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
