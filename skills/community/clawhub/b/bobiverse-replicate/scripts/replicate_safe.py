#!/usr/bin/env python3
"""Hardened replication runner for Bobiverse OpenClaw skill.

Security properties:
- strict input validation
- validated workspace-only path enforcement under ~/.openclaw
- no shell command interpolation
- dry-run issued nonce required for execute mode
- dry-run by default with transactional clone staging
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

SERIAL_RE = re.compile(r"^Bob-[0-9A-Za-z]+-[A-Za-z0-9-]{1,39}-\d{4}-\d{2}-\d{2}$")
AGENT_RE = re.compile(r"^[a-z0-9-]{1,80}$")
WORKSPACE_ROOT_FILES = ("SOUL.md", "IDENTITY.md", "AGENTS.md")
PENDING_APPROVAL_TTL = timedelta(minutes=15)
EXECUTE_AUDIT_EVENTS = {"execute-started", "execute-failed", "execute-succeeded"}


@dataclass(frozen=True)
class Plan:
    clone_id: str
    agent_id: str
    parent_workspace: Path
    clone_workspace: Path
    staging_workspace: Path


def utc_now(current_time: datetime | None = None) -> datetime:
    current = current_time or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc)


def get_openclaw_root() -> Path:
    return (Path.home() / ".openclaw").expanduser().resolve()


def ensure_within_openclaw(path: Path, openclaw_root: Path) -> Path:
    resolved = path.expanduser().resolve()
    root = openclaw_root.expanduser().resolve()
    if root not in (resolved, *resolved.parents):
        raise ValueError(f"Path escapes ~/.openclaw boundary: {resolved}")
    return resolved


def count_workspaces(openclaw_root: Path) -> int:
    if not openclaw_root.exists():
        return 0
    return len(
        [
            p
            for p in openclaw_root.iterdir()
            if p.is_dir() and (p.name == "workspace" or p.name.startswith("workspace-"))
        ]
    )


def ensure_no_symlinks(workspace: Path) -> None:
    for entry in workspace.rglob("*"):
        if entry.is_symlink():
            raise ValueError(f"Workspace contains a symlink, which is not allowed: {entry}")


def validate_parent_workspace(path: Path, openclaw_root: Path) -> Path:
    parent = ensure_within_openclaw(path, openclaw_root)
    if parent == openclaw_root:
        raise ValueError("Parent workspace must be a validated workspace directory, not ~/.openclaw itself.")
    if not parent.exists() or not parent.is_dir():
        raise ValueError(f"Parent workspace does not exist: {parent}")
    if parent.parent != openclaw_root:
        raise ValueError("Parent workspace must be a direct child of ~/.openclaw.")
    if parent.name != "workspace" and not parent.name.startswith("workspace-"):
        raise ValueError("Parent workspace must be named workspace or workspace-<agent-id>.")

    missing = [name for name in WORKSPACE_ROOT_FILES if not (parent / name).is_file()]
    if missing:
        raise ValueError(
            "Parent workspace is missing required root files: " + ", ".join(sorted(missing))
        )

    ensure_no_symlinks(parent)
    return parent


def build_plan(args: argparse.Namespace, openclaw_root: Path) -> Plan:
    if not SERIAL_RE.match(args.clone_id):
        raise ValueError("Invalid clone-id format. Expected Bob-<gen>-<system>-YYYY-MM-DD")

    agent_id = args.clone_id.lower()
    if not AGENT_RE.match(agent_id):
        raise ValueError("Derived agent-id is invalid.")

    parent = validate_parent_workspace(Path(args.parent_workspace), openclaw_root)
    clone_workspace = ensure_within_openclaw(openclaw_root / f"workspace-{agent_id}", openclaw_root)
    staging_workspace = ensure_within_openclaw(
        openclaw_root / f".replication-staging-{agent_id}",
        openclaw_root,
    )
    if clone_workspace == parent:
        raise ValueError("Clone workspace resolves to the same path as the parent workspace.")

    return Plan(
        clone_id=args.clone_id,
        agent_id=agent_id,
        parent_workspace=parent,
        clone_workspace=clone_workspace,
        staging_workspace=staging_workspace,
    )


def write_audit(openclaw_root: Path, payload: dict) -> None:
    audit_path = openclaw_root / "replication-audit.log"
    with audit_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")


def last_execute_time(openclaw_root: Path) -> datetime | None:
    audit_path = openclaw_root / "replication-audit.log"
    if not audit_path.exists():
        return None
    last_exec: datetime | None = None
    with audit_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if obj.get("event") not in EXECUTE_AUDIT_EVENTS:
                    continue
                ts = obj.get("timestamp_utc")
                if not isinstance(ts, str):
                    continue
                parsed = datetime.fromisoformat(ts)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                if last_exec is None or parsed > last_exec:
                    last_exec = parsed
            except (json.JSONDecodeError, ValueError):
                continue
    return last_exec


def pending_approval_path(openclaw_root: Path, clone_id: str) -> Path:
    return openclaw_root / "replication-pending" / f"{clone_id}.json"


def remove_pending_approval(openclaw_root: Path, clone_id: str) -> None:
    path = pending_approval_path(openclaw_root, clone_id)
    if path.exists():
        path.unlink()


def safe_rmtree(path: Path, openclaw_root: Path) -> None:
    resolved = ensure_within_openclaw(path, openclaw_root)
    if resolved == openclaw_root:
        raise ValueError("Refusing to delete ~/.openclaw root.")
    if resolved.exists():
        shutil.rmtree(resolved)


def create_pending_approval(
    openclaw_root: Path,
    plan: Plan,
    purpose: str,
    existing_workspaces: int,
    current_time: datetime | None = None,
) -> dict:
    now = utc_now(current_time)
    expires = now + PENDING_APPROVAL_TTL
    nonce = secrets.token_urlsafe(12)
    payload = {
        "clone_id": plan.clone_id,
        "agent_id": plan.agent_id,
        "parent_workspace": str(plan.parent_workspace),
        "clone_workspace": str(plan.clone_workspace),
        "nonce": nonce,
        "purpose": purpose,
        "created_at_utc": now.isoformat(),
        "expires_at_utc": expires.isoformat(),
    }

    approval_path = pending_approval_path(openclaw_root, plan.clone_id)
    approval_path.parent.mkdir(parents=True, exist_ok=True)
    approval_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    write_audit(
        openclaw_root,
        {
            "timestamp_utc": now.isoformat(),
            "event": "dry-run-created",
            "clone_id": plan.clone_id,
            "agent_id": plan.agent_id,
            "parent_workspace": str(plan.parent_workspace),
            "clone_workspace": str(plan.clone_workspace),
            "existing_workspaces": existing_workspaces,
            "purpose": purpose,
            "pending_expires_at_utc": expires.isoformat(),
        },
    )
    return payload


def load_pending_approval(
    openclaw_root: Path,
    plan: Plan,
    purpose: str,
    confirm: str,
    current_time: datetime | None = None,
) -> dict:
    approval_path = pending_approval_path(openclaw_root, plan.clone_id)
    if not approval_path.exists():
        raise ValueError("No pending approval found. Run the safe runner in dry-run mode first.")

    try:
        pending = json.loads(approval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Pending approval record is invalid. Re-run dry-run mode.") from exc

    expires_raw = pending.get("expires_at_utc")
    nonce = pending.get("nonce")
    if not isinstance(expires_raw, str) or not isinstance(nonce, str):
        raise ValueError("Pending approval record is incomplete. Re-run dry-run mode.")

    expires_at = datetime.fromisoformat(expires_raw)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    now = utc_now(current_time)
    if now > expires_at:
        remove_pending_approval(openclaw_root, plan.clone_id)
        raise ValueError("Pending approval expired. Re-run dry-run mode to get a new confirmation token.")

    expected_values = {
        "clone_id": plan.clone_id,
        "agent_id": plan.agent_id,
        "parent_workspace": str(plan.parent_workspace),
        "clone_workspace": str(plan.clone_workspace),
        "purpose": purpose,
    }
    for key, expected in expected_values.items():
        if pending.get(key) != expected:
            raise ValueError(f"Pending approval does not match the provided {key.replace('_', ' ')}.")

    expected_confirm = f"REPLICATE {plan.clone_id} {nonce}"
    if confirm != expected_confirm:
        raise ValueError("Invalid confirmation token. Expected exact: REPLICATE <clone-id> <nonce>")

    return pending


def run(argv: list[str] | None = None, current_time: datetime | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe Bobiverse replication runner")
    parser.add_argument("--clone-id", required=True)
    parser.add_argument("--parent-workspace", required=True)
    parser.add_argument("--purpose", required=True, help="Why replication is needed now")
    parser.add_argument(
        "--confirm",
        default="",
        help="Must equal: REPLICATE <clone-id> <nonce> for execute mode",
    )
    parser.add_argument("--execute", action="store_true", help="Perform changes. Default is dry-run.")
    parser.add_argument(
        "--allow-high-workspace-count",
        action="store_true",
        help="Required when existing workspaces >= 10",
    )
    parser.add_argument(
        "--override-cooldown-reason",
        default="",
        help="Required to bypass 24h cooldown between confirmed execute runs",
    )

    args = parser.parse_args(argv)
    openclaw_root = get_openclaw_root()
    openclaw_root.mkdir(parents=True, exist_ok=True)

    purpose = args.purpose.strip()
    if len(purpose) < 12:
        raise ValueError("Purpose statement too short; provide concrete justification.")

    plan = build_plan(args, openclaw_root)

    existing = count_workspaces(openclaw_root)
    if existing >= 10 and not args.allow_high_workspace_count:
        raise ValueError("Workspace count >= 10. Re-run with --allow-high-workspace-count to continue.")

    cooldown_override = args.override_cooldown_reason.strip()
    base_summary = {
        "clone_id": plan.clone_id,
        "agent_id": plan.agent_id,
        "parent_workspace": str(plan.parent_workspace),
        "clone_workspace": str(plan.clone_workspace),
        "existing_workspaces": existing,
        "purpose": purpose,
        "cooldown_override_reason": cooldown_override or None,
    }

    if not args.execute:
        pending = create_pending_approval(
            openclaw_root,
            plan,
            purpose,
            existing,
            current_time=current_time,
        )
        print(
            json.dumps(
                {
                    "timestamp_utc": pending["created_at_utc"],
                    "event": "dry-run-created",
                    **base_summary,
                    "pending_expires_at_utc": pending["expires_at_utc"],
                    "confirm_token": f"REPLICATE {plan.clone_id} {pending['nonce']}",
                },
                indent=2,
            )
        )
        return 0

    load_pending_approval(
        openclaw_root,
        plan,
        purpose,
        args.confirm,
        current_time=current_time,
    )

    previous_exec = last_execute_time(openclaw_root)
    if previous_exec is not None:
        hours_since = (utc_now(current_time) - previous_exec).total_seconds() / 3600.0
        if hours_since < 24.0 and len(cooldown_override) < 12:
            raise ValueError(
                "24h cooldown active. Provide --override-cooldown-reason with concrete necessity to proceed."
            )

    if plan.clone_workspace.exists():
        raise ValueError(f"Clone workspace already exists: {plan.clone_workspace}")

    if plan.staging_workspace.exists():
        safe_rmtree(plan.staging_workspace, openclaw_root)

    started_at = utc_now(current_time)
    write_audit(
        openclaw_root,
        {
            "timestamp_utc": started_at.isoformat(),
            "event": "execute-started",
            **base_summary,
            "staging_workspace": str(plan.staging_workspace),
        },
    )

    try:
        shutil.copytree(plan.parent_workspace, plan.staging_workspace, symlinks=True)
        ensure_no_symlinks(plan.staging_workspace)
        shutil.move(str(plan.staging_workspace), str(plan.clone_workspace))
        subprocess.run(
            ["openclaw", "agents", "add", plan.agent_id, "--workspace", str(plan.clone_workspace)],
            check=True,
            shell=False,
        )
    except Exception as exc:
        cleanup_errors: list[str] = []
        for candidate in (plan.staging_workspace, plan.clone_workspace):
            try:
                safe_rmtree(candidate, openclaw_root)
            except FileNotFoundError:
                continue
            except Exception as cleanup_exc:  # pragma: no cover - cleanup failure is unlikely
                cleanup_errors.append(f"{candidate}: {cleanup_exc}")

        error_text = f"{type(exc).__name__}: {exc}"
        if cleanup_errors:
            error_text = f"{error_text}; cleanup issues: {'; '.join(cleanup_errors)}"

        write_audit(
            openclaw_root,
            {
                "timestamp_utc": utc_now(current_time).isoformat(),
                "event": "execute-failed",
                **base_summary,
                "staging_workspace": str(plan.staging_workspace),
                "error": error_text,
            },
        )
        remove_pending_approval(openclaw_root, plan.clone_id)
        raise

    write_audit(
        openclaw_root,
        {
            "timestamp_utc": utc_now(current_time).isoformat(),
            "event": "execute-succeeded",
            **base_summary,
            "staging_workspace": str(plan.staging_workspace),
        },
    )
    remove_pending_approval(openclaw_root, plan.clone_id)

    print(
        json.dumps(
            {
                "timestamp_utc": utc_now(current_time).isoformat(),
                "event": "execute-succeeded",
                **base_summary,
                "status": "ok",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
