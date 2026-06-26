#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_STATE_DIR = "/home/node/.openclaw"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install generic Codex profile failover configs into an OpenClaw workspace")
    parser.add_argument("--workspace", required=True, help="OpenClaw workspace root")
    parser.add_argument("--session-key", default="agent:main:main", help="Session key to watch")
    parser.add_argument("--threshold", type=float, default=10.0, help="Switch threshold percent")
    parser.add_argument("--interval", type=int, default=60, help="Watchdog interval seconds")
    parser.add_argument("--probe-interval", type=int, default=60, help="Usage probe interval seconds")
    parser.add_argument("--state-dir", default=DEFAULT_STATE_DIR, help="OpenClaw state directory")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    config_dir = workspace / "config"
    state_dir = workspace / "state"
    config_dir.mkdir(parents=True, exist_ok=True)
    state_dir.mkdir(parents=True, exist_ok=True)

    watchdog = {
        "agent": "main",
        "thresholdPercent": args.threshold,
        "switchOnUsageError": True,
        "sessionTargets": [args.session_key],
        "intervalSeconds": args.interval,
        "usageProbeEverySeconds": args.probe_interval,
        "switchSource": "auto-watchdog",
        "eventLogPath": str((workspace / "state" / "codex-profile-watchdog-events.jsonl").resolve()),
        "logPath": str((workspace / "state" / "codex-profile-watchdog.log").resolve()),
    }
    threshold = {
        "agent": "main",
        "thresholdPercent": args.threshold,
        "switchOnUsageError": True,
        "sessionTargets": [args.session_key],
        "switchSource": "auto-threshold",
        "eventLogPath": str((workspace / "state" / "codex-profile-switch-events.jsonl").resolve()),
    }

    watchdog_path = config_dir / "codex-profile-watchdog.json"
    threshold_path = config_dir / "codex-profile-rotation.json"
    watchdog_path.write_text(json.dumps(watchdog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    threshold_path.write_text(json.dumps(threshold, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = {
        "workspace": str(workspace),
        "stateDir": args.state_dir,
        "watchdogConfig": str(watchdog_path),
        "thresholdConfig": str(threshold_path),
        "nextCommands": {
            "dryRun": f"python3 {SKILL_DIR / 'scripts' / 'codex_profile_threshold_guard.py'} --config {threshold_path} --state-dir {args.state_dir} --json",
            "applyOnce": f"python3 {SKILL_DIR / 'scripts' / 'codex_profile_threshold_guard.py'} --config {threshold_path} --state-dir {args.state_dir} --apply --json",
            "startWatchdog": f"nohup python3 {SKILL_DIR / 'scripts' / 'codex_profile_watchdog.py'} --config {watchdog_path} --state-dir {args.state_dir} --apply >> {workspace / 'state' / 'codex-profile-watchdog.log'} 2>&1 &",
            "manualTrigger": f"python3 {SKILL_DIR / 'scripts' / 'trigger_profile_failover.py'} --config {watchdog_path} --state-dir {args.state_dir}",
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
