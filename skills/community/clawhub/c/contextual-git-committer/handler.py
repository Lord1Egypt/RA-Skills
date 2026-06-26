#!/usr/bin/env python3
"""Contextual Git-Committer — Gathers staged changes and workspace context for AI-powered commit message generation."""

import argparse
import os
import re
import subprocess
import sys


def run_git(*args):
    """Run a git command and return its stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def get_staged_diff():
    """Return the staged diff, or None if nothing is staged."""
    return run_git("diff", "--cached")


def get_recent_commits(count=5):
    """Return recent commit messages for style reference."""
    output = run_git("log", f"--max-count={count}", "--pretty=format:%s")
    if output:
        return output.split("\n")
    return []


def get_changed_files():
    """Return a list of staged files with their status."""
    output = run_git("diff", "--cached", "--name-status")
    if not output:
        return []
    files = []
    for line in output.split("\n"):
        if line.strip():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                files.append({"status": parts[0], "file": parts[1]})
            else:
                files.append({"status": "M", "file": parts[0]})
    return files


def get_diff_stats():
    """Return a shortstat summary of staged changes."""
    return run_git("diff", "--cached", "--shortstat")


def parse_modified_functions(diff_text):
    """Extract function/method names that were modified in the diff."""
    functions = set()
    # Match hunk headers that show function context
    # Format: @@ -l,s +l,s @@ function_name
    pattern = r"@@[^@]+@@\s+(.+)"
    for match in re.finditer(pattern, diff_text):
        ctx = match.group(1).strip()
        if ctx:
            # Take the first identifier (function/class name)
            parts = re.split(r"\s", ctx, maxsplit=1)
            name = parts[0].strip()
            if name and not name.startswith("("):
                functions.add(name)
    return sorted(functions)


def get_terminal_history(count=10):
    """Read recent terminal history from common shell history files."""
    home = os.path.expanduser("~")
    history_files = [
        os.path.join(home, ".bash_history"),
        os.path.join(home, ".zsh_history"),
    ]

    lines = []
    for hf in history_files:
        if os.path.isfile(hf):
            try:
                with open(hf, "r", errors="replace") as f:
                    all_lines = f.readlines()
                # zsh history has timestamps: ": 1234567890:0;command"
                cleaned = []
                for line in all_lines:
                    line = line.strip()
                    # Strip zsh timestamp prefix
                    if line.startswith(":"):
                        match = re.match(r":\s*\d+:\d+;(.+)", line)
                        if match:
                            line = match.group(1)
                    if line:
                        cleaned.append(line)
                lines.extend(cleaned)
            except OSError:
                continue

    # Return the most recent unique commands
    seen = set()
    unique = []
    for line in reversed(lines):
        if line not in seen:
            seen.add(line)
            unique.append(line)
        if len(unique) >= count:
            break

    return list(reversed(unique))


def get_branch_name():
    """Return the current branch name."""
    return run_git("rev-parse", "--abbrev-ref", "HEAD")


def format_changed_files_table(files):
    """Format the changed files list as a markdown table."""
    if not files:
        return "No files staged."

    status_map = {
        "A": "Added",
        "M": "Modified",
        "D": "Deleted",
        "R": "Renamed",
        "C": "Copied",
        "T": "Type change",
    }

    lines = ["| Status | File |", "|--------|------|"]
    for f in files:
        label = status_map.get(f["status"], f["status"])
        lines.append(f"| {label} | `{f['file']}` |")
    return "\n".join(lines)


def format_output(diff_text, style="conventional", scope=None):
    """Format the gathered context into structured markdown for the AI."""
    files = get_changed_files()
    stats = get_diff_stats()
    commits = get_recent_commits()
    functions = parse_modified_functions(diff_text)
    history = get_terminal_history()
    branch = get_branch_name()

    sections = []

    # Header
    header = "## Git Context for Commit Message Generation\n"
    if branch:
        header += f"\n**Branch:** `{branch}`\n"
    if stats:
        header += f"**Summary:** {stats}\n"
    if style:
        header += f"**Preferred style:** {style}\n"
    if scope:
        header += f"**Scope:** {scope}\n"
    sections.append(header)

    # Changed files
    sections.append("### Staged Files\n" + format_changed_files_table(files))

    # Modified functions
    if functions:
        fn_list = ", ".join(f"`{f}`" for f in functions)
        sections.append(f"### Functions/Sections Modified\n{fn_list}")

    # Diff content (truncated for large diffs)
    if len(diff_text) > 8000:
        sections.append(
            "### Staged Diff (truncated)\n```\n"
            + diff_text[:8000]
            + "\n... (truncated)\n```"
        )
    else:
        sections.append("### Staged Diff\n```\n" + diff_text + "\n```")

    # Recent terminal history
    if history:
        hist_lines = []
        for cmd in history:
            hist_lines.append(f"- `{cmd}`")
        sections.append("### Recent Terminal History\n" + "\n".join(hist_lines))

    # Recent commits for style reference
    if commits:
        commit_lines = []
        for c in commits:
            commit_lines.append(f"- {c}")
        sections.append(
            "### Recent Commits (for style reference)\n" + "\n".join(commit_lines)
        )

    return "\n\n".join(sections)


def cmd_suggest_commit(args):
    """Handle the suggest-commit command."""
    # Check we're in a git repo
    if run_git("rev-parse", "--is-inside-work-tree") is None:
        print("Error: Not inside a Git repository. Please run this from a Git project.")
        sys.exit(1)

    # Get staged diff
    diff_text = get_staged_diff()

    if not diff_text:
        print(
            "No staged changes found.\n\n"
            "Stage your changes first with:\n"
            "  `git add <file>` — stage specific files\n"
            "  `git add -p` — stage interactively by hunk\n\n"
            "Then run suggest_commit again to generate messages."
        )
        sys.exit(0)

    output = format_output(diff_text, style=args.style, scope=args.scope)
    print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Contextual Git-Committer — AI-powered commit message generator"
    )
    subparsers = parser.add_subparsers(dest="command")

    # suggest-commit command
    suggest = subparsers.add_parser(
        "suggest-commit", help="Analyze staged changes and suggest commit messages"
    )
    suggest.add_argument(
        "--style",
        default="conventional",
        choices=["conventional", "detailed"],
        help="Message style preference (default: conventional)",
    )
    suggest.add_argument(
        "--scope",
        default=None,
        help="Module or area being updated (e.g., 'auth', 'api')",
    )

    args = parser.parse_args()

    if args.command == "suggest-commit":
        cmd_suggest_commit(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
