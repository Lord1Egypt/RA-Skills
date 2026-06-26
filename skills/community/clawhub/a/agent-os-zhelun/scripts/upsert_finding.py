#!/usr/bin/env python3
"""Agent OS — Upsert Finding

Create or update an audit finding in .agent-os/findings.jsonl.

Usage:
    python upsert_finding.py --title "..." --severity P1 [--id AF-...] [--status open]
    python upsert_finding.py --list
    python upsert_finding.py --list --status open --severity P0

All flags are optional for creation. Use --id to update an existing finding.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_SEVERITIES = {"P0", "P1", "P2", "P3"}
VALID_STATUSES = {
    "open", "accepted", "fixed", "verified", "closed",
    "deferred", "false_positive",
}
DEFAULT_AGENT_OS_DIR = ".agent-os"
FINDINGS_FILE = "findings.jsonl"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_agent_os_root(project_root: str | None = None) -> Path:
    """Locate the .agent-os directory, walking up from project_root or cwd."""
    start = Path(project_root) if project_root else Path.cwd()
    candidate = start / DEFAULT_AGENT_OS_DIR
    if candidate.is_dir():
        return candidate
    # Walk up one level
    for parent in start.parents:
        candidate = parent / DEFAULT_AGENT_OS_DIR
        if candidate.is_dir():
            return candidate
    # Not found — return default (will be created on write)
    return start / DEFAULT_AGENT_OS_DIR


def _read_findings(agent_os_root: Path) -> list[dict[str, Any]]:
    """Read all findings from the JSONL file."""
    findings_path = agent_os_root / FINDINGS_FILE
    if not findings_path.exists():
        return []
    items: list[dict[str, Any]] = []
    for line_no, raw in enumerate(findings_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError as exc:
            print(f"WARNING: skipping malformed line {line_no}: {exc}", file=sys.stderr)
    return items


def _write_findings(agent_os_root: Path, findings: list[dict[str, Any]]) -> None:
    """Write all findings back to the JSONL file."""
    agent_os_root.mkdir(parents=True, exist_ok=True)
    findings_path = agent_os_root / FINDINGS_FILE
    lines = [json.dumps(f, ensure_ascii=False) for f in findings]
    findings_path.write_text("\n".join(lines) + "\n" if lines else "", encoding="utf-8")


def _generate_id(agent_os_root: Path) -> str:
    """Generate a new finding ID: AF-YYYYMMDD-NNN."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"AF-{today}-"
    existing = _read_findings(agent_os_root)
    max_seq = 0
    for f in existing:
        fid = f.get("id", "")
        if fid.startswith(prefix):
            try:
                seq = int(fid[len(prefix):])
                max_seq = max(max_seq, seq)
            except ValueError:
                pass
    return f"{prefix}{max_seq + 1:03d}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_create(args: argparse.Namespace) -> int:
    """Create a new finding."""
    root = _find_agent_os_root(args.project_root)

    severity = args.severity.upper()
    if severity not in VALID_SEVERITIES:
        print(f"ERROR: invalid severity '{severity}'. Must be one of {VALID_SEVERITIES}", file=sys.stderr)
        return 1

    status = args.status or "open"
    if status not in VALID_STATUSES:
        print(f"ERROR: invalid status '{status}'. Must be one of {VALID_STATUSES}", file=sys.stderr)
        return 1

    finding_id = _generate_id(root)
    evidence = args.evidence.split(",") if args.evidence else []
    tags = args.tags.split(",") if args.tags else []

    finding = {
        "id": finding_id,
        "date": args.date or _today(),
        "source": args.source or "manual",
        "repo": args.repo or "",
        "severity": severity,
        "status": status,
        "title": args.title,
        "owner": args.owner or "",
        "evidence": evidence,
        "next_action": args.next_action or "",
        "verification": args.verification or "",
        "tags": tags,
        "updated_at": _now_iso(),
    }

    if args.dry_run:
        print("[DRY RUN] Would create finding:")
        print(json.dumps(finding, indent=2, ensure_ascii=False))
        return 0

    findings = _read_findings(root)
    findings.append(finding)
    _write_findings(root, findings)
    print(f"Created finding: {finding_id}")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update an existing finding by ID."""
    root = _find_agent_os_root(args.project_root)
    findings = _read_findings(root)

    target_idx = None
    for i, f in enumerate(findings):
        if f.get("id") == args.id:
            target_idx = i
            break

    if target_idx is None:
        print(f"ERROR: finding '{args.id}' not found", file=sys.stderr)
        return 1

    finding = findings[target_idx]

    if args.severity:
        severity = args.severity.upper()
        if severity not in VALID_SEVERITIES:
            print(f"ERROR: invalid severity '{severity}'", file=sys.stderr)
            return 1
        finding["severity"] = severity

    if args.status:
        if args.status not in VALID_STATUSES:
            print(f"ERROR: invalid status '{args.status}'", file=sys.stderr)
            return 1
        finding["status"] = args.status

    for field in ("title", "owner", "next_action", "verification", "repo", "source"):
        val = getattr(args, field, None)
        if val:
            finding[field] = val

    if args.evidence:
        finding["evidence"] = args.evidence.split(",")

    if args.tags:
        finding["tags"] = args.tags.split(",")

    finding["updated_at"] = _now_iso()

    if args.dry_run:
        print(f"[DRY RUN] Would update finding {args.id}:")
        print(json.dumps(finding, indent=2, ensure_ascii=False))
        return 0

    findings[target_idx] = finding
    _write_findings(root, findings)
    print(f"Updated finding: {args.id}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List findings, optionally filtered."""
    root = _find_agent_os_root(args.project_root)
    findings = _read_findings(root)

    if args.status:
        findings = [f for f in findings if f.get("status") == args.status]

    if args.severity:
        sev = args.severity.upper()
        findings = [f for f in findings if f.get("severity") == sev]

    if args.repo:
        findings = [f for f in findings if f.get("repo") == args.repo]

    if not findings:
        print("No findings found.")
        return 0

    for f in findings:
        print(json.dumps(f, ensure_ascii=False))

    print(f"\nTotal: {len(findings)} finding(s)")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="upsert_finding",
        description="Create or update audit findings in .agent-os/findings.jsonl",
    )
    parser.add_argument("--project-root", default=None,
                        help="Project root directory (default: current working directory)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview action without writing files")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # --- create ---
    create_p = sub.add_parser("create", help="Create a new finding")
    create_p.add_argument("--title", required=True, help="Finding title (required)")
    create_p.add_argument("--severity", required=True, help="P0/P1/P2/P3 (required)")
    create_p.add_argument("--status", default=None, help="Initial status (default: open)")
    create_p.add_argument("--source", default=None, help="Source (e.g. daily-audit, manual)")
    create_p.add_argument("--repo", default=None, help="Repository or project identifier")
    create_p.add_argument("--owner", default=None, help="Agent or human responsible")
    create_p.add_argument("--evidence", default=None, help="Comma-separated file paths or refs")
    create_p.add_argument("--next-action", default=None, help="What needs to happen next")
    create_p.add_argument("--verification", default=None, help="How to confirm it's resolved")
    create_p.add_argument("--tags", default=None, help="Comma-separated tags")
    create_p.add_argument("--date", default=None, help="Date (YYYY-MM-DD, default: today)")

    # --- update ---
    update_p = sub.add_parser("update", help="Update an existing finding")
    update_p.add_argument("--id", required=True, help="Finding ID to update (e.g. AF-20260601-001)")
    update_p.add_argument("--title", default=None)
    update_p.add_argument("--severity", default=None, help="New severity")
    update_p.add_argument("--status", default=None, help="New status")
    update_p.add_argument("--source", default=None)
    update_p.add_argument("--repo", default=None)
    update_p.add_argument("--owner", default=None)
    update_p.add_argument("--evidence", default=None, help="Replace evidence (comma-separated)")
    update_p.add_argument("--next-action", default=None)
    update_p.add_argument("--verification", default=None)
    update_p.add_argument("--tags", default=None, help="Replace tags (comma-separated)")

    # --- list ---
    list_p = sub.add_parser("list", help="List findings")
    list_p.add_argument("--status", default=None, help="Filter by status")
    list_p.add_argument("--severity", default=None, help="Filter by severity")
    list_p.add_argument("--repo", default=None, help="Filter by repo")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "create":
        return cmd_create(args)
    elif args.command == "update":
        return cmd_update(args)
    elif args.command == "list":
        return cmd_list(args)
    else:
        # Default: if --title and --severity are provided, treat as create
        if hasattr(args, 'title') and args.title:
            return cmd_create(args)
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
