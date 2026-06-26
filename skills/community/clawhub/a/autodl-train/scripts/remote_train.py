#!/usr/bin/env python3
"""Start or resume a remote training job over SSH."""

from __future__ import annotations

import shlex
import sys
from typing import Any, Dict

from common import (
    ConfigArgumentParser,
    SkillError,
    build_activation_block,
    build_guard_block,
    build_process_match,
    json_dump,
    load_config,
    print_error,
    print_json,
    remote_path,
    run_remote_script,
    shell_quote,
    validate_required_config,
)


def build_train_command(config: Dict[str, Any], resume_from: str | None) -> str:
    command = str(config["train_command"]).strip()
    if resume_from:
        template = str(config.get("resume_argument_template") or "--resume-from {checkpoint}")
        command = f"{command} {template.format(checkpoint=shlex.quote(resume_from))}"
    return command


def build_remote_start_script(config: Dict[str, Any], *, train_command: str, log_path: str) -> str:
    process_match = build_process_match({**config, "train_command": train_command})
    launcher_path = remote_path(config, ".autoclaw-launch.sh")
    return f"""
{build_guard_block(config)}
TRAIN_LOG={shell_quote(log_path)}
TRAIN_COMMAND={shell_quote(train_command)}
PROCESS_MATCH={shell_quote(process_match)}
LAUNCHER_PATH={shell_quote(launcher_path)}
mkdir -p "$(dirname "$TRAIN_LOG")"
PRE_START_LOG_SIZE=$(stat -c '%s' "$TRAIN_LOG" 2>/dev/null || echo 0)
printf '=== AutoDL train operator start ===\n' >> "$TRAIN_LOG"
printf 'timestamp=%s\n' "$(date '+%F %T %z')" >> "$TRAIN_LOG"
printf 'project=%s\n' "$PROJECT_PATH" >> "$TRAIN_LOG"
printf 'command=%s\n' "$TRAIN_COMMAND" >> "$TRAIN_LOG"
cat > "$LAUNCHER_PATH" <<'EOF_AUTOCLAW_LAUNCHER'
#!/usr/bin/env bash
set -euo pipefail
PROJECT_PATH={shell_quote(config['project_path'])}
cd "$PROJECT_PATH"
{build_activation_block(config)}
exec {train_command}
EOF_AUTOCLAW_LAUNCHER
chmod 700 "$LAUNCHER_PATH"
nohup "$LAUNCHER_PATH" >> "$TRAIN_LOG" 2>&1 < /dev/null &
PID=$!
sleep 2
RUNNING=0
if ps -p "$PID" >/dev/null 2>&1; then
  RUNNING=1
fi
POST_START_LOG_SIZE=$(stat -c '%s' "$TRAIN_LOG" 2>/dev/null || echo 0)
LOG_GREW=0
if [ "$POST_START_LOG_SIZE" -gt "$PRE_START_LOG_SIZE" ]; then
  LOG_GREW=1
fi
if [ "$RUNNING" -eq 0 ] && [ "$LOG_GREW" -eq 1 ]; then
  RUNNING=1
fi
printf 'START_OK=%s\n' "$RUNNING"
printf 'PID=%s\n' "$PID"
printf 'LOG_PATH=%s\n' "$TRAIN_LOG"
printf 'PROCESS_MATCH=%s\n' "$PROCESS_MATCH"
printf 'LAUNCHER_PATH=%s\n' "$LAUNCHER_PATH"
printf 'LOG_GREW=%s\n' "$LOG_GREW"
printf 'MONITOR_HINT=%s\n' "python scripts/check_status.py --config config.json && python scripts/monitor_resources.py --config config.json"
""".strip()


def parse_start_output(stdout: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"ok": True}
    for line in stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        payload[key.lower()] = value
    payload["ok"] = payload.get("start_ok") == "1"
    payload["status"] = "started" if payload["ok"] else "unknown"
    if payload.get("pid"):
        try:
            payload["pid"] = int(payload["pid"])
        except ValueError:
            pass
    payload["suggested_next_steps"] = [
        "Run check_status.py in 10-30 seconds to confirm the launcher PID and fresh log output.",
        "Run monitor_resources.py if GPU utilization looks lower than expected.",
        "Run summarize_log.py --action summarize after enough steps have accumulated in the log.",
    ]
    return payload


def main() -> int:
    parser = ConfigArgumentParser("Start or resume a remote training job on AutoDL.")
    parser.add_argument("--resume-from", help="Checkpoint path relative to the project path or absolute on the remote host.")
    args = parser.parse_args()

    try:
        config = load_config(args)
        validate_required_config(config, require_train_command=True)
        train_command = build_train_command(config, args.resume_from)
        log_path = remote_path(config, str(config.get("log_path") or "logs/train.log"))
        result = run_remote_script(config, build_remote_start_script(config, train_command=train_command, log_path=log_path))
        payload = parse_start_output(result.stdout)
        payload["log_path"] = payload.get("log_path", log_path)
        payload["process_match"] = payload.get("process_match", build_process_match(config))
        if args.resume_from:
            payload["resume_from"] = args.resume_from
        if args.json:
            print_json(payload)
        else:
            print("Start training result")
            print(f"- status: {payload['status']}")
            print(f"- pid: {payload.get('pid', 'unknown')}")
            print(f"- log_path: {payload['log_path']}")
            print(f"- process_match: {payload['process_match']}")
            if args.resume_from:
                print(f"- resume_from: {args.resume_from}")
            print("- next:")
            for item in payload["suggested_next_steps"]:
                print(f"  - {item}")
            print("\nStructured output")
            print(json_dump(payload))
        return 0
    except SkillError as exc:
        print_error(str(exc), json_mode=args.json)
        return 1


if __name__ == "__main__":
    sys.exit(main())
