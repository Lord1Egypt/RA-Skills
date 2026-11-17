#!/usr/bin/env python3
"""Manage independent owner-controlled per-category automatic-reply permissions."""

from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


SAFE_REFERENCE = re.compile(r"[A-Za-z0-9._-]{1,200}")


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    state_root = Path(state_override).expanduser() if state_override else Path.home() / ".openclaw"
    return state_root / "ecommerce-gmail-customer-service"


def config_path() -> Path:
    return runtime_dir() / "config.json"


def permissions_path() -> Path:
    return runtime_dir() / "auto_reply_permissions.json"


def pending_path() -> Path:
    return runtime_dir() / "pending_category_confirmations.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def valid_reference(value: object) -> bool:
    return isinstance(value, str) and bool(SAFE_REFERENCE.fullmatch(value))


def require_owner_confirmation(args: argparse.Namespace) -> None:
    if not getattr(args, "confirm_owner_request", False):
        raise SystemExit(
            "This changes owner-controlled automatic-reply permissions. Confirm the current owner's request and rerun with --confirm-owner-request"
        )


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def permission_defaults() -> dict:
    return {"schema_version": 1, "categories": {}, "updated_at": None}


def pending_defaults() -> dict:
    return {"schema_version": 1, "events": {}, "updated_at": None}


def load_state(path: Path, defaults: dict, label: str) -> dict:
    if not path.exists():
        return dict(defaults)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{label} must be a JSON object")
    if not isinstance(payload.get("schema_version"), int):
        raise SystemExit(f"{label}.schema_version must be an integer")
    return payload


def load_permissions() -> dict:
    payload = load_state(
        permissions_path(), permission_defaults(), "auto-reply permission state"
    )
    if not isinstance(payload.get("categories"), dict):
        raise SystemExit("auto-reply permission state.categories must be an object")
    return payload


def load_pending() -> dict:
    payload = load_state(
        pending_path(), pending_defaults(), "pending category-confirmation state"
    )
    if not isinstance(payload.get("events"), dict):
        raise SystemExit("pending category-confirmation state.events must be an object")
    return payload


