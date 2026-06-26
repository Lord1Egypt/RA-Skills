#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

BLOCK_BEGIN = "<!-- agent-todo:begin -->"
BLOCK_END = "<!-- agent-todo:end -->"
DEFAULT_SUCCESS = "Mark done and report back to source"
DEFAULT_OPENCLAW = Path.home() / ".openclaw" / "openclaw.json"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_deadline(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    lower = text.lower()
    now = datetime.now().astimezone()
    if any(x in text for x in ["今天", "今晚"]):
        dt = now.replace(hour=23, minute=59, second=0, microsecond=0)
        return dt.isoformat(timespec="seconds")
    if any(x in text for x in ["明天", "明早"]):
        dt = (now + timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
        return dt.isoformat(timespec="seconds")
    if any(x in text for x in ["这周", "本周", "周末"]):
        days = (6 - now.weekday()) % 7
        dt = (now + timedelta(days=days)).replace(hour=23, minute=59, second=0, microsecond=0)
        return dt.isoformat(timespec="seconds")
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=now.tzinfo).isoformat(timespec="seconds")
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text).astimezone().isoformat(timespec="seconds")
    except ValueError:
        return text


def deadline_ts(text: str) -> float:
    if not text:
        return float("inf")
    try:
        return datetime.fromisoformat(text).timestamp()
    except ValueError:
        return float("inf")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


