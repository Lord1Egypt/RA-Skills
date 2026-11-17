#!/usr/bin/env python3
"""Write a BOOK BRAIN outer reference stub (.ref.txt or .md)."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--lines", nargs="*", default=[])
    ap.add_argument("--resonance-to", help="Outer brain label for lyra-brain style edge")
    args = ap.parse_args()

    lines = [
        f"Title: {args.title}",
        f"Last updated: {datetime.now(timezone.utc).date()}",
        "",
    ]
    if args.resonance_to:
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
        lines.insert(0, f"SESSION_{day} --resonance--> {args.resonance_to}")
    for line in args.lines:
        lines.append(line)
    lines.append("")

    out = args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())