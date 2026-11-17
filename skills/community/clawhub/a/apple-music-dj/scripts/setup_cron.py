#!/usr/bin/env python3
"""
setup_cron.py — Automation scheduler for Apple Music DJ.

Generates and installs crontab entries for recurring jobs:
  weekly-mix        Generate a fresh playlist every Monday morning (opt-in: --jobs weekly-mix; it WRITES)
  new-releases      Check for new releases from favourite artists weekly (report only)
  daily-drop        Surface a daily pick recommendation (report only)
  health-check      Scan playlists for removed/stale tracks monthly (report only)
  monthly-drift     Snapshot taste + report drift monthly (opt-in: --jobs monthly-drift)

Usage:
  python3 setup_cron.py list                    Show planned cron jobs
  python3 setup_cron.py install [--jobs J,...]  Install selected (or all) jobs
  python3 setup_cron.py install --dry-run       Print the exact crontab lines + a digest; change nothing
  python3 setup_cron.py install --confirm DIGEST  Install exactly the lines that digest was printed for
  python3 setup_cron.py remove  [--jobs J,...]  Remove selected (or all) jobs
  python3 setup_cron.py status                  Show currently installed jobs

Options:
  --profile PATH    Path to taste profile JSON (required for install)
  --storefront SF   Storefront code (default: from config)
  --log-dir DIR     Directory for log files (default: ~/.apple-music-dj/logs)

Requires: crontab available on the system.
"""

