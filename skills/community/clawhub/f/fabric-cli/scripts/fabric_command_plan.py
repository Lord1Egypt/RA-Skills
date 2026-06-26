#!/usr/bin/env python3
"""Build a shell-quoted Fabric CLI command plan without executing it."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

READ_ACTIONS = {"search", "path", "workspace-current", "workspace-list", "task-list", "inbox", "bin", "subscription", "ask-read"}
WRITE_ACTIONS = {"note", "link", "file", "save", "folder", "task-add", "task-done", "task-edit", "workspace-select", "ask-write"}
DESTRUCTIVE_ACTIONS = {"task-rm"}


def q(value: str) -> str:
    return shlex.quote(value)


def add_tags(parts: list[str], tags: list[str] | None) -> None:
    for tag in tags or []:
        parts.extend(["--tag", q(tag)])


def add_optional(parts: list[str], flag: str, value: str | None) -> None:
    if value:
        parts.extend([flag, q(value)])


def risk_for(action: str) -> str:
    if action in READ_ACTIONS:
        return "read"
    if action in DESTRUCTIVE_ACTIONS:
        return "destructive"
    return "write"


def command_plan(args: argparse.Namespace) -> dict[str, Any]:
    action = args.action
    parts: list[str]
    verification: list[str] = []
    notes: list[str] = []

    if action == "search":
        if not args.query:
            raise ValueError("--query is required for search")
        parts = ["fabric"]
        if args.prefer_json:
            parts.append("--json")
        parts.extend(["search", q(args.query)])
        add_tags(parts, args.tag)
        verification.append("Review returned results and summarise only relevant matches.")
    elif action == "path":
        parts = ["fabric", "path"]
        if args.query:
            parts.append(q(args.query))
        verification.append("Confirm the expected space or folder appears in the output.")
    elif action == "note":
        if args.content_file:
            parts = ["cat", q(args.content_file), "|", "fabric", "note"]
            notes.append("Inspect and redact the local file before executing.")
        elif args.text:
            parts = ["printf", "%s\\n", q(args.text), "|", "fabric", "note"]
        else:
            raise ValueError("Use --text or --content-file for note")
        add_optional(parts, "--parent", args.parent)
        add_tags(parts, args.tag)
        verification.append("Search the exact first heading or browse the parent path to confirm creation if CLI output is not enough.")
    elif action == "link":
        if not args.url:
            raise ValueError("--url is required for link")
        parts = ["fabric", "link", q(args.url)]
        add_optional(parts, "--title", args.title)
        add_optional(parts, "--parent", args.parent)
        add_tags(parts, args.tag)
        verification.append("Search exact URL or title if the CLI output lacks an identifier.")
    elif action == "file":
        if not args.path:
            raise ValueError("--path is required for file")
        parts = ["fabric", "file", q(args.path)]
        add_optional(parts, "--title", args.title)
        add_optional(parts, "--parent", args.parent)
        add_tags(parts, args.tag)
        verification.extend(["Before executing, verify the local file exists and is readable.", "Browse the parent path or search the exact title after upload."])
    elif action == "save":
        if args.content_file:
            parts = ["cat", q(args.content_file), "|", "fabric", "save"]
        elif args.text:
            parts = ["fabric", "save", q(args.text)]
        elif args.url:
            parts = ["fabric", "save", q(args.url)]
        elif args.path:
            parts = ["fabric", "save", q(args.path)]
        else:
            raise ValueError("Use --text, --url, --path, or --content-file for save")
        add_optional(parts, "--title", args.title)
        add_optional(parts, "--parent", args.parent)
        add_tags(parts, args.tag)
        verification.append("Verify inferred type and created item from CLI output or follow-up search.")
    elif action == "folder":
        if not args.title:
            raise ValueError("--title is required for folder name")
        parts = ["fabric", "folder", q(args.title)]
        add_optional(parts, "--parent", args.parent)
        add_tags(parts, args.tag)
        verification.append("Use `fabric path` to confirm the folder exists.")
    elif action == "task-list":
        parts = ["fabric", "task", "list"]
        if args.done:
            parts.append("--done")
        elif args.todo:
            parts.append("--todo")
        verification.append("Use returned task IDs for later task operations.")
    elif action == "task-add":
        if not args.title:
            raise ValueError("--title is required for task-add")
        parts = ["fabric", "task", "add", q(args.title)]
        add_optional(parts, "--due-date", args.due_date)
        add_optional(parts, "--priority", args.priority)
        verification.append("List tasks to confirm the new task if CLI output is ambiguous.")
    elif action in {"task-done", "task-edit", "task-rm"}:
        if not args.task_id:
            raise ValueError(f"--task-id is required for {action}")
        sub = action.split("-")[1]
        parts = ["fabric", "task", sub, q(args.task_id)]
        if action == "task-edit":
            add_optional(parts, "--title", args.title)
        verification.append("Run `fabric task list` before this command to verify task ID and after it to verify result.")
    elif action == "workspace-current":
        parts = ["fabric", "workspace", "current"]
        verification.append("Use this workspace name in the final response.")
    elif action == "workspace-list":
        parts = ["fabric", "workspace", "list"]
        verification.append("Use exact workspace name for selection.")
    elif action == "workspace-select":
        if not args.workspace:
            raise ValueError("--workspace is required for workspace-select")
        parts = ["fabric", "workspace", "select", q(args.workspace)]
        verification.append("Run `fabric workspace current` after selection and report active workspace.")
    elif action in {"ask-read", "ask-write"}:
        if not args.query:
            raise ValueError("--query is required for ask")
        parts = ["fabric", "ask", q(args.query)]
        verification.append("For write-like ask requests, verify the action with search, path, or task list before reporting success.")
    elif action in {"inbox", "bin", "subscription"}:
        parts = ["fabric", action]
        verification.append("Summarise relevant output; do not dump large raw lists.")
    else:
        raise ValueError(f"Unsupported action: {action}")

    risk = risk_for(action)
    return {"action": action, "risk": risk, "requires_confirmation": risk == "destructive" or action == "workspace-select", "commands": [" ".join(parts)], "verification": verification, "notes": notes}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a shell-quoted Fabric CLI command plan without executing it.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--action", required=True, choices=sorted(READ_ACTIONS | WRITE_ACTIONS | DESTRUCTIVE_ACTIONS), help="Intent/action to plan.")
    parser.add_argument("--query", help="Search query, path query, or ask question depending on action.")
    parser.add_argument("--text", help="Short note/save text. Prefer --content-file for long content.")
    parser.add_argument("--content-file", help="Local UTF-8 file to pipe into note/save.")
    parser.add_argument("--url", help="URL for link/save.")
    parser.add_argument("--path", help="Local file path for file/save.")
    parser.add_argument("--title", help="Title, folder name, task title, or file/link title depending on action.")
    parser.add_argument("--parent", help="Fabric parent path.")
    parser.add_argument("--tag", action="append", help="Tag to add. May be repeated.")
    parser.add_argument("--task-id", help="Task ID for task-done/edit/rm.")
    parser.add_argument("--due-date", help="Task due date, ideally YYYY-MM-DD.")
    parser.add_argument("--priority", help="Task priority such as HIGH if supported by installed CLI.")
    parser.add_argument("--workspace", help="Workspace name for workspace-select.")
    parser.add_argument("--todo", action="store_true", help="For task-list, list pending tasks.")
    parser.add_argument("--done", action="store_true", help="For task-list, list completed tasks.")
    parser.add_argument("--prefer-json", action="store_true", help="For search, include global --json in the planned command.")
    parser.add_argument("--shell-only", action="store_true", help="Print only the planned shell command instead of JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    if args.content_file and not Path(args.content_file).exists():
        print(f"Error: --content-file does not exist: {args.content_file}", file=sys.stderr)
        return 2
    try:
        plan = command_plan(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(plan["commands"][0] if args.shell_only else json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
