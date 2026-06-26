#!/usr/bin/env python3
"""Live demo: AgentPathfinder with real tool audit + dashboard + chat notifications."""
import sys
import subprocess
import time
import json
from pathlib import Path

sys.path.insert(0, '/data/.openclaw/workspace/skills/certainlogic-pathfinder')

from agentpathfinder.task_engine import TaskEngine
from agentpathfinder.issuing_layer import IssuingLayer
from agentpathfinder.tool_audit import AuditedToolExecutor

# ── Paths ──
DATA_DIR = Path.home() / ".agentpathfinder" / "pathfinder_data"
SKILL_DIR = Path("/data/.openclaw/workspace/skills/certainlogic-pathfinder")

def chat(msg):
    print(f"\n🟢 CHAT NOTIFICATION: {msg}\n")
    sys.stdout.flush()

def update_dashboard(task_id):
    subprocess.run([
        sys.executable, str(SKILL_DIR / "scripts" / "dashboard_v130.py"),
        "generate", "--task", task_id
    ], cwd=str(SKILL_DIR), capture_output=True)
    print(f"  📊 Dashboard updated")

# ── Init ──
print("=" * 60)
print("  AGENT PATHFINDER — LIVE DEMO")
print("=" * 60)

task = TaskEngine(data_dir=DATA_DIR)
issuer = IssuingLayer(task)

# ── Create Task ──
print("\n1) Creating task 'deploy' with 4 steps...")
step_list = [{"name": "test"}, {"name": "build"}, {"name": "push"}, {"name": "restart"}]
task_id = task.create_task("deploy", step_list)
print(f"   ✅ Task created: {task_id}")
chat(f"🚀 Task 'deploy' created: {task_id}")

update_dashboard(task_id)
print(f"\n   🌐 Dashboard: http://localhost:9999/agentpathfinder_dashboard.html")
print("   (Open it in your browser NOW — hit refresh between steps)")
print("\n   --- Starting execution in 5 seconds ---\n")
time.sleep(5)

# ── Step 1: Test (PASS) ──
print("\n2) Step 1: TEST — Simulating pytest run...")
audit1 = task.get_tool_audit(task_id, 1)
exec1 = AuditedToolExecutor(audit1)

# Run a real command
tool_id1 = audit1.log_tool_call("exec", {"command": "pytest tests/ -v --tb=short"})
exec_result = exec1.exec("echo 'tests passed: 17/17'")
audit1.log_tool_result(tool_id1, result=exec_result, exit_code=0)

# Issue token
task.set_step_running(task_id, 1, idempotency_key="test-v1")
token = issuer.issue_step_token(task_id, 1, result=exec_result, result_hash="ok1234")
chat(f"✅ Step 1 TEST — passed. Token: {token['token_id']}")
print(f"   ✅ Token issued: {token['token_id']}")

update_dashboard(task_id)
time.sleep(3)

# ── Step 2: Build (PASS with error caught) ──
print("\n3) Step 2: BUILD — Running commands with audit...")
audit2 = task.get_tool_audit(task_id, 2)
exec2 = AuditedToolExecutor(audit2)

# Read a config file
config = exec2.read_file("/etc/os-release")
print(f"   📄 Read /etc/os-release ({len(config)} chars)")

# Simulate an auth failure (logged but task continues)
tool_id2a = audit2.log_tool_call("exec", {"command": "docker push myapp:v1.3"})
audit2.log_tool_result(tool_id2a, None, exit_code=1, error="denied: requested access to the resource is denied")
print("   ⚠️ Docker push denied — recorded in audit trail")

# Build succeeds
tool_id2b = audit2.log_tool_call("exec", {"command": "docker build -t myapp:v1.3 ."})
build_result = exec2.exec("echo 'docker build completed in 2.3s'")
audit2.log_tool_result(tool_id2b, build_result, exit_code=0)
print(f"   ✅ Build OK")

# Issue token
task.set_step_running(task_id, 2, idempotency_key="build-v1")
token2 = issuer.issue_step_token(task_id, 2, result=build_result, result_hash="ok5678")
chat(f"✅ Step 2 BUILD — passed. 1 auth failure caught & logged. Token: {token2['token_id']}")

update_dashboard(task_id)
time.sleep(3)

# ── Step 3: Push (FAIL) ──
print("\n4) Step 3: PUSH — Simulating registry failure...")
audit3 = task.get_tool_audit(task_id, 3)
exec3 = AuditedToolExecutor(audit3)

try:
    exec3.exec("false")  # This will fail and be auto-logged
except:
    pass

issuer.fail_step(task_id, 3, "docker push denied: authentication required")
chat(f"❌ Step 3 PUSH — FAILED: Docker auth denied")
print(f"   ❌ Step failed. Task paused.")

update_dashboard(task_id)
time.sleep(3)

# ── Step 4: Restart (PASS with hanging call) ──
print("\n5) Step 4: RESTART — Deploying container...")
audit4 = task.get_tool_audit(task_id, 4)

# Start a health check but never log result (hanging call)
audit4.log_tool_call("web_fetch", {"url": "http://localhost:8080/health", "timeout": 5})
# DELIBERATELY NO RESULT
print("   ⏳ Health check started (no result = hanging call)")

# Restart succeeds
exec4 = AuditedToolExecutor(audit4)
restart_result = exec4.exec("echo 'container up on port 8080'")

task.set_step_running(task_id, 4, idempotency_key="restart-v1")
token4 = issuer.issue_step_token(task_id, 4, result=restart_result, result_hash="ok9999")
chat(f"✅ Step 4 RESTART — passed. 1 hanging call detected. Token: {token4['token_id']}")
print(f"   ✅ Token issued: {token4['token_id']}")

update_dashboard(task_id)

# ── Summary ──
print("\n" + "=" * 60)
print("  DEMO COMPLETE")
print("=" * 60)

status = task.get_status(task_id)
print(f"\n📋 Task: {status['name']} ({task_id})")
print(f"   Progress: {status['progress']}")
print(f"   State: {status['overall_state']}")
for s in status['steps']:
    icon = "✅" if s['state'] == 'complete' else "❌" if s['state'] == 'failed' else "⏳"
    print(f"   {icon} Step {s['step_number']}: {s['name']} ({s['state']})")

# Audit stats
audit_file = DATA_DIR / "audit" / f"{task_id}.jsonl"
if audit_file.exists():
    events = [json.loads(l) for l in audit_file.read_text().strip().split("\n")]
    tool_calls = [e for e in events if e.get('event') == 'TOOL_INVOKED']
    tool_errs = [e for e in events if e.get('event') == 'TOOL_RESULT' and e.get('status') == 'error']
    print(f"\n📊 Audit events: {len(events)}")
    print(f"   Tool calls logged: {len(tool_calls)}")
    print(f"   Tool errors caught: {len(tool_errs)}")

# Hanging calls
hanging = audit4.get_active_calls()
print(f"\n⚠️ Hanging calls (no result): {len(hanging)}")
for h in hanging:
    print(f"   - {h['tool_name']} ({h['tool_id']})")

print(f"\n🌐 Dashboard: http://localhost:9999/agentpathfinder_dashboard.html")
print("=" * 60)
