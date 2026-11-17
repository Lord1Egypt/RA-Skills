#!/usr/bin/env python3
"""Locked, revisioned JSON blackboard helper for multi-model handoffs.

Schema-compatible upgrade of the original helper. Existing schema_version=1
boards remain valid; route lifecycle state is recorded as typed audit actions
rather than by changing the top-level board shape.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

COLLECTIONS = (
    "facts",
    "inferences",
    "user_decisions",
    "evidence",
    "actions",
    "test_results",
    "failed_attempts",
    "open_questions",
)
STATUSES = {"active", "completed", "blocked", "needs_user", "needs_verification"}
TOP_KEYS = {
    "schema_version",
    "task_id",
    "goal",
    "status",
    "policy",
    "revision",
    *COLLECTIONS,
    "next",
    "hop_count",
    "updated_by",
    "updated_at",
}
TRANSITIONS = {
    "active": {"needs_user", "needs_verification", "blocked", "completed"},
    "needs_user": {"active"},
    "needs_verification": {"active", "blocked", "completed"},
    "blocked": set(),
    "completed": set(),
}

ROUTE_PREFIX = "ROUTE:"
ROUTE_CLAIM_PREFIX = "ROUTE_CLAIM:"
ROUTE_RESOLVE_PREFIX = "ROUTE_RESOLVE:"
ROUTE_FAIL_PREFIX = "ROUTE_FAIL:"
STATE_PREFIX = "STATE:"
POLICY_PREFIX = "POLICY:"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.I,
)
PROVENANCE_KINDS = {"file", "tool", "url", "user", "command", "model_output"}
DEFAULT_BACKUP_LIMIT = 20


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def now() -> str:
    return utc_now().isoformat(timespec="microseconds").replace("+00:00", "Z")


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def norm(value: Any) -> str:
    return " ".join(str(value).strip().split())


def norm_lower(value: Any) -> str:
    return norm(value).casefold()


def load(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("board root must be a JSON object")
    return data


@contextmanager
def board_lock(path: str | Path, exclusive: bool = True):
    lock_path = Path(f"{path}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _backup_limit() -> int:
    raw = os.environ.get("BLACKBOARD_BACKUP_LIMIT", str(DEFAULT_BACKUP_LIMIT))
    try:
        return max(0, min(int(raw), 500))
    except ValueError:
        return DEFAULT_BACKUP_LIMIT


def _fsync_dir(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _prune_backups(path: Path) -> None:
    limit = _backup_limit()
    backups = sorted(
        path.parent.glob(f"{path.name}.bak.*"),
        key=lambda item: item.name,
        reverse=True,
    )
    for stale in backups[limit:]:
        try:
            stale.unlink()
        except FileNotFoundError:
            pass


def atomic_write(path: str | Path, data: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and _backup_limit() > 0:
        stamp = utc_now().strftime("%Y%m%dT%H%M%S.%fZ")
        backup = target.with_name(f"{target.name}.bak.{stamp}")
        shutil.copyfile(target, backup)
        with backup.open("rb") as handle:
            os.fsync(handle.fileno())

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, target)
        _fsync_dir(target.parent)
        _prune_backups(target)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def route_tuple(nxt: dict[str, Any]) -> list[str]:
    return [
        norm_lower(nxt.get(key, ""))
        for key in ("capability_needed", "recommended_model", "instruction")
    ]


def _entry_metadata(entry: dict[str, Any]) -> dict[str, Any]:
    value = entry.get("metadata")
    return value if isinstance(value, dict) else {}


def _audit_event(entry: dict[str, Any]) -> str:
    event = _entry_metadata(entry).get("event")
    return str(event or "")


def _route_id_from_entry(entry: dict[str, Any]) -> str | None:
    metadata = _entry_metadata(entry)
    candidate = metadata.get("route_id")
    if isinstance(candidate, str) and candidate:
        return candidate
    for provenance in entry.get("provenance", []):
        if not isinstance(provenance, dict):
            continue
        candidate = provenance.get("route_id")
        if isinstance(candidate, str) and candidate:
            return candidate
    return None


def _route_payload_from_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    metadata = _entry_metadata(entry)
    payload = metadata.get("payload")
    if isinstance(payload, dict):
        return payload
    for provenance in entry.get("provenance", []):
        if not isinstance(provenance, dict):
            continue
        if provenance.get("locator") not in {"route_payload", "route_tuple"}:
            continue
        excerpt = provenance.get("excerpt")
        if not isinstance(excerpt, str):
            continue
        try:
            decoded = json.loads(excerpt)
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, dict):
            return decoded
        if isinstance(decoded, list) and len(decoded) == 3:
            return {
                "capability_needed": decoded[0],
                "recommended_model": decoded[1],
                "instruction": decoded[2],
            }
    return None


def route_records(board: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Reconstruct route lifecycle state from append-only audit actions."""
    records: dict[str, dict[str, Any]] = {}
    legacy_counter = 0

    for entry in board.get("actions", []):
        if not isinstance(entry, dict):
            continue
        event = _audit_event(entry)
        content = str(entry.get("content", ""))
        route_id = _route_id_from_entry(entry)

        if event == "route_created" or content.startswith(ROUTE_PREFIX):
            payload = _route_payload_from_entry(entry)
            if route_id is None:
                legacy_counter += 1
                legacy_key = str(entry.get("entry_id") or legacy_counter)
                route_id = str(
                    uuid.uuid5(uuid.NAMESPACE_URL, f"blackboard-route:{legacy_key}")
                )
            if payload is None:
                # The original format only preserved the route tuple in provenance.
                payload = {
                    "capability_needed": content[len(ROUTE_PREFIX) :].strip(),
                    "recommended_model": "",
                    "instruction": "",
                }
            records[route_id] = {
                "route_id": route_id,
                "state": "pending",
                "payload": payload,
                "created_at": entry.get("created_at"),
                "created_by": (entry.get("written_by") or {}).get("model"),
                "created_entry_id": entry.get("entry_id"),
                "claim": None,
                "resolution": None,
            }
            continue

        if route_id is None or route_id not in records:
            continue

        record = records[route_id]
        if event == "route_claimed" or content.startswith(ROUTE_CLAIM_PREFIX):
            record["state"] = "claimed"
            record["claim"] = {
                "model": (entry.get("written_by") or {}).get("model"),
                "agent": (entry.get("written_by") or {}).get("agent"),
                "unit": _entry_metadata(entry).get("unit"),
                "lease_until": _entry_metadata(entry).get("lease_until"),
                "claimed_at": entry.get("created_at"),
                "entry_id": entry.get("entry_id"),
            }
        elif event == "route_resolved" or content.startswith(ROUTE_RESOLVE_PREFIX):
            record["state"] = "resolved"
            record["resolution"] = {
                "model": (entry.get("written_by") or {}).get("model"),
                "at": entry.get("created_at"),
                "entry_id": entry.get("entry_id"),
                "result_entry_ids": _entry_metadata(entry).get("result_entry_ids", []),
            }
        elif event == "route_failed" or content.startswith(ROUTE_FAIL_PREFIX):
            record["state"] = "failed"
            record["resolution"] = {
                "model": (entry.get("written_by") or {}).get("model"),
                "at": entry.get("created_at"),
                "entry_id": entry.get("entry_id"),
                "error": _entry_metadata(entry).get("error"),
            }

    return records


