---
name: AgentPathfinder
description: "Cryptographically signed audit trails for AI agent tool calls. Every tool invocation is HMAC-SHA256 signed. Full arguments and results logged. Live dashboard shows which command failed, what the error was, whether agent claimed success falsely. The provenance layer for agent execution."
---

# AgentPathfinder

> **[Company Brain Core OS](https://certainlogic.ai/brain) — Free, local, deterministic knowledge base for your agent. Start here before adding audit trails.**

**Your AI agent said "Done." Prove it.** Cryptographically signed tool-level audit trails. See exactly which command failed, what the error was, and whether your agent lied about success.

---

## Part of the CertainLogic Stack

This skill works **standalone**. Install it, sign your tool calls, get proof of execution.

**Works even better with [Company Brain Core OS](https://certainlogic.ai/brain)** (`clawhub install company-brain-os`):
- Brain stores your audit patterns and flags suspicious signatures
- **CertainLogic Smart Router** — routes audit queries to the right tier
- **Skill Vetter Plus** — verifies audit integrity before external review

**All three are independent.** Use Pathfinder alone when you need verifiable execution. Add Brain when you want smart correlation of audit events.

---

## What This Is

The **provenance layer for AI agent execution.** Every tool call is cryptographically signed with HMAC-SHA256. Every failure is recorded. Every lie is detectable.

AgentPathfinder doesn't make your agent honest. It makes dishonesty **proveable.**

## What You Get

| Feature | How It Works | Truth Status |
|---------|-------------|--------------|
| ✅ Signed task tracking | Green = agent signed claim of completion | NOT verified — recorded only |
| ❌ Signed failure tracking | Red = agent signed claim of failure | NOT verified — recorded only |
| 🔒 Cryptographic signing | HMAC-SHA256 on every claimed event | Signature is real |
| 📋 Tamper-evident audit | Unauthorized edits break HMAC | Tampering detected if no key |
| 🔍 Tool-level audit | Every TOOL_INVOKED and TOOL_RESULT logged | Shows what actually ran |
| 📊 Live dashboard | Auto-refreshing HTML with tool call tree | Real-time HMAC verification |
| 🕒 Hanging call detection | Detects TOOL_INVOKED with no TOOL_RESULT | Catch stuck tools |
| 🧾 Fraud alerts | Alerts when agent claims success but tool errored | See false claims |
| 🔄 Crash recovery | Atomic writes + fsync + rename | Works |
| 💬 Chat notifications | SDK callbacks send updates to agent's chat | Real-time status |

**Pro (coming soon):** Multi-agent tracking, audit exports, webhooks.
**Enterprise:** On-prem, SSO/SAML, hosted vault.

## What This Is NOT

| ❌ Does NOT | Why |
|-------------|-----|
| Verify tasks are actually complete | It records claims. You must verify the work independently. |
| Prevent agents from lying | It signs what the agent says. False claims get signed too. |
| Replace human verification | It helps you track claims. You still need to check the actual work. |

## The Problem

Your AI agent says **"Done"** — but you have no idea what actually happened at the tool level.

- **Silent failures:** The agent claims success while `docker push` returned `exit_code=1`
- **Missing steps:** The agent skips `pytest` entirely and claims all tests passed
- **Wrong commands:** The agent runs `echo "done"` instead of the actual build
- **Crash recovery:** The agent restarts, has no memory of which tool calls were in-flight
- **Multi-agent confusion:** Two agents claim the same step — who actually did it?

You only find out when your customer does. 😤

## Installation

```bash
clawhub install certainlogicai.agentpathfinder
```

## Quick Start

```bash
# Create a signed task
python3 -m agentpathfinder create deploy "test,build,push,restart"
# → Task created: deploy-a7f3d2e1

# Start the audit chain for a step
# (automatically done when agent runs tools)

# View the live dashboard
cd ~/.openclaw/skills/certainlogicai.agentpathfinder
python3 scripts/dashboard_v130.py watch --task deploy-a7f3d2e1
# → Serves dashboard at http://localhost:8080
# → Auto-refreshes every 2 seconds
# → Shows tool call tree with args, results, HMAC signatures
# → Fraud alerts: hanging calls, false claims, missing results

# View audit trail
python3 -m agentpathfinder audit deploy-a7f3d2e1
# → Lists all signed tool events

# Export audit trail
python3 scripts/dashboard_v130.py export --task deploy-a7f3d2e1
# → Signed JSONL with every event + HMAC verification
```

## SDK Usage

```python
from agentpathfinder import TaskEngine
from agentpathfinder.tool_audit import ToolAuditChain, AuditedToolExecutor

# Initialize tool audit
task = TaskEngine(data_dir="~/.agentpathfinder")
step_list = [
    {"name": "test"},
    {"name": "build"},
    {"name": "push"},
    {"name": "restart"},
]
task_id = task.create_task("deploy", step_list)

# Start audit for a step
audit = task.get_tool_audit(task_id, step_number=1)

# Manually log a tool call
tool_id = audit.log_tool_call("exec", {"command": "pytest tests/ -v"})
# ... run the command ...
audit.log_tool_result(tool_id, result={"passed": True, "count": 17}, exit_code=0)
# → Logs TOOL_INVOKED with args + HMAC
# → Logs TOOL_RESULT with exit_code + output + HMAC

# Or use the executor wrapper (auto-logs real commands)
executor = AuditedToolExecutor(audit)
result = executor.exec("echo hello")  # Auto-logged

# Detect fraud
audit.detect_hanging_calls()  # Tools invoked but no result
audit.get_tool_summary()      # What was called, what failed
```

## CLI Reference

```bash
python3 -m agentpathfinder create <name> <steps>       # Create task (comma-separated steps)
python3 -m agentpathfinder status <task_id>            # View task status
python3 -m agentpathfinder audit <task_id>             # Verify HMAC signatures
python3 -m agentpathfinder reset-step <task_id> <n>    # Reset step (signed action)
```

## Dashboard

```bash
# Live watch mode with built-in HTTP server
python3 scripts/dashboard_v130.py watch --task <task_id>
# → http://localhost:8080

# Generate static report
python3 scripts/dashboard_v130.py generate --task <task_id>

# Export as JSON
python3 scripts/dashboard_v130.py export --task <task_id>
```

**Dashboard shows:**
- Tool call tree (args + results visible)
- HMAC signature for every event
- Integrity verification panel (tampered/corrupted count)
- Fraud alerts (hanging calls, false claims)
- Tool summary by category
- Multi-task support
- Dark mode with CertainLogic brand colors

## Safety

**Read SAFETY.md before using in production.**

Key limitations:
- Agent with filesystem access can read vault shards — **not a sandbox**
- False completions get signed — system records claims, not truth
- No independent observer — agent controls both execution AND logging

## License

MIT License © CertainLogic
