#!/usr/bin/env python3
"""Shared registry helper for Claude Code remote control sessions.

Centralises all JSON I/O, file locking, permissions, and constants so that
the bash scripts never contain inline Python for registry operations.

Usage from bash:
    python3 "$SCRIPT_DIR/registry.py" <command> [args...]

Commands:
    ensure-dir                          Create state dir with safe permissions
    add <name> <url> <dir> [uuid]       Register a new active session
    mark-dead <name>                    Mark a session dead + capture UUID
    prune [days]                        Remove dead entries older than N days (default 30)
    list                                Print session listing with tmux status
    idle-timeout                        Print idle timeout in seconds
    trust-workspace <workdir>           Pre-seed workspace trust in ~/.claude.json
"""

import fcntl
import glob
import json
import os
import subprocess
import sys
import time

# ── Constants ────────────────────────────────────────────────────────────────

IDLE_TIMEOUT_SECS = 1800  # 30 minutes — single source of truth

STATE_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "claude-rc")
REGISTRY = os.path.join(STATE_DIR, "sessions.json")
REGISTRY_LOCK = os.path.join(STATE_DIR, "sessions.lock")
CLAUDE_CONFIG = os.path.join(os.path.expanduser("~"), ".claude.json")
CLAUDE_CONFIG_LOCK = os.path.join(STATE_DIR, "claude_config.lock")

# ── Helpers ──────────────────────────────────────────────────────────────────


def ensure_dir():
    """Create state directory with restricted permissions (#7)."""
    old_umask = os.umask(0o077)
    try:
        os.makedirs(STATE_DIR, mode=0o700, exist_ok=True)
    finally:
        os.umask(old_umask)


def _load(path):
    """Load JSON from path. Returns {} on missing file or corrupt JSON (#17)."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Warning: corrupt JSON in {path}, resetting", file=sys.stderr)
        return {}
    # Other exceptions (PermissionError, IOError) propagate intentionally.


def _save(path, data):
    """Write JSON atomically with restricted permissions."""
    old_umask = os.umask(0o077)
    try:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)  # atomic on POSIX
    finally:
        os.umask(old_umask)


def _with_lock(lock_path, fn):
    """Run fn() while holding an exclusive flock on lock_path."""
    ensure_dir()
    old_umask = os.umask(0o077)
    try:
        fd = open(lock_path, "w")
    finally:
        os.umask(old_umask)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        return fn()
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()


# ── Commands ─────────────────────────────────────────────────────────────────


def cmd_ensure_dir():
    ensure_dir()


def cmd_add(name, url, workdir, local_uuid=""):
    """Register a new active session (#7, #17)."""

    def _do():
        r = _load(REGISTRY)
        r[name] = {
            "url": url,
            "dir": workdir,
            "local_uuid": local_uuid,
            "status": "active",
            "started_at": int(time.time()),
        }
        _save(REGISTRY, r)

    _with_lock(REGISTRY_LOCK, _do)


def cmd_mark_dead(name):
    """Mark a session dead and capture UUID from .jsonl files."""

    def _do():
        r = _load(REGISTRY)
        if name not in r:
            return
        entry = r[name]
        entry["status"] = "dead"
        entry["stopped_at"] = int(time.time())
        if not entry.get("local_uuid"):
            proj_dir = os.path.expanduser(
                "~/.claude/projects/" + entry["dir"].replace("/", "-")
            )
            started_at = entry.get("started_at", 0)
            files = [
                f
                for f in glob.glob(proj_dir + "/*.jsonl")
                if os.path.getmtime(f) > started_at
            ]
            if files:
                entry["local_uuid"] = (
                    os.path.basename(sorted(files, key=os.path.getmtime)[-1]).replace(
                        ".jsonl", ""
                    )
                )
            else:
                print(
                    f"Warning: could not capture UUID for '{name}' "
                    f"— no matching .jsonl files in {proj_dir}",
                    file=sys.stderr,
                )
        _save(REGISTRY, r)

    _with_lock(REGISTRY_LOCK, _do)


def cmd_prune(days=30):
    """Remove dead entries older than N days."""

    def _do():
        r = _load(REGISTRY)
        cutoff = int(time.time()) - days * 86400
        pruned = {
            k: v
            for k, v in r.items()
            if not (v.get("status") == "dead" and v.get("stopped_at", 0) < cutoff)
        }
        _save(REGISTRY, pruned)

    _with_lock(REGISTRY_LOCK, _do)


def cmd_list():
    """Print session listing with tmux liveness check."""
    r = _load(REGISTRY)
    if not r:
        print("No sessions.")
        return

    for name, v in r.items():
        # Derive tmux session name the same way start_session.sh does
        emoji_and_animal = name.split(" | ")[0].strip()
        animal_slug = (
            emoji_and_animal.split(None, 1)[-1].lower()
            if " " in emoji_and_animal
            else emoji_and_animal.lower()
        )
        dirbase = name.split(" | ")[-1].strip()
        tmux_name = f"cc-{animal_slug}-{dirbase}"
        tmux_name = "".join(c for c in tmux_name if c.isalnum() or c == "-")

        tmux_alive = (
            subprocess.run(
                ["tmux", "has-session", "-t", tmux_name], capture_output=True
            ).returncode
            == 0
        )

        registry_status = v.get("status", "unknown")

        if tmux_alive:
            status = "\U0001f7e2"  # green
        elif registry_status == "dead":
            status = "\U0001f534"  # red
        else:
            status = "\U0001f7e1"  # yellow

        print(f"{status} {name}  (tmux: {tmux_name})")
        print(f"   dir:    {v.get('dir', '?')}")
        print(f"   url:    {v.get('url', '?')}")
        if registry_status == "dead":
            uuid = v.get("local_uuid", "")
            if uuid:
                print(f"   uuid:   {uuid}")
                print(
                    f'   resume: claude -r "{uuid}" --dangerously-skip-permissions --remote-control'
                )
            else:
                print("   uuid:   (not captured)")
        print()


def cmd_idle_timeout():
    """Print idle timeout in seconds."""
    print(IDLE_TIMEOUT_SECS)


def cmd_trust_workspace(workdir):
    """Pre-seed workspace trust in ~/.claude.json with flock (#5, #17)."""

    def _do():
        try:
            with open(CLAUDE_CONFIG) as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        except json.JSONDecodeError:
            print(
                f"Warning: corrupt JSON in {CLAUDE_CONFIG}, resetting",
                file=sys.stderr,
            )
            config = {}
        projects = config.setdefault("projects", {})
        proj = projects.setdefault(workdir, {})
        if not proj.get("hasTrustDialogAccepted"):
            proj["hasTrustDialogAccepted"] = True
            tmp = CLAUDE_CONFIG + ".tmp"
            with open(tmp, "w") as f:
                json.dump(config, f, indent=2)
            os.replace(tmp, CLAUDE_CONFIG)

    _with_lock(CLAUDE_CONFIG_LOCK, _do)


# ── CLI dispatcher ───────────────────────────────────────────────────────────

COMMANDS = {
    "ensure-dir": lambda args: cmd_ensure_dir(),
    "add": lambda args: cmd_add(*args),
    "mark-dead": lambda args: cmd_mark_dead(args[0]),
    "prune": lambda args: cmd_prune(int(args[0]) if args else 30),
    "list": lambda args: cmd_list(),
    "idle-timeout": lambda args: cmd_idle_timeout(),
    "trust-workspace": lambda args: cmd_trust_workspace(args[0]),
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: {sys.argv[0]} <command> [args...]", file=sys.stderr)
        print(f"Commands: {', '.join(COMMANDS)}", file=sys.stderr)
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])