def active_route(board: dict[str, Any]) -> dict[str, Any] | None:
    if not any(str(value).strip() for value in (board.get("next") or {}).values()):
        return None
    wanted = route_tuple(board["next"])
    candidates = [
        record
        for record in route_records(board).values()
        if record["state"] in {"pending", "claimed"}
        and route_tuple(record.get("payload") or {}) == wanted
    ]
    if candidates:
        return candidates[-1]

    # Compatibility for boards created by the old helper where the route tuple
    # may be incomplete in the action audit entry.
    candidates = [
        record
        for record in route_records(board).values()
        if record["state"] in {"pending", "claimed"}
    ]
    return candidates[-1] if candidates else None


def route_history(board: dict[str, Any]) -> list[list[str]]:
    return [route_tuple(record["payload"]) for record in route_records(board).values()]


def decision_has_user_provenance(entry: dict[str, Any]) -> bool:
    writer = entry.get("written_by") or {}
    return str(writer.get("model", "")).startswith("user/") and any(
        isinstance(item, dict) and item.get("kind") == "user"
        for item in entry.get("provenance", [])
    )


def approval_used(board: dict[str, Any], entry_id: str) -> bool:
    marker = f"approved by {entry_id}"
    return any(marker in str(entry.get("content", "")) for entry in board["actions"])


def policy_approval_used(board: dict[str, Any], entry_id: str) -> bool:
    marker = f"approval {entry_id}"
    return any(
        str(entry.get("content", "")).startswith(POLICY_PREFIX)
        and marker in str(entry.get("content", ""))
        for entry in board["actions"]
    )


def target_blocked(board: dict[str, Any], target: str) -> str | None:
    normalised_target = norm_lower(target).rstrip("/")
    for entry in board["user_decisions"]:
        content = norm(entry.get("content", ""))
        if content.upper().startswith("DO_NOT_TOUCH:"):
            blocked = norm_lower(content.split(":", 1)[1]).rstrip("/")
            if normalised_target == blocked or (
                blocked and normalised_target.startswith(f"{blocked}/")
            ):
                return str(entry["entry_id"])
    return None


