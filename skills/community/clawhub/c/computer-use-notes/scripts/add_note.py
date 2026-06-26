#!/usr/bin/env python3
import argparse
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MEM_DIR = ROOT / "memory"
RAW = MEM_DIR / "computer-use-notes.jsonl"
BOARD = MEM_DIR / "computer-use-notes.md"

CATS = ["can-do", "partial", "cannot-do"]
TITLES = {
    "can-do": "能做（Can Do）",
    "partial": "部分能做（Partial）",
    "cannot-do": "不能做（Cannot Do）",
}


def load_entries():
    items = []
    if RAW.exists():
        for line in RAW.read_text(encoding="utf-8").splitlines():
            if line.strip():
                items.append(json.loads(line))
    return items


def rebuild_board(entries):
    lines = ["# Computer Use 能力记录", ""]
    lines.append(f"更新于：{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    for cat in CATS:
        lines.append(f"## {TITLES[cat]}")
        subset = [e for e in entries if e.get("category") == cat]
        if not subset:
            lines.append("- （暂无）")
        else:
            for e in subset[-200:]:
                lines.append(f"- [{e['time']}] {e['note']}")
        lines.append("")
    BOARD.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True, choices=CATS)
    p.add_argument("--note", required=True)
    args = p.parse_args()

    MEM_DIR.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {"time": now, "category": args.category, "note": args.note.strip()}

    with RAW.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    entries = load_entries()
    rebuild_board(entries)
    print(json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    main()
