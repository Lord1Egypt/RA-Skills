# AgentPathfinder: v1.2.x vs v1.3.0 — What Actually Happens When You Use It

This document shows the EXACT difference in what you see and what gets logged.

---

## Scenario: Your AI agent runs a 3-step deployment task

### Step 1: Run tests
### Step 2: Build Docker image  
### Step 3: Push to registry

Your agent uses `exec` to run shell commands. Here's what happens.

---

## BEFORE v1.3.0 (v1.2.x) — What Gets Logged

### You create the task:
```bash
$ pf create deploy_api "run_tests" "build_image" "push_registry"
```

### Your agent claims step 1 is done:
```python
engine.claim_step(task_id, step_number=1, agent_id="agent_1")
```

### What gets written to the audit trail:
```json
{"event": "step_claimed", "task_id": "abc-123", "step_number": 1, "agent_id": "agent_1", "seq": 1, "hmac_truncated": "a1b2c..."}
```

### What you see:
```
$ pf status deploy_api
✅ deploy_api — 1/3 complete
```

### What you DON'T see:
- What command the agent actually ran
- What the output was
- Whether the tests passed or failed
- What files were read or written
- Any tool calls the agent made

**The audit trail only records: "Agent_1 claimed step 1 was done."**

If something breaks in production, you have NO RECORD of:
- The actual `docker build` command
- The actual `docker push` output
- Whether the agent ran `pytest` or `rm -rf`

---

## AFTER v1.3.0 — What Gets Logged

### Same task creation:
```bash
$ pf create deploy_api "run_tests" "build_image" "push_registry"
```

### Your agent now uses tool audit before claiming:
```python
# NEW in v1.3.0 — get tool audit for this step
audit = engine.get_tool_audit(task_id, step_number=1)
executor = AuditedToolExecutor(audit)

# Run tests — FULLY LOGGED
result = executor.exec("pytest tests/ --tb=short")
# Logs: command="pytest tests/ --tb=short", stdout="3 passed...", returncode=0

# Build image — FULLY LOGGED
result = executor.exec("docker build -t myapp:v1 .")
# Logs: command="docker build...", stdout="Successfully built..."

# Read config — FULLY LOGGED
content = executor.read_file("/app/config.yml")
# Logs: path="/app/config.yml", content_length=256

# Write deployment manifest — FULLY LOGGED
executor.write_file("/app/manifest.json", '{"version": "1.0"}')
# Logs: path="/app/manifest.json", bytes_written=19

# NOW claim the step
engine.claim_step(task_id, step_number=1, agent_id="agent_1")
```

### What gets written to the audit trail (same file, same HMAC):

```json
// BEFORE: You only got this
{"event": "step_claimed", "task_id": "abc-123", "step_number": 1, "agent_id": "agent_1", "seq": 1}

// AFTER: You get this PLUS all the tool calls
{"event": "TOOL_INVOKED", "task_id": "abc-123", "tool_id": "tl_a1b2c3", "tool_name": "exec", 
 "args": {"command": "pytest tests/ --tb=short", "timeout": null}, "seq": 2}

{"event": "TOOL_RESULT", "task_id": "abc-123", "tool_id": "tl_a1b2c3", "status": "completed",
 "result": {"stdout": "========================= test session starts =========================\nplatform linux -- Python 3.13...\n========================== 3 passed in 0.42s ==========================\n", "stderr": "", "returncode": 0},
 "exit_code": 0, "duration_ms": 420, "seq": 3}

{"event": "TOOL_INVOKED", "task_id": "abc-123", "tool_id": "tl_d4e5f6", "tool_name": "exec",
 "args": {"command": "docker build -t myapp:v1 ."}, "seq": 4}

{"event": "TOOL_RESULT", "task_id": "abc-123", "tool_id": "tl_d4e5f6", "status": "completed",
 "result": {"stdout": "Successfully built 7d4a8c9f2e1b\n", "stderr": "", "returncode": 0},
 "exit_code": 0, "duration_ms": 12500, "seq": 5}

{"event": "TOOL_INVOKED", "task_id": "abc-123", "tool_id": "tl_g7h8i9", "tool_name": "read_file",
 "args": {"path": "/app/config.yml"}, "seq": 6}

{"event": "TOOL_RESULT", "task_id": "abc-123", "tool_id": "tl_g7h8i9", "status": "completed",
 "result": {"content_length": 256, "path": "/app/config.yml"}, "exit_code": 0, "duration_ms": 8, "seq": 7}

{"event": "TOOL_INVOKED", "task_id": "abc-123", "tool_id": "tl_j0k1l2", "tool_name": "write_file",
 "args": {"path": "/app/manifest.json", "content_length": 19}, "seq": 8}

{"event": "TOOL_RESULT", "task_id": "abc-123", "tool_id": "tl_j0k1l2", "status": "completed",
 "result": {"bytes_written": 19, "path": "/app/manifest.json"}, "exit_code": 0, "duration_ms": 3, "seq": 9}

// And finally the step claim
{"event": "step_claimed", "task_id": "abc-123", "step_number": 1, "agent_id": "agent_1", "seq": 10}
```

---

## What You Can Do With v1.3.0 That You Couldn't Do Before

### 1. Forensic Investigation After Failure

**Scenario:** Production broke at 2AM. You wake up at 8AM.

