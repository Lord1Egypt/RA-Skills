#!/usr/bin/env python3
"""
Agent GTD - Task Manager
JSON API wrapper for Taskwarrior with witness gate support.
"""
import subprocess
import json
import sys
import os
from datetime import datetime

# Configuration
TASKRC = os.path.expanduser("~/.taskrc")
DEFAULT_RC = [
    "rc.confirmation=no",
    "rc.verbose=nothing",
    "rc.json.array=yes",
    "rc.search.case.sensitive=no"
]

def run_task(args, capture=True):
    """Execute a task command with consistent overrides."""
    cmd = ["task"] + DEFAULT_RC + args
    result = subprocess.run(cmd, capture_output=capture, text=True)
    return result.stdout if capture else result.returncode

def gtd_list(filter_query=None):
    """Return filtered tasks as clean JSON."""
    query = ["status:pending", "export"]
    if filter_query:
        query.insert(0, filter_query)
    output = run_task(query)
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return []

def gtd_capture(description, project="Inbox", tags=None):
    """Quick capture to inbox or specified project."""
    args = ["add", description, f"project:{project}"]
    if tags:
        for tag in tags:
            args.append(f"+{tag}")
    return run_task(args)

def check_witness_gate(task_id, witnessed):
    """Check if task is gated and requires approval."""
    task_json = run_task([str(task_id), "export"])
    try:
        tasks = json.loads(task_json)
        if tasks:
            task = tasks[0]
            tags = task.get("tags", [])
            if "gate" in tags and not witnessed:
                return {
                    "status": "gated",
                    "message": "Witness Gate Active. Authorization required.",
                    "task": {
                        "id": task["id"],
                        "uuid": task["uuid"],
                        "description": task["description"]
                    }
                }
    except json.JSONDecodeError:
        pass
    return None

def get_next_steps(limit=5):
    """Fetch next steps from Taskwarrior."""
    next_tasks = gtd_list("+next")
    urgent_tasks = gtd_list("+urgent")
    
    steps = []
    for t in (urgent_tasks + next_tasks)[:limit]:
        desc = t.get('description', 'Untitled')
        proj = t.get('project', '')
        tid = t.get('id', '?')
        steps.append(f"#{tid} [{proj}] {desc}" if proj else f"#{tid} {desc}")
    return steps

def handle_sleep(summary):
    """Handle session close with validation."""
    next_steps = get_next_steps(limit=3)
    
    if not next_steps:
        print("⚠️  Warning: No +next or +urgent tasks found.")
        print("   Consider adding next steps before sleeping.")
        steps_str = "(none defined)"
    else:
        steps_str = ", ".join(next_steps)
    
    full_summary = f"{summary} | next: {steps_str}"
    
    print("🌙 Session Close")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Summary: {summary}")
    print(f"Next: {steps_str}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Handoff persistence is handled by the agent's own session-close protocol.
    # The summary above is printed for the human / next session to see.
    return 0

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No action. Use: list, capture, done, delete, clarify, sleep"}))
        return 1
    
    action = sys.argv[1]
    
    if action == "list":
        filt = sys.argv[2] if len(sys.argv) > 2 else None
        tasks = gtd_list(filt)
        print(json.dumps(tasks, indent=2))
        
    elif action == "capture":
        desc = sys.argv[2]
        proj = sys.argv[3] if len(sys.argv) > 3 else "Inbox"
        tags = sys.argv[4:] if len(sys.argv) > 4 else []
        result = gtd_capture(desc, proj, tags)
        print(result)
        
    elif action == "clarify":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing task ID"}))
            return 1
        tid = sys.argv[2]
        mods = sys.argv[3:]
        
        witnessed = "--witnessed" in mods
        if witnessed:
            mods.remove("--witnessed")
        
        is_status_change = any(m.startswith("status:") for m in mods)
        if is_status_change:
            gate_error = check_witness_gate(tid, witnessed)
            if gate_error:
                print(json.dumps(gate_error))
                return 0
        
        print(run_task([tid, "modify"] + mods))
        
    elif action == "done":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing task ID"}))
            return 1
        tid = sys.argv[2]
        witnessed = "--witnessed" in sys.argv
        
        gate_error = check_witness_gate(tid, witnessed)
        if gate_error:
            print(json.dumps(gate_error))
            return 0
        
        print(run_task([tid, "done"]))
        
    elif action == "delete":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Missing task ID"}))
            return 1
        tid = sys.argv[2]
        witnessed = "--witnessed" in sys.argv
        
        gate_error = check_witness_gate(tid, witnessed)
        if gate_error:
            print(json.dumps(gate_error))
            return 0
        
        print(run_task([tid, "delete"]))
    
    elif action == "sleep":
        summary = sys.argv[2] if len(sys.argv) > 2 else "Session closed"
        return handle_sleep(summary)
        
    else:
        print(json.dumps({"error": f"Unknown action: {action}"}))
        return 1

if __name__ == "__main__":
    sys.exit(main() or 0)
