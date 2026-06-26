#!/usr/bin/env python3
"""
Daily Report Data Collector
Cross-platform (macOS, Linux, Windows) script that:
1. Auto-discovers git repos the user worked on a given date
2. Collects commit logs across ALL branches
3. Gathers CodeBuddy Agent session overviews
4. Outputs structured JSON to stdout

Supports:
  --date YYYY-MM-DD   Collect data for a specific date
  --yesterday          Shortcut for yesterday
  --days-ago N         Collect data from N days ago
  (default: today)

Requirements: Python 3.6+ (standard library only) + git CLI
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# Platform Detection & Path Helpers
# ============================================================

SYSTEM = platform.system()  # "Darwin", "Linux", "Windows"


def get_home() -> Path:
    """Get user home directory, cross-platform."""
    return Path.home()


def get_codebuddy_data_dir() -> Path:
    """Get CodeBuddy's application data directory per platform."""
    home = get_home()
    if SYSTEM == "Darwin":
        return home / "Library" / "Application Support" / "CodeBuddy CN"
    elif SYSTEM == "Linux":
        xdg = os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))
        return Path(xdg) / "CodeBuddy CN"
    elif SYSTEM == "Windows":
        appdata = os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))
        return Path(appdata) / "CodeBuddy CN"
    return home / ".codebuddy-data"


def get_default_search_dirs() -> list:
    """
    Return search directories. Strategy: scan the ENTIRE home directory.
    No hardcoded guessing — we find ALL repos wherever they are,
    including hidden directories like .qclaw, .gongfeng-copilot, etc.
    """
    home = get_home()
    dirs = [home]  # Start from HOME, the script will walk into all subdirs

    # On Windows, also scan common non-home drive letters
    if SYSTEM == "Windows":
        for drive in ["C", "D", "E", "F"]:
            drive_path = Path(f"{drive}:/")
            if drive_path.is_dir() and drive_path != home.anchor:
                # Don't scan entire C:/, just common dev dirs on other drives
                for name in ["projects", "Projects", "code", "Code",
                             "repos", "Repos", "work", "Work", "dev", "Dev"]:
                    candidate = drive_path / name
                    if candidate.is_dir():
                        dirs.append(candidate)

    return dirs


# Directories that should NEVER be searched (waste of time, too deep, or system dirs)
GLOBAL_EXCLUDE_DIRS = {
    # System / application directories (never contain user repos)
    "Library", "Applications", "Music", "Movies", "Pictures", "Public",
    "AppData", "Application Data", "ProgramData",
    # Package managers & runtime caches
    "node_modules", "vendor", ".cache", "__pycache__",
    "venv", ".venv", "env", ".tox",
    "dist", "build", "target", "out", ".gradle", ".m2",
    # Large tool directories
    ".Trash", ".npm", ".yarn", ".pnpm-store",
    ".docker", ".vagrant", ".local",
    # IDE metadata (not repos themselves)
    ".vscode-server", ".cursor-server",
}


# ============================================================
# Config Loading (optional)
# ============================================================

def load_config() -> dict:
    """Load optional config.yaml from the skill's references/ directory."""
    config = {
        "extra_search_dirs": [],
        "git_author": "",
        "exclude_dirs": [
            "node_modules", "vendor", ".cache", "__pycache__",
            "venv", ".venv", "env", ".env", ".tox",
            "dist", "build", "target", "out",
        ],
        "max_depth": 5,
    }

    # Try to find config.yaml relative to this script
    script_dir = Path(__file__).parent.parent  # skill root
    config_path = script_dir / "references" / "config.yaml"

    if config_path.exists():
        try:
            # Parse simple YAML manually (no pyyaml dependency)
            content = config_path.read_text(encoding="utf-8")
            config = _parse_simple_yaml(content, config)
        except Exception:
            pass  # Silently fall back to defaults

    return config


def _parse_simple_yaml(content: str, defaults: dict) -> dict:
    """Minimal YAML parser for our simple config format. No dependency needed."""
    result = dict(defaults)
    current_list_key = None

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            current_list_key = None if not stripped.startswith("  -") else current_list_key
            if not stripped.startswith("  -"):
                current_list_key = None
            continue

        if stripped.startswith("- "):
            if current_list_key and current_list_key in result:
                val = stripped[2:].strip().strip('"').strip("'")
                if isinstance(result[current_list_key], list):
                    result[current_list_key].append(val)
        elif ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key in result:
                if isinstance(result[key], list):
                    current_list_key = key
                    if value:
                        result[key] = [value]
                elif isinstance(result[key], int):
                    try:
                        result[key] = int(value)
                    except ValueError:
                        pass
                else:
                    result[key] = value
            else:
                current_list_key = None

    return result


# ============================================================
# Git Author Detection
# ============================================================

