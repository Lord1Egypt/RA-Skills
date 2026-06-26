from __future__ import annotations

import argparse
import json
from typing import Any

from .config import AppConfig, AppConfigError, ToolkitPaths
from .http import ApiError, FeishuHttpClient
from .members import MemberDirectory
from .tasks import TaskService, add_default_member_to_created_task, parse_due_input, parse_member_args


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _resolve_members(directory: MemberDirectory, names: list[str]) -> list[str]:
    open_ids: list[str] = []
    for name in names:
        result = directory.resolve(name)
        if result["status"] != "matched":
            raise ValueError(json.dumps(result, ensure_ascii=False))
        open_ids.append(result["member"]["open_id"])
    return open_ids


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="feishu_task")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--task-guid", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--page-size", type=int, default=20)
    list_parser.add_argument("--page-token")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--summary", required=True)
    create_parser.add_argument("--description")
    create_parser.add_argument("--start-date")
    create_parser.add_argument("--start-at")
    create_parser.add_argument("--due-date")
    create_parser.add_argument("--due-at")
    create_parser.add_argument("--origin-title")
    create_parser.add_argument("--origin-url")
    create_parser.add_argument("--raw-body")

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--task-guid", required=True)
    update_parser.add_argument("--summary")
    update_parser.add_argument("--description")
    update_parser.add_argument("--start-date")
    update_parser.add_argument("--start-at")
    update_parser.add_argument("--due-date")
    update_parser.add_argument("--due-at")
    update_parser.add_argument("--clear-due", action="store_true")
    update_parser.add_argument("--clear-start", action="store_true")
    update_parser.add_argument("--raw-body")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--task-guid", required=True)
    delete_parser.add_argument("--yes", action="store_true")

    for name in ("complete", "reopen"):
        action_parser = subparsers.add_parser(name)
        action_parser.add_argument("--task-guid", required=True)

    for name in ("add-members", "remove-members"):
        action_parser = subparsers.add_parser(name)
        action_parser.add_argument("--task-guid", required=True)
        action_parser.add_argument("--member", action="append", required=True)
        action_parser.add_argument("--raw-body")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = ToolkitPaths.discover()
    try:
        service = TaskService(FeishuHttpClient(AppConfig.load(paths)))
        if args.command == "get":
            _print(service.get_task(args.task_guid))
            return 0
        if args.command == "list":
            _print(service.list_tasks(page_size=args.page_size, page_token=args.page_token))
            return 0
        if args.command == "create":
            start = parse_due_input(args.start_date, args.start_at, clear=False, timezone_name=service.client.config.timezone)
            due = parse_due_input(args.due_date, args.due_at, clear=False, timezone_name=service.client.config.timezone)
            created = service.create_task(
                summary=args.summary,
                description=args.description,
                start=start,
                due=due,
                origin_title=args.origin_title,
                origin_url=args.origin_url,
                raw_body=args.raw_body,
            )
            if service.client.config.default_member_open_id:
                created = add_default_member_to_created_task(service, created, service.client.config.default_member_open_id)
            _print(created)
            return 0
        if args.command == "update":
            start = parse_due_input(args.start_date, args.start_at, clear=args.clear_start, timezone_name=service.client.config.timezone)
            due = parse_due_input(args.due_date, args.due_at, clear=args.clear_due, timezone_name=service.client.config.timezone)
            clear_fields: list[str] = []
            if args.clear_start:
                clear_fields.append("start")
            if args.clear_due:
                clear_fields.append("due")
            _print(
                service.update_task(
                    task_guid=args.task_guid,
                    summary=args.summary,
                    description=args.description,
                    start=start,
                    due=due,
                    clear_fields=clear_fields,
                    raw_body=args.raw_body,
                )
            )
            return 0
        if args.command == "delete":
            if not args.yes:
                raise ValueError("delete requires --yes")
            _print(service.delete_task(args.task_guid))
            return 0
        if args.command == "complete":
            _print(service.complete_task(args.task_guid))
            return 0
        if args.command == "reopen":
            _print(service.reopen_task(args.task_guid))
            return 0
        directory = MemberDirectory.from_paths(paths)
        open_ids = _resolve_members(directory, parse_member_args(args.member))
        if args.command == "add-members":
            _print(service.add_members(args.task_guid, open_ids, raw_body=args.raw_body))
            return 0
        if args.command == "remove-members":
            _print(service.remove_members(args.task_guid, open_ids, raw_body=args.raw_body))
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
