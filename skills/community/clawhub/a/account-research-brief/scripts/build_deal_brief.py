#!/usr/bin/env python3
"""Account Research Brief

Turns raw notes into a structured digest for account research brief.

Parameters for this build:
{
  "sections": [
    "deal_context",
    "key_facts",
    "risks",
    "open_questions",
    "next_step",
    "sources"
  ]
}

Usage:
    python3 account_research_brief.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Account Research Brief"


def read_flat(path):
    """Read a small YAML-ish file: `key: value`, `- item` lists, '#' comments."""
    data, key = {}, None
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}")
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" in stripped:
            name, _, value = stripped.partition(":")
            name, value = name.strip(), value.strip().strip('"').strip("'")
            if value == "":
                data[name] = []
                key = name
            else:
                data[name] = value
                key = None
    return data


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_out(out_dir, name, lines):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {path}")
    return path


SECTIONS = ["deal_context", "key_facts", "risks", "open_questions", "next_step", "sources"]


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("#"):
            current = line.lstrip("#").strip()
            blocks.append((current, []))
        elif blocks:
            blocks[-1][1].append(line.rstrip())
    report = [f"# {TITLE} digest", "", f"source: {input_path}", ""]
    for section in SECTIONS:
        report.append(f"## {section}")
        found = False
        for name, body in blocks:
            if section.lower() in name.lower():
                found = True
                for line in body:
                    if line.strip():
                        report.append(f"- {line.strip()}")
        if not found:
            report.append(f"- (no notes for {section})")
        report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never build a per-deal brief from personal social profiles, leaked databases or bought contact data.", "Never present a fact without its source URL and the date it was checked.", "Never turn the brief into a targeting list; it covers one live deal only."]:
        report.append(f"- {rule}")
    write_out(out_dir, "digest.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