import sys
if sys.version_info < (3, 10):
    sys.exit(
        f"ERROR: Python 3.10+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import errno
import hashlib
import os
import re
import shlex
import stat
import subprocess
from pathlib import Path

from _common import APP_DIR, ensure_private_dir, load_config, tighten_app_dir

SCRIPT_DIR = Path(__file__).resolve().parent
MARKER = "# apple-music-dj"
DEFAULT_LOG_DIR = APP_DIR / "logs"

# Anything that could end a crontab line, or that cron itself rewrites, must never reach one.
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


# ── Input validation ─────────────────────────────────────────────
# Values end up in a crontab line that /bin/sh parses on a schedule, indefinitely, so they
# are validated here (and shell-quoted in build_job_defs) instead of trusted.

def validate_path(value: str, label: str) -> str:
    """Absolute, normalized path with no newline/control characters or '%'."""
    if not value or not value.strip():
        raise ValueError(f"{label} is empty.")
    if _CONTROL_CHARS.search(value):
        raise ValueError(f"{label} contains a newline or control character.")
    if "%" in value:
        raise ValueError(f"{label} contains '%', which cron treats as a newline.")
    return os.path.abspath(os.path.expanduser(value))


def validate_python(value: str) -> str:
    path = validate_path(value, "--python")
    if not (os.path.isfile(path) and os.access(path, os.X_OK)):
        raise ValueError(f"--python {path} is not an executable file.")
    return path


def validate_storefront(value: str) -> str:
    if not re.fullmatch(r"[a-z]{2}|auto", value or ""):
        raise ValueError(f"Storefront '{value}' must be a two-letter lowercase code like 'us' (or 'auto').")
    return value


def validate_job_names(value: str) -> list[str]:
    names = [n.strip() for n in value.split(",") if n.strip()]
    if not names:
        raise ValueError("--jobs was given but names no jobs (e.g. --jobs weekly-mix,daily-drop).")
    for name in names:
        if not re.fullmatch(r"[a-z][a-z0-9-]{0,31}", name):
            raise ValueError(f"Job name '{name}' isn't valid (lowercase letters, digits and dashes only).")
    return names


# ── Job Definitions ──────────────────────────────────────────────

def build_job_defs(python: str, profile: str, sf: str,
                   log_dir: str) -> dict[str, dict]:
    """Return cron job definitions keyed by job name."""
    # These land in a crontab line that /bin/sh parses, so quote every dynamic value
    # (a profile path with spaces, or shell metacharacters, must stay one argument).
    q = shlex.quote
    python, profile, sf = q(python), q(profile), q(sf)
    strategy = q(str(SCRIPT_DIR / "strategy_engine.py"))
    daily_pick = q(str(SCRIPT_DIR / "daily_pick.py"))
    new_releases = q(str(SCRIPT_DIR / "new_releases.sh"))
    health = q(str(SCRIPT_DIR / "playlist_health.py"))
    profiler = q(str(SCRIPT_DIR / "taste_profiler.py"))
    drift = q(str(SCRIPT_DIR / "taste_drift.py"))

    return {
        "weekly-mix": {
            "description": "Generate a fresh playlist every Monday at 7 AM (writes to your library; opt-in)",
            "schedule": "0 7 * * 1",
            "command": (
                f"{python} {strategy} --strategy trend "
                f"--profile {profile} --storefront {sf} --create"
            ),
            "log": f"{log_dir}/weekly-mix.log",
            "optional": True,  # the only default-schedulable job that writes, so it must be named
        },
        "new-releases": {
            "description": "Check for new releases every Wednesday at 8 AM",
            "schedule": "0 8 * * 3",
            # new_releases.sh takes <profile.json> <storefront> (report only: no --create-playlist)
            "command": f"bash {new_releases} {profile} {sf}",
            "log": f"{log_dir}/new-releases.log",
        },
        "daily-drop": {
            "description": "Surface a daily pick every day at 8:30 AM",
            "schedule": "30 8 * * *",
            # daily_pick.py takes positional <profile.json> <storefront>
            "command": (
                f"{python} {daily_pick} daily {profile} {sf}"
            ),
            "log": f"{log_dir}/daily-drop.log",
        },
        "health-check": {
            "description": "Scan playlists for issues on the 1st of each month",
            "schedule": "0 9 1 * *",
            "command": (
                f"{python} {health} check all --profile {profile}"
            ),
            "log": f"{log_dir}/health-check.log",
        },
        "monthly-drift": {
            "description": "Snapshot your taste and report drift on the 2nd of each month (opt-in)",
            "schedule": "0 9 2 * *",
            # Subshell so the log redirect covers both commands
            "command": (
                f"({python} {profiler} --storefront {sf} --output {profile} "
                f"&& {python} {drift} --profile {profile} --since 30d --format text)"
            ),
            "log": f"{log_dir}/monthly-drift.log",
            "optional": True,
        },
    }


def format_cron_line(job: dict, name: str) -> str:
    """Format a single crontab line with logging and marker.

    `umask 077` makes anything the job (or its log redirect) creates owner-only. The log path
    is quoted like every other dynamic value, and the finished line is refused if it contains
    a newline/control character or '%' (cron turns '%' into a newline even inside quotes).
    """
    line = (
        f"{job['schedule']} umask 077; {job['command']} >> {shlex.quote(job['log'])} 2>&1 "
        f"{MARKER}:{name}"
    )
    if _CONTROL_CHARS.search(line) or "%" in line:
        raise ValueError(f"Refusing to build a crontab line for '{name}': it contains a newline, "
                         f"control character or '%'.")
    return line


# ── Enforced confirmation ────────────────────────────────────────

def install_digest(lines: list[str]) -> str:
    """Short digest of the exact crontab lines an install would add (order-insensitive).

    `install` only proceeds when given the digest that `--dry-run` printed, so what gets
    scheduled is provably what was reviewed — a skill instruction ("show the user first") is
    not a control; this is.
    """
    return hashlib.sha256("\n".join(sorted(lines)).encode()).hexdigest()[:12]


# ── Private log files ────────────────────────────────────────────

def prepare_logs(log_dir: str, log_paths: list[str]) -> None:
    """Create the log directory and log files owner-only, before cron ever writes to them.

    Shell redirection would create the files under the ambient umask (typically world-readable),
    and the logs hold playlist names, track picks and artist preferences. Refuses symlinks,
    directories/files owned by someone else, and directories other users can write to.
    """
    d = Path(log_dir)
    if d.is_symlink():
        raise ValueError(f"Log directory {d} is a symlink; refusing to write logs through it.")
    tighten_app_dir(d)
    ensure_private_dir(d, tighten=(d == DEFAULT_LOG_DIR))
    st = os.lstat(d)
    if not stat.S_ISDIR(st.st_mode):
        raise ValueError(f"Log directory {d} is not a directory.")
    if st.st_uid != os.getuid():
        raise ValueError(f"Log directory {d} is owned by another user.")
    if st.st_mode & 0o022:
        raise ValueError(f"Log directory {d} is writable by other users; choose a private directory.")
    for log in log_paths:
        try:
            fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
        except OSError as e:
            if e.errno == errno.ELOOP:
                raise ValueError(f"Log file {log} is a symlink; refusing to write through it.") from e
            raise
        try:
            fst = os.fstat(fd)
            if not stat.S_ISREG(fst.st_mode) or fst.st_uid != os.getuid():
                raise ValueError(f"Log file {log} is not a regular file owned by you.")
            os.fchmod(fd, 0o600)  # tighten a pre-existing file; the open() mode only covers new ones
        finally:
            os.close(fd)


# ── Crontab Interaction ─────────────────────────────────────────

def get_current_crontab() -> str:
    """Read current crontab, returning empty string if none."""
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
    except FileNotFoundError:
        print("ERROR: crontab not found on this system.", file=sys.stderr)
        sys.exit(1)
    return ""


def set_crontab(content: str) -> bool:
    """Write content as the new crontab."""
    try:
        result = subprocess.run(
            ["crontab", "-"], input=content, capture_output=True, text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("ERROR: crontab not found on this system.", file=sys.stderr)
        return False


def get_installed_jobs() -> list[str]:
    """Return list of installed apple-music-dj job names."""
    crontab = get_current_crontab()
    jobs = []
    for line in crontab.splitlines():
        if MARKER in line:
            # Extract job name from marker
            parts = line.split(f"{MARKER}:")
            if len(parts) > 1:
                jobs.append(parts[-1].strip())
    return jobs


# ── Commands ─────────────────────────────────────────────────────

def cmd_list(job_defs: dict[str, dict]):
    """Show all available jobs and their schedules."""
    installed = set(get_installed_jobs())
    print("Available apple-music-dj cron jobs:\n")
    for name, job in job_defs.items():
        status = "✅ installed" if name in installed else "⬚ not installed"
        opt_in = "  (opt-in: pass --jobs)" if job.get("optional") else ""
        print(f"  {name:20s} {status}{opt_in}")
        print(f"    {job['description']}")
        print(f"    Schedule: {job['schedule']}")
        print(f"    Command:  {job['command']}")
        print(f"    Log:      {job['log']}")
        print()


def cmd_install(job_defs: dict[str, dict], selected: list[str],
                log_dir: str, dry_run: bool = False, confirm: str | None = None):
    """Install selected cron jobs.

    Nothing is installed unless `confirm` equals the digest of the exact lines (printed by
    `--dry-run`, or by a bare `install`, which then exits 2 without changing anything).
    """
    known = [n for n in selected if n in job_defs]
    for name in selected:
        if name not in job_defs:
            print(f"WARNING: Unknown job '{name}', skipping.", file=sys.stderr)
    if not known:
        print("ERROR: No valid jobs selected.", file=sys.stderr)
        sys.exit(1)
    try:
        new_lines = {name: format_cron_line(job_defs[name], name) for name in known}
        digest = install_digest(list(new_lines.values()))
        if dry_run or confirm is None:
            title = ("Dry run — these lines WOULD be added to your crontab (nothing was changed):"
                     if dry_run else "Confirmation required — these lines would be added to your crontab:")
            print(f"{title}\n")
            for name in known:
                print(new_lines[name])
            print(f"\nDigest: {digest}")
            print(f"To install exactly these lines, re-run the same command with:  --confirm {digest}")
            if not dry_run:
                print("Nothing was installed (no --confirm given).", file=sys.stderr)
                sys.exit(2)
            return
        if confirm.strip().lower() != digest:
            raise ValueError("--confirm doesn't match the lines this command would install (different jobs, "
                             "paths or storefront than the ones that were reviewed). Run --dry-run again "
                             "and confirm the digest it prints.")
        prepare_logs(log_dir, [job_defs[n]["log"] for n in known])
    except (ValueError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    crontab = get_current_crontab()
    lines = crontab.splitlines()

    # Remove existing apple-music-dj lines for selected jobs
    filtered = []
    for line in lines:
        is_ours = False
        for name in selected:
            if f"{MARKER}:{name}" in line:
                is_ours = True
                break
        if not is_ours:
            filtered.append(line)

    # Add new lines
    for name in known:
        filtered.append(new_lines[name])
        print(f"  ✅ {name}: {job_defs[name]['schedule']}")

    new_crontab = "\n".join(filtered)
    if not new_crontab.endswith("\n"):
        new_crontab += "\n"

    if set_crontab(new_crontab):
        print(f"\n{len(selected)} job(s) installed successfully.")
    else:
        print("ERROR: Failed to update crontab.", file=sys.stderr)
        sys.exit(1)


def cmd_remove(job_defs: dict[str, dict], selected: list[str]):
    """Remove selected cron jobs."""
    crontab = get_current_crontab()
    lines = crontab.splitlines()

    removed = 0
    filtered = []
    for line in lines:
        is_ours = False
        for name in selected:
            if f"{MARKER}:{name}" in line:
                is_ours = True
                removed += 1
                print(f"  🗑  Removed: {name}")
                break
        if not is_ours:
            filtered.append(line)

    if removed == 0:
        print("No matching jobs found to remove.")
        return

    new_crontab = "\n".join(filtered)
    if not new_crontab.endswith("\n"):
        new_crontab += "\n"

    if set_crontab(new_crontab):
        print(f"\n{removed} job(s) removed.")
    else:
        print("ERROR: Failed to update crontab.", file=sys.stderr)
        sys.exit(1)


def cmd_status():
    """Show currently installed apple-music-dj cron jobs."""
    installed = get_installed_jobs()
    if not installed:
        print("No apple-music-dj cron jobs currently installed.")
        return

    print(f"{len(installed)} apple-music-dj job(s) installed:\n")
    crontab = get_current_crontab()
    for line in crontab.splitlines():
        if MARKER in line:
            print(f"  {line}")
    print()


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Apple Music DJ — Automation Scheduler"
    )
    parser.add_argument("command", choices=["list", "install", "remove", "status"],
                        help="Action to perform")
    parser.add_argument("--jobs", default=None,
                        help="Comma-separated job names (default: the report-only jobs; weekly-mix and monthly-drift are opt-in)")
    parser.add_argument("--profile", default=None,
                        help="Path to taste profile JSON")
    parser.add_argument("--storefront", default=None,
                        help="Storefront code")
    parser.add_argument("--log-dir", default=None,
                        help="Directory for log files")
    parser.add_argument("--python", default=None,
                        help="Path to python3 executable")
    parser.add_argument("--dry-run", action="store_true",
                        help="install: print the exact crontab lines and a digest, without installing anything")
    parser.add_argument("--confirm", default=None, metavar="DIGEST",
                        help="install: required to install; the digest printed by --dry-run for these exact lines")

    args = parser.parse_args()
    config = load_config()

    # Resolve defaults, then validate everything that will be written into a crontab line
    try:
        sf = validate_storefront(args.storefront or config.get("default_storefront", "us"))
        log_dir = validate_path(args.log_dir or str(DEFAULT_LOG_DIR), "--log-dir")
        python_path = validate_python(args.python or sys.executable)
        profile = validate_path(args.profile or str(APP_DIR / "profile.json"), "--profile")
        # `is not None`: an explicit but empty --jobs must be rejected, not treated as "all"
        jobs = validate_job_names(args.jobs) if args.jobs is not None else None
        if args.confirm is not None and not re.fullmatch(r"[0-9a-f]{12}", args.confirm.strip().lower()):
            raise ValueError("--confirm expects the 12-character digest printed by --dry-run.")
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    job_defs = build_job_defs(python_path, profile, sf, log_dir)
    all_names = list(job_defs.keys())

    # Opt-in jobs are only installed when named with --jobs
    selected = [n for n in all_names if not job_defs[n].get("optional")]
    if jobs is not None:
        unknown = [n for n in jobs if n not in job_defs]
        if unknown:
            print(f"ERROR: Unknown job(s): {', '.join(unknown)}. Available: {', '.join(all_names)}.",
                  file=sys.stderr)
            sys.exit(1)
        selected = jobs

    if args.command == "list":
        cmd_list(job_defs)
    elif args.command == "install":
        if not args.profile:
            print("WARNING: Using default profile path. "
                  "Specify --profile for a custom location.", file=sys.stderr)
        cmd_install(job_defs, selected, log_dir, dry_run=args.dry_run, confirm=args.confirm)
    elif args.command == "remove":
        cmd_remove(job_defs, selected if jobs is not None else all_names)
    elif args.command == "status":
        cmd_status()


if __name__ == "__main__":
    main()
