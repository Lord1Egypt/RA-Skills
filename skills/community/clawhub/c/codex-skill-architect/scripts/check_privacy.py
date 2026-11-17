#!/usr/bin/env python3
"""Scan a release directory for common privacy risks."""

import argparse
import re
from pathlib import Path


USERS_PATH = "/" + "Users" + "/"
WINDOWS_USERS_PATH = "C:" + "\\Users\\"
HOME_PATH = "/" + "home" + "/"

PATTERNS = [
    (rf"(?i){USERS_PATH}", "macOS absolute home path"),
    (rf"(?i){re.escape(WINDOWS_USERS_PATH)}", "Windows absolute home path"),
    (rf"(?i){HOME_PATH}", "Linux absolute home path"),
    (r"~[\\/]\.codex", "Codex private config path"),
    (r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", "email address"),
    (r"(?<!\d)1[3-9]\d{9}(?!\d)", "mainland China mobile number"),
    (r"\b[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b", "mainland China ID number"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path.cwd()))
    args = parser.parse_args()

    root = Path(args.root).resolve()
    issues = []
    scanned = 0

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "check_privacy.py":
            continue
        if any(part in {".git", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in {".zip", ".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scanned += 1

        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern, label in PATTERNS:
                if re.search(pattern, line):
                    issues.append((path.relative_to(root), lineno, label, line.strip()[:120]))

    if issues:
        for rel, lineno, label, snippet in issues:
            print(f"{rel}:{lineno} [{label}]: {snippet}")
        print(f"scanned_files={scanned}")
        print("PRIVACY_ISSUES_FOUND")
        raise SystemExit(1)

    print(f"scanned_files={scanned}")
    print("PRIVACY_CHECK_OK")


if __name__ == "__main__":
    main()
