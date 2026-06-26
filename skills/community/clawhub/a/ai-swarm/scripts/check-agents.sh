#!/usr/bin/env bash
# Universal check-agents.sh — Monitor all active agents across ALL projects
# Run via cron or heartbeat to babysit agents
# Now also generates EOR logs on completion detection

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
TASKS_FILE="$SWARM_DIR/active-tasks.json"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"

[[ -f "$TASKS_FILE" ]] || exit 0

python3 << PYEOF
import json, subprocess, os, sys

script_dir = os.path.dirname(os.path.abspath("$SWARM_DIR/check-agents.sh"))
# Use the known swarm dir
script_dir = "$SWARM_DIR"
tasks_path = os.path.join(script_dir, "active-tasks.json")
notify_path = os.path.join(script_dir, "pending-notifications.txt")
eor_script = os.path.join(script_dir, "eor-log.sh")

with open(tasks_path) as f:
    data = json.load(f)

changed = False
notifications = []

for task in data.get("tasks", []):
    if task["status"] != "running":
        continue
    
    session = task["tmuxSession"]
    
    # Check if tmux session is still alive
    result = subprocess.run(["tmux", "has-session", "-t", session], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        # Session ended
        branch = task.get("branch", "")
        project_dir = task.get("projectDir", task.get("worktree", "."))
        task_id = task.get("id", "unknown")
        agent = task.get("agent", "swarm")
        
        # --- Generate EOR log ---
        if os.path.isfile(eor_script) and os.path.isdir(project_dir):
            try:
                eor_result = subprocess.run(
                    ["bash", eor_script, project_dir, task_id, "", agent],
                    capture_output=True, text=True, timeout=30
                )
                if eor_result.returncode == 0:
                    print(f"EOR log generated for {task_id}")
                else:
                    print(f"EOR log failed for {task_id}: {eor_result.stderr[:200]}")
            except Exception as e:
                print(f"EOR log error for {task_id}: {e}")
        
        # Check for PR
        pr_num = ""
        try:
            pr_result = subprocess.run(
                ["gh", "pr", "list", "--head", branch, "--json", "number", "-q", ".[0].number"],
                capture_output=True, text=True, cwd=project_dir, timeout=15
            )
            pr_num = pr_result.stdout.strip()
        except:
            pass
        
        task["status"] = "done"
        task["completedAt"] = int(subprocess.run(["date", "+%s"], capture_output=True, text=True).stdout.strip()) * 1000
        
        if pr_num:
            task["pr"] = int(pr_num)
            notifications.append(f"✅ Agent {session} completed task '{task_id}' for {task.get('project','?')}. PR #{pr_num} ready for review. EOR log written.")
        else:
            notifications.append(f"✅ Agent {session} completed task '{task_id}' for {task.get('project','?')}. Check branch {branch}. EOR log written.")
        
        changed = True

if changed:
    with open(tasks_path, "w") as f:
        json.dump(data, f, indent=2)

if notifications:
    with open(notify_path, "a") as f:
        for n in notifications:
            f.write(n + "\n")
    print("\n".join(notifications))
else:
    print("All agents still running or no active tasks.")
PYEOF
