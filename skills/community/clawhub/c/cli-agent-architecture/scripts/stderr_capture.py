#!/usr/bin/env python3
"""
stderr Capture — formats and attaches stderr to failed command output.

When a command fails, the LLM needs to see what went wrong. This script:
1. Accepts stderr content (via stdin or --stderr flag)
2. Formats it with clear delimiters
3. Truncates to MAX_LINES to avoid flooding context
4. Returns a structured block the LLM can parse

Usage:
    python3 stderr_capture.py < <stderr_data>
    echo "$stderr" | python3 stderr_capture.py [--command "grep foo"]
    python3 stderr_capture.py --stderr "$stderr" --command "ls /nonexistent"

Exit codes:
    0 — stderr was empty/no content
    1 — stderr captured and formatted successfully
"""

import sys
import argparse

DEFAULT_MAX_LINES = 30


def format_stderr_attachment(
    stderr: str,
    command: str = "",
    max_lines: int = DEFAULT_MAX_LINES
) -> str:
    """
    Format stderr for display when a command fails.

    Args:
        stderr: Raw stderr content
        command: The command that produced this stderr (optional, for context)
        max_lines: Maximum stderr lines to include (default: 30)

    Returns:
        Formatted string with delimiters, or empty string if stderr was empty
    """
    if not stderr or not stderr.strip():
        return ""

    lines = stderr.strip().splitlines()

    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["[... additional stderr truncated ...]"]

    header = "--- stderr ---"
    if command:
        header += f" (command: {command})"

    footer = "--- end stderr ---"

    return "\n".join([""] + [header] + lines + [footer, ""])


def format_failure_result(
    stdout: str,
    stderr: str,
    exit_code: int,
    command: str = "",
    duration: float = 0.0,
    truncated_path: str = None
) -> str:
    """
    Format a complete failure response for the LLM.

    Args:
        stdout: Command stdout
        stderr: Command stderr
        exit_code: Command exit code
        command: The command string (optional)
        duration: Execution duration in seconds (optional)
        truncated_path: Path to full output if truncated (optional)

    Returns:
        Complete formatted failure response
    """
    parts = []

    if duration > 0:
        parts.append(f"[exit:{exit_code} | {duration:.2f}s]")
    else:
        parts.append(f"[exit:{exit_code}]")

    if truncated_path:
        parts.append(f"[output truncated — full content: see {truncated_path}]")

    stderr_attachment = format_stderr_attachment(stderr, command)
    if stderr_attachment:
        parts.append(stderr_attachment)

    if not stdout.strip() and not stderr.strip():
        parts.append("(no output produced)")

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Capture and format stderr on command failure")
    parser.add_argument(
        "--stderr", "-e", type=str, default=None,
        help="stderr content (if not reading from stdin)"
    )
    parser.add_argument(
        "--command", "-c", type=str, default="",
        help="The command that produced this stderr (for context)"
    )
    parser.add_argument(
        "--max-lines", "-n", type=int, default=DEFAULT_MAX_LINES,
        help=f"Max stderr lines to include (default: {DEFAULT_MAX_LINES})"
    )
    args = parser.parse_args()

    # Get stderr content
    if args.stderr is not None:
        stderr = args.stderr
    else:
        stderr = sys.stdin.read()

    formatted = format_stderr_attachment(stderr, args.command, args.max_lines)

    if formatted:
        sys.stdout.write(formatted)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
