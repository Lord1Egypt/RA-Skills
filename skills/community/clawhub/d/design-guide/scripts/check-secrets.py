#!/usr/bin/env python3
"""Reject likely committed credentials without matching normal prose."""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


RULES = {
    "OpenAI-style API key": re.compile(r"(?<![A-Za-z0-9])" + "sk-" + r"[A-Za-z0-9_-]{20,}(?![A-Za-z0-9])"),
    "GitHub token": re.compile(r"(?<![A-Za-z0-9])" + "gh" + r"[opusr]_[A-Za-z0-9]{20,}(?![A-Za-z0-9])"),
    "local absolute path": re.compile(r"/home/" + "Arabica" + r"(?:/|\b)"),
}

EXCLUDED_PARTS = {".git", ".codex", "__pycache__"}
EXCLUDED_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".tmp"}


def candidate_files(root: pathlib.Path) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return [root / item.decode() for item in result.stdout.split(b"\0") if item]

    files: list[pathlib.Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if relative.as_posix() == ".design-guide/profile.md":
            continue
        files.append(path)
    return sorted(files)


def scan(root: pathlib.Path) -> list[str]:
    findings: list[str] = []
    for path in candidate_files(root):
        relative = path.relative_to(root).as_posix()
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(content.splitlines(), 1):
            for label, pattern in RULES.items():
                if pattern.search(line):
                    findings.append(f"{relative}:{line_number}: {label}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=t("Scan tracked files for likely credentials and local paths."))
    add_locale_argument(parser)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    findings = scan(root)
    if findings:
        print(t("Potential secret or local-path leakage:", args.locale))
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(t("Secret and local-path scan: OK", args.locale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
