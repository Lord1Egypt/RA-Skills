#!/usr/bin/env python3
"""
Overflow Truncator — handles large command output to prevent context overflow.

When stdout exceeds MAX_LINES, this script:
1. Returns the first SHOW_HEAD lines (context anchor)
2. Truncates the middle with a clear marker
3. Returns the last SHOW_TAIL lines (recent context)
4. Writes the full output to a temp file for later inspection

Usage:
    python3 truncator.py < <large_output>
    echo "$output" | python3 truncator.py [--lines N]

Exit codes:
    0 — output was passed through (no truncation needed)
    1 — output was truncated, temp file created
"""

import sys
import os
import tempfile
import argparse

DEFAULT_MAX_LINES = 200
SHOW_HEAD = 50
SHOW_TAIL = 20


def truncate_output(stdout: str, max_lines: int = DEFAULT_MAX_LINES) -> tuple[str, str | None]:
    """
    Truncate output if it exceeds max_lines.

    Args:
        stdout: The raw string output to potentially truncate
        max_lines: Threshold for truncation (default: 200)

    Returns:
        (processed_output, temp_file_path or None)
        If temp_file_path is not None, full output was written there.
    """
    lines = stdout.splitlines()
    temp_path = None

    if len(lines) <= max_lines:
        return stdout, None

    # Build truncated output
    head_lines = lines[:SHOW_HEAD]
    tail_lines = lines[-SHOW_TAIL:]
    truncated_count = len(lines) - SHOW_HEAD - SHOW_TAIL

    head = "\n".join(head_lines)
    tail = "\n".join(tail_lines)
    truncated_marker = (
        f"\n[... {truncated_count} lines truncated ...]\n"
        f"[Full output: see <tempfile>]"
    )

    # Write full output to temp file
    fd, temp_path = tempfile.mkstemp(prefix="cli_trunc_", suffix=".txt")
    try:
        os.write(fd, stdout.encode("utf-8", errors="replace"))
    finally:
        os.close(fd)

    truncated_output = f"{head}\n{truncated_marker}\n{tail}"

    return truncated_output, temp_path


def main():
    parser = argparse.ArgumentParser(description="Truncate large command output")
    parser.add_argument(
        "--lines", "-n", type=int, default=DEFAULT_MAX_LINES,
        help=f"Max lines before truncation (default: {DEFAULT_MAX_LINES})"
    )
    parser.add_argument(
        "--show-head", type=int, default=SHOW_HEAD,
        help=f"Lines to show at start (default: {SHOW_HEAD})"
    )
    parser.add_argument(
        "--show-tail", type=int, default=SHOW_TAIL,
        help=f"Lines to show at end (default: {SHOW_TAIL})"
    )
    args = parser.parse_args()

    # Read all of stdin
    stdout = sys.stdin.read()

    truncated, temp_path = truncate_output(stdout, max_lines=args.lines)

    # Write processed output to stdout
    if temp_path:
        # Show the truncated version
        sys.stdout.write(truncated)
        # Add the temp file reference as stderr message
        print(f"\n[Full output ({len(stdout.splitlines())} lines) written to: {temp_path}]", file=sys.stderr)
        sys.exit(1)
    else:
        sys.stdout.write(truncated)
        sys.exit(0)


if __name__ == "__main__":
    main()
