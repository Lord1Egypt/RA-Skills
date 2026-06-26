#!/usr/bin/env python3
"""AgentPathfinder CLI entry point."""
import argparse
import sys
import json
from pathlib import Path

# Add parent to path when run as module
sys.path.insert(0, str(Path(__file__).parent))

from agentpathfinder.task_engine import TaskEngine
from agentpathfinder.issuing_layer import IssuingLayer
from agentpathfinder.tool_audit import AuditedToolExecutor

DATA_DIR = Path.home() / ".agentpathfinder" / "pathfinder_data"


def cmd_create(args):
    engine = TaskEngine(data_dir=DATA_DIR)
    steps = [{"name": s.strip()} for s in args.steps.split(",")]
    task_id = engine.create_task(args.name, steps)
    print(f"Task created: {task_id}")
    return task_id


def cmd_status(args):
    engine = TaskEngine(data_dir=DATA_DIR)
    status = engine.get_status(args.task_id)
    print(json.dumps(status, indent=2))


def cmd_audit(args):
    engine = TaskEngine(data_dir=DATA_DIR)
    audit_file = DATA_DIR / "audit" / f"{args.task_id}.jsonl"
    if not audit_file.exists():
        print(f"No audit trail found for {args.task_id}")
        sys.exit(1)

    events = [json.loads(l) for l in audit_file.read_text().strip().split("\n")]
    tool_events = [e for e in events if e.get("event", "").startswith("TOOL_")]

    print(f"Audit trail: {args.task_id}")
    print(f"Total events: {len(events)}")
    print(f"Tool events: {len(tool_events)}")
    for ev in tool_events:
        icon = "🔧" if ev["event"] == "TOOL_INVOKED" else "✅" if ev.get("status") == "completed" else "❌"
        tool = ev.get("tool_name", "?")
        print(f"  {icon} [{ev['event']}] {tool} step={ev.get('step_number', '?')}")


def cmd_version(args):
    print("AgentPathfinder v1.2.0")


def cmd_reset_step(args):
    engine = TaskEngine(data_dir=DATA_DIR)
    step = engine.reset_step(args.task_id, args.step_number)
    print(f"Step {args.step_number} reset to pending")


def main():
    parser = argparse.ArgumentParser(description="AgentPathfinder CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a new task")
    p_create.add_argument("name", help="Task name")
    p_create.add_argument("steps", help="Comma-separated step names")
    p_create.set_defaults(func=cmd_create)

    p_status = sub.add_parser("status", help="Show task status")
    p_status.add_argument("task_id", help="Task ID")
    p_status.set_defaults(func=cmd_status)

    p_audit = sub.add_parser("audit", help="Show audit trail")
    p_audit.add_argument("task_id", help="Task ID")
    p_audit.set_defaults(func=cmd_audit)

    p_reset = sub.add_parser("reset-step", help="Reset a failed step")
    p_reset.add_argument("task_id", help="Task ID")
    p_reset.add_argument("step_number", type=int, help="Step number")
    p_reset.set_defaults(func=cmd_reset_step)

    p_version = sub.add_parser("version", help="Show version")
    p_version.set_defaults(func=cmd_version)

    args = parser.parse_args()
    if args.command == "version":
        args.func(args)
        return
    args.func(args)


if __name__ == "__main__":
    main()
