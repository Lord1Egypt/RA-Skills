#!/usr/bin/env python3
"""Build a routing index from SKILL.md files under a pack directory."""

import argparse
import os
import re
from pathlib import Path


def first_heading(path):
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.parent.name


def section_headings(path):
    headings = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if re.match(r"^## ", line):
            headings.append(line[3:].strip())
    return headings[:6]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--root", default=str(Path.cwd()))
    args = parser.parse_args()

    pack_dir = Path(args.pack_dir)
    index = Path(args.index)
    root = Path(args.root)
    packs = sorted(pack_dir.rglob("SKILL.md"))
    lines = [
        "# Skill Routing Index",
        "",
        f"- Generated: {len(packs)} skill packs",
        "",
    ]
    for pack in packs:
        rel = os.path.relpath(pack, root)
        title = first_heading(pack)
        sections = "；".join(section_headings(pack))
        lines.append(f"- {title}：`{rel}`；核心章节：{sections}")

    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"packs={len(packs)}")
    print(f"index={index}")


if __name__ == "__main__":
    main()
