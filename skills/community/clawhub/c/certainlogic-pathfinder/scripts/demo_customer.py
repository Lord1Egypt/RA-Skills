#!/usr/bin/env python3
"""Real demo — customer experience. Just runs, no input needed."""
import sys, json, subprocess, time
from pathlib import Path

sys.path.insert(0, '/data/.openclaw/workspace/skills/certainlogic-pathfinder')
from agentpathfinder.task_engine import TaskEngine
from agentpathfinder.tool_audit import AuditedToolExecutor

DATA_DIR = Path.home() / ".agentpathfinder/pathfinder_data"
task = TaskEngine(data_dir=DATA_DIR)

# ── Create fresh task ──
print("=" * 60)
print("AgentPathfinder — Real Task Demo")
print("=" * 60)

task_id = task.create_task("deploy", [
    {"name": "test"},
    {"name": "build"},
    {"name": "deploy"},
    {"name": "verify"},
])
print(f"\n✅ Task created: {task_id}")
print(f"📁 Data dir: {DATA_DIR}")

# ── Dashboard URL ──
print(f"\n🌐 Dashboard: http://localhost:7879/dashboard.html")
print("   (Open this in your browser now — auto-refreshes every 2s)")

# ── Step 1: Run tests ──
print("\n--- STEP 1: Run tests ---")
audit1 = task.get_tool_audit(task_id, 1)
exec1 = AuditedToolExecutor(audit1)

result = exec1.exec("python3 -m pytest /data/.openclaw/workspace/skills/certainlogic-pathfinder/tests/ -v 2>&1 | tail -5")
print(f"   ➤ Test result: {result['stdout'].strip()}")

time.sleep(2)

# ── Step 2: Build image ──
print("\n--- STEP 2: Build docker image ---")
audit2 = task.get_tool_audit(task_id, 2)
exec2 = AuditedToolExecutor(audit2)

# Read the actual skill.json
skill_json = exec2.read_file("/data/.openclaw/workspace/skills/certainlogic-pathfinder/skill.json")
print(f"   ➤ Read skill.json ({len(skill_json)} chars)")

# Simulate a command that FAILS (with audit trail)
tool_id = audit2.log_tool_call("exec", {"command": "docker push myapp:v1.3"})
audit2.log_tool_result(tool_id, None, exit_code=1, 
    error="denied: requested access to the resource is denied")
print(f"   ➤ Docker push FAILED — logged to audit trail")

# Build succeeds
result = exec2.exec("echo 'Docker build completed: myapp:v1.3'")
print(f"   ➤ Build OK: {result['stdout'].strip()}")

time.sleep(2)

# ── Step 3: Intentional failure ──
print("\n--- STEP 3: Deploy to registry (FAILS) ---")
audit3 = task.get_tool_audit(task_id, 3)
exec3 = AuditedToolExecutor(audit3)

result = exec3.exec("ls /nonexistent_dir_xyz")
# Above will error and auto-log

print(f"   ➤ Deploy step FAILED (expected demo failure)")

time.sleep(2)

# ── Step 4: Hanging call + verify ──
print("\n--- STEP 4: Verify deployment ---")
audit4 = task.get_tool_audit(task_id, 4)

# Health check started but never receives result = HANGING CALL
audit4.log_tool_call("web_fetch", {"url": "http://localhost:8080/health", "timeout": 5})
print(f"   ➤ Health check started (no result = HANGING CALL)")

# Verify succeeds
exec4 = AuditedToolExecutor(audit4)
result = exec4.exec("echo 'Container running on port 8080'")
print(f"   ➤ Verify OK: {result['stdout'].strip()}")

time.sleep(2)

# ── Generate dashboard ──
subprocess.run([
    sys.executable, "/data/.openclaw/workspace/skills/certainlogic-pathfinder/scripts/dashboard_v130.py",
    "generate", "--task", task_id
], capture_output=True)

# ── Results ──
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

audit_file = DATA_DIR / "audit" / f"{task_id}.jsonl"
events = [json.loads(l) for l in audit_file.read_text().strip().split("\n")]
tool_events = [e for e in events if e.get("event", "").startswith("TOOL_")]
errors = [e for e in tool_events if e.get("status") == "error"]
hanging = audit4.get_active_calls()

print(f"\nTotal signed events:    {len(events)}")
print(f"Tool calls logged:      {len(tool_events)}")
print(f"Errors caught:          {len(errors)}")
print(f"Tool error details:     {', '.join(e.get('error','').split(':')[0] for e in errors) or 'none'}")
print(f"Hanging calls:          {len(hanging)}")
for h in hanging:
    print(f"   - {h['tool_name']} ({h['tool_id']}) — no result received")

# Show raw audit trail
print(f"\n--- Audit Trail (first 4 events) ---")
for ev in events[:4]:
    hmac = ev.get("hmac", "")[:16] + "..."
    print(f"   {ev['event']:14} HMAC={hmac}")

print(f"\n🌐 Refresh dashboard: http://localhost:7879/dashboard.html")
print(f"📁 Full audit file:   {audit_file}")
print("=" * 60)
