#!/usr/bin/env python3
"""Statically audit Dataify integration source files for unsafe patterns."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


RULES = (
    ("command_line_token", "error", re.compile(r"add_argument\([^\n]*['\"]--(?:api-)?token['\"]", re.I), "Read DATAIFY_API_TOKEN from the environment."),
    ("legacy_token_name", "error", re.compile(r"\bDATAIFY_TOKEN\b"), "Use DATAIFY_API_TOKEN consistently."),
    ("literal_bearer", "error", re.compile(r"Bearer\s+[A-Za-z0-9_-]{16,}"), "Remove credential literals from source."),
    ("unbounded_polling", "warning", re.compile(r"while\s+True\s*:", re.I), "Bound polling by timeout and return recovery state."),
    ("subprocess_default_encoding", "warning", re.compile(r"subprocess\.run\([^\n]*text=True(?![^\n]*encoding=)", re.I), "Decode subprocess output explicitly as UTF-8."),
    ("task_id_only", "warning", re.compile(r"return\s+[^\n]*task_id(?![^\n]*(result|data))", re.I), "Wait for completion and return the final result by default."),
)


def audit_text(text: str, filename: str) -> list[dict]:
    findings = []
    for code, severity, pattern, remediation in RULES:
        for match in pattern.finditer(text):
            findings.append({
                "code": code,
                "severity": severity,
                "file": filename,
                "line": text.count("\n", 0, match.start()) + 1,
                "remediation": remediation,
            })
    return findings


def paths(values: list[str]) -> list[Path]:
    result = []
    for value in values:
        path = Path(value)
        if path.is_dir():
            result.extend(item for item in path.rglob("*") if item.suffix.lower() in {".py", ".js", ".ts", ".go", ".sh"})
        elif path.is_file():
            result.append(path)
    return sorted(set(result))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    findings = []
    for path in paths(args.targets):
        try:
            findings.extend(audit_text(path.read_text(encoding="utf-8", errors="replace"), str(path)))
        except OSError as exc:
            findings.append({"code": "read_error", "severity": "error", "file": str(path), "line": 0, "remediation": str(exc)})
    result = {"files": len(paths(args.targets)), "findings": findings, "errors": sum(item["severity"] == "error" for item in findings)}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print("{severity} {file}:{line} {code} — {remediation}".format(**item))
        print("Audited {} files; {} findings.".format(result["files"], len(findings)))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