def read_config() -> dict:
    try:
        payload = json.loads(config_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read runtime configuration: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("Runtime configuration must be a JSON object")
    return payload


def category_from_item(item: object) -> dict[str, str]:
    if not isinstance(item, dict):
        raise SystemExit("Each atomic issue must be an object")
    intent_id = item.get("intent_id")
    scenario_key = item.get("scenario_key")
    if not valid_reference(intent_id) or not valid_reference(scenario_key):
        raise SystemExit(
            "Each atomic issue requires safe intent_id and scenario_key values"
        )
    return {"intent_id": intent_id, "scenario_key": scenario_key}


def category_key(category: dict[str, str]) -> str:
    return f"{category['intent_id']}::{category['scenario_key']}"


def unique_categories(categories: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for category in categories:
        key = category_key(category)
        if key not in seen:
            seen.add(key)
            result.append(category)
    return result


def load_atomic_issues(args: argparse.Namespace, label: str) -> list[dict[str, str]]:
    input_path = Path(args.input)
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read {label}: {exc}") from exc
    finally:
        if getattr(args, "delete_input", False):
            try:
                input_path.unlink(missing_ok=True)
            except OSError as exc:
                raise SystemExit(
                    f"Unable to remove consumed temporary input: {exc}"
                ) from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("atomic_issues"), list):
        raise SystemExit(f"{label} must contain a non-empty atomic_issues list")
    issues = payload["atomic_issues"]
    if not issues:
        raise SystemExit(f"{label} must contain a non-empty atomic_issues list")
    return unique_categories([category_from_item(item) for item in issues])


def require_sent_references(args: argparse.Namespace) -> dict[str, str]:
    values = {
        "draft_id": getattr(args, "draft_id", None),
        "thread_id": getattr(args, "thread_id", None),
        "sent_message_id": getattr(args, "sent_message_id", None),
    }
    invalid = [name for name, value in values.items() if not valid_reference(value)]
    if invalid:
        raise SystemExit(
            "A sent-Draft confirmation event requires safe " + ", ".join(invalid)
        )
    return values  # type: ignore[return-value]


def ensure_category(
    permissions: dict, category: dict[str, str], timestamp: str
) -> dict:
    categories = permissions["categories"]
    key = category_key(category)
    existing = categories.get(key)
    if not isinstance(existing, dict):
        existing = {
            **category,
            "enabled": False,
            "enabled_at": None,
            "disabled_at": None,
            "approval_source": None,
            "approval_event_id": None,
            "owner_confirmed_at": None,
            "first_seen_at": timestamp,
            "last_seen_at": timestamp,
        }
        categories[key] = existing
    else:
        existing["intent_id"] = category["intent_id"]
        existing["scenario_key"] = category["scenario_key"]
        existing["last_seen_at"] = timestamp
        if not isinstance(existing.get("enabled"), bool):
            existing["enabled"] = False
        for field in (
            "enabled_at",
            "disabled_at",
            "approval_source",
            "approval_event_id",
            "owner_confirmed_at",
            "first_seen_at",
        ):
            existing.setdefault(field, None)
    return existing


def event_matches(
    event: object, source: str, references: dict[str, str], categories: list[dict[str, str]]
) -> bool:
    if not isinstance(event, dict):
        return False
    if event.get("source") != source:
        return False
    if any(event.get(name) != value for name, value in references.items()):
        return False
    current = event.get("categories")
    if not isinstance(current, list):
        return False
    try:
        return {category_key(category_from_item(item)) for item in current} == {
            category_key(category) for category in categories
        }
    except SystemExit:
        return False


def record_sent(args: argparse.Namespace) -> None:
    references = require_sent_references(args)
    categories = load_atomic_issues(args, "atomic issue input")
    permissions = load_permissions()
    pending = load_pending()
    timestamp = now()
    for category in categories:
        ensure_category(permissions, category, timestamp)

    for event_id, event in pending["events"].items():
        if event_matches(event, args.source, references, categories):
            print(
                json.dumps(
                    {
                        "event_id": event_id,
                        "created": False,
                        "source": args.source,
                        "categories": categories,
                    },
                    ensure_ascii=False,
                )
            )
            return

    event_id = f"pending-{uuid.uuid4()}"
    pending["events"][event_id] = {
        "event_id": event_id,
        "source": args.source,
        **references,
        "categories": categories,
        "created_at": timestamp,
        "resolved_categories": {},
    }
    permissions["updated_at"] = timestamp
    pending["updated_at"] = timestamp
    atomic_json(permissions_path(), permissions)
    atomic_json(pending_path(), pending)
    print(
        json.dumps(
            {
                "event_id": event_id,
                "created": True,
                "source": args.source,
                "categories": categories,
            },
            ensure_ascii=False,
        )
    )


def resolve_event(args: argparse.Namespace) -> None:
    require_owner_confirmation(args)
    pending = load_pending()
    event = pending["events"].get(args.event_id)
    if not isinstance(event, dict):
        raise SystemExit("Unknown or expired category-confirmation event")
    category = category_from_item(
        {"intent_id": args.intent_id, "scenario_key": args.scenario_key}
    )
    key = category_key(category)
    event_categories = event.get("categories")
    if not isinstance(event_categories, list) or key not in {
        category_key(category_from_item(item)) for item in event_categories
    }:
        raise SystemExit("The requested category is not part of this confirmation event")

    permissions = load_permissions()
    timestamp = now()
    permission = ensure_category(permissions, category, timestamp)
    if args.value == "on":
        permission.update(
            {
                "enabled": True,
                "enabled_at": timestamp,
                "disabled_at": None,
                "approval_source": event.get("source"),
                "approval_event_id": args.event_id,
                "owner_confirmed_at": timestamp,
            }
        )
    else:
        permission.update(
            {
                "enabled": False,
                "disabled_at": timestamp,
                "approval_source": event.get("source"),
                "approval_event_id": args.event_id,
                "owner_confirmed_at": timestamp,
            }
        )

    resolutions = event.setdefault("resolved_categories", {})
    resolutions[key] = {"value": args.value, "owner_confirmed_at": timestamp}
    expected = {
        category_key(category_from_item(item)) for item in event_categories
    }
    resolved = set(resolutions) if isinstance(resolutions, dict) else set()
    resolved_event = expected.issubset(resolved)
    if resolved_event:
        pending["events"].pop(args.event_id, None)
    permissions["updated_at"] = timestamp
    pending["updated_at"] = timestamp
    atomic_json(permissions_path(), permissions)
    atomic_json(pending_path(), pending)
    print(
        json.dumps(
            {
                "event_id": args.event_id,
                "intent_id": category["intent_id"],
                "scenario_key": category["scenario_key"],
                "enabled": permission["enabled"],
                "event_resolved": resolved_event,
            },
            ensure_ascii=False,
        )
    )


def disable_category(args: argparse.Namespace) -> None:
    require_owner_confirmation(args)
    category = category_from_item(
        {"intent_id": args.intent_id, "scenario_key": args.scenario_key}
    )
    permissions = load_permissions()
    key = category_key(category)
    permission = permissions["categories"].get(key)
    if not isinstance(permission, dict):
        raise SystemExit("This category has no recorded automatic-reply permission")
    timestamp = now()
    permission.update(
        {
            "enabled": False,
            "disabled_at": timestamp,
            "owner_confirmed_at": timestamp,
        }
    )
    permissions["updated_at"] = timestamp
    atomic_json(permissions_path(), permissions)
    print(json.dumps({"category": key, "enabled": False}, ensure_ascii=False))


def disable_all(args: argparse.Namespace) -> None:
    require_owner_confirmation(args)
    permissions = load_permissions()
    timestamp = now()
    disabled = 0
    for permission in permissions["categories"].values():
        if not isinstance(permission, dict):
            continue
        if permission.get("enabled") is True:
            disabled += 1
        permission.update(
            {
                "enabled": False,
                "disabled_at": timestamp,
                "owner_confirmed_at": timestamp,
            }
        )
    permissions["updated_at"] = timestamp
    atomic_json(permissions_path(), permissions)
    print(json.dumps({"disabled": disabled, "all_categories_enabled": False}))


def check_auto_send(args: argparse.Namespace) -> None:
    config = read_config()
    automation = config.get("automation", {})
    reasons: list[dict[str, str]] = []
    if not isinstance(automation, dict) or automation.get("send_mode") != "auto_send":
        reasons.append({"code": "auto_send_disabled"})
    elif not isinstance(automation.get("auto_send_confirmed_at"), str) or not automation.get(
        "auto_send_confirmed_at"
    ):
        reasons.append({"code": "auto_send_not_confirmed"})

    try:
        categories = load_atomic_issues(args, "atomic issue input")
    except SystemExit as exc:
        reasons.append({"code": "atomic_issues_required", "detail": str(exc)})
        categories = []
    permissions = load_permissions()
    matched: list[dict[str, str]] = []
    for category in categories:
        key = category_key(category)
        permission = permissions["categories"].get(key)
        if not isinstance(permission, dict):
            reasons.append({"code": "auto_reply_permission_missing", **category})
            continue
        if permission.get("enabled") is not True:
            reasons.append({"code": "auto_reply_permission_disabled", **category})
            continue
        matched.append(category)

    result = {"allowed": not reasons, "matched_categories": matched, "reasons": reasons}
    print(json.dumps(result, ensure_ascii=False))
    if reasons:
        raise SystemExit(1)


def status(_: argparse.Namespace) -> None:
    permissions = load_permissions()
    pending = load_pending()
    categories = permissions["categories"]
    enabled = sum(
        1 for value in categories.values() if isinstance(value, dict) and value.get("enabled") is True
    )
    print(
        json.dumps(
            {
                "categories": len(categories),
                "enabled_categories": enabled,
                "pending_confirmation_events": len(pending["events"]),
                "permissions_path": str(permissions_path()),
            },
            ensure_ascii=False,
        )
    )


def pending_retention_days() -> int:
    retention = read_config().get("retention", {})
    days = retention.get("pending_category_confirmation_days") if isinstance(retention, dict) else None
    if type(days) is not int or days < 0:
        raise SystemExit(
            "retention.pending_category_confirmation_days must be a non-negative integer"
        )
    return days


def purge_events(_: argparse.Namespace) -> None:
    pending = load_pending()
    retention_days = pending_retention_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted = 0
    skipped = 0
    for event_id, event in list(pending["events"].items()):
        try:
            created_at = datetime.fromisoformat(event["created_at"])
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=timezone.utc)
            if created_at < cutoff:
                pending["events"].pop(event_id, None)
                deleted += 1
        except (KeyError, TypeError, ValueError):
            skipped += 1
    if deleted:
        pending["updated_at"] = now()
        atomic_json(pending_path(), pending)
    print(
        json.dumps(
            {
                "deleted": deleted,
                "skipped": skipped,
                "retention_days": retention_days,
            }
        )
    )
