#!/usr/bin/env python3
"""Resolve Feishu task creator/member payload from minimal intent slots.

This script is the single source of truth for creator/member normalization in
the feishu-task-agent skill. It reads JSON from stdin by default and writes a
single JSON object to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional


CREATE_AS_VALUES = {"unspecified", "app", "user"}


class ResolveError(Exception):
    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message


def _normalize_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ResolveError("invalid_string_field", "string field must be a string")
    value = value.strip()
    return value or None


def _normalize_string_list(value: Any, field_name: str) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ResolveError("invalid_follower_list", f"{field_name} must be an array of strings")

    normalized: List[str] = []
    for item in value:
        item_value = _normalize_string(item)
        if item_value is None:
            continue
        normalized.append(item_value)
    return normalized


def _ensure_user_id(value: str, field_name: str) -> None:
    if value.startswith("cli_"):
        raise ResolveError("invalid_user_member_id", f"{field_name} must be a user id, not an app id")


def _validate_output(output: Dict[str, Any], app_id: Optional[str]) -> None:
    members = output.get("members")
    if not isinstance(members, list) or not members:
        raise ResolveError("invalid_members", "members must be a non-empty array")

    assignee_count = 0
    seen_role_pairs = set()
    for member in members:
        if not isinstance(member, dict):
            raise ResolveError("invalid_member_shape", "each member must be an object")

        member_id = _normalize_string(member.get("id"))
        role = _normalize_string(member.get("role"))
        member_type = _normalize_string(member.get("type"))
        if not member_id or not role or not member_type:
            raise ResolveError("missing_member_field", "each member must include id, role, and type")

        role_pair = (member_id, role)
        if role_pair in seen_role_pairs:
            raise ResolveError("duplicate_member_role", "same member cannot repeat the same role")
        seen_role_pairs.add(role_pair)

        if role == "assignee":
            assignee_count += 1
        elif role != "follower":
            raise ResolveError("invalid_member_role", "role must be assignee or follower")

        if member_type == "app":
            if not app_id or member_id != app_id:
                raise ResolveError("invalid_app_member_id", "type=app can only be used with the configured app_id")
        elif member_type == "user":
            _ensure_user_id(member_id, "member.id")
        else:
            raise ResolveError("invalid_member_type", "type must be app or user")

    if assignee_count != 1:
        raise ResolveError("invalid_assignee_count", "members must contain exactly one assignee")


def _resolve_config_path(args: argparse.Namespace) -> Optional[Path]:
    explicit = args.config_path or os.getenv("OPENCLAW_CONFIG_PATH")
    if explicit:
        return Path(explicit).expanduser()

    default_path = Path.home() / ".openclaw" / "openclaw.json"
    if default_path.exists():
        return default_path
    return None


def _load_openclaw_config(args: argparse.Namespace) -> Dict[str, Any]:
    config_path = _resolve_config_path(args)
    if config_path is None or not config_path.exists():
        raise ResolveError("missing_openclaw_config", "cannot resolve OpenClaw config file for app_id lookup")

    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError as exc:
        raise ResolveError("invalid_openclaw_config", f"OpenClaw config is not valid JSON: {exc.msg}") from exc


def _resolve_app_id_from_config(args: argparse.Namespace) -> Optional[str]:
    config = _load_openclaw_config(args)
    feishu = ((config.get("channels") or {}).get("feishu") or {})

    legacy_app_id = _normalize_string(feishu.get("appId"))
    if legacy_app_id:
        return legacy_app_id

    accounts = feishu.get("accounts")
    if not isinstance(accounts, dict) or not accounts:
        return None

    account_id = args.account_id or os.getenv("OPENCLAW_FEISHU_ACCOUNT_ID") or _normalize_string(feishu.get("defaultAccount"))
    if account_id:
        account = accounts.get(account_id)
        if not isinstance(account, dict):
            raise ResolveError("invalid_feishu_account", f'Feishu account "{account_id}" not found in OpenClaw config')
        return _normalize_string(account.get("appId"))

    if len(accounts) == 1:
        only_account = next(iter(accounts.values()))
        if isinstance(only_account, dict):
            return _normalize_string(only_account.get("appId"))
    return None


def resolve_creator_members(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ResolveError("invalid_input", "input must be a JSON object")

    create_as_raw = _normalize_string(payload.get("create_as")) or "unspecified"
    if create_as_raw not in CREATE_AS_VALUES:
        raise ResolveError("invalid_create_as", 'create_as must be one of "unspecified", "app", or "user"')

    sender_open_id = _normalize_string(payload.get("sender_open_id"))
    if sender_open_id is None:
        raise ResolveError("missing_sender_open_id", "sender_open_id is required")
    _ensure_user_id(sender_open_id, "sender_open_id")

    app_id = _normalize_string(payload.get("app_id"))
    explicit_assignee_open_id = _normalize_string(payload.get("explicit_assignee_open_id"))
    explicit_follower_open_ids = _normalize_string_list(
        payload.get("explicit_follower_open_ids"), "explicit_follower_open_ids"
    )

    if explicit_assignee_open_id is not None:
        if app_id and explicit_assignee_open_id == app_id:
            raise ResolveError("invalid_explicit_assignee", "explicit assignee must be a user, not app_id")
        _ensure_user_id(explicit_assignee_open_id, "explicit_assignee_open_id")

    for follower_id in explicit_follower_open_ids:
        _ensure_user_id(follower_id, "explicit_follower_open_ids")

    resolved_create_as = "app" if create_as_raw == "unspecified" else create_as_raw
    if resolved_create_as == "app" and app_id is None:
        raise ResolveError("missing_app_id", "app_id is required when create_as resolves to app")

    assignee_id: str
    assignee_type: str
    if explicit_assignee_open_id is not None:
        assignee_id = explicit_assignee_open_id
        assignee_type = "user"
    elif resolved_create_as == "app":
        assignee_id = app_id or ""
        assignee_type = "app"
    else:
        assignee_id = sender_open_id
        assignee_type = "user"

    members: List[Dict[str, str]] = [
        {"id": assignee_id, "role": "assignee", "type": assignee_type},
    ]

    follower_candidates = explicit_follower_open_ids if explicit_follower_open_ids else [sender_open_id]
    seen_followers = set()
    for follower_id in follower_candidates:
        if follower_id == assignee_id:
            continue
        if follower_id in seen_followers:
            continue
        seen_followers.add(follower_id)
        members.append({"id": follower_id, "role": "follower", "type": "user"})

    output = {
        "ok": True,
        "create_as": resolved_create_as,
        "auth_type": "tenant" if resolved_create_as == "app" else "user",
        "current_user_id": sender_open_id,
        "members": members,
    }
    _validate_output(output, app_id)
    return output


def _merge_runtime_context(payload: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    merged = dict(payload)
    sender_open_id = args.sender_open_id or payload.get("sender_open_id") or os.getenv("OPENCLAW_SENDER_OPEN_ID")
    app_id = args.app_id or payload.get("app_id") or os.getenv("OPENCLAW_APP_ID")
    if app_id is None:
        app_id = _resolve_app_id_from_config(args)
    if sender_open_id is not None:
        merged["sender_open_id"] = sender_open_id
    if app_id is not None:
        merged["app_id"] = app_id
    return merged


def _load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    raw = args.input_json
    if raw is None:
        raw = sys.stdin.read()
    raw = (raw or "").strip()
    if not raw:
        raise ResolveError("empty_input", "input JSON is required via stdin or --input-json")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ResolveError("invalid_json", f"input is not valid JSON: {exc.msg}") from exc


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve Feishu task creator/member payload")
    parser.add_argument("--input-json", help="Input JSON object. If omitted, reads from stdin.")
    parser.add_argument("--sender-open-id", help="Runtime sender open_id from message context.")
    parser.add_argument("--app-id", help="Runtime app id for app members, e.g. cli_xxx. Overrides config lookup.")
    parser.add_argument("--account-id", help="Feishu account id in OpenClaw config, e.g. main. Defaults to feishu.defaultAccount.")
    parser.add_argument("--config-path", help="Path to OpenClaw config JSON. Defaults to OPENCLAW_CONFIG_PATH or ~/.openclaw/openclaw.json.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    try:
        payload = _merge_runtime_context(_load_payload(args), args)
        output = resolve_creator_members(payload)
    except ResolveError as exc:
        error = {"ok": False, "error_code": exc.error_code, "message": exc.message}
        json.dump(error, sys.stdout, ensure_ascii=True, indent=2 if args.pretty else None)
        sys.stdout.write("\n")
        return 1

    json.dump(output, sys.stdout, ensure_ascii=True, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
