#!/usr/bin/env python3
"""Store short-lived redacted AI-draft baselines for ongoing draft-edit learning."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    root = Path(state_override).expanduser() if state_override else Path.home() / ".openclaw"
    return root / "ecommerce-gmail-customer-service"


def baseline_dir() -> Path:
    return runtime_dir() / "draft-baselines"


def config_path() -> Path:
    return runtime_dir() / "config.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(value: str) -> str:
    return re.sub(
        r"https?://\S+|[\w.+-]+@[\w.-]+|\b\d{5,}\b", "[REDACTED]", value
    )


def safe_draft_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,200}", value):
        raise SystemExit("draft-id may contain only letters, numbers, dot, underscore, or hyphen")
    return value


def baseline_path(draft_id: str) -> Path:
    return baseline_dir() / f"{safe_draft_id(draft_id)}.json"


def read_config() -> dict:
    try:
        return json.loads(config_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read runtime configuration: {exc}") from exc


def require_draft_edit_learning() -> dict:
    config = read_config()
    learning = config.get("learning", {})
    if learning.get("enabled") is not True or not learning.get("consent_granted_at"):
        raise SystemExit(
            "Ongoing draft-edit learning is disabled or has no recorded owner consent"
        )
    return config


def baseline_retention_days(config: dict) -> int:
    value = config.get("learning", {}).get("draft_baseline_retention_days")
    if not isinstance(value, int) or value < 0:
        raise SystemExit("learning.draft_baseline_retention_days must be a non-negative integer")
    return value


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def read_body(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"Unable to read draft body file: {exc}") from exc


def snapshot(args: argparse.Namespace) -> None:
    require_draft_edit_learning()
    body = redact(read_body(args.body_file))
    payload = {
        "draft_id": args.draft_id,
        "thread_id": args.thread_id,
        "message_id": args.message_id,
        "intent": args.intent,
        "created_at": now(),
        "body": body,
        "hash": hashlib.sha256(body.encode()).hexdigest(),
    }
    atomic_json(baseline_path(args.draft_id), payload)
    print(json.dumps({"saved": args.draft_id}))


def compare(args: argparse.Namespace) -> None:
    require_draft_edit_learning()
    try:
        previous = json.loads(baseline_path(args.draft_id).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read draft baseline: {exc}") from exc
    current = redact(read_body(args.body_file))
    diff = list(
        difflib.unified_diff(
            previous["body"].splitlines(), current.splitlines(), lineterm=""
        )
    )
    print(
        json.dumps(
            {
                "changed": previous["body"] != current,
                "draft_id": args.draft_id,
                "diff": diff,
            }
        )
    )


def finalize(args: argparse.Namespace) -> None:
    baseline_path(args.draft_id).unlink(missing_ok=True)
    print(json.dumps({"finalized": args.draft_id}))


def purge(_: argparse.Namespace) -> None:
    retention_days = baseline_retention_days(read_config())
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted = 0
    skipped = 0
    directory = baseline_dir()
    if directory.is_dir():
        for candidate in directory.glob("*.json"):
            try:
                created_at = datetime.fromisoformat(
                    json.loads(candidate.read_text(encoding="utf-8"))["created_at"]
                )
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)
                if created_at < cutoff:
                    candidate.unlink()
                    deleted += 1
            except (OSError, ValueError, KeyError, json.JSONDecodeError):
                skipped += 1
    print(
        json.dumps(
            {
                "deleted": deleted,
                "skipped": skipped,
                "retention_days": retention_days,
            }
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage short-lived redacted baselines for ongoing draft-edit learning"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--draft-id", required=True)
    snapshot_parser.add_argument("--thread-id", required=True)
    snapshot_parser.add_argument("--message-id", required=True)
    snapshot_parser.add_argument("--intent", required=True)
    snapshot_parser.add_argument("--body-file", required=True)
    snapshot_parser.set_defaults(func=snapshot)

    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("--draft-id", required=True)
    compare_parser.add_argument("--body-file", required=True)
    compare_parser.set_defaults(func=compare)

    finalize_parser = subparsers.add_parser("finalize")
    finalize_parser.add_argument("--draft-id", required=True)
    finalize_parser.set_defaults(func=finalize)

    purge_parser = subparsers.add_parser("purge")
    purge_parser.set_defaults(func=purge)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