def detect_git_author() -> str:
    """Auto-detect the git user name from global git config."""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "user.name"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    # Fallback: try system username
    return os.environ.get("USER", os.environ.get("USERNAME", ""))


# ============================================================
# Repository Discovery
# ============================================================

def discover_repos(search_dirs: list, exclude_dirs: set, max_depth: int) -> list:
    """
    Walk through search directories and find ALL git repositories,
    including those in hidden directories (e.g. .qclaw, .gongfeng-copilot).
    Cross-platform, uses os.walk instead of shell commands.
    """
    repos = []
    seen = set()

    # Merge user-configured excludes with global excludes
    all_excludes = GLOBAL_EXCLUDE_DIRS | exclude_dirs

    for search_dir in search_dirs:
        search_dir = Path(search_dir)
        if not search_dir.is_dir():
            continue

        base_depth = len(search_dir.parts)

        for root, dirs, _files in os.walk(str(search_dir)):
            root_path = Path(root)
            current_depth = len(root_path.parts) - base_depth

            # Prune depth
            if current_depth >= max_depth:
                dirs.clear()
                continue

            # Check if this directory is a git repo
            if ".git" in dirs:
                try:
                    repo_path = root_path.resolve()
                except OSError:
                    continue
                repo_key = str(repo_path)
                if repo_key not in seen:
                    seen.add(repo_key)
                    repos.append(repo_path)
                # Don't recurse deeper into this repo's subdirs
                dirs.clear()
                continue

            # Prune excluded directories, but ALLOW hidden dirs (like .qclaw)
            # Only exclude specific known-useless dirs
            dirs[:] = [
                d for d in dirs
                if d not in all_excludes and d != ".git"
            ]

    return repos


# ============================================================
# Git Log Collection
# ============================================================

def get_commits_for_date(repo_path: Path, author: str,
                         target_date: datetime = None) -> list:
    """
    Get all commits for the target date across ALL branches for the given author.
    If target_date is None, defaults to today.
    Returns a list of commit dicts.
    """
    commits = []

    if target_date is None:
        target_date = datetime.now()

    # Calculate the time range: [target_date 00:00:00, target_date+1 00:00:00)
    date_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    date_end = date_start + timedelta(days=1)
    since_str = date_start.strftime("%Y-%m-%d %H:%M:%S")
    until_str = date_end.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cmd = [
            "git", "-C", str(repo_path),
            "log", "--all",
            f"--since={since_str}",
            f"--until={until_str}",
            "--format=%h||%s||%D||%ai",
            "--no-merges",
        ]
        if author:
            cmd.append(f"--author={author}")

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )

        if result.returncode != 0:
            return commits

        seen_hashes = set()
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("||")
            if len(parts) >= 4:
                commit_hash = parts[0].strip()
                if commit_hash in seen_hashes:
                    continue
                seen_hashes.add(commit_hash)

                # Extract branch name from decoration
                decoration = parts[2].strip()
                branch = _extract_branch(decoration)

                commits.append({
                    "hash": commit_hash,
                    "message": parts[1].strip(),
                    "branch": branch,
                    "time": parts[3].strip()[:19],  # Trim timezone
                })

    except Exception:
        pass

    return commits


def _extract_branch(decoration: str) -> str:
    """Extract branch name from git log decoration string."""
    if not decoration:
        return ""
    # e.g. "HEAD -> main, origin/main"
    parts = [p.strip() for p in decoration.split(",")]
    for part in parts:
        if "HEAD -> " in part:
            return part.replace("HEAD -> ", "")
        if not part.startswith("origin/") and not part.startswith("tag:"):
            return part
    for part in parts:
        if part.startswith("origin/"):
            return part.replace("origin/", "")
    return parts[0] if parts else ""


def get_diff_stats(repo_path: Path, author: str,
                   target_date: datetime = None) -> str:
    """Get overall diff statistics for the target date's commits."""
    if target_date is None:
        target_date = datetime.now()

    date_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    date_end = date_start + timedelta(days=1)
    since_str = date_start.strftime("%Y-%m-%d %H:%M:%S")
    until_str = date_end.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cmd = [
            "git", "-C", str(repo_path),
            "log", "--all",
            f"--since={since_str}",
            f"--until={until_str}",
            "--format=",
            "--stat",
            "--no-merges",
        ]
        if author:
            cmd.append(f"--author={author}")

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15
        )

        if result.returncode != 0:
            return ""

        # Parse the last summary line like: "10 files changed, 150 insertions(+), 30 deletions(-)"
        total_files = 0
        total_add = 0
        total_del = 0

        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if "file" in line and "changed" in line:
                parts = line.split(",")
                for part in parts:
                    part = part.strip()
                    if "file" in part:
                        try:
                            total_files += int(part.split()[0])
                        except (ValueError, IndexError):
                            pass
                    elif "insertion" in part:
                        try:
                            total_add += int(part.split()[0])
                        except (ValueError, IndexError):
                            pass
                    elif "deletion" in part:
                        try:
                            total_del += int(part.split()[0])
                        except (ValueError, IndexError):
                            pass

        if total_files > 0:
            return f"+{total_add} -{total_del} across {total_files} files"
        return ""

    except Exception:
        return ""