LEGACY_PERMISSION_FIELDS = (
    "auto_send_approved",
    "auto_send_approved_at",
    "auto_send_confirmation",
    "sent_draft_confirmation",
)


def migrate_legacy_memory_permissions(memory_path: Path) -> bool:
    """Move legacy in-memory flags to disabled standalone category records."""
    try:
        text = memory_path.read_text(encoding="utf-8")
        begin = "<!-- ECS_MEMORY_JSON_BEGIN -->"
        end = "<!-- ECS_MEMORY_JSON_END -->"
        body = text.split(begin, 1)[1].split(end, 1)[0].strip()
        body = body.removeprefix("```json").removesuffix("```").strip()
        memory = json.loads(body)
    except (OSError, IndexError, json.JSONDecodeError):
        return False
    playbooks = memory.get("handling_playbooks") if isinstance(memory, dict) else None
    if not isinstance(playbooks, list):
        return False
    permissions = load_permissions()
    changed = False
    timestamp = now()
    for playbook in playbooks:
        if not isinstance(playbook, dict):
            continue
        has_legacy_fields = any(field in playbook for field in LEGACY_PERMISSION_FIELDS)
        if not has_legacy_fields:
            continue
        try:
            category = category_from_item(playbook)
        except SystemExit:
            category = None
        if category:
            permission = ensure_category(permissions, category, timestamp)
            # Legacy approvals did not use the new explicit confirmation-event
            # model. Preserve the category record, but fail closed until the
            # owner confirms it through a new event.
            permission["enabled"] = False
            permission["disabled_at"] = timestamp
            permission["migration_note"] = "legacy_user_memory_permission_disabled"
        for field in LEGACY_PERMISSION_FIELDS:
            if field in playbook:
                playbook.pop(field, None)
                changed = True
    if not changed:
        return False
    memory["schema_version"] = max(int(memory.get("schema_version", 1)), 5)
    memory["updated_at"] = timestamp
    replacement = (
        f"{begin}\n```json\n{json.dumps(memory, ensure_ascii=False, indent=2)}\n```\n{end}"
    )
    temporary = memory_path.with_suffix(".tmp")
    temporary.write_text(
        text.split(begin, 1)[0] + replacement + text.split(end, 1)[1],
        encoding="utf-8",
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, memory_path)
    permissions["updated_at"] = timestamp
    atomic_json(permissions_path(), permissions)
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage independent owner-controlled per-category automatic-reply permissions"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser(
        "record-sent",
        help="Record a known sent AI Draft and create a pending owner-confirmation event",
    )
    record_parser.add_argument("--source", choices=["gmail-sent", "openclaw-sent"], required=True)
    record_parser.add_argument("--draft-id", required=True)
    record_parser.add_argument("--thread-id", required=True)
    record_parser.add_argument("--sent-message-id", required=True)
    record_parser.add_argument("--input", required=True)
    record_parser.add_argument("--delete-input", action="store_true")
    record_parser.set_defaults(func=record_sent)

    confirm_parser = subparsers.add_parser(
        "confirm",
        help="Resolve one pending category confirmation and set its automatic-reply switch",
    )
    confirm_parser.add_argument("--event-id", required=True)
    confirm_parser.add_argument("--intent-id", required=True)
    confirm_parser.add_argument("--scenario-key", required=True)
    confirm_parser.add_argument("value", choices=["on", "off"])
    confirm_parser.add_argument("--confirm-owner-request", action="store_true")
    confirm_parser.set_defaults(func=resolve_event)

    disable_parser = subparsers.add_parser(
        "disable", help="Turn off one existing category automatic-reply switch"
    )
    disable_parser.add_argument("--intent-id", required=True)
    disable_parser.add_argument("--scenario-key", required=True)
    disable_parser.add_argument("--confirm-owner-request", action="store_true")
    disable_parser.set_defaults(func=disable_category)

    disable_all_parser = subparsers.add_parser(
        "disable-all", help="Turn off all category automatic-reply switches without deleting categories"
    )
    disable_all_parser.add_argument("--confirm-owner-request", action="store_true")
    disable_all_parser.set_defaults(func=disable_all)

    check_parser = subparsers.add_parser(
        "check", help="Check whether every atomic issue has an enabled independent category permission"
    )
    check_parser.add_argument("--input", required=True)
    check_parser.add_argument("--delete-input", action="store_true")
    check_parser.set_defaults(func=check_auto_send)

    status_parser = subparsers.add_parser("status", help="Show non-sensitive permission-state summary")
    status_parser.set_defaults(func=status)

    purge_parser = subparsers.add_parser(
        "purge-events", help="Remove expired unresolved category-confirmation events"
    )
    purge_parser.set_defaults(func=purge_events)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
