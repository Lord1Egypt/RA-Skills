#!/usr/bin/env python3
"""Manage owner-controlled long-term customer-service memory only."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


BEGIN = "<!-- ECS_MEMORY_JSON_BEGIN -->"
END = "<!-- ECS_MEMORY_JSON_END -->"
SAFE_REFERENCE = re.compile(r"[A-Za-z0-9._-]{1,200}")


def runtime_dir() -> Path:
    state_override = os.environ.get("OPENCLAW_STATE_DIR")
    state_root = Path(state_override).expanduser() if state_override else Path.home() / ".openclaw"
    return state_root / "ecommerce-gmail-customer-service"


def memory_path() -> Path:
    return runtime_dir() / "user_memory.md"


def config_path() -> Path:
    return runtime_dir() / "config.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_owner_confirmation(args: argparse.Namespace) -> None:
    if not getattr(args, "confirm_owner_request", False):
        raise SystemExit(
            "This changes owner-controlled user memory. Confirm the current owner's request and rerun with --confirm-owner-request"
        )


def read_config() -> dict:
    try:
        payload = json.loads(config_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read runtime configuration: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("Runtime configuration must be a JSON object")
    return payload


def require_draft_edit_learning_enabled() -> None:
    learning = read_config().get("learning", {})
    if learning.get("enabled") is not True or not learning.get("consent_granted_at"):
        raise SystemExit(
            "This operation requires explicitly enabled ongoing draft-edit learning with recorded consent"
        )


def require_merge_permission(args: argparse.Namespace) -> None:
    if args.source in {"onboarding", "sent-draft"}:
        require_owner_confirmation(args)
        return
    if args.source == "draft-edit":
        require_draft_edit_learning_enabled()
        return
    raise SystemExit(f"Unsupported memory update source: {args.source}")


def load_memory() -> tuple[str, dict]:
    try:
        text = memory_path().read_text(encoding="utf-8")
        body = text.split(BEGIN, 1)[1].split(END, 1)[0].strip()
        body = body.removeprefix("```json").removesuffix("```").strip()
        data = json.loads(body)
    except (OSError, IndexError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read user memory: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Managed user memory must contain a JSON object")
    return text, data


def write_memory(text: str, data: dict) -> None:
    replacement = (
        f"{BEGIN}\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```\n{END}"
    )
    target = memory_path()
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(
        text.split(BEGIN, 1)[0] + replacement + text.split(END, 1)[1],
        encoding="utf-8",
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, target)


def load_input(args: argparse.Namespace, label: str) -> dict:
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
    if not isinstance(payload, dict):
        raise SystemExit(f"{label} must be a JSON object")
    return payload


def unique(values: list) -> list:
    return list(dict.fromkeys(value for value in values if value))


def playbook_key(item: dict) -> str:
    intent_id = item.get("intent_id", "")
    scenario_key = item.get("scenario_key", "")
    if not (
        isinstance(intent_id, str)
        and isinstance(scenario_key, str)
        and SAFE_REFERENCE.fullmatch(intent_id)
        and SAFE_REFERENCE.fullmatch(scenario_key)
    ):
        raise SystemExit("playbook requires safe intent_id and scenario_key values")
    return f"{intent_id}::{scenario_key}"


LEGACY_PERMISSION_FIELDS = {
    "auto_send_approved",
    "auto_send_approved_at",
    "auto_send_confirmation",
    "sent_draft_confirmation",
}


def reject_permission_fields(item: dict) -> None:
    fields = sorted(LEGACY_PERMISSION_FIELDS.intersection(item))
    if fields:
        raise SystemExit(
            "Automatic-reply permissions are stored separately in auto_reply_permissions.json; do not write "
            + ", ".join(fields)
            + " to user_memory.md"
        )


def strip_legacy_permission_fields(item: dict) -> bool:
    changed = False
    for field in LEGACY_PERMISSION_FIELDS:
        if field in item:
            item.pop(field, None)
            changed = True
    return changed


def merge(args: argparse.Namespace) -> None:
    require_merge_permission(args)
    text, data = load_memory()
    update = load_input(args, "memory update")
    raw_playbooks = update.get("handling_playbooks", [])
    if not isinstance(raw_playbooks, list):
        raise SystemExit("handling_playbooks must be a list")

    profile = update.get("style_profile", {})
    if not isinstance(profile, dict):
        raise SystemExit("style_profile must be an object")
    target = data.setdefault("style_profile", {"status": "not_reviewed", "items": []})
    if not isinstance(target, dict) or not isinstance(target.get("items"), list):
        raise SystemExit("Existing style_profile must contain an items list")
    if profile.get("status"):
        target["status"] = profile["status"]
    for item in profile.get("items", []):
        if not isinstance(item, dict) or not item.get("key"):
            raise SystemExit("style item requires key")
        existing = next(
            (value for value in target["items"] if value.get("key") == item["key"]),
            None,
        )
        if existing:
            existing.update(
                {key: value for key, value in item.items() if value is not None}
            )
        else:
            target["items"].append(item)

    plans = data.setdefault("handling_playbooks", [])
    if not isinstance(plans, list):
        raise SystemExit("handling_playbooks must be a list")
    for existing in plans:
        if isinstance(existing, dict):
            strip_legacy_permission_fields(existing)
    for raw_item in raw_playbooks:
        if not isinstance(raw_item, dict):
            raise SystemExit("handling_playbook entries must be objects")
        reject_permission_fields(raw_item)
        item = dict(raw_item)
        key = playbook_key(item)
        existing = next(
            (
                value
                for value in plans
                if isinstance(value, dict) and playbook_key(value) == key
            ),
            None,
        )
        if existing:
            for field in (
                "handling_steps",
                "preferred_phrasing",
                "avoid_phrasing",
                "constraints",
                "observation_ids",
            ):
                existing[field] = unique(existing.get(field, []) + item.get(field, []))
            existing.update(
                {
                    field: value
                    for field, value in item.items()
                    if field
                    not in {
                        "handling_steps",
                        "preferred_phrasing",
                        "avoid_phrasing",
                        "constraints",
                        "observation_ids",
                    }
                    and value is not None
                }
            )
        else:
            plans.append(item)

    if "history_learning" in update:
        history_learning = update["history_learning"]
        if not isinstance(history_learning, dict):
            raise SystemExit("history_learning must be an object")
        data.setdefault("history_learning", {}).update(history_learning)
    data["schema_version"] = max(int(data.get("schema_version", 1)), 5)
    data["updated_at"] = now()
    write_memory(text, data)
    print(json.dumps({"updated": True, "source": args.source, "playbooks": len(plans)}))


def empty_memory() -> dict:
    learning = read_config().get("learning", {})
    window_days = learning.get("history_window_days", 30)
    if not isinstance(window_days, int) or window_days < 1:
        window_days = 30
    return {
        "schema_version": 5,
        "history_learning": {
            "status": "cleared",
            "window_days": window_days,
            "approved_at": None,
            "last_scan_at": None,
            "source_threads": 0,
        },
        "style_profile": {"status": "not_reviewed", "items": []},
        "handling_playbooks": [],
        "updated_at": now(),
    }


def clear_all(args: argparse.Namespace) -> None:
    require_owner_confirmation(args)
    if not args.confirm_delete_all:
        raise SystemExit(
            "Clearing all long-term memory is irreversible. Rerun with --confirm-delete-all"
        )
    text, _ = load_memory()
    write_memory(text, empty_memory())
    print(
        json.dumps(
            {
                "cleared": True,
                "message": "All long-term user memory was reset. Independent category automatic-reply permissions were not changed.",
            }
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage owner-controlled long-term customer-service memory"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("--input", required=True)
    merge_parser.add_argument(
        "--source", choices=["onboarding", "sent-draft", "draft-edit"], required=True
    )
    merge_parser.add_argument("--confirm-owner-request", action="store_true")
    merge_parser.add_argument(
        "--delete-input",
        action="store_true",
        help="Remove the controlled temporary update file after it is consumed",
    )
    merge_parser.set_defaults(func=merge)

    clear_parser = subparsers.add_parser(
        "clear", help="Clear all long-term memory without changing category automatic-reply permissions"
    )
    clear_parser.add_argument("--confirm-owner-request", action="store_true")
    clear_parser.add_argument("--confirm-delete-all", action="store_true")
    clear_parser.set_defaults(func=clear_all)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
