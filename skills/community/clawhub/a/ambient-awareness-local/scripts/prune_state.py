#!/usr/bin/env python3
"""Bound ambient-awareness JSONL retention without reading event payloads."""

from __future__ import annotations
import argparse
from pathlib import Path

def trim(path: Path, keep_lines: int) -> None:
    if not path.exists():
        return
    lines = path.read_bytes().splitlines(keepends=True)
    if len(lines) <= keep_lines:
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(b"".join(lines[-keep_lines:]))
    tmp.replace(path)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--keep-event-lines", type=int, default=10000)
    parser.add_argument("--keep-wake-lines", type=int, default=2000)
    args = parser.parse_args()
    if args.keep_event_lines < 1 or args.keep_wake_lines < 1:
        parser.error("retention counts must be positive")
    trim(args.state_dir / "event_log.jsonl", args.keep_event_lines)
    trim(args.state_dir / "wake_requests.jsonl", args.keep_wake_lines)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
