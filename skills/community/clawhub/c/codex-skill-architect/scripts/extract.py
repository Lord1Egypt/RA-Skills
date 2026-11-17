#!/usr/bin/env python3
"""Extract marked sections from SKILL.md and replace them with a short marker."""

import argparse
import json
from pathlib import Path


def find_block(lines, start_marker, end_marker):
    start = None
    end = None
    for index, line in enumerate(lines):
        if start is None and line.startswith(start_marker):
            start = index
        elif start is not None and line.startswith(end_marker):
            end = index
            break
    if start is None or end is None:
        raise ValueError(f"block not found: {start_marker} -> {end_marker}")
    return start, end


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--markers", action="append", help="start_marker|end_marker")
    parser.add_argument("--output", default="")
    parser.add_argument("--replace-marker", default="## 已外移说明\n\n内容已外移到独立文件。")
    parser.add_argument("--config", default="")
    args = parser.parse_args()

    skill = Path(args.skill)
    lines = skill.read_text(encoding="utf-8").splitlines(keepends=True)
    extracted_lines = 0
    outputs = 0

    if args.config:
        config = json.loads(Path(args.config).read_text(encoding="utf-8"))
        for item in config.get("sections", []):
            start, end = find_block(lines, item["start"], item["end"])
            extracted_lines += end - start
            extracted_text = "".join(lines[start:end])
            replace_marker = item.get("replace_marker", args.replace_marker).replace("\\n", "\n")
            marker = replace_marker + "\n" if not replace_marker.endswith("\n") else replace_marker
            lines[start:end] = [marker]
            output = Path(item["output"])
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(extracted_text, encoding="utf-8")
            outputs += 1
    else:
        if not args.markers or not args.output:
            raise SystemExit("Use --markers/--output or --config")
        replace_marker = args.replace_marker.replace("\\n", "\n")
        for spec in args.markers:
            start_marker, end_marker = spec.split("|", 1)
            start, end = find_block(lines, start_marker, end_marker)
            extracted_lines += end - start
            extracted_text = "".join(lines[start:end])
            marker = replace_marker + "\n" if not replace_marker.endswith("\n") else replace_marker
            lines[start:end] = [marker]
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(extracted_text, encoding="utf-8")
        outputs = 1

    skill.write_text("".join(lines), encoding="utf-8")
    print(f"extracted_lines={extracted_lines}")
    print(f"outputs={outputs}")


if __name__ == "__main__":
    main()
