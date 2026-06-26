#!/usr/bin/env python3
"""Move Claude Code session(s) to another project directory and update cwd references.

Usage:
    python move-session.py <session_id> <target_project_path> [--cwd-mode first|all]
    python move-session.py <id1> <id2> <target_project_path> [--cwd-mode all]

Options:
    --cwd-mode first   Only update the first cwd occurrence (default)
    --cwd-mode all     Update all cwd occurrences in the session file

Cross-platform: works on Windows (Git Bash, PowerShell, cmd) and macOS/Linux.
Handles Windows backslash paths in JSON (double-escaped \\\\) correctly.
"""

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


def get_claude_projects_dir() -> Path:
    """Get the Claude Code projects directory, cross-platform."""
    if platform.system() == "Windows":
        return Path(os.environ.get("USERPROFILE", "")) / ".claude" / "projects"
    return Path.home() / ".claude" / "projects"


def path_to_project_name(p: str) -> str:
    """Convert a filesystem path to a Claude Code project name.

    Claude Code source: H.replace(/[^a-zA-Z0-9]/g, "-")
    All non-alphanumeric characters become "-". Truncated at 200 chars + hash suffix.

    /Users/es6kr/.agents -> -Users-es6kr--agents
    /Users/es6kr/ghq/github.com/es6kr -> -Users-es6kr-ghq-github-com-es6kr
    C:\\Users\\es6kr\\.agents -> C--Users-es6kr--agents
    """
    import re

    result = re.sub(r"[^a-zA-Z0-9]", "-", p)
    if len(result) <= 200:
        return result
    # Claude Code uses abs(crc32(path)).toString(36) for hash suffix
    import zlib

    raw = zlib.crc32(p.encode())
    if raw >= (1 << 31):
        raw -= (1 << 32)
    hash_suffix = _base36(abs(raw))
    return f"{result[:200]}-{hash_suffix}"


def _base36(n: int) -> str:
    """Convert integer to base36 string."""
    if n == 0:
        return "0"
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    result = []
    while n:
        result.append(chars[n % 36])
        n //= 36
    return "".join(reversed(result))


def find_session_file(session_id: str, projects_dir: Path) -> Path | None:
    """Find a session JSONL file across all project directories."""
    if not projects_dir.is_dir():
        return None
    filename = f"{session_id}.jsonl"
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / filename
        if candidate.exists():
            return candidate
    return None


def extract_cwd_values(content: str) -> list[str]:
    """Extract unique cwd values from JSONL content."""
    import re
    return sorted(set(re.findall(r'"cwd":"([^"]*)"', content)))


def replace_cwd(content: str, old_suffix: str, mode: str) -> tuple[str, int]:
    """Replace cwd values in JSONL content.

    Args:
        content: Full file content
        old_suffix: The path suffix to remove (e.g., \\\\sub-project)
        mode: 'first' or 'all'

    Returns:
        (new_content, replacement_count)
    """
    if mode == "all":
        lines = content.split("\n")
        total = 0
        new_lines = []
        for line in lines:
            if old_suffix in line and '"cwd"' in line:
                count = line.count(old_suffix)
                line = line.replace(old_suffix, "")
                total += count
            new_lines.append(line)
        return "\n".join(new_lines), total
    else:
        # first mode: only replace in lines that contain "cwd"
        # Actually, replace the first occurrence of the full cwd pattern
        lines = content.split("\n")
        total = 0
        new_lines = []
        replaced = False
        for line in lines:
            if not replaced and old_suffix in line and '"cwd"' in line:
                line = line.replace(old_suffix, "", 1)
                total = 1
                replaced = True
            new_lines.append(line)
        return "\n".join(new_lines), total


def main():
    parser = argparse.ArgumentParser(description="Move Claude Code sessions between projects")
    parser.add_argument("args", nargs="+", help="session_id(s) followed by target_project_path")
    parser.add_argument("--cwd-mode", choices=["first", "all"], default="first",
                        help="'first' updates only the first cwd occurrence, 'all' updates every cwd (default: first)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")

    opts = parser.parse_args()

    if len(opts.args) < 2:
        parser.error("Need at least one session_id and a target_project_path")

    target_path = opts.args[-1]
    session_ids = opts.args[:-1]

    projects_dir = get_claude_projects_dir()
    target_project_name = path_to_project_name(target_path)
    target_dir = projects_dir / target_project_name

    if not opts.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for sid in session_ids:
        print(f"\n--- Session: {sid} ---")

        session_file = find_session_file(sid, projects_dir)
        if not session_file:
            print(f"  ERROR: Session file not found in {projects_dir}")
            continue

        source_project = session_file.parent.name
        print(f"  Source: {source_project}")
        print(f"  Target: {target_project_name}")

        if source_project == target_project_name:
            print("  SKIP: Already in target project")
            continue

        # Read content
        content = session_file.read_text(encoding="utf-8")

        # Extract cwd values
        cwd_values = extract_cwd_values(content)
        print(f"  Current cwd values: {cwd_values}")

        # Determine what to replace: find the suffix that differs from target
        # e.g., cwd has "...<ORG>\\<repo>", target is "...<ORG>"
        # We need to remove "\\<repo>" part

        # Normalize target path for JSON comparison
        target_normalized = target_path.replace("\\", "/").rstrip("/")

        replaced_total = 0
        for cwd_val in cwd_values:
            # Normalize cwd for comparison (JSON has double-backslash)
            cwd_normalized = cwd_val.replace("\\\\", "/")

            if cwd_normalized == target_normalized:
                continue  # Already correct

            if not cwd_normalized.startswith(target_normalized + "/"):
                # Check if target is a parent of cwd
                if target_normalized.startswith(cwd_normalized):
                    continue  # cwd is parent of target, skip
                print(f"  WARN: cwd '{cwd_val}' doesn't share prefix with target, skipping")
                continue

            # Find the suffix to remove
            suffix_normalized = cwd_normalized[len(target_normalized):]
            # Convert back to JSON-escaped form matching the original encoding
            if "\\\\" in cwd_val:
                # Windows JSON encoding: path separators stored as double-backslash
                suffix_json = suffix_normalized.replace("/", chr(92) + chr(92))
            else:
                # macOS/Linux: path separators stored as-is
                suffix_json = suffix_normalized

            print(f"  Removing suffix: {repr(suffix_json)} from cwd (mode={opts.cwd_mode})")

            if not opts.dry_run:
                content, count = replace_cwd(content, suffix_json, opts.cwd_mode)
                replaced_total += count

        if opts.dry_run:
            print(f"  DRY-RUN: Would replace cwd and move file")
            continue

        # Write updated content
        session_file.write_text(content, encoding="utf-8")

        # Verify
        new_cwd_values = extract_cwd_values(content)
        print(f"  Updated cwd values: {new_cwd_values}")
        print(f"  Replacements: {replaced_total}")

        # Move file
        dest_file = target_dir / session_file.name
        shutil.move(str(session_file), str(dest_file))
        print(f"  Moved to: {dest_file}")

        # Move subagent directory if exists
        subagent_dir = session_file.parent / sid
        if subagent_dir.is_dir():
            dest_subagent = target_dir / sid
            shutil.move(str(subagent_dir), str(dest_subagent))
            print(f"  Moved subagent dir: {dest_subagent}")

    print("\nDone.")


if __name__ == "__main__":
    main()
