#!/usr/bin/env python3
"""Check whether common Chinese official-document fonts appear installed on Windows."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


REQUIRED = [
    "方正小标宋简体",
    "仿宋_GB2312",
    "楷体_GB2312",
    "黑体",
    "宋体",
]

HINTS = {
    "方正小标宋简体": ["小标宋", "FZXiaoBiaoSong", "FZXBS", "方正小标宋"],
    "仿宋_GB2312": ["仿宋", "FangSong", "仿宋_GB2312"],
    "楷体_GB2312": ["楷体", "KaiTi", "楷体_GB2312"],
    "黑体": ["黑体", "SimHei"],
    "宋体": ["宋体", "SimSun"],
}


def scan_fonts(font_dir: Path) -> dict:
    files = []
    if font_dir.exists():
        files = [p.name for p in font_dir.iterdir() if p.is_file()]
    joined = "\n".join(files).lower()
    results = {}
    for font in REQUIRED:
        hints = HINTS[font]
        matched = [name for name in files if any(hint.lower() in name.lower() for hint in hints)]
        results[font] = {"found": bool(matched), "matches": matched[:10]}
        if not matched and any(hint.lower() in joined for hint in hints):
            results[font]["found"] = True
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", default=os.environ.get("WINDIR", r"C:\Windows") + r"\Fonts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = scan_fonts(Path(args.font_dir))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    for font, info in result.items():
        mark = "FOUND" if info["found"] else "MISSING"
        matches = ", ".join(info["matches"]) if info["matches"] else "-"
        print(f"[{mark}] {font}: {matches}")


if __name__ == "__main__":
    main()
