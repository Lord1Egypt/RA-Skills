#!/usr/bin/env python3
"""Check whether a remote training job is still active."""

from __future__ import annotations

import datetime as dt
import sys
from typing import Any, Dict, List

from common import (
    ConfigArgumentParser,
    SkillError,
    build_guard_block,
    build_process_match,
    load_config,
    print_error,
    print_json,
    read_remote_file_tail,
    run_remote_script,
    select_remote_log_file,
    shell_quote,
    validate_required_config,
)
from log_utils import detect_failures


def build_status_probe_script(config: Dict[str, Any]) -> str:
    process_match = build_process_match(config)
    return f"""
{build_guard_block(config)}
PROCESS_MATCH={shell_quote(process_match)}
printf 'TIME=%s\n' "$(date '+%F %T %z')"
printf 'PROCESS_MATCH=%s\n' "$PROCESS_MATCH"
echo '__PROCESS_START__'
ps -eo pid=,lstart=,etimes=,command= | grep -F -- "$PROCESS_MATCH" | grep -v 'grep -F' || true
echo '__PROCESS_END__'
echo '__GPU_START__'
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv,noheader,nounits 2>/dev/null || true
fi
echo '__GPU_END__'
""".strip()


def parse_processes(section: str) -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    for line in section.splitlines():
        parts = line.strip().split(None, 7)
        if len(parts) < 8:
            continue
        pid, wday, month, day, time_value, year, etimes, command = parts
        processes.append(
            {
                "pid": int(pid),
                "start_time": f"{wday} {month} {day} {time_value} {year}",
                "elapsed_seconds": int(etimes),
                "command": command,
            }
        )
    return processes


def parse_gpu_apps(section: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line in section.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            continue
        pid, process_name, memory = parts
        if not pid.isdigit():
            continue
        rows.append({"pid": int(pid), "process_name": process_name, "used_gpu_memory_mb": int(memory or 0)})
    return rows


def split_sections(stdout: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {"meta": [], "process": [], "gpu": []}
    active = "meta"
    mapping = {
        "__PROCESS_START__": "process",
        "__PROCESS_END__": "meta",
        "__GPU_START__": "gpu",
        "__GPU_END__": "meta",
    }
    for line in stdout.splitlines():
        if line in mapping:
            active = mapping[line]
            continue
        sections[active].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def compute_status(processes: List[Dict[str, Any]], gpu_apps: List[Dict[str, Any]], log_info: Dict[str, Any]) -> str:
    failures = detect_failures(log_info.get("text", ""))
    log_is_recent = False
    if log_info.get("mtime"):
        try:
            log_dt = dt.datetime.strptime(log_info["mtime"], "%Y-%m-%d %H:%M:%S.%f %z")
            log_is_recent = (dt.datetime.now(log_dt.tzinfo) - log_dt).total_seconds() < 900
        except ValueError:
            try:
                log_dt = dt.datetime.strptime(log_info["mtime"], "%Y-%m-%d %H:%M:%S %z")
                log_is_recent = (dt.datetime.now(log_dt.tzinfo) - log_dt).total_seconds() < 900
            except ValueError:
                log_is_recent = False
    if processes:
        return "running"
    if failures:
        return "failed"
    if gpu_apps and log_is_recent:
        return "running"
    if log_info.get("found"):
        return "stopped"
    return "unknown"


def main() -> int:
    parser = ConfigArgumentParser("Check the status of a remote AutoDL training job.")
    args = parser.parse_args()

    try:
        config = load_config(args)
        validate_required_config(config, require_train_command=False)
        probe_result = run_remote_script(config, build_status_probe_script(config))
        sections = split_sections(probe_result.stdout)
        meta = {}
        for line in sections["meta"].splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                meta[key.lower()] = value

        processes = parse_processes(sections["process"])
        gpu_apps = parse_gpu_apps(sections["gpu"])
        log_path = select_remote_log_file(config)
        log_info = {"found": False, "path": None, "mtime": None, "text": ""}
        if log_path:
            log_info = read_remote_file_tail(config, log_path, tail_lines=int(config.get("status_log_tail", 40)))
        failures = detect_failures(log_info.get("text", ""))
        matched_gpu_apps = [row for row in gpu_apps if row["pid"] in {proc["pid"] for proc in processes}]
        status = compute_status(processes, matched_gpu_apps or gpu_apps, log_info)

        payload: Dict[str, Any] = {
            "status": status,
            "pid": processes[0]["pid"] if processes else None,
            "start_time": processes[0]["start_time"] if processes else None,
            "process_match": meta.get("process_match", build_process_match(config)),
            "latest_log_time": log_info.get("mtime"),
            "latest_log_path": log_info.get("path"),
            "latest_log_excerpt": log_info.get("text", "").splitlines()[-12:],
            "processes": processes,
            "gpu_processes": matched_gpu_apps or gpu_apps,
            "failure_hints": failures,
        }

        if args.json:
            print_json(payload)
        else:
            print("Training status")
            print(f"- status: {payload['status']}")
            print(f"- pid: {payload['pid'] or 'not found'}")
            print(f"- start_time: {payload['start_time'] or 'unknown'}")
            print(f"- latest_log_time: {payload['latest_log_time'] or 'unknown'}")
            print(f"- latest_log_path: {payload['latest_log_path'] or 'not found'}")
            if payload["gpu_processes"]:
                gpu_bits = ", ".join(
                    f"pid={row['pid']} mem={row['used_gpu_memory_mb']}MB" for row in payload["gpu_processes"]
                )
                print(f"- gpu_activity: {gpu_bits}")
            else:
                print("- gpu_activity: no matched GPU process found")
            if payload["failure_hints"]:
                first = payload["failure_hints"][0]
                print(f"- failure_hint: {first['type']} -> {first['possible_cause']}")
            if payload["latest_log_excerpt"]:
                print("- latest_log_excerpt:")
                for line in payload["latest_log_excerpt"]:
                    print(f"  {line}")
        return 0
    except SkillError as exc:
        print_error(str(exc), json_mode=args.json)
        return 1


if __name__ == "__main__":
    sys.exit(main())