@dataclass
class Runtime:
    script_dir: Path
    workspace: Path
    data_dir: Path
    tasks_path: Path
    local_path: Path
    heartbeat_path: Path
    openclaw_path: Path
    openclaw: dict[str, Any]
    current_agent_id: str
    current_agent_label: str

    @classmethod
    def detect(cls, script_dir: Path) -> "Runtime":
        workspace_env = os.environ.get("AGENT_TODO_WORKSPACE")
        todo_db_env = os.environ.get("TODO_DB")
        if workspace_env:
            workspace = Path(workspace_env).expanduser().resolve()
        elif todo_db_env:
            workspace = Path(todo_db_env).expanduser().resolve().parent
        else:
            workspace = (script_dir / ".." / "..").resolve()

        openclaw_path = Path(os.environ.get("OPENCLAW_CONFIG", str(DEFAULT_OPENCLAW))).expanduser().resolve()
        openclaw = load_json(openclaw_path, {}) if openclaw_path.exists() else {}
        data_dir = workspace / ".agent-todo"
        tasks_path = data_dir / "tasks.json"
        local_path = data_dir / "local.json"
        heartbeat_path = workspace / "HEARTBEAT.md"

        local_cfg = load_json(local_path, {}) if local_path.exists() else {}
        agent_id = str(local_cfg.get("agent_id") or "").strip()
        label = str(local_cfg.get("label") or "").strip()

        for agent in openclaw.get("agents", {}).get("list", []):
            if Path(agent.get("workspace", "")).expanduser().resolve() == workspace:
                agent_id = agent_id or str(agent.get("id") or agent.get("name") or "local")
                identity = agent.get("identity", {}) or {}
                label = label or str(identity.get("name") or agent.get("name") or agent_id)
                break

        if not agent_id:
            agent_id = "local"
        if not label:
            label = agent_id

        return cls(
            script_dir=script_dir,
            workspace=workspace,
            data_dir=data_dir,
            tasks_path=tasks_path,
            local_path=local_path,
            heartbeat_path=heartbeat_path,
            openclaw_path=openclaw_path,
            openclaw=openclaw,
            current_agent_id=agent_id,
            current_agent_label=label,
        )

    def init_store(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.tasks_path.exists():
            write_json(self.tasks_path, {"version": 2, "tasks": []})

    def load_tasks(self) -> list[dict[str, Any]]:
        self.init_store()
        data = load_json(self.tasks_path, {"version": 2, "tasks": []})
        return list(data.get("tasks", []))

    def save_tasks(self, tasks: list[dict[str, Any]]) -> None:
        write_json(self.tasks_path, {"version": 2, "tasks": tasks})

    def heartbeat_command(self, workspace: Path | None = None) -> str:
        workspace = (workspace or self.workspace).resolve()
        script_path = (self.script_dir / "script.sh").resolve()
        try:
            rel = os.path.relpath(script_path, workspace)
            if not rel.startswith(".."):
                return f"AGENT_TODO_WORKSPACE={shlex.quote(str(workspace))} bash ./{rel} run-pending --claim"
        except ValueError:
            pass
        return (
            f"AGENT_TODO_WORKSPACE={shlex.quote(str(workspace))} "
            f"bash {shlex.quote(str(script_path))} run-pending --claim"
        )

    def discovered_workspaces(self) -> list[Path]:
        items: list[Path] = []
        defaults_workspace = self.openclaw.get("agents", {}).get("defaults", {}).get("workspace")
        if defaults_workspace:
            items.append(Path(defaults_workspace).expanduser().resolve())
        for agent in self.openclaw.get("agents", {}).get("list", []):
            workspace = agent.get("workspace")
            if workspace:
                items.append(Path(workspace).expanduser().resolve())
        items.append(self.workspace)

        result: list[Path] = []
        seen: set[str] = set()
        for item in items:
            key = str(item)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    def find_agent_workspace(self, agent_id: str) -> Path:
        matches: list[Path] = []
        for workspace in self.discovered_workspaces():
            local_path = workspace / ".agent-todo" / "local.json"
            if not local_path.exists():
                continue
            try:
                local_cfg = load_json(local_path, {})
            except Exception:
                continue
            if str(local_cfg.get("agent_id") or "").strip() == agent_id:
                matches.append(workspace)
        if not matches:
            raise SystemExit(
                f"ERROR: agent '{agent_id}' not found in discovered workspaces from {self.openclaw_path}."
            )
        if len(matches) > 1:
            joined = ", ".join(str(x) for x in matches)
            raise SystemExit(f"ERROR: multiple workspaces declare agent_id '{agent_id}': {joined}")
        return matches[0]


def ensure_heartbeat_block(path: Path, command: str, write: bool) -> tuple[str, bool]:
    block = "\n".join(
        [
            BLOCK_BEGIN,
            "### Agent Todo 队列",
            "检查当前 workspace 的 agent-todo 是否有可执行任务：",
            f"- 命令: `{command}`",
            "- 逻辑: 如果返回 `EXECUTE_NOW`，立即执行该任务；如果返回 `HEARTBEAT_OK`，继续处理其他 heartbeat 项。",
            "- 注意: 完成后调用 `done`，受阻则调用 `block`。",
            BLOCK_END,
        ]
    )
    if path.exists():
        content = path.read_text(encoding="utf-8")
    else:
        content = ""

    pattern = re.compile(re.escape(BLOCK_BEGIN) + r".*?" + re.escape(BLOCK_END), re.S)
    if pattern.search(content):
        new_content = pattern.sub(block, content, count=1)
    elif content.strip():
        suffix = "\n" if content.endswith("\n") else "\n\n"
        new_content = f"{content}{suffix}{block}\n"
    else:
        new_content = block + "\n"

    changed = new_content != content
    if write and changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new_content, encoding="utf-8")
    return new_content, changed


def format_status(status: str) -> str:
    return {
        "pending": "⏳ pending",
        "running": "🏃 running",
        "blocked": "🧱 blocked",
        "done": "✅ done",
        "cancelled": "❌ cancelled",
    }.get(status, status)


def task_by_id(tasks: list[dict[str, Any]], task_id: str) -> dict[str, Any]:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise SystemExit(f"未找到任务: {task_id}")


