#!/usr/bin/env python3
"""
docker-log-inspector.py — Filter and analyze Docker container logs
Usage: python3 docker-log-inspector.py <container> [--since 5m] [--filter ERROR|WARN|CRIT]

Example: python3 docker-log-inspector.py my-app --since 30m --filter ERROR
"""

import argparse
import subprocess
import sys
import re
from datetime import datetime


def get_logs(container, since, tail):
    cmd = ["docker", "logs", container, "--tail", str(tail)]
    if since:
        cmd.extend(["--since", since])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        print("⚠️  docker logs timed out", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("❌ Docker not found. Is Docker installed?", file=sys.stderr)
        sys.exit(1)


def filter_logs(logs, pattern, ignore_case):
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)
    lines = logs.splitlines()
    return [line for line in lines if regex.search(line)]


def summarize(lines):
    """Return a short summary of log severity counts."""
    counts = {"ERROR": 0, "WARN": 0, "INFO": 0, "DEBUG": 0, "FATAL": 0, "CRIT": 0, "TRACE": 0}
    for line in lines:
        upper = line.upper()
        for key in counts:
            if key in upper:
                counts[key] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Filter and analyze Docker logs.")
    parser.add_argument("container", help="Container name or ID")
    parser.add_argument("--since", default="10m", help="Time range (e.g. 30m, 2h, 2024-01-01T00:00:00)")
    parser.add_argument("--filter", default=None, help="Regex pattern to filter log lines")
    parser.add_argument("--tail", type=int, default=500, help="Number of recent lines to fetch")
    parser.add_argument("--ignore-case", action="store_true", help="Case-insensitive filter")
    parser.add_argument("--summary", action="store_true", help="Show severity summary instead of full output")
    args = parser.parse_args()

    print(f"📋 Fetching logs from '{args.container}' (last {args.tail} lines, since {args.since})...")
    logs = get_logs(args.container, args.since, args.tail)

    if not logs.strip():
        print("ℹ️  No log output.")
        return

    if args.filter:
        matched = filter_logs(logs, args.filter, args.ignore_case)
        print(f"🔍 Filter: '{args.filter}' — {len(matched)} matching lines\n")
        if args.summary:
            counts = summarize(matched)
            print("Severity distribution:")
            for sev, cnt in sorted(counts.items(), key=lambda x: -x[1]):
                if cnt:
                    print(f"  {sev:>6}: {cnt}")
        else:
            for line in matched:
                print(line)
    else:
        if args.summary:
            counts = summarize(logs.splitlines())
            print("Severity distribution:")
            for sev, cnt in sorted(counts.items(), key=lambda x: -x[1]):
                if cnt:
                    print(f"  {sev:>6}: {cnt}")
        else:
            print(logs)


if __name__ == "__main__":
    main()