def validate_entry(entry: dict[str, Any], collection: str, errors: list[str]) -> None:
    prefix = f"{collection}/{entry.get('entry_id', '?')}"
    for key in ("entry_id", "content", "written_by", "provenance", "verified_by", "created_at"):
        if key not in entry:
            errors.append(f"{prefix}: missing {key}")

    try:
        uuid.UUID(str(entry.get("entry_id", "")))
    except (ValueError, TypeError, AttributeError):
        errors.append(f"{prefix}: invalid entry_id UUID")

    if not isinstance(entry.get("content"), str) or not entry.get("content", "").strip():
        errors.append(f"{prefix}: non-empty content required")

    writer = entry.get("written_by", {})
    writer_model = writer.get("model", "") if isinstance(writer, dict) else ""
    if not str(writer_model).strip():
        errors.append(f"{prefix}: written_by.model required")

    created_at = parse_time(entry.get("created_at"))
    if created_at is None:
        errors.append(f"{prefix}: created_at must be ISO-8601")

    provenance_items = entry.get("provenance", [])
    if not isinstance(provenance_items, list) or not provenance_items:
        errors.append(f"{prefix}: non-empty provenance required")
    else:
        for index, item in enumerate(provenance_items):
            item_prefix = f"{prefix}: provenance[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_prefix} must be object")
                continue
            if item.get("kind") not in PROVENANCE_KINDS or not item.get("source"):
                errors.append(f"{item_prefix} needs valid kind and source")
            if item.get("sha256") and not SHA256_RE.fullmatch(str(item["sha256"])):
                errors.append(f"{item_prefix}: invalid sha256")
            if item.get("route_id") and not UUID_RE.fullmatch(str(item["route_id"])):
                errors.append(f"{item_prefix}: invalid route_id")

    metadata = entry.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append(f"{prefix}: metadata must be object")
    elif isinstance(metadata, dict) and metadata.get("route_id"):
        if not UUID_RE.fullmatch(str(metadata["route_id"])):
            errors.append(f"{prefix}: metadata.route_id must be UUID")

    if collection == "user_decisions" and not decision_has_user_provenance(entry):
        errors.append(f"{prefix}: user decision requires user/* writer and user provenance")
    if collection == "test_results" and not re.match(
        r"^(PASS|FAIL):", str(entry.get("content", "")), re.I
    ):
        errors.append(f"{prefix}: test result must begin PASS: or FAIL:")

    confidence = entry.get("confidence")
    if confidence is not None and (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not 0 <= confidence <= 1
    ):
        errors.append(f"{prefix}: confidence must be 0..1")

    verifications = entry.get("verified_by", [])
    if not isinstance(verifications, list):
        errors.append(f"{prefix}: verified_by must be list")
    else:
        seen_verifiers: set[str] = set()
        for verification in verifications:
            if (
                not isinstance(verification, dict)
                or not verification.get("model")
                or parse_time(verification.get("at")) is None
                or not isinstance(verification.get("provenance"), list)
                or not verification.get("provenance")
            ):
                errors.append(f"{prefix}: malformed verification")
                continue
            verifier = str(verification["model"])
            if verifier == writer_model:
                errors.append(f"{prefix}: writer cannot self-verify")
            if verifier in seen_verifiers:
                errors.append(f"{prefix}: duplicate verifier {verifier}")
            seen_verifiers.add(verifier)


def independent_pass(board: dict[str, Any]) -> bool:
    action_writers = {
        (entry.get("written_by") or {}).get("model")
        for entry in board["actions"]
        if _audit_event(entry)
        not in {
            "route_created",
            "route_claimed",
            "route_resolved",
            "route_failed",
            "state_transition",
            "policy_change",
        }
        and not str(entry.get("content", "")).startswith(
            (
                ROUTE_PREFIX,
                ROUTE_CLAIM_PREFIX,
                ROUTE_RESOLVE_PREFIX,
                ROUTE_FAIL_PREFIX,
                STATE_PREFIX,
                POLICY_PREFIX,
            )
        )
    }
    action_writers.discard(None)

    for entry in board["test_results"]:
        if not str(entry.get("content", "")).upper().startswith("PASS:"):
            continue
        writer = (entry.get("written_by") or {}).get("model")
        if writer and writer not in action_writers:
            return True
        for verification in entry.get("verified_by", []):
            verifier = verification.get("model")
            if verifier and verifier != writer and verifier not in action_writers:
                return True
    return False


