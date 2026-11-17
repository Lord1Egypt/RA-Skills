#!/usr/bin/env python3
"""Appointment Scheduling Rules

Flags US compliance risks in a draft for appointment scheduling rules.

Parameters for this build:
{
  "rules": [
    {
      "label": "possible missing commercial email opt-out",
      "pattern": "(?i)(no opt out|do not reply|no way to stop)"
    },
    {
      "label": "no sender postal address in the footer",
      "pattern": "(?i)(contact us at|our website|email us at)"
    },
    {
      "label": "guaranteed outcome claim in the copy",
      "pattern": "(?i)(we promise|always available|guaranteed)"
    },
    {
      "label": "unapproved cancellation fee or waiver",
      "pattern": "(?i)(no fee|free cancel|waive|waived)"
    },
    {
      "label": "clinical detail inside a reminder",
      "pattern": "(?i)(diagnos|test result|medication|symptom|treatment)"
    },
    {
      "label": "customer detail left in a shared template",
      "pattern": "(?i)(dear [A-Z][a-z]+|patient name|account number|customer name)"
    }
  ]
}

Usage:
    python3 appointment_scheduling_rules.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Appointment Scheduling Rules"


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


RULES = [{"label": "possible missing commercial email opt-out", "pattern": "(?i)(no opt out|do not reply|no way to stop)"}, {"label": "no sender postal address in the footer", "pattern": "(?i)(contact us at|our website|email us at)"}, {"label": "guaranteed outcome claim in the copy", "pattern": "(?i)(we promise|always available|guaranteed)"}, {"label": "unapproved cancellation fee or waiver", "pattern": "(?i)(no fee|free cancel|waive|waived)"}, {"label": "clinical detail inside a reminder", "pattern": "(?i)(diagnos|test result|medication|symptom|treatment)"}, {"label": "customer detail left in a shared template", "pattern": "(?i)(dear [A-Z][a-z]+|patient name|account number|customer name)"}]


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    report = [f"# {TITLE} compliance check", "", f"source: {input_path}", ""]
    hits = []
    for number, line in enumerate(lines, 1):
        low = line.lower()
        for rule in RULES:
            pattern = str(rule.get("pattern", "")).lower()
            if pattern and pattern in low:
                hits.append((number, rule.get("label", pattern), line.strip()[:120]))
    if hits:
        report.append("## Flags")
        for number, label, snippet in hits:
            report.append(f"- line {number} - {label}: {snippet}")
    else:
        report.append("## No flags")
    report.append("")
    report.append("A flag is a prompt for a human, not a verdict. Fix the wording, then re-run.")
    report.append("")
    report.append("## Guardrails to keep")
    for rule_text in ["Never send a reminder, a confirmation or a no-show notice; the business sends the message from its own system.", "Never put a customer name, phone number, email address or appointment detail into a shared policy or checklist file.", "Never quote a cancellation fee, a deposit amount or a waiver the business has not approved, and never waive one for a customer."]:
        report.append(f"- {rule_text}")
    write_out(out_dir, "compliance-check.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
