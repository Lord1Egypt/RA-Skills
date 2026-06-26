#!/usr/bin/env python3
"""
Patches an existing anthropic-report.py to use the new format_report().

Reads the reference implementation from format_report.py (same directory)
and replaces the existing format_report function in the target file.

Usage:
  python3 patch_format.py /usr/local/bin/anthropic-report.py
  python3 patch_format.py --dry-run /usr/local/bin/anthropic-report.py
"""

import sys
import shutil
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def load_new_format():
    """Load format_report.py and extract from CLI_THRESHOLD to end."""
    source = (SCRIPT_DIR / "format_report.py").read_text()
    lines = source.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.startswith("CLI_THRESHOLD"):
            start = i
            break
    if start is None:
        print("ERROR: Cannot find CLI_THRESHOLD in format_report.py")
        sys.exit(1)
    return "\n".join(lines[start:])


def patch(target_path: str, dry_run: bool = False):
    target = Path(target_path)
    if not target.exists():
        print(f"ERROR: {target} not found")
        sys.exit(1)

    content = target.read_text()
    new_func = load_new_format()

    # Find existing format_report block (may include CLI_THRESHOLD or HIGH_OUTPUT_THRESHOLD)
    patterns = [
        r'(# ── (?:Format|CLI).*?\n)?(?:(?:CLI_THRESHOLD|HIGH_OUTPUT_THRESHOLD).*?\n\n)?def format_report\(date_str.*?(?=\ndef [a-z_]+\()',
        r'def format_report\(date_str.*?(?=\ndef [a-z_]+\()',
    ]

    match = None
    for pat in patterns:
        match = re.search(pat, content, re.DOTALL)
        if match:
            break

    if not match:
        print("ERROR: Cannot find format_report function in target")
        sys.exit(1)

    replacement = (
        "# ── Format report ───────────────────────────────────────\n\n"
        + new_func
        + "\n\n"
    )
    new_content = content[:match.start()] + replacement + content[match.end():]

    # Remove duplicate threshold constants if any
    new_content = re.sub(
        r'\nCLI_THRESHOLD = \d+\s*\n(?=.*HIGH_OUTPUT_THRESHOLD)',
        '\n', new_content, count=1, flags=re.DOTALL
    )

    if dry_run:
        print("=== DRY RUN ===")
        print(f"Would replace {len(match.group())} chars in {target}")
        print(f"New function preview:\n{new_func[:300]}...")
    else:
        backup = target.with_suffix(".py.pre-format-patch")
        shutil.copy2(target, backup)
        print(f"Backup: {backup}")
        target.write_text(new_content)
        print(f"Patched: {target}")
        print(f"Test: python3 {target}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print(f"Usage: {sys.argv[0]} [--dry-run] /path/to/anthropic-report.py")
        sys.exit(1)

    patch(args[0], dry_run="--dry-run" in flags)
