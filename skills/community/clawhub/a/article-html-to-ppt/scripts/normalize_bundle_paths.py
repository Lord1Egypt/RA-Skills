#!/usr/bin/env python3
"""Rewrite local absolute workspace paths in bundle evidence files to bundle-relative paths.

QA reports, render reports, build manifests, and state files record the absolute
path of every artefact they inspected. Those paths are correct on the machine
that produced them and leak the author's home directory everywhere else, so a
bundle must be normalized before it is distributed.

This script is the enforcement partner of `scripts/audit_bundle.py`: audit
detects the leak, this script fixes it. It only rewrites text-like evidence
files (JSON and Markdown); it never touches PPTX, PDF, or PNG payloads.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Deliberate exceptions are declared once, in the same document the bundle audit
# uses, so a file is never exempt from the audit but flagged by the normalizer.
DEFAULT_ALLOWLIST = ROOT / "packaging" / "audit-allowlist.json"
ALLOWED_CODE = "BUNDLE_ABSOLUTE_PATH_LEAK"

# Text formats that may carry recorded artefact paths. Binary deliverables are
# deliberately excluded: a path inside a PPTX is part of the rendered document,
# not bundle metadata.
TEXT_SUFFIXES = {".json", ".md", ".txt", ".log", ".yml", ".yaml"}

# Directories that are never rewritten. node_modules is vendored third-party
# code, and .git history must not be mutated by a packaging step.
SKIP_DIRS = {"node_modules", ".git"}

# Absolute workspace prefixes seen in practice. Each pattern captures the
# author's workspace root up to and including the pack directory, so the
# replacement collapses it to a bundle-relative "./".
#
# Example:
#   /Users/alice/.openclaw/workspace/private-artifacts/pptsmith-pmo-consulting-pack/qa/x.json
#   -> ./qa/x.json
WORKSPACE_PREFIX_PATTERNS = (
    # macOS / Linux agent workspace layouts.
    re.compile(r"/(?:Users|home)/[^/\"'\s]+/\.openclaw/workspace/[^/\"'\s]*/[^/\"'\s]*/"),
    re.compile(r"/(?:Users|home)/[^/\"'\s]+/\.openclaw/workspace/[^/\"'\s]*/"),
    # Windows agent workspace layouts.
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\"'\s]+\\\\\.openclaw\\\\workspace\\\\(?:[^\\\\\"'\s]+\\\\)+"),
)

# Any remaining home-directory prefix that is not an agent workspace. These are
# reported rather than rewritten, because collapsing them to "./" could produce
# a wrong relative path.
RESIDUAL_HOME = re.compile(r"(?:/(?:Users|home)/[^/\"'\s]+|[A-Za-z]:\\\\Users\\\\[^\\\\\"'\s]+)")


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if SKIP_DIRS.intersection(path.relative_to(root).parts):
            continue
        files.append(path)
    return files


def load_allowed_paths(allowlist: Path) -> set[str]:
    """Return the bundle-relative paths allowed to contain an absolute path literal."""
    if not allowlist.exists():
        return set()
    document = json.loads(allowlist.read_text(encoding="utf-8"))
    allowed: set[str] = set()
    for entry in document.get("allowlist", []) or []:
        if isinstance(entry, dict) and ALLOWED_CODE in (entry.get("codes") or []):
            target = str(entry.get("path", "")).strip()
            if target:
                allowed.add(target)
    return allowed


def normalize_text(text: str) -> tuple[str, int]:
    total = 0
    for pattern in WORKSPACE_PREFIX_PATTERNS:
        text, count = pattern.subn("./", text)
        total += count
    return text, total


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Rewrite local absolute workspace paths in bundle evidence files to bundle-relative paths.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Bundle root to normalize (default: repository root).")
    parser.add_argument("--allowlist", type=Path, default=DEFAULT_ALLOWLIST, help="Shared exception document; entries carrying BUNDLE_ABSOLUTE_PATH_LEAK are skipped.")
    parser.add_argument("--check", action="store_true", help="Report what would change and exit non-zero if anything would; do not write.")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    allowed = load_allowed_paths(args.allowlist if args.allowlist.is_absolute() else root / args.allowlist)
    changed: list[tuple[Path, int]] = []
    residual: list[tuple[Path, str]] = []
    skipped: list[Path] = []

    for path in iter_text_files(root):
        relative = path.relative_to(root)
        if relative.as_posix() in allowed:
            skipped.append(relative)
            continue
        original = path.read_text(encoding="utf-8", errors="ignore")
        normalized, count = normalize_text(original)
        if count:
            changed.append((relative, count))
            if not args.check:
                path.write_text(normalized, encoding="utf-8")
        leftover = RESIDUAL_HOME.search(normalized)
        if leftover:
            residual.append((relative, leftover.group(0)))

    for rel, count in changed:
        verb = "would rewrite" if args.check else "rewrote"
        print(f"{verb} {count} path(s): {rel}")
    for rel, sample in residual:
        print(f"RESIDUAL_HOME_PATH {rel}: {sample}", file=sys.stderr)

    print(f"files scanned under {root}: {len(iter_text_files(root))}; files changed: {len(changed)}; allowlisted: {len(skipped)}; residual leaks: {len(residual)}")

    if residual:
        return 1
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