def render_report(task: dict[str, Any]) -> str:
    title = task["title"]
    source = task.get("source", "")
    completed_at = task.get("completed_at", "")
    result = task.get("result", "")
    success = task.get("success_criteria", "")

    forum = re.match(r"^forum:#(\d+)(/reply:(\d+))?$", source)
    if forum:
        topic_id = forum.group(1)
        lines = [
            "【回帖内容】",
            f"✅ 已完成：{title}",
            f" - 话题：#{topic_id}",
            f" - 完成时间：{completed_at}",
        ]
        if result:
            lines.append(f" - 结果：{result}")
        if success:
            lines.append(f" - 对照标准：{success}")
        lines.extend(["", "如无遗漏，我这边先收口。"])
        return "\n".join(lines)

    if source.startswith("chat:"):
        lines = ["【回消息内容】", f"✅ 已完成：{title}", f" - 完成时间：{completed_at}"]
        if result:
            lines.append(f" - 结果：{result}")
        if success:
            lines.append(f" - 对照标准：{success}")
        return "\n".join(lines)

    lines = ["【通用汇报】", f"✅ {title}", f" - completed_at: {completed_at}"]
    if source:
        lines.insert(2, f" - source: {source}")
    if result:
        lines.append(f" - result: {result}")
    if success:
        lines.append(f" - success_criteria: {success}")
    return "\n".join(lines)


def select_task(tasks: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [x for x in tasks if x["status"] not in {"done", "cancelled", "blocked"}]
    if not valid:
        return None

    done_ids = {x["id"] for x in tasks if x["status"] == "done"}
    candidates: list[dict[str, Any]] = []
    for task in valid:
        deps = [x for x in task.get("depends_on", []) if x]
        if any(dep not in done_ids for dep in deps):
            continue
        candidates.append(task)
    if not candidates:
        return None

    def sort_key(task: dict[str, Any]) -> tuple[Any, ...]:
        pref = 1 if task.get("parent_id") else 2
        if task["status"] == "running":
            return (pref, 0, task.get("last_attempt_at") or task.get("created_at") or "")
        return (pref, 1, deadline_ts(task.get("deadline", "")), task.get("created_at") or "")

    candidates.sort(key=sort_key)
    return candidates[0]


def new_task(runtime: Runtime, title: str, args: argparse.Namespace, owner_id: str | None = None) -> dict[str, Any]:
    ts = now_iso()
    owner_id = owner_id or runtime.current_agent_id
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "status": "pending",
        "task_type": args.task_type,
        "source": args.source or "",
        "next_action": args.next_action or title,
        "success_criteria": args.success_criteria or DEFAULT_SUCCESS,
        "result": "",
        "deadline": parse_deadline(args.deadline or ""),
        "owner_agent_id": owner_id,
        "created_by_agent_id": runtime.current_agent_id,
        "claimed_at": "",
        "last_attempt_at": "",
        "blocked_reason": "",
        "parent_id": args.parent_id or "",
        "depends_on": [x.strip() for x in (args.depends_on or "").split(",") if x.strip()],
        "created_at": ts,
        "updated_at": ts,
        "completed_at": "",
        "tags": [x.strip() for x in (args.tags or "").split(",") if x.strip()],
    }


