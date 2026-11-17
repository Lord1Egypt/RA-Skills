#!/usr/bin/env python3
"""Audit a SKILL.md and report large sections that may be externalized."""

import argparse
import re
from pathlib import Path


def section_stats(text):
    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        if re.match(r"^#{1,4} ", line):
            headings.append((index, line.strip()))
    sections = []
    for i, (start, heading) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end])
        sections.append(
            {
                "heading": heading,
                "start": start + 1,
                "end": end,
                "lines": end - start,
                "chars": len(body),
                "cjk": len(re.findall(r"[\u4e00-\u9fff]", body)),
            }
        )
    return lines, sections


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--threshold", type=int, default=50)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    path = Path(args.skill)
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines, sections = section_stats(text)
    candidates = [s for s in sections if s["lines"] >= args.threshold]

    report = [
        f"# Skill Architect Audit",
        "",
        f"- SKILL: {path}",
        f"- Total lines: {len(lines)}",
        f"- Sections: {len(sections)}",
        f"- Candidate externalizable sections (>= {args.threshold} lines): {len(candidates)}",
        "",
        "## Candidates",
        "",
        "| Lines | Heading | Start | End | CJK |",
        "| ---: | --- | ---: | ---: | ---: |",
    ]
    for section in candidates:
        report.append(
            f"| {section['lines']} | {section['heading']} | {section['start']} | {section['end']} | {section['cjk']} |"
        )
    report_text = "\n".join(report) + "\n"

    if args.output:
        Path(args.output).write_text(report_text, encoding="utf-8")
    print(report_text)


if __name__ == "__main__":
    main()
