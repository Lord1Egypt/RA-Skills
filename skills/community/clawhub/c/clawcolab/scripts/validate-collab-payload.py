#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

SUSPICIOUS_PATTERNS = {
    "api_key": re.compile(r"(?i)(api[_-]?key|secret[_-]?key)\s*[:=]\s*\S+"),
    "token": re.compile(r"(?i)(token|bearer)\s*[:=]\s*\S+"),
    "password": re.compile(r"(?i)password\s*[:=]\s*\S+"),
    "private_key": re.compile(r"-----BEGIN (RSA|EC|OPENSSH|DSA)? ?PRIVATE KEY-----"),
    "ssh_alias": re.compile(r"(?im)^\s*host\s+\S+\s*$"),
}


def scan_text(text: str):
    findings = []
    for name, pattern in SUSPICIOUS_PATTERNS.items():
        for match in pattern.finditer(text):
            snippet = match.group(0)[:160].replace("\n", " ")
            findings.append((name, snippet))
    return findings


def main():
    parser = argparse.ArgumentParser(description="Scan collaboration payloads for likely sensitive content.")
    parser.add_argument("paths", nargs="+", help="Files to scan")
    args = parser.parse_args()

    total = 0
    for raw in args.paths:
        path = Path(raw)
        if not path.exists() or not path.is_file():
            print(f"SKIP {path}: not a file", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        findings = scan_text(text)
        if findings:
            print(f"FAIL {path}")
            for name, snippet in findings:
                print(f"  - {name}: {snippet}")
            total += len(findings)
        else:
            print(f"OK   {path}")

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