**v1.2.x:** You see:
```
Agent_1 claimed "push_registry" at 02:15
```
That's it. You have NO IDEA what actually happened.

**v1.3.0:** You see:
```
02:14:32 — TOOL_INVOKED | exec | docker build -t myapp:latest
02:14:45 — TOOL_RESULT  | exec | completed | 13 seconds
02:14:46 — TOOL_INVOKED | exec | docker tag myapp:latest registry.io/myapp:latest
02:14:47 — TOOL_RESULT  | exec | completed | 1 second
02:14:48 — TOOL_INVOKED | exec | docker push registry.io/myapp:latest
02:15:02 — TOOL_RESULT  | exec | ERROR | exit_code=1 | stderr="denied: requested access to the resource is denied"
02:15:03 — step_claimed | push_registry | agent_1
```

**You know immediately:** The push failed with authentication error, but the agent claimed success anyway.

---

### 2. Detecting Agent Lies

**Scenario:** Agent says "tests passed."

**v1.2.x:** You have to TRUST it. No evidence.

**v1.3.0:** You check:
```json
{"event": "TOOL_RESULT", "tool_name": "exec", 
 "result": {"stdout": "========================== 3 passed in 0.42s ==========================\n"},
 "exit_code": 0}
```

Or if the agent is lying:
```json
{"event": "TOOL_RESULT", "tool_name": "exec",
 "result": {"stdout": "========================== 2 failed, 1 passed ==========================\n"},
 "exit_code": 1}
```

The agent might still CLAIM the step passed, but you can CROSS-CHECK the tool output.

**Important:** AgentPathfinder doesn't AUTOMATICALLY catch the lie. But now you have the EVIDENCE to catch it yourself.

---

### 3. Compliance: "Show Me Everything the AI Did"

**Scenario:** Compliance officer asks "What commands did your AI run on our production servers last month?"

**v1.2.x:** "Uh... agent_1 claimed step 3 was done. That's all I have."

**v1.3.0:** 
```bash
$ grep '"tool_name": "exec"' audit_trail.jsonl | jq '.args.command'
"pytest tests/ --tb=short"
"docker build -t myapp:v1 ."
"docker push registry.io/myapp:v1"
"kubectl rollout restart deploy/myapp"
"curl -X POST https://api.internal/init"
```

Full command history. HMAC-signed. Tamper-evident.

---

### 4. Crash Recovery With Context

**Scenario:** Agent crashes after running 47 of 100 tests.

**v1.2.x:** You see: "Step 1 claimed complete." But you don't know which tests were actually run.

**v1.3.0:** 
```json
{"event": "TOOL_INVOKED", "tool_id": "tl_abc", "args": {"command": "pytest test_file_47.py"}}
{"event": "TOOL_RESULT", "tool_id": "tl_abc", "status": "completed"}
{"event": "TOOL_INVOKED", "tool_id": "tl_def", "args": {"command": "pytest test_file_48.py"}}
// CRASH HAPPENS HERE — no TOOL_RESULT for tl_def
```

You see EXACTLY which test file it was running when it crashed. Resume from file 48.

---

### 5. Cost/Debugging: How Long Did Each Step Take?

**v1.3.0 tool results include `duration_ms`:**
```json
{"tool_name": "exec", "args": {"command": "docker build..."}, "duration_ms": 12500}
{"tool_name": "exec", "args": {"command": "docker push..."}, "duration_ms": 45000}
{"tool_name": "read_file", "args": {"path": "/app/config.yml"}, "duration_ms": 8}
```

Build took 12.5s. Push took 45s. Config read took 8ms. You can identify bottlenecks.

---

## Summary Table

| What You Want To Know | v1.2.x (Before) | v1.3.0 (After) |
|-----------------------|-----------------|----------------|
| Which agent claimed what step? | ✅ Yes | ✅ Yes |
| When did the agent claim it? | ✅ Yes | ✅ Yes |
| What command did the agent run? | ❌ No | ✅ Full command logged |
| What was the command output? | ❌ No | ✅ Full stdout/stderr logged |
| Did the command succeed? | ❌ No | ✅ Exit code logged |
| How long did it take? | ❌ No | ✅ Duration logged |
| What files did it read? | ❌ No | ✅ File paths logged |
| What files did it write? | ❌ No | ✅ File paths + sizes logged |
| Can I see the full audit history? | ✅ Yes (step claims only) | ✅ Yes (steps + all tools) |
| Is the audit tamper-evident? | ✅ Yes (HMAC-signed) | ✅ Yes (HMAC-signed) |
| Can I catch an agent lying? | ❌ No evidence | ⚠️ Evidence exists, but YOU must check |

---

## The Honest Pitch (One Line)

**v1.2.x:** "Your agent says it did the work. You believe it."

**v1.3.0:** "Your agent says it did the work. Here's the actual command it ran, the actual output, and a cryptographic proof nobody edited the record. You still decide if you believe it — but now you have evidence."

---

## What v1.3.0 Is NOT

- ❌ It does NOT prevent the agent from running dangerous commands
- ❌ It does NOT automatically detect agent lies — it gives you evidence to check
- ❌ It does NOT verify the agent actually did the work — it logs what it claimed
- ❌ It does NOT prevent deletion of the audit file

**v1.3.0 = Receipt system for AI agent actions. That's it.**
