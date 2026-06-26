#!/usr/bin/env python3
"""Upsert OpenClaw channel/binding/session config into openclaw.json."""

import argparse
import copy
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VALID_DM_SCOPE = {
    "main",
    "per-peer",
    "per-channel-peer",
    "per-account-channel-peer",
}

DEFAULT_DM_SCOPE = "per-account-channel-peer"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upsert OpenClaw channels/bindings/session config."
    )
    parser.add_argument("--config", default="~/.openclaw/openclaw.json")
    parser.add_argument("--agent-id", required=True)
    parser.add_argument(
        "--channel",
        default="feishu",
        choices=["feishu"],
        help="Supported channel for this skill: feishu",
    )
    parser.add_argument("--routing-mode", choices=["account", "peer"], required=True)

    parser.add_argument("--account-id")
    parser.add_argument("--app-id")
    parser.add_argument("--app-secret")
    parser.add_argument("--bot-name")

    parser.add_argument("--peer-kind", choices=["group", "direct"])
    parser.add_argument("--peer-id")

    parser.add_argument("--ensure-dm-scope", choices=sorted(VALID_DM_SCOPE))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    return parser.parse_args()


def fail(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def validate_args(args: argparse.Namespace) -> None:
    if not re.fullmatch(r"[a-z0-9-]+", args.agent_id):
        fail("--agent-id must match [a-z0-9-]+")

    if args.routing_mode == "account":
        if not args.account_id:
            fail("--account-id is required when --routing-mode=account")
    if args.routing_mode == "peer":
        if not args.peer_kind:
            fail("--peer-kind is required when --routing-mode=peer")
        if not args.peer_id:
            fail("--peer-id is required when --routing-mode=peer")


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        fail(f"config file not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as f:
            content = json.load(f)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in config: {exc}")
    if not isinstance(content, dict):
        fail("config root must be a JSON object")
    return content


def route_signature(match: Dict[str, Any]) -> Tuple[str, Optional[str], Optional[str], Optional[str]]:
    peer = match.get("peer")
    peer_kind = None
    peer_id = None
    if isinstance(peer, dict):
        peer_kind = peer.get("kind")
        peer_id = peer.get("id")
    return (
        str(match.get("channel", "")),
        match.get("accountId"),
        peer_kind,
        peer_id,
    )


def build_binding_match(args: argparse.Namespace) -> Dict[str, Any]:
    match: Dict[str, Any] = {"channel": args.channel}
    if args.routing_mode == "account":
        match["accountId"] = args.account_id
    else:
        match["peer"] = {"kind": args.peer_kind, "id": args.peer_id}
        if args.account_id:
            match["accountId"] = args.account_id
    return match


def ensure_route_not_conflicting(
    bindings: List[Dict[str, Any]],
    agent_id: str,
    target_match: Dict[str, Any],
) -> None:
    target_sig = route_signature(target_match)
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        if route_signature(binding.get("match", {})) != target_sig:
            continue
        existing_agent = binding.get("agentId")
        if existing_agent and existing_agent != agent_id:
            fail(
                "route conflict: same route already bound to another agent "
                f"({existing_agent})"
            )


def backup_file(path: Path) -> Path:
    suffix = time.strftime("%Y%m%d%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak.{suffix}")
    shutil.copy2(path, backup_path)
    return backup_path


def upsert_account(config: Dict[str, Any], args: argparse.Namespace, summary: Dict[str, Any]) -> None:
    if args.routing_mode != "account":
        summary["channelAccount"] = {
            "status": "skipped",
            "reason": "routing-mode is not account",
        }
        return

    channels = config.setdefault("channels", {})
    if not isinstance(channels, dict):
        fail("config.channels must be an object")

    channel_obj = channels.setdefault(args.channel, {})
    if not isinstance(channel_obj, dict):
        fail(f"config.channels.{args.channel} must be an object")

    accounts = channel_obj.setdefault("accounts", {})
    if not isinstance(accounts, dict):
        fail(f"config.channels.{args.channel}.accounts must be an object")

    existing = accounts.get(args.account_id)
    if existing is None:
        existing = {}
        accounts[args.account_id] = existing
        status = "created"
    elif not isinstance(existing, dict):
        fail(
            f"config.channels.{args.channel}.accounts.{args.account_id} must be an object"
        )
    else:
        status = "updated"

    before = copy.deepcopy(existing)
    if args.app_id:
        existing["appId"] = args.app_id
    if args.app_secret:
        existing["appSecret"] = args.app_secret
    if args.bot_name:
        existing["botName"] = args.bot_name

    summary["channelAccount"] = {
        "status": status,
        "accountId": args.account_id,
        "before": before,
        "after": copy.deepcopy(existing),
    }


def upsert_binding(config: Dict[str, Any], args: argparse.Namespace, summary: Dict[str, Any]) -> None:
    bindings = config.setdefault("bindings", [])
    if not isinstance(bindings, list):
        fail("config.bindings must be an array")

    target_match = build_binding_match(args)
    ensure_route_not_conflicting(bindings, args.agent_id, target_match)
    target_sig = route_signature(target_match)

    desired = {"agentId": args.agent_id, "match": target_match}

    for idx, item in enumerate(bindings):
        if not isinstance(item, dict):
            continue
        match = item.get("match")
        if not isinstance(match, dict):
            continue
        if item.get("agentId") == args.agent_id and route_signature(match) == target_sig:
            before = copy.deepcopy(item)
            bindings[idx] = desired
            summary["binding"] = {
                "status": "updated",
                "before": before,
                "after": copy.deepcopy(desired),
            }
            return

    bindings.append(desired)
    summary["binding"] = {"status": "created", "after": desired}


def upsert_dm_scope(config: Dict[str, Any], args: argparse.Namespace, summary: Dict[str, Any]) -> None:
    target = args.ensure_dm_scope or DEFAULT_DM_SCOPE
    if target != DEFAULT_DM_SCOPE:
        fail(
            "for multi-agent Feishu setup, dmScope must be per-account-channel-peer"
        )
    session = config.setdefault("session", {})
    if not isinstance(session, dict):
        fail("config.session must be an object")

    current = session.get("dmScope")
    if current != target:
        session["dmScope"] = target
        status = "set" if current is None else "updated"
        summary["dmScope"] = {"status": status, "from": current, "to": target}
        return

    summary["dmScope"] = {"status": "unchanged", "value": current}


def write_config(path: Path, content: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    args = parse_args()
    validate_args(args)

    config_path = Path(os.path.expanduser(args.config))
    config = copy.deepcopy(load_config(config_path))

    summary: Dict[str, Any] = {"configPath": str(config_path)}
    upsert_account(config, args, summary)
    upsert_binding(config, args, summary)
    upsert_dm_scope(config, args, summary)

    if not args.no_backup and not args.dry_run:
        backup_path = backup_file(config_path)
        summary["backupPath"] = str(backup_path)

    if not args.dry_run:
        write_config(config_path, config)
        summary["write"] = "applied"
    else:
        summary["write"] = "dry-run"

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