# ============================================================
# CodeBuddy Agent Session Collection
# ============================================================

def collect_agent_sessions(target_date: datetime = None) -> list:
    """
    Scan CodeBuddy's brain directory for Agent session overviews
    that were modified on the target date.
    """
    sessions = []
    data_dir = get_codebuddy_data_dir()

    # Look for brain directories
    brain_patterns = [
        data_dir / "User" / "globalStorage" / "tencent-cloud.coding-copilot" / "brain",
        data_dir / "User" / "globalStorage" / "tencent-cloud.codebuddy" / "brain",
    ]

    if target_date is None:
        target_date = datetime.now()
    check_date = target_date.date()

    for brain_dir in brain_patterns:
        if not brain_dir.is_dir():
            continue

        try:
            for session_dir in brain_dir.iterdir():
                if not session_dir.is_dir():
                    continue

                overview_file = session_dir / "overview.md"
                if not overview_file.exists():
                    continue

                # Check if modified today
                try:
                    mtime = datetime.fromtimestamp(overview_file.stat().st_mtime)
                    if mtime.date() != check_date:
                        continue

                    content = overview_file.read_text(encoding="utf-8")
                    if content.strip():
                        sessions.append({
                            "session_id": session_dir.name,
                            "overview_content": content[:3000],  # Limit size
                            "modified_time": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                        })
                except Exception:
                    continue

        except Exception:
            continue

    # Sort by modification time
    sessions.sort(key=lambda s: s["modified_time"], reverse=True)
    return sessions


# ============================================================
# Main
# ============================================================

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Daily Report Data Collector - collect git commits and agent sessions"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Target date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        "--yesterday",
        action="store_true",
        help="Shortcut to collect yesterday's data"
    )
    parser.add_argument(
        "--days-ago",
        type=int,
        default=None,
        help="Collect data from N days ago (e.g. --days-ago 2 for the day before yesterday)"
    )
    return parser.parse_args()


def resolve_target_date(args) -> datetime:
    """Determine the target date from command-line arguments."""
    now = datetime.now()

    if args.date:
        try:
            return datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(
                f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.",
                file=sys.stderr
            )
            sys.exit(1)
    elif args.yesterday:
        return now - timedelta(days=1)
    elif args.days_ago is not None:
        if args.days_ago < 0:
            print("Error: --days-ago must be >= 0.", file=sys.stderr)
            sys.exit(1)
        return now - timedelta(days=args.days_ago)
    else:
        return now


def main():
    args = parse_args()
    target_date = resolve_target_date(args)
    errors = []

    # 1. Load config
    config = load_config()

    # 2. Detect git author
    author = config.get("git_author", "") or detect_git_author()
    if not author:
        errors.append(
            "Could not detect git author. "
            "Set git_author in config.yaml or run: git config --global user.name 'Your Name'"
        )

    # 3. Build search directory list
    search_dirs = get_default_search_dirs()

    # Add extra dirs from config
    for extra in config.get("extra_search_dirs", []):
        extra_path = Path(extra).expanduser()
        if extra_path.is_dir() and extra_path not in search_dirs:
            search_dirs.append(extra_path)

    if not search_dirs:
        errors.append(
            "No development directories found. "
            "Add extra_search_dirs to config.yaml."
        )

    # 4. Discover repos
    exclude_dirs = set(config.get("exclude_dirs", []))
    max_depth = config.get("max_depth", 5)
    all_repos = discover_repos(search_dirs, exclude_dirs, max_depth)

    # 5. Collect commits for each repo
    repo_data = []
    for repo_path in all_repos:
        commits = get_commits_for_date(repo_path, author, target_date)
        if not commits:
            continue  # Skip repos with no commits on target date

        diff_stats = get_diff_stats(repo_path, author, target_date)
        repo_data.append({
            "path": str(repo_path),
            "name": repo_path.name,
            "commits": commits,
            "diff_stats": diff_stats,
        })

    # Sort repos by number of commits (most active first)
    repo_data.sort(key=lambda r: len(r["commits"]), reverse=True)

    # 6. Collect Agent sessions
    agent_sessions = collect_agent_sessions(target_date)

    # 7. Build output
    date_str = target_date.strftime("%Y-%m-%d")
    output = {
        "date": date_str,
        "system": SYSTEM,
        "git_author": author,
        "search_dirs_scanned": [str(d) for d in search_dirs],
        "repos_discovered": len(all_repos),
        "repos": repo_data,
        "agent_sessions": agent_sessions,
        "errors": errors,
    }

    # Output JSON to stdout
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