def validate(board: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(board, dict):
        return ["root must be object"]

    extra = set(board) - TOP_KEYS
    missing = TOP_KEYS - set(board)
    if extra:
        errors.append("unknown top-level keys: " + ", ".join(sorted(extra)))
    if missing:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing)))
    if errors:
        return errors

    if board["schema_version"] != 1:
        errors.append("schema_version must be 1")
    try:
        uuid.UUID(str(board["task_id"]))
    except (ValueError, TypeError, AttributeError):
        errors.append("task_id is not UUID")
    if not isinstance(board["goal"], str) or not board["goal"].strip():
        errors.append("goal required")
    if board["status"] not in STATUSES:
        errors.append("invalid status")

    policy = board["policy"]
    if (
        not isinstance(policy, dict)
        or set(policy) != {"max_hops"}
        or isinstance(policy.get("max_hops"), bool)
        or not isinstance(policy.get("max_hops"), int)
        or policy.get("max_hops", 0) < 1
    ):
        errors.append("policy.max_hops must be positive integer")
        max_hops = 0
    else:
        max_hops = policy["max_hops"]

    if (
        isinstance(board["revision"], bool)
        or not isinstance(board["revision"], int)
        or board["revision"] < 0
    ):
        errors.append("revision must be non-negative integer")
    if (
        isinstance(board["hop_count"], bool)
        or not isinstance(board["hop_count"], int)
        or board["hop_count"] < 0
    ):
        errors.append("hop_count must be non-negative integer")
    elif board["hop_count"] > max_hops:
        errors.append("hop_count exceeds board policy")

    if (
        not isinstance(board["next"], dict)
        or set(board["next"])
        != {"capability_needed", "recommended_model", "instruction"}
        or not all(isinstance(value, str) for value in board["next"].values())
    ):
        errors.append("invalid next object")

    if not isinstance(board["updated_by"], str) or not board["updated_by"].strip():
        errors.append("updated_by required")
    if parse_time(board["updated_at"]) is None:
        errors.append("updated_at must be ISO-8601")

    all_ids: list[Any] = []
    for collection in COLLECTIONS:
        if not isinstance(board[collection], list):
            errors.append(f"{collection} must be list")
            continue
        for entry in board[collection]:
            if not isinstance(entry, dict):
                errors.append(f"{collection}: entry must be object")
                continue
            all_ids.append(entry.get("entry_id"))
            validate_entry(entry, collection, errors)
    if len(all_ids) != len(set(all_ids)):
        errors.append("entry_id reused")

    pending = active_route(board)
    next_has_values = any(value.strip() for value in board["next"].values())
    if next_has_values and pending is None:
        errors.append("next is populated but no active route audit record exists")
    if not next_has_values:
        active_records = [
            record
            for record in route_records(board).values()
            if record["state"] in {"pending", "claimed"}
        ]
        if active_records:
            errors.append("active route exists while next is empty")

    if board["status"] == "completed":
        if next_has_values:
            errors.append("completed requires empty next")
        if not independent_pass(board):
            errors.append("completed requires independent PASS")
    if board["status"] == "needs_user" and not board["open_questions"]:
        errors.append("needs_user requires open_questions")
    if board["status"] == "needs_verification" and "verif" not in board["next"].get(
        "capability_needed", ""
    ).lower():
        errors.append("needs_verification must request verification")

    return errors


def require_valid(board: dict[str, Any]) -> None:
    errors = validate(board)
    if errors:
        raise SystemExit("INVALID\n- " + "\n- ".join(errors))


def check_revision(board: dict[str, Any], expected: int | None) -> None:
    if expected is not None and board["revision"] != expected:
        raise SystemExit(
            f"revision conflict: expected {expected}, found {board['revision']}"
        )


def provenance(args: argparse.Namespace) -> list[dict[str, Any]]:
    item: dict[str, Any] = {"kind": args.kind, "source": args.source}
    for key in ("locator", "sha256", "excerpt"):
        value = getattr(args, key, None)
        if value:
            item[key] = value
    route_id = getattr(args, "route_id", None)
    if route_id:
        item["route_id"] = route_id
    return [item]


def make_entry(args: argparse.Namespace) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "entry_id": str(uuid.uuid4()),
        "content": args.content,
        "written_by": {"model": args.model},
        "provenance": provenance(args),
        "verified_by": [],
        "created_at": now(),
    }
    if getattr(args, "agent", None):
        entry["written_by"]["agent"] = args.agent
    if getattr(args, "confidence", None) is not None:
        entry["confidence"] = args.confidence
    if getattr(args, "route_id", None):
        entry["metadata"] = {"route_id": args.route_id}
    return entry


def audit_entry(
    model: str,
    content: str,
    event: str,
    *,
    agent: str | None = None,
    route_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    excerpt: str | None = None,
) -> dict[str, Any]:
    provenance_item: dict[str, Any] = {
        "kind": "model_output",
        "source": model,
        "locator": event,
    }
    if route_id:
        provenance_item["route_id"] = route_id
    if excerpt is not None:
        provenance_item["excerpt"] = excerpt
    entry_metadata = {"event": event}
    if route_id:
        entry_metadata["route_id"] = route_id
    if metadata:
        entry_metadata.update(metadata)
    entry: dict[str, Any] = {
        "entry_id": str(uuid.uuid4()),
        "content": content,
        "written_by": {"model": model},
        "provenance": [provenance_item],
        "verified_by": [],
        "created_at": now(),
        "metadata": entry_metadata,
    }
    if agent:
        entry["written_by"]["agent"] = agent
    return entry


def commit(path: str | Path, board: dict[str, Any], model: str) -> None:
    board["revision"] += 1
    board["updated_by"] = model
    board["updated_at"] = now()
    require_valid(board)
    atomic_write(path, board)


def last_state_time(board: dict[str, Any], state: str) -> str:
    times = [
        entry["created_at"]
        for entry in board["actions"]
        if _audit_event(entry) == "state_transition"
        and str(entry.get("content", "")).endswith(f" -> {state}")
    ]
    return max(times, default="")


