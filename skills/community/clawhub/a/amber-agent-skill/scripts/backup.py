#!/usr/bin/env python3
"""Additive, local-only agent-session backup. Sources are always read-only."""
import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import sys

EXCLUDES = (".credentials.json", "auth.json", "*.credentials.json", "*token*", "*.pem", "*.key", "id_*")
PATHS = (".claude/projects", ".claude/todos", ".claude/history.jsonl",
         ".codex/sessions", ".codex/archived_sessions", ".codex/history.jsonl", ".codex/session_index.jsonl", ".codex/memories")

def excluded(path):
    return any(fnmatch.fnmatch(part.lower(), pattern) for part in path.parts for pattern in EXCLUDES)

def private_mkdir(path):
    missing = []
    cursor = path
    while not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent
    for directory in reversed(missing):
        directory.mkdir(mode=0o700)

def backup(config, destination, dry_run=False):
    destination = Path(destination).expanduser().resolve()
    hosts = config.get("hosts")
    if not isinstance(hosts, list) or not hosts:
        raise ValueError("hosts must be a nonempty list")
    seen = set()
    prepared = []
    for host in hosts:
        name = host.get("name", "")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name) or name in seen:
            raise ValueError("invalid or duplicate host name")
        seen.add(name)
        root_text = host.get("source_root", "")
        if not root_text or not Path(root_text).is_absolute():
            raise ValueError("source_root must be an explicit absolute local path")
        root = Path(root_text).resolve()
        if destination == root or destination.is_relative_to(root) or root.is_relative_to(destination):
            raise ValueError("source and destination must not overlap")
        prepared.append((name, root))
    report = {"dry_run": dry_run, "hosts": [], "status": "ok"}
    for name, root in prepared:
        row = {"host": name, "copied": 0, "planned": 0, "existing": 0, "absent": [], "errors": []}
        for relative in PATHS:
            source = root / relative
            if any(p.is_symlink() for p in [source, *source.parents] if p != root and p.is_relative_to(root)):
                row["errors"].append(relative + ": source ancestor symlink rejected")
                continue
            if not source.exists():
                row["absent"].append(relative)
                continue
            candidates = []
            if source.is_symlink():
                row["errors"].append(relative + ": symlink rejected")
                continue
            if source.is_dir():
                def walk_error(error):
                    row["errors"].append(str(error))
                for directory, dirs, names in os.walk(source, followlinks=False, onerror=walk_error):
                    parent = Path(directory)
                    for d in list(dirs):
                        p = parent / d
                        if p.is_symlink():
                            row["errors"].append(str(p.relative_to(root)) + ": symlink rejected")
                            dirs.remove(d)
                        elif excluded(p.relative_to(root)):
                            dirs.remove(d)
                    candidates.extend(parent / n for n in names)
            else:
                candidates = [source]
            for path in candidates:
                rel = path.relative_to(root)
                if excluded(rel):
                    continue
                if path.is_symlink() or not path.is_file():
                    row["errors"].append(str(rel) + ": non-regular source rejected")
                    continue
                target = destination / name / rel
                # Reject destination links, including ancestors, before creating anything.
                if any(p.is_symlink() for p in [target, *target.parents]):
                    row["errors"].append(str(rel) + ": destination symlink rejected")
                    continue
                if target.exists():
                    if target.is_file():
                        row["existing"] += 1
                    else:
                        row["errors"].append(str(rel) + ": destination type conflict")
                    continue
                if dry_run:
                    row["planned"] += 1
                    continue
                created = False
                try:
                    private_mkdir(target.parent)
                    # Exclusive creation prevents replacing existing backup bytes.
                    with path.open("rb") as src:
                        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                        created = True
                        with os.fdopen(fd, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                    row["copied"] += 1
                except OSError as exc:
                    # A partial new file is not a successful backup; remove only our new file.
                    if created and target.is_file():
                        target.unlink()
                    row["errors"].append(str(rel) + ": " + str(exc))
        row["status"] = "partial" if row["errors"] and (row["copied"] or row["planned"] or row["existing"]) else "failed" if row["errors"] or len(row["absent"]) == len(PATHS) else "ok"
        report["hosts"].append(row)
    statuses = {row["status"] for row in report["hosts"]}
    report["status"] = "ok" if statuses == {"ok"} else "failed" if statuses == {"failed"} else "partial"
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hosts", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print("WARNING: transcripts can contain secrets; filename exclusions are not redaction.", file=sys.stderr)
    try:
        report = backup(json.loads(args.hosts.read_text()), args.destination, args.dry_run)
    except (ValueError, OSError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "ok" else 1

if __name__ == "__main__":
    raise SystemExit(main())
