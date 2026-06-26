#!/bin/bash
# milestone-check.sh — Check if a milestone is complete and trigger codex-test
# Called by update-task-status.sh after any task reaches 'done'.
# Usage: milestone-check.sh <task_id>
#
# Reads milestones[] from active-tasks.json.
# If the task belongs to a milestone and ALL tasks in that milestone are done,
# writes a milestone_done signal and POSTs /hooks/agent to trigger codex-test.

set -euo pipefail

TASK_ID="${1:?Usage: milestone-check.sh <task_id>}"

TASKS_FILE="$HOME/.openclaw/workspace/swarm/active-tasks.json"
SWARM_DIR="$HOME/.openclaw/workspace/swarm"
SIGNAL_FILE="/tmp/agent-swarm-signals.jsonl"
IDEM_DIR="/tmp/agent-swarm-idem"
GATEWAY_URL="http://127.0.0.1:18789"

[[ ! -f "$TASKS_FILE" ]] && exit 0

HOOK_TOKEN=$(cat "$SWARM_DIR/hook-token" 2>/dev/null || echo "")
NOTIFY_TARGET=$(cat "$SWARM_DIR/notify-target" 2>/dev/null || echo "")
PROJECT_DIR=$(cat "$SWARM_DIR/project-dir" 2>/dev/null || echo "")

# Run Python to determine if any milestone is newly complete
python3 - <<PYEOF
import json, sys, os, subprocess
from datetime import datetime, timezone

tasks_file = os.path.expanduser("$TASKS_FILE")
task_id = "$TASK_ID"
signal_file = "$SIGNAL_FILE"
idem_dir = "$IDEM_DIR"
hook_token = "$HOOK_TOKEN"
notify_target = "$NOTIFY_TARGET"
project_dir = "$PROJECT_DIR"
gateway_url = "$GATEWAY_URL"

with open(tasks_file) as f:
    data = json.load(f)

milestones = data.get("milestones", [])
tasks_by_id = {t["id"]: t for t in data.get("tasks", [])}

triggered = []

for ms in milestones:
    ms_id = ms["id"]
    ms_task_ids = ms.get("task_ids", [])

    # Does this milestone contain the just-completed task?
    if task_id not in ms_task_ids:
        continue

    # Are ALL tasks in this milestone done?
    all_done = all(
        tasks_by_id.get(tid, {}).get("status") == "done"
        for tid in ms_task_ids
    )
    if not all_done:
        continue

    # Idempotency: only trigger once per milestone
    os.makedirs(idem_dir, exist_ok=True)
    idem_file = os.path.join(idem_dir, f"milestone-{ms_id}")
    if os.path.exists(idem_file):
        print(f"SKIP: milestone {ms_id} already triggered", file=sys.stderr)
        continue
    open(idem_file, "w").close()

    # Write milestone_done signal
    ts = int(datetime.now(timezone.utc).timestamp())
    signal = json.dumps({
        "event": "milestone_done",
        "milestone": ms_id,
        "milestone_name": ms.get("name", ms_id),
        "task_ids": ms_task_ids,
        "time": ts
    })
    with open(signal_file, "a") as sf:
        sf.write(signal + "\n")

    print(f"MILESTONE COMPLETE: {ms_id} — {ms.get('name', '')}")

    # Build test scope description
    test_scope = ms.get("test_scope", {})
    unit_files = test_scope.get("unit_test_files", [])
    verify_script = test_scope.get("verify_script", "")
    description = test_scope.get("description", "")

    unit_files_str = "\n".join(f"  - {f}" for f in unit_files) if unit_files else "  (none specified)"
    verify_str = f"  scripts/{verify_script}" if verify_script else "  (none)"

    agent_msg = f"""里程碑完成信号：{ms_id} — {ms.get("name", "")}

包含任务：{", ".join(ms_task_ids)}
测试说明：{description}

请执行以下步骤：
1. 读取 {tasks_file} 确认里程碑任务全部 done
2. 派发 codex-test agent 执行以下测试：
   - 工作目录：{project_dir}
   - 需要单元测试的文件：
{unit_files_str}
   - 验收脚本：{verify_str}
3. codex-test 任务 ID 格式：{ms_id}-test（例如 M1-test）
4. 如果测试全部通过：
   - 在 active-tasks.json 里标记该里程碑 test_status = "passed"
   - Telegram 通知：✅ {ms_id} 测试通过
   - 检查是否还有下一个里程碑的任务需要 dispatch
5. 如果有测试失败：
   - 定位到具体任务 → 返回对应 agent 修复
   - Telegram 通知：❌ {ms_id} 测试失败，已返回修复
"""

    if hook_token:
        import subprocess, json as _json
        payload = _json.dumps({
            "message": agent_msg,
            "name": f"swarm-milestone-{ms_id}",
            "sessionKey": f"hook:swarm:milestone:{ms_id}",
            "deliver": True,
            "channel": "telegram",
            "to": notify_target,
            "model": "anthropic/claude-sonnet-4-20250514",
            "thinking": "low",
            "timeoutSeconds": 180
        })
        subprocess.Popen(
            ["curl", "-s", "-X", "POST", f"{gateway_url}/hooks/agent",
             "-H", f"Authorization: Bearer {hook_token}",
             "-H", "Content-Type: application/json",
             "-d", payload],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        print(f"Triggered codex-test for milestone {ms_id}")

    triggered.append(ms_id)

if not triggered:
    sys.exit(0)

print(f"Milestone(s) triggered: {triggered}")
PYEOF