def common_task_parser(parser: argparse.ArgumentParser, include_parent: bool = True) -> None:
    parser.add_argument("--task-type", default="general")
    parser.add_argument("--deadline", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--next-action", default="")
    parser.add_argument("--success-criteria", default=DEFAULT_SUCCESS)
    parser.add_argument("--tags", default="")
    if include_parent:
        parser.add_argument("--parent-id", default="")
        parser.add_argument("--depends-on", default="")


def cmd_init(runtime: Runtime, _args: argparse.Namespace) -> int:
    runtime.init_store()
    print(f"✅ agent-todo queue initialized: {runtime.tasks_path}")
    return 0


def cmd_doctor(runtime: Runtime, _args: argparse.Namespace) -> int:
    runtime.init_store()
    print("agent-todo doctor")
    print(f"- workspace: {runtime.workspace}")
    print(f"- tasks: {runtime.tasks_path}")
    print(f"- local config: {runtime.local_path}")
    print(f"- openclaw config: {runtime.openclaw_path}")
    print(f"- current agent: {runtime.current_agent_id} ({runtime.current_agent_label})")
    print(f"- discovered workspaces: {len(runtime.discovered_workspaces())}")
    command = runtime.heartbeat_command()
    _, changed = ensure_heartbeat_block(runtime.heartbeat_path, command, write=False)
    print(f"- heartbeat file: {runtime.heartbeat_path}")
    print(f"- heartbeat command: {command}")
    print(f"- heartbeat managed block: {'missing ⚠️' if changed else 'configured ✅'}")
    return 0


def cmd_setup_heartbeat(runtime: Runtime, args: argparse.Namespace) -> int:
    targets = runtime.discovered_workspaces() if args.all else [runtime.workspace]
    for workspace in targets:
        hb_path = workspace / "HEARTBEAT.md"
        command = runtime.heartbeat_command(workspace)
        _, changed = ensure_heartbeat_block(hb_path, command, write=args.write)
        state = "updated" if changed else "ok"
        if args.dry_run and not args.write:
            action = "would update" if changed else "already configured"
        elif args.write:
            action = "updated" if changed else "already configured"
        else:
            action = "preview"
        print(f"- {workspace}: {action} ({state})")
    if not args.write:
        print("\nUse --write to persist the managed heartbeat block.")
    return 0


def cmd_add(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    task = new_task(runtime, args.title, args)
    tasks.append(task)
    runtime.save_tasks(tasks)
    print(f"✅ task queued [{task['id']}]")
    print(f"   title: {task['title']}")
    print(f"   type: {task['task_type']}")
    print(f"   owner_agent_id: {task['owner_agent_id']}")
    if task["deadline"]:
        print(f"   deadline: {task['deadline']}")
    if task["next_action"]:
        print(f"   next_action: {task['next_action']}")
    return 0


def cmd_dispatch(runtime: Runtime, args: argparse.Namespace) -> int:
    target_workspace = runtime.find_agent_workspace(args.to_agent)
    target_runtime = Runtime.detect(runtime.script_dir)
    target_runtime.workspace = target_workspace
    target_runtime.data_dir = target_workspace / ".agent-todo"
    target_runtime.tasks_path = target_runtime.data_dir / "tasks.json"
    target_runtime.local_path = target_runtime.data_dir / "local.json"
    target_runtime.heartbeat_path = target_workspace / "HEARTBEAT.md"
    tasks = target_runtime.load_tasks()
    task = new_task(runtime, args.title, args, owner_id=args.to_agent)
    tasks.append(task)
    target_runtime.save_tasks(tasks)
    print(f"✅ task dispatched [{task['id']}]")
    print(f"   to_agent: {args.to_agent}")
    print(f"   workspace: {target_workspace}")
    print(f"   title: {task['title']}")
    return 0


def cmd_plan(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    parent = new_task(runtime, args.title, args)
    parent["next_action"] = f"Break down and complete plan: {args.title}"
    parent["success_criteria"] = args.success_criteria or "All planned steps are completed and reported back"
    tasks.append(parent)

    prev = ""
    steps = [x.strip() for x in args.steps.split(";") if x.strip()]
    if not steps:
        raise SystemExit("错误: plan 必须提供可用的 --steps")
    print(f"📋 parent plan [{parent['id']}]")
    print(f"   title: {args.title}")
    for idx, step in enumerate(steps, start=1):
        child_args = argparse.Namespace(**vars(args))
        child_args.parent_id = parent["id"]
        child_args.depends_on = prev
        child_args.next_action = step
        child_args.success_criteria = f"Step {idx}/{len(steps)} completed for plan: {args.title}"
        child = new_task(runtime, f"{args.title} / step {idx}: {step}", child_args)
        tasks.append(child)
        prev = child["id"]
        print(f"✅ child {idx} [{child['id']}]")
        print(f"   title: {child['title']}")
        if child["depends_on"]:
            print(f"   depends_on: {child['depends_on'][0]}")
    runtime.save_tasks(tasks)
    print(f"📦 plan queued: {args.title}")
    print(f"   parent: {parent['id']}")
    print(f"   steps: {len(steps)}")
    return 0


def cmd_list(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    filtered = []
    for task in tasks:
        if args.status and task["status"] != args.status:
            continue
        if args.owner_agent and task.get("owner_agent_id") != args.owner_agent:
            continue
        filtered.append(task)
    print("\n═══════════════════════════════════════")
    print("  agent-todo execution queue")
    print("═══════════════════════════════════════\n")
    if not filtered:
        print("  (no matching tasks)\n")
        return 0
    for task in filtered:
        print(f"  {format_status(task['status'])} [{task['id'][:8]}]")
        print(f"     title: {task['title']}")
        if task.get("task_type"):
            print(f"     type: {task['task_type']}")
        if task.get("owner_agent_id"):
            print(f"     owner_agent_id: {task['owner_agent_id']}")
        if task.get("deadline"):
            print(f"     deadline: {task['deadline']}")
        if task.get("source"):
            print(f"     source: {task['source']}")
        if task.get("next_action"):
            print(f"     next_action: {task['next_action']}")
        print()
    return 0


def cmd_show(runtime: Runtime, args: argparse.Namespace) -> int:
    task = task_by_id(runtime.load_tasks(), args.id)
    print("\n═══════════════════════════════════════")
    print("  task detail")
    print("═══════════════════════════════════════")
    for key in [
        "id",
        "title",
        "task_type",
        "owner_agent_id",
        "created_by_agent_id",
        "source",
        "status",
        "deadline",
        "next_action",
        "success_criteria",
        "created_at",
        "updated_at",
        "last_attempt_at",
        "completed_at",
        "result",
        "parent_id",
        "depends_on",
        "tags",
    ]:
        print(f"  {key:17} {task.get(key, '')}")
    print()
    return 0


def cmd_report(runtime: Runtime, args: argparse.Namespace) -> int:
    print(render_report(task_by_id(runtime.load_tasks(), args.id)))
    return 0


def cmd_done(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    task = task_by_id(tasks, args.id)
    ts = now_iso()
    task["status"] = "done"
    task["updated_at"] = ts
    task["completed_at"] = ts
    task["result"] = args.note
    runtime.save_tasks(tasks)
    print(f"✅ task done [{task['id']}]")
    print(f"   title: {task['title']}")
    print("\n═══ completion report ═══")
    print(render_report(task))
    return 0


def cmd_block(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    task = task_by_id(tasks, args.id)
    task["status"] = "blocked"
    task["blocked_reason"] = args.reason
    task["result"] = args.reason
    task["updated_at"] = now_iso()
    runtime.save_tasks(tasks)
    print(f"🧱 task blocked [{task['id']}]")
    if args.reason:
        print(f"   reason: {args.reason}")
    return 0


def cmd_unblock(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    task = task_by_id(tasks, args.id)
    if task["status"] != "blocked":
        print(f"⚠️ 任务 [{task['id']}] 状态是 {task['status']}，不是 blocked，无需 unblock")
        return 0
    task["status"] = "pending"
    task["updated_at"] = now_iso()
    runtime.save_tasks(tasks)
    print(f"✅ task unblocked [{task['id']}]")
    print(f"   title: {task['title']}")
    return 0


def cmd_cancel(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    task = task_by_id(tasks, args.id)
    task["status"] = "cancelled"
    task["result"] = args.reason
    task["updated_at"] = now_iso()
    runtime.save_tasks(tasks)
    print(f"❌ task cancelled [{task['id']}]")
    if args.reason:
        print(f"   reason: {args.reason}")
    return 0


def cmd_run_pending(runtime: Runtime, args: argparse.Namespace) -> int:
    tasks = runtime.load_tasks()
    selected = select_task(tasks)
    if not selected:
        print("HEARTBEAT_OK")
        return 0
    if args.claim:
        ts = now_iso()
        selected["status"] = "running"
        selected["claimed_at"] = selected.get("claimed_at") or ts
        selected["last_attempt_at"] = ts
        selected["updated_at"] = ts
        runtime.save_tasks(tasks)
    print("EXECUTE_NOW")
    for key in ["id", "title", "task_type", "owner_agent_id", "created_by_agent_id", "source", "deadline", "next_action", "success_criteria"]:
        if selected.get(key):
            print(f"{key}: {selected[key]}")
    if selected.get("tags"):
        print(f"tags: {','.join(selected['tags'])}")
    if selected.get("parent_id"):
        print(f"parent_id: {selected['parent_id']}")
    if selected.get("depends_on"):
        print(f"depends_on: {','.join(selected['depends_on'])}")
    print("\nDo the task now. When finished, call:")
    print(f"./script.sh done {selected['id']} --note \"what was completed\"")
    print("If blocked, call:")
    print(f"./script.sh block {selected['id']} --reason \"why it is blocked\"")
    return 0


def cmd_agents_list(runtime: Runtime, _args: argparse.Namespace) -> int:
    for workspace in runtime.discovered_workspaces():
        local_path = workspace / ".agent-todo" / "local.json"
        if not local_path.exists():
            continue
        local_cfg = load_json(local_path, {})
        agent_id = local_cfg.get("agent_id") or ""
        label = local_cfg.get("label") or ""
        print(f"- {agent_id}\t{label}\t{workspace}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-todo", add_help=True)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")
    sub.add_parser("doctor")

    p = sub.add_parser("setup-heartbeat")
    p.add_argument("--write", action="store_true")
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("add")
    p.add_argument("title")
    common_task_parser(p)

    p = sub.add_parser("dispatch")
    p.add_argument("title")
    p.add_argument("--to-agent", required=True)
    common_task_parser(p)

    p = sub.add_parser("plan")
    p.add_argument("title")
    p.add_argument("--steps", required=True)
    common_task_parser(p)

    p = sub.add_parser("list")
    p.add_argument("--status", default="")
    p.add_argument("--owner-agent", default="")

    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("view")
    p.add_argument("id")
    p = sub.add_parser("report")
    p.add_argument("id")

    p = sub.add_parser("run-pending")
    p.add_argument("--claim", action="store_true")

    p = sub.add_parser("done")
    p.add_argument("id")
    p.add_argument("--note", default="")
    p = sub.add_parser("complete")
    p.add_argument("id")
    p.add_argument("--note", default="")

    p = sub.add_parser("block")
    p.add_argument("id")
    p.add_argument("--reason", default="")

    p = sub.add_parser("unblock")
    p.add_argument("id")

    p = sub.add_parser("cancel")
    p.add_argument("id")
    p.add_argument("--reason", default="")

    agents = sub.add_parser("agents")
    agents_sub = agents.add_subparsers(dest="agents_command", required=True)
    agents_sub.add_parser("list")

    return parser


def main() -> int:
    script_dir = Path(__file__).resolve().parents[1]
    runtime = Runtime.detect(script_dir)
    parser = build_parser()
    args = parser.parse_args()

    command = args.command
    if command == "init":
        return cmd_init(runtime, args)
    if command == "doctor":
        return cmd_doctor(runtime, args)
    if command == "setup-heartbeat":
        return cmd_setup_heartbeat(runtime, args)
    if command == "add":
        return cmd_add(runtime, args)
    if command == "dispatch":
        return cmd_dispatch(runtime, args)
    if command == "plan":
        return cmd_plan(runtime, args)
    if command == "list":
        return cmd_list(runtime, args)
    if command in {"show", "view"}:
        return cmd_show(runtime, args)
    if command == "report":
        return cmd_report(runtime, args)
    if command == "run-pending":
        return cmd_run_pending(runtime, args)
    if command in {"done", "complete"}:
        return cmd_done(runtime, args)
    if command == "block":
        return cmd_block(runtime, args)
    if command == "unblock":
        return cmd_unblock(runtime, args)
    if command == "cancel":
        return cmd_cancel(runtime, args)
    if command == "agents" and args.agents_command == "list":
        return cmd_agents_list(runtime, args)
    parser.error(f"unknown command: {command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
