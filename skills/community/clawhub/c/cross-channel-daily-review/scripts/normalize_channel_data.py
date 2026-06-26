#!/usr/bin/env python3
import json
import sys

VALID = {"active", "configured", "missing", "collection_failed"}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: normalize_channel_data.py <input.json> <output.json>", file=sys.stderr)
        return 2
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("input must be a list")
    out = []
    for item in data:
        channel = str(item.get("channel", "")).strip().lower()
        if not channel:
            raise ValueError("channel is required")
        status = str(item.get("status", "missing")).strip().lower()
        if status not in VALID:
            raise ValueError(f"invalid status for {channel}: {status}")
        norm = {
            "channel": channel,
            "channel_label": item.get("channel_label") or channel.title(),
            "status": status,
            "date": item.get("date", ""),
            "time_window": item.get("time_window", ""),
            "source_refs": item.get("source_refs") or [],
            "summary_points": item.get("summary_points") or [],
            "issues": item.get("issues") or [],
            "wins": item.get("wins") or [],
            "missing_reason": item.get("missing_reason", ""),
            "notes": item.get("notes") or [],
        }
        out.append(norm)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
