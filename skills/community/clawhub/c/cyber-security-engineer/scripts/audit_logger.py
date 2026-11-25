#!/usr/bin/env python3
"""Tamper-evident audit log for privileged actions.

Events are appended to ``~/.openclaw/security/privileged-audit.jsonl``, one JSON
object per line. Each entry carries ``prev``: the SHA-256 of the line before it.
Editing, removing or reordering an earlier entry breaks the chain, which
``verify`` reports:

    python3 audit_logger.py verify

Limits: the log belongs to the user who runs OpenClaw, so that user (or an agent
running as that user) can replace the whole file with a freshly chained one. The
chain detects partial edits; it does not replace shipping the log to a system the
agent cannot write to. No network calls are made.
"""
import argparse
import getpass
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

AUDIT_LOG = Path.home() / ".openclaw" / "security" / "privileged-audit.jsonl"
MAX_BYTES = 5 * 1024 * 1024  # rotate to "<name>.1" past this size
_TAIL_BYTES = 64 * 1024


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _line_hash(line: bytes) -> str:
    return hashlib.sha256(line.rstrip(b"\r\n")).hexdigest()


def _last_line(path: Path) -> Optional[bytes]:
    try:
        with path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - _TAIL_BYTES))
            lines = [ln for ln in f.read().splitlines() if ln.strip()]
    except OSError:
        return None
    return lines[-1] if lines else None


def _current_user() -> str:
    try:
        return getpass.getuser()
    except Exception:
        return "unknown"


def append_audit(event: Dict[str, Any], path: Optional[Path] = None) -> bool:
    """Append one event. Returns False when it could not be written.

    Callers decide what a failed write means: ``guarded_privileged_exec.py``
    refuses to run a privileged command it cannot record.
    """
    path = AUDIT_LOG if path is None else path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        last = _last_line(path)
        prev = _line_hash(last) if last is not None else ""
        if path.exists() and path.stat().st_size >= MAX_BYTES:
            os.replace(str(path), str(path) + ".1")  # the chain continues across the rotation
        payload = {"ts_utc": _utc_now_iso(), "user": _current_user(), "pid": os.getpid(), **event, "prev": prev}
        data = (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")
        fd = os.open(str(path), os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            if os.name != "nt":
                os.fchmod(fd, 0o600)
            os.write(fd, data)
        finally:
            os.close(fd)
        return True
    except Exception:
        return False


def verify(path: Optional[Path] = None) -> Dict[str, Any]:
    """Check the hash chain. Entries written before chaining existed count as ``legacy``."""
    path = AUDIT_LOG if path is None else path
    result: Dict[str, Any] = {"file": str(path), "entries": 0, "chained": 0, "legacy": 0, "ok": True, "broken_at": None}
    try:
        lines = [ln for ln in path.read_bytes().splitlines() if ln.strip()]
    except FileNotFoundError:
        return result
    except OSError as exc:
        result.update(ok=False, error=str(exc))
        return result

    previous: Optional[bytes] = None
    seen_chained = False
    for number, line in enumerate(lines, 1):
        result["entries"] += 1
        try:
            entry = json.loads(line)
        except ValueError:
            entry = None
        if not isinstance(entry, dict):
            result.update(ok=False, broken_at=number, error="entry is not a JSON object")
            break
        if "prev" not in entry:
            if seen_chained:  # an unchained entry after chained ones was inserted by hand
                result.update(ok=False, broken_at=number, error="unchained entry after chained entries")
                break
            result["legacy"] += 1
        else:
            # The first line of a file may follow a rotated file, so its link cannot be checked here.
            if previous is not None and entry["prev"] != _line_hash(previous):
                result.update(ok=False, broken_at=number, error="hash chain does not match the previous entry")
                break
            seen_chained = True
            result["chained"] += 1
        previous = line
    return result


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Privileged-action audit log")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("verify", help="Verify the audit log's hash chain")
    check.add_argument("--file", default=str(AUDIT_LOG), help="Audit log to verify")
    args = parser.parse_args(argv)
    report = verify(Path(args.file).expanduser())
    sys.stdout.write(json.dumps(report, indent=2) + "\n")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
