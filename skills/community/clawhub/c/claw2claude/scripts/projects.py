#!/usr/bin/env python3
"""
Session-level project registry.
Stored at ~/.openclaw/skills/claw2claude/state/projects.json

Usage:
  projects.py list                        # List all active projects
  projects.py register <path> <name>      # Register a project
  projects.py get <name_or_path>          # Look up a project
  projects.py last                        # Get the most recently active project
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "state" / "projects.json"


def load():
    STATE_FILE.parent.mkdir(exist_ok=True)
    if not STATE_FILE.exists():
        return {"projects": []}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Safely degrade to empty state on corruption; keep the broken file for inspection
        backup = STATE_FILE.with_suffix(".corrupted")
        try:
            STATE_FILE.rename(backup)
        except OSError:
            pass
        return {"projects": []}


def save(data):
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(STATE_FILE)  # Atomic replace


def _resolve_display_name(path: str, projects: list) -> str:
    """
    Detect basename conflicts and upgrade to parent/name format when needed.
    e.g. ~/a/backend and ~/b/backend become a/backend and b/backend respectively.
    """
    p = Path(path)
    base = p.name
    conflict = any(
        proj["path"] != path and Path(proj["path"]).name == base
        for proj in projects
    )
    if conflict:
        return f"{p.parent.name}/{base}"
    return base


def register(path: str, name: str):
    path = str(Path(path).expanduser().resolve())
    data = load()
    projects = data["projects"]

    # Override the provided name with the conflict-resolved display name
    display_name = _resolve_display_name(path, projects)

    # Update existing entry or add a new one
    for p in projects:
        if p["path"] == path:
            p["name"] = display_name
            p["last_active"] = datetime.now().isoformat()
            save(data)
            print(json.dumps(p, ensure_ascii=False))
            return

    entry = {
        "path": path,
        "name": display_name,
        "last_active": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
    }
    projects.append(entry)

    # Keep at most 20 projects, sorted by most recently active.
    # The new entry always sorts first (last_active = now), so it is never cut.
    data["projects"] = sorted(projects, key=lambda x: x["last_active"], reverse=True)[:20]

    # Re-check all display names after adding the new entry to catch newly introduced conflicts.
    # entry is still in data["projects"] by reference, so its name may be updated here.
    for proj in data["projects"]:
        proj["name"] = _resolve_display_name(proj["path"], data["projects"])

    save(data)
    print(json.dumps(entry, ensure_ascii=False))


def touch(path: str):
    """Update a project's last_active timestamp."""
    path = str(Path(path).expanduser().resolve())
    data = load()
    for p in data["projects"]:
        if p["path"] == path:
            p["last_active"] = datetime.now().isoformat()
            save(data)
            return
    # Not found — register it using the directory name
    name = Path(path).name
    register(path, name)


def get(name_or_path: str):
    data = load()
    # Treat as a filesystem path only when it looks like one (absolute, home-relative, or ./relative).
    # Conflict-resolved display names like "a/backend" also contain "/" but are not paths.
    is_path = name_or_path.startswith(("/", "~", "./", "../"))
    query = str(Path(name_or_path).expanduser().resolve()) if is_path else name_or_path
    for p in data["projects"]:
        if p["path"] == query or p["name"] == name_or_path:
            print(json.dumps(p, ensure_ascii=False))
            return
    print("null")


def list_projects():
    data = load()
    projects = data["projects"]
    if not projects:
        print("(no projects registered)")
        return
    print("Active projects:")
    for i, p in enumerate(projects, 1):
        last = p["last_active"][:10]
        print(f"  {i}. [{p['name']}] {p['path']}  (last active: {last})")


def last():
    data = load()
    projects = data["projects"]
    if not projects:
        print("null")
        return
    print(json.dumps(projects[0], ensure_ascii=False))


cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

if cmd == "list":
    list_projects()
elif cmd == "register" and len(sys.argv) >= 4:
    register(sys.argv[2], sys.argv[3])
elif cmd == "touch" and len(sys.argv) >= 3:
    touch(sys.argv[2])
elif cmd == "get" and len(sys.argv) >= 3:
    get(sys.argv[2])
elif cmd == "last":
    last()
else:
    print(f"Unknown command: {cmd}", file=sys.stderr)
    sys.exit(1)
