#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def bullets(items):
    items = items or ["- 无"]
    return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items)) if items and not str(items[0]).startswith("-") else "\n".join(items)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: write_raw_reviews.py <normalized.json> <template.md> <output-root>", file=sys.stderr)
        return 2
    data = json.load(open(sys.argv[1], "r", encoding="utf-8"))
    template = Path(sys.argv[2]).read_text(encoding="utf-8")
    out_root = Path(sys.argv[3])
    written = []
    for item in data:
        date = item["date"]
        yyyy, mm, _ = date.split("-")
        out_dir = out_root / yyyy / mm
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{item['channel']}_{date}.md"
        status_display = "已检出" if item["status"] == "active" else item.get("missing_reason") or item["status"]
        text = template
        replacements = {
            "{{channel_label}}": item.get("channel_label", item["channel"]),
            "{{date}}": date,
            "{{time_window}}": item.get("time_window", ""),
            "{{status_display}}": status_display,
            "{{scope_key}}": str(item.get("scope_key", f"{item['channel']}:unknown")),
            "{{scope_type}}": str(item.get("scope_type", "unknown")),
            "{{participant_shape}}": str(item.get("participant_shape", "unknown")),
            "{{bot_count}}": str(item.get("bot_count", 0)),
            "{{session_count}}": str(item.get("session_count", len(item.get("source_refs") or []))),
            "{{source_refs}}": ", ".join(item.get("source_refs") or ["无"]),
            "{{summary_points}}": bullets(item.get("summary_points") or ["- 无可确认摘录"]),
            "{{issues}}": bullets(item.get("issues") or ["- 无"]),
            "{{wins}}": bullets(item.get("wins") or ["- 无"]),
            "{{notes}}": bullets(item.get("notes") or [f"- 状态：{item['status']}"]),
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        out_path.write_text(text, encoding="utf-8")
        written.append(str(out_path))
    print(json.dumps({"written": written}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
