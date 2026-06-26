---
name: claw-mission-killer
description: Interrupt a running agent task and rollback its session to the state before the last triggering user message. Use when an agent is stuck, running the wrong task, or needs to be redirected. Triggers on phrases like "interrupt agent", "stop agent and rollback", "cut agent task", "terminate and reset agent", "kill my_agent", "kill all agents", "终止 agent 任务并回滚", "kill掉", "打断". Supports all configured agents by ID, or all agents at once with --all.
---

# agent-interrupt

> One command. Agent stops. Memory rolled back. Like it never happened.

When an agent goes off-track — running the wrong task, stuck in a loop, or executing something you didn't intend — `agent-interrupt` kills it cleanly and rewinds its memory to before it received that task.

---

## Quick Start

After installing, run once to set up all your agents:

```bash
python -X utf8 scripts/install.py
```

Then just tell your assistant:

```
kill dev1
kill all
```

---

## What It Does

1. **Kills the process** — Finds and terminates the agent's running subprocess (precise PID or workspace path fallback)
2. **Verifies it's dead** — Aborts if any process survives; transcript stays untouched
3. **Backs up memory** — Saves the removed messages to `interrupt-logs/` for recovery
4. **Rolls back transcript** — Deletes the last user message (the task trigger) and everything after it
5. **Agent wakes up clean** — It enters standby with no memory of the interrupted task

---

## Fuzzy Agent Matching

No need to remember exact agent IDs. It understands names:

```
kill dev1        → matches zero_dev1
kill pm          → matches zero_pm
kill 开发工程师   ��� matches by Chinese name
kill all         → interrupts every agent except main
```

---

## Precise Kill (Recommended)

For agents running long scripts, use `run.py` wrapper so they can be killed precisely:

```bash
# Instead of: python your_script.py
python -X utf8 scripts/run.py --agent <your_agent_id> -- python your_script.py
```

`install.py` automatically adds this protocol to all your agents' `AGENTS.md` files.
New agents added later are picked up automatically via a background watcher.

---

## Recovery

Every rollback is backed up:
```
~/.openclaw/agents/<id>/interrupt-logs/rollback-YYYYMMDD-HHMMSS.jsonl
```
Append the backup lines back to the transcript to restore.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `interrupt.py` | Kill + rollback (main script) |
| `install.py` | One-time setup for all agents |
| `run.py` | Wrapper for precise kill support |
| `watch.py` | Auto-injects new agents (runs via cron) |
| `mark.py` | Manual PID registration (advanced) |

---

## Platform

Works on Windows, Linux, macOS. No external dependencies beyond Python stdlib.