def entry_for_id(board: dict[str, Any], entry_id: str) -> dict[str, Any] | None:
    return next(
        (
            entry
            for collection in COLLECTIONS
            for entry in board[collection]
            if entry.get("entry_id") == entry_id
        ),
        None,
    )


def route_results(board: dict[str, Any], route_id: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for collection in COLLECTIONS:
        if collection == "actions":
            continue
        for entry in board[collection]:
            if _route_id_from_entry(entry) == route_id:
                output.append({"collection": collection, **entry})
    output.sort(key=lambda item: item.get("created_at", ""))
    return output


def _print_result(payload: dict[str, Any], as_json: bool, fallback: str) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(fallback)


def cmd_init(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        if Path(args.board).exists():
            raise SystemExit("board already exists")
        board: dict[str, Any] = {
            "schema_version": 1,
            "task_id": str(uuid.uuid4()),
            "goal": args.goal,
            "status": "active",
            "policy": {"max_hops": args.max_hops},
            "revision": 0,
        }
        for collection in COLLECTIONS:
            board[collection] = []
        board["next"] = {
            "capability_needed": "",
            "recommended_model": "",
            "instruction": "",
        }
        board.update(hop_count=0, updated_by=args.model, updated_at=now())
        require_valid(board)
        atomic_write(args.board, board)
        _print_result(
            {"ok": True, "task_id": board["task_id"], "revision": 0},
            args.json,
            board["task_id"],
        )


def cmd_show(args: argparse.Namespace) -> None:
    with board_lock(args.board, False):
        board = load(args.board)
        require_valid(board)
        print(json.dumps(board, indent=2, ensure_ascii=False))


def cmd_summary(args: argparse.Namespace) -> None:
    limit = max(1, min(args.limit, 50))
    with board_lock(args.board, False):
        board = load(args.board)
        require_valid(board)
        pending = active_route(board)
        recent = {
            collection: board[collection][-limit:]
            for collection in COLLECTIONS
            if board[collection]
        }
        payload = {
            "ok": True,
            "task_id": board["task_id"],
            "goal": board["goal"],
            "status": board["status"],
            "revision": board["revision"],
            "hop_count": board["hop_count"],
            "max_hops": board["policy"]["max_hops"],
            "next": board["next"],
            "active_route": pending,
            "counts": {collection: len(board[collection]) for collection in COLLECTIONS},
            "recent": recent,
            "updated_by": board["updated_by"],
            "updated_at": board["updated_at"],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_validate(args: argparse.Namespace) -> None:
    with board_lock(args.board, False):
        errors = validate(load(args.board))
    if errors:
        if args.json:
            print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        else:
            print("INVALID\n- " + "\n- ".join(errors))
        raise SystemExit(1)
    _print_result({"ok": True, "valid": True}, args.json, "VALID")


def cmd_guard(args: argparse.Namespace) -> None:
    with board_lock(args.board, False):
        board = load(args.board)
        require_valid(board)
        hit = target_blocked(board, args.target)
        if hit:
            raise SystemExit(f"DO_NOT_TOUCH constraint {hit} blocks target")
        _print_result({"ok": True, "allowed": True}, args.json, "ALLOWED")


def cmd_add(args: argparse.Namespace) -> None:
    if args.route_id and not UUID_RE.fullmatch(args.route_id):
        raise SystemExit("--route-id must be a UUID")
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        if board["status"] in {"completed", "blocked"}:
            raise SystemExit("terminal board is immutable")
        if args.collection == "user_decisions" and (
            not args.model.startswith("user/") or args.kind != "user"
        ):
            raise SystemExit("user_decisions require user/* model and --kind user")
        if args.collection == "actions":
            if not args.target:
                raise SystemExit("actions require --target and prior guard")
            hit = target_blocked(board, args.target)
            if hit:
                raise SystemExit(f"DO_NOT_TOUCH constraint {hit} blocks target")
        if args.route_id:
            record = route_records(board).get(args.route_id)
            if record is None:
                raise SystemExit("route_id not found")
            if record["state"] in {"resolved", "failed"}:
                raise SystemExit("cannot append to a terminal route")

        if args.destructive:
            if args.collection != "actions":
                raise SystemExit("--destructive only applies to actions")
            approvals = {entry["entry_id"]: entry for entry in board["user_decisions"]}
            approved = approvals.get(args.approval_entry or "")
            wanted = "approve: " + norm_lower(args.target)
            if (
                not approved
                or not decision_has_user_provenance(approved)
                or norm_lower(approved["content"]) != wanted
            ):
                raise SystemExit(
                    "destructive action requires exact user-provenance APPROVE: <target>"
                )
            if approval_used(board, approved["entry_id"]):
                raise SystemExit("approval already used")
            args.content = (
                f"DESTRUCTIVE target {norm(args.target)} "
                f"(approved by {approved['entry_id']}): {args.content}"
            )
        elif args.approval_entry:
            raise SystemExit("--approval-entry requires --destructive")

        entry = make_entry(args)
        board[args.collection].append(entry)
        commit(args.board, board, args.model)
        _print_result(
            {
                "ok": True,
                "entry_id": entry["entry_id"],
                "collection": args.collection,
                "revision": board["revision"],
                "route_id": args.route_id,
            },
            args.json,
            entry["entry_id"],
        )


def cmd_verify(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        if board["status"] in {"completed", "blocked"}:
            raise SystemExit("terminal board is immutable")
        found = entry_for_id(board, args.entry_id)
        if not found:
            raise SystemExit("entry not found")
        if found["written_by"]["model"] == args.model:
            raise SystemExit("self-verification forbidden")
        if any(item.get("model") == args.model for item in found["verified_by"]):
            raise SystemExit("model has already verified this entry")
        found["verified_by"].append(
            {"model": args.model, "at": now(), "provenance": provenance(args)}
        )
        commit(args.board, board, args.model)
        _print_result(
            {"ok": True, "verified": args.entry_id, "revision": board["revision"]},
            args.json,
            "verified",
        )


def cmd_route(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        if board["status"] != "active":
            raise SystemExit("routing allowed only from active")
        current = active_route(board)
        if current:
            raise SystemExit(
                f"pending route already exists: {current['route_id']} ({current['state']})"
            )
        if board["hop_count"] >= board["policy"]["max_hops"]:
            raise SystemExit("hop limit reached")

        nxt = {
            "capability_needed": norm(args.capability),
            "recommended_model": norm(args.recommended_model),
            "instruction": norm(args.instruction),
        }
        signature = route_tuple(nxt)
        recent_signatures = route_history(board)[-3:]
        if not args.allow_repeat and signature in recent_signatures:
            raise SystemExit(
                "recent repeated route rejected; pass --allow-repeat only when new evidence justifies it"
            )

        route_id = str(uuid.uuid4())
        payload = {**nxt, "route_id": route_id}
        entry = audit_entry(
            args.model,
            f"{ROUTE_PREFIX} {route_id} {nxt['capability_needed']}",
            "route_created",
            agent=args.agent,
            route_id=route_id,
            metadata={"payload": payload},
            excerpt=json.dumps(payload, separators=(",", ":"), ensure_ascii=False),
        )
        board["actions"].append(entry)
        board["next"] = nxt
        board["hop_count"] += 1
        commit(args.board, board, args.model)
        _print_result(
            {
                "ok": True,
                "route_id": route_id,
                "hop_count": board["hop_count"],
                "revision": board["revision"],
                "next": nxt,
            },
            args.json,
            str(board["hop_count"]),
        )


def _claim_is_live(record: dict[str, Any]) -> bool:
    if record.get("state") != "claimed":
        return False
    lease_until = parse_time((record.get("claim") or {}).get("lease_until"))
    return lease_until is not None and lease_until > utc_now()


def cmd_claim_route(args: argparse.Namespace) -> None:
    lease_seconds = max(30, min(args.lease_seconds, 86400))
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        record = route_records(board).get(args.route_id)
        if record is None:
            raise SystemExit("route not found")
        if record["state"] in {"resolved", "failed"}:
            raise SystemExit(f"route is already {record['state']}")
        if record["state"] == "claimed" and _claim_is_live(record):
            claim = record.get("claim") or {}
            raise SystemExit(
                f"route already claimed by {claim.get('model')} until {claim.get('lease_until')}"
            )

        lease_until = (utc_now() + timedelta(seconds=lease_seconds)).isoformat(
            timespec="seconds"
        ).replace("+00:00", "Z")
        entry = audit_entry(
            args.model,
            f"{ROUTE_CLAIM_PREFIX} {args.route_id} unit={args.unit or 'none'}",
            "route_claimed",
            agent=args.agent,
            route_id=args.route_id,
            metadata={"unit": args.unit or None, "lease_until": lease_until},
        )
        board["actions"].append(entry)
        commit(args.board, board, args.model)
        _print_result(
            {
                "ok": True,
                "route_id": args.route_id,
                "state": "claimed",
                "unit": args.unit or None,
                "lease_until": lease_until,
                "revision": board["revision"],
            },
            args.json,
            "claimed",
        )


def _ensure_route_matches_next(board: dict[str, Any], record: dict[str, Any]) -> None:
    if route_tuple(record.get("payload") or {}) != route_tuple(board["next"]):
        raise SystemExit("route does not match the current next instruction")


def cmd_resolve_route(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        record = route_records(board).get(args.route_id)
        if record is None:
            raise SystemExit("route not found")
        if record["state"] == "resolved":
            _print_result(
                {"ok": True, "route_id": args.route_id, "state": "resolved", "idempotent": True},
                args.json,
                "resolved",
            )
            return
        if record["state"] == "failed":
            raise SystemExit("failed route cannot be resolved")
        _ensure_route_matches_next(board, record)

        result_ids = list(dict.fromkeys(args.result_entry or []))
        missing = [entry_id for entry_id in result_ids if entry_for_id(board, entry_id) is None]
        if missing:
            raise SystemExit("unknown result entry id(s): " + ", ".join(missing))
        entry = audit_entry(
            args.model,
            f"{ROUTE_RESOLVE_PREFIX} {args.route_id}",
            "route_resolved",
            agent=args.agent,
            route_id=args.route_id,
            metadata={"result_entry_ids": result_ids},
        )
        board["actions"].append(entry)
        board["next"] = {
            "capability_needed": "",
            "recommended_model": "",
            "instruction": "",
        }
        commit(args.board, board, args.model)
        _print_result(
            {
                "ok": True,
                "route_id": args.route_id,
                "state": "resolved",
                "result_entry_ids": result_ids,
                "revision": board["revision"],
            },
            args.json,
            "resolved",
        )


def cmd_fail_route(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        record = route_records(board).get(args.route_id)
        if record is None:
            raise SystemExit("route not found")
        if record["state"] == "failed":
            _print_result(
                {"ok": True, "route_id": args.route_id, "state": "failed", "idempotent": True},
                args.json,
                "failed",
            )
            return
        if record["state"] == "resolved":
            raise SystemExit("resolved route cannot be failed")
        _ensure_route_matches_next(board, record)

        entry = audit_entry(
            args.model,
            f"{ROUTE_FAIL_PREFIX} {args.route_id}: {norm(args.error)}",
            "route_failed",
            agent=args.agent,
            route_id=args.route_id,
            metadata={"error": norm(args.error)},
        )
        board["actions"].append(entry)
        board["next"] = {
            "capability_needed": "",
            "recommended_model": "",
            "instruction": "",
        }
        commit(args.board, board, args.model)
        _print_result(
            {
                "ok": True,
                "route_id": args.route_id,
                "state": "failed",
                "error": norm(args.error),
                "revision": board["revision"],
            },
            args.json,
            "failed",
        )


def cmd_route_status(args: argparse.Namespace) -> None:
    with board_lock(args.board, False):
        board = load(args.board)
        require_valid(board)
        record = (
            route_records(board).get(args.route_id)
            if args.route_id
            else active_route(board)
        )
        if record is None:
            payload = {"ok": True, "found": False, "revision": board["revision"]}
        else:
            payload = {
                "ok": True,
                "found": True,
                "revision": board["revision"],
                **record,
                "claim_live": _claim_is_live(record),
                "result_count": len(route_results(board, record["route_id"])),
            }
        _print_result(payload, args.json, payload.get("state", "none"))


def cmd_route_results(args: argparse.Namespace) -> None:
    with board_lock(args.board, False):
        board = load(args.board)
        require_valid(board)
        record = route_records(board).get(args.route_id)
        if record is None:
            raise SystemExit("route not found")
        results = route_results(board, args.route_id)
        payload = {
            "ok": True,
            "route_id": args.route_id,
            "state": record["state"],
            "revision": board["revision"],
            "count": len(results),
            "results": results,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        old = board["status"]
        if args.status not in TRANSITIONS[old]:
            raise SystemExit(f"transition {old} -> {args.status} forbidden")
        if old == "needs_user" and args.status == "active":
            since = last_state_time(board, "needs_user")
            if not any(
                entry["created_at"] > since for entry in board["user_decisions"]
            ):
                raise SystemExit(
                    "needs_user requires a newer user decision before resume"
                )
        if args.status in {"blocked", "completed"} and active_route(board):
            raise SystemExit("resolve or fail the active route before entering a terminal state")
        if args.status == "completed":
            if not independent_pass(board):
                raise SystemExit("completion requires independent PASS")
            board["next"] = {
                "capability_needed": "",
                "recommended_model": "",
                "instruction": "",
            }
        board["actions"].append(
            audit_entry(
                args.model,
                f"{STATE_PREFIX} {old} -> {args.status}",
                "state_transition",
                agent=args.agent,
            )
        )
        board["status"] = args.status
        commit(args.board, board, args.model)
        _print_result(
            {"ok": True, "status": args.status, "revision": board["revision"]},
            args.json,
            args.status,
        )


def cmd_policy(args: argparse.Namespace) -> None:
    with board_lock(args.board, True):
        board = load(args.board)
        require_valid(board)
        check_revision(board, args.expect_revision)
        old = board["policy"]["max_hops"]
        new = args.max_hops
        if new < 1 or new < board["hop_count"]:
            raise SystemExit("max_hops cannot be below 1 or current hop_count")
        approval_id = ""
        if new > old:
            decisions = {entry["entry_id"]: entry for entry in board["user_decisions"]}
            approved = decisions.get(args.approval_entry or "")
            wanted = f"approve_policy: max_hops {old} -> {new}"
            if (
                not approved
                or not decision_has_user_provenance(approved)
                or norm_lower(approved["content"]) != wanted
            ):
                raise SystemExit(
                    "raising max_hops requires exact user-provenance APPROVE_POLICY decision"
                )
            if policy_approval_used(board, approved["entry_id"]):
                raise SystemExit("policy approval already used")
            approval_id = approved["entry_id"]
        board["policy"]["max_hops"] = new
        board["actions"].append(
            audit_entry(
                args.model,
                f"{POLICY_PREFIX} max_hops {old} -> {new} approval {approval_id or 'not-required'}",
                "policy_change",
                agent=args.agent,
            )
        )
        commit(args.board, board, args.model)
        _print_result(
            {"ok": True, "max_hops": new, "revision": board["revision"]},
            args.json,
            str(new),
        )


def add_json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="emit structured JSON")


def common_source(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", required=True)
    parser.add_argument("--agent")
    parser.add_argument("--kind", required=True, choices=sorted(PROVENANCE_KINDS))
    parser.add_argument("--source", required=True)
    parser.add_argument("--locator")
    parser.add_argument("--sha256")
    parser.add_argument("--excerpt")
    parser.add_argument("--route-id")
    parser.add_argument("--expect-revision", type=int)
    add_json_flag(parser)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="cmd", required=True)

    command = commands.add_parser("init")
    command.add_argument("board")
    command.add_argument("--goal", required=True)
    command.add_argument("--model", required=True)
    command.add_argument("--max-hops", type=int, default=6)
    add_json_flag(command)
    command.set_defaults(fn=cmd_init)

    command = commands.add_parser("show")
    command.add_argument("board")
    command.set_defaults(fn=cmd_show)

    command = commands.add_parser("summary")
    command.add_argument("board")
    command.add_argument("--limit", type=int, default=4)
    command.set_defaults(fn=cmd_summary)

    command = commands.add_parser("validate")
    command.add_argument("board")
    add_json_flag(command)
    command.set_defaults(fn=cmd_validate)

    command = commands.add_parser("guard")
    command.add_argument("board")
    command.add_argument("--target", required=True)
    add_json_flag(command)
    command.set_defaults(fn=cmd_guard)

    command = commands.add_parser("add")
    command.add_argument("board")
    command.add_argument("collection", choices=COLLECTIONS)
    command.add_argument("--content", required=True)
    command.add_argument("--confidence", type=float)
    command.add_argument("--target")
    command.add_argument("--destructive", action="store_true")
    command.add_argument("--approval-entry")
    common_source(command)
    command.set_defaults(fn=cmd_add)

    command = commands.add_parser("verify")
    command.add_argument("board")
    command.add_argument("entry_id")
    common_source(command)
    command.set_defaults(fn=cmd_verify)

    command = commands.add_parser("route")
    command.add_argument("board")
    command.add_argument("--capability", required=True)
    command.add_argument("--recommended-model", default="")
    command.add_argument("--instruction", required=True)
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--expect-revision", type=int)
    command.add_argument("--allow-repeat", action="store_true")
    add_json_flag(command)
    command.set_defaults(fn=cmd_route)

    command = commands.add_parser("claim-route")
    command.add_argument("board")
    command.add_argument("route_id")
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--unit")
    command.add_argument("--lease-seconds", type=int, default=900)
    command.add_argument("--expect-revision", type=int)
    add_json_flag(command)
    command.set_defaults(fn=cmd_claim_route)

    command = commands.add_parser("resolve-route")
    command.add_argument("board")
    command.add_argument("route_id")
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--result-entry", action="append")
    command.add_argument("--expect-revision", type=int)
    add_json_flag(command)
    command.set_defaults(fn=cmd_resolve_route)

    command = commands.add_parser("fail-route")
    command.add_argument("board")
    command.add_argument("route_id")
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--error", required=True)
    command.add_argument("--expect-revision", type=int)
    add_json_flag(command)
    command.set_defaults(fn=cmd_fail_route)

    command = commands.add_parser("route-status")
    command.add_argument("board")
    command.add_argument("--route-id")
    add_json_flag(command)
    command.set_defaults(fn=cmd_route_status)

    command = commands.add_parser("route-results")
    command.add_argument("board")
    command.add_argument("route_id")
    command.set_defaults(fn=cmd_route_results)

    command = commands.add_parser("status")
    command.add_argument("board")
    command.add_argument("status", choices=sorted(STATUSES))
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--expect-revision", type=int)
    add_json_flag(command)
    command.set_defaults(fn=cmd_status)

    command = commands.add_parser("policy")
    command.add_argument("board")
    command.add_argument("--max-hops", type=int, required=True)
    command.add_argument("--approval-entry")
    command.add_argument("--model", required=True)
    command.add_argument("--agent")
    command.add_argument("--expect-revision", type=int)
    add_json_flag(command)
    command.set_defaults(fn=cmd_policy)

    return root


def main() -> None:
    args = parser().parse_args()
    try:
        args.fn(args)
    except subprocess_errors() as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2) from error


def subprocess_errors() -> tuple[type[BaseException], ...]:
    # Kept as a function so callers can import the module without evaluating
    # optional platform-specific exception types.
    return (OSError, json.JSONDecodeError, ValueError)


if __name__ == "__main__":
    main()
