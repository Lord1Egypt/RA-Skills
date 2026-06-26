#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


def split_frontmatter(text: str):
    if text.startswith("---\n"):
        m = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
        if m:
            return m.group(1), text[m.end():]
    return "", text


def parse_yaml_simple(y: str):
    out = {}
    for line in y.splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_\-]+)\s*:\s*(.*?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def main():
    ap = argparse.ArgumentParser(description="Archive old stale memory logs (forget via downgrade/archive)")
    ap.add_argument("workspace", nargs="?", default=os.getcwd())
    ap.add_argument("--archive-days", type=int, default=60)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    daily = ws / "memory" / "daily"
    arch = ws / "memory" / "archive" / "raw" / "daily"
    arch.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = 0
    today = dt.date.today()

    for p in sorted(daily.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        if not m:
            continue
        d = dt.date.fromisoformat(m.group(1))
        age = (today - d).days
        if age <= args.archive_days:
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")
        fm, _ = split_frontmatter(text)
        meta = parse_yaml_simple(fm)
        status = meta.get("status", "")
        polarity = meta.get("polarity", "positive")

        # only archive stale/low-risk positives by default
        if status not in ("stale", "archived", "") or polarity == "negative":
            skipped += 1
            continue

        target = arch / p.name
        if not args.dry_run:
            shutil.move(str(p), str(target))
        moved += 1

    if not args.dry_run:
        sem = ws / "skills" / "duru-memory" / "scripts" / "memory-semantic-search.py"
        if sem.exists():
            subprocess.run(["uv", "run", "python", str(sem), "warmup", str(ws), "--build-only"], check=False, cwd=str(ws / "skills" / "duru-memory"))

    print(json.dumps({
        "workspace": str(ws),
        "archive_days": args.archive_days,
        "moved_to_archive": moved,
        "skipped": skipped,
        "dry_run": bool(args.dry_run),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
