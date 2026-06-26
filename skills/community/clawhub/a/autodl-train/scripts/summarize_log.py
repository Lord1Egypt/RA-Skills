#!/usr/bin/env python3
"""Read, analyze, and summarize remote training logs."""

from __future__ import annotations

import sys
from typing import Any, Dict

from common import (
    ConfigArgumentParser,
    SkillError,
    load_config,
    print_error,
    print_json,
    read_remote_file_tail,
    select_remote_log_file,
    validate_required_config,
)
from log_utils import detect_failures, extract_metrics, isolate_latest_run, summarize_log


ACTIONS = {"read", "detect-failure", "summarize"}


def main() -> int:
    parser = ConfigArgumentParser("Read and summarize remote AutoDL training logs.")
    parser.add_argument("--action", choices=sorted(ACTIONS), default="summarize")
    parser.add_argument("--tail", type=int, help="How many recent log lines to inspect.")
    args = parser.parse_args()

    try:
        config = load_config(args)
        validate_required_config(config, require_train_command=False)
        log_path = select_remote_log_file(config)
        if not log_path:
            raise SkillError("no log file found; set log_path or log_candidates")
        tail_lines = args.tail or (
            int(config.get("summary_log_tail", 400)) if args.action != "read" else int(config.get("status_log_tail", 40))
        )
        log_info = read_remote_file_tail(config, log_path, tail_lines=tail_lines)
        log_text = log_info.get("text", "")
        latest_run_text = isolate_latest_run(log_text)

        if args.action == "read":
            metrics = extract_metrics(latest_run_text)
            payload: Dict[str, Any] = {
                "log_path": log_info.get("path"),
                "latest_log_time": log_info.get("mtime"),
                "tail_lines": tail_lines,
                "metrics": metrics,
                "excerpt": latest_run_text.splitlines()[-tail_lines:],
            }
            if args.json:
                print_json(payload)
            else:
                print("Recent training log")
                print(f"- log_path: {payload['log_path']}")
                print(f"- latest_log_time: {payload['latest_log_time'] or 'unknown'}")
                latest = payload["metrics"].get("latest", {})
                if latest:
                    joined = ", ".join(f"{key}={value:g}" for key, value in latest.items())
                    print(f"- parsed_metrics: {joined}")
                else:
                    print("- parsed_metrics: no stable metric pattern detected")
                print("- excerpt:")
                for line in payload["excerpt"][-40:]:
                    print(f"  {line}")
            return 0

        if args.action == "detect-failure":
            failures = detect_failures(latest_run_text)
            payload = {
                "log_path": log_info.get("path"),
                "latest_log_time": log_info.get("mtime"),
                "failure_count": len(failures),
                "failures": failures,
            }
            if args.json:
                print_json(payload)
            else:
                print("Failure detection")
                print(f"- log_path: {payload['log_path']}")
                print(f"- failure_count: {payload['failure_count']}")
                if failures:
                    for item in failures:
                        print(f"- type: {item['type']}")
                        print(f"  cause: {item['possible_cause']}")
                        print(f"  suggestion: {item['suggestion']}")
                        print(f"  resume_recommended: {'yes' if item['resume_recommended'] else 'no'}")
                        print(f"  hit: {item['line']}")
                else:
                    print("- no common failure keywords found in the inspected log window")
            return 0

        summary = summarize_log(latest_run_text)
        payload = {
            "log_path": log_info.get("path"),
            "latest_log_time": log_info.get("mtime"),
            "analyzed_run_excerpt": latest_run_text.splitlines()[-20:],
            **summary,
        }
        if args.json:
            print_json(payload)
        else:
            print("Training summary")
            print(f"- log_path: {payload['log_path']}")
            print(f"- latest_log_time: {payload['latest_log_time'] or 'unknown'}")
            print(payload["human_summary"])
        return 0
    except SkillError as exc:
        print_error(str(exc), json_mode=args.json)
        return 1


if __name__ == "__main__":
    sys.exit(main())
