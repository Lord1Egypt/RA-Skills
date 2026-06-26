from __future__ import annotations

import argparse
import json
from typing import Any

from .config import AppConfig, AppConfigError, ToolkitPaths, load_json
from .http import ApiError, FeishuHttpClient
from .members import MemberDirectory, sync_members


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="feishu_members")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync")
    subparsers.add_parser("stats")

    resolve_parser = subparsers.add_parser("resolve")
    resolve_parser.add_argument("--query", required=True)

    subparsers.add_parser("validate-aliases")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = ToolkitPaths.discover()
    try:
        if args.command == "sync":
            client = FeishuHttpClient(AppConfig.load(paths))
            _print(sync_members(client, paths))
            return 0
        if args.command == "stats":
            members = load_json(paths.members_file, {"member_count": 0, "members": []})
            meta = load_json(paths.sync_meta_file, {})
            _print({"member_count": members.get("member_count", 0), "sync_meta": meta})
            return 0
        directory = MemberDirectory.from_paths(paths)
        if args.command == "resolve":
            _print(directory.resolve(args.query))
            return 0
        if args.command == "validate-aliases":
            _print({"invalid_aliases": directory.validate_aliases()})
            return 0
    except (ApiError, AppConfigError, ValueError) as exc:
        payload = {"error": type(exc).__name__, "message": str(exc)}
        if isinstance(exc, ApiError):
            payload["code"] = exc.code
            payload["status"] = exc.status
            payload["payload"] = exc.payload
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1
    parser.error(f"unsupported command: {args.command}")
    return 2
