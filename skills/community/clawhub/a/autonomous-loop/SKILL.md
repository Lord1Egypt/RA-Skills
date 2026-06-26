---
name: autonomous-loop
description: "Add self-sustaining autonomous loop capability to an OpenClaw agent. The agent keeps working after each reply until a stop file is placed. Use when: (1) creating a new long-running agent, (2) converting an existing agent to autonomous mode, (3) debugging a loop that stopped unexpectedly."
metadata: {"openclaw": {"emoji": "🔄", "requires": {"os": ["darwin"]}}}
---

# Autonomous Loop

Keeps an OpenClaw agent working continuously without human intervention. After each reply, the plugin waits N seconds and automatically sends the next task instruction — until you place a stop file.

## Installation

```bash
# Copy the plugin into OpenClaw's extensions directory
cp -r ~/.openclaw/skills/local/autonomous-loop/plugin \
      ~/.openclaw/extensions/autonomous-loop
```

Verify it loaded:

```bash
openclaw plugins info autonomous-loop
openclaw gateway status
```

If not shown, restart the Gateway: `openclaw gateway restart`

## How It Works

```
Agent finishes a reply
        │
        ▼
[agent_end event]  ← plugin listens here
        │
        ├─ stop file exists? → skip this round
        │
        ▼
Wait delayMs (default 30s)
        │
        ├─ check stop file again (double-check)
        │
        ▼
Send next task message to the same session via WebSocket
        │
        ▼
Agent starts next round of work ────────────────────────↑ loop
```

Logs are written to: `~/.openclaw/logs/autonomous-loop-{agentId}.log`

## Configuration

Add to `~/.openclaw/openclaw.json` under the `plugins` key:

```json
{
  "plugins": {
    "autonomous-loop": {
      "delayMs": 30000,
      "defaultMessage": "Read TASKS.md and PROGRESS.md. Pick the highest-priority Pending task and execute it. Update both files when done.",
      "agents": {
        "david": "Read TASKS.md and PROGRESS.md to understand the current project state, then:\n\n1. If there is an in-progress task, continue it\n2. Otherwise pick the highest-priority Pending task (skip tasks requiring user input)\n3. Execute the task, verify with end-to-end browser testing, take a screenshot as proof\n4. Update TASKS.md and PROGRESS.md",
        "allen": "Read Todo.md. Pick the highest-priority incomplete task and execute it. Update Todo.md when done."
      }
    }
  }
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `delayMs` | number | Milliseconds to wait before sending the next message (default: 30000) |
| `defaultMessage` | string | Fallback message used when no per-agent message is configured |
| `agents` | object | Per-agent messages. Key = agentId, value = message string |

## Stop & Resume

```bash
# Pause a specific agent's loop
touch ~/.openclaw/autonomous-loop.{agentId}.stop

# Resume the loop
rm ~/.openclaw/autonomous-loop.{agentId}.stop

# Watch the loop log live
tail -f ~/.openclaw/logs/autonomous-loop-{agentId}.log
```

## Log Reference

| Log entry | Meaning |
|-----------|---------|
| `countdown-started` | Normal — reply finished, countdown running |
| `message-sent` | Normal — message delivered, next round started |
| `stop-file-detected` | Stop file found by watcher, loop paused |
| `skipped-stop-flag` | Stop file present at trigger time, skipped |
| `send-error` | Message delivery failed — check if gateway is running |
| `skipped-no-assistant-text` | Agent reply had no text content, skipped |
| `skipped-no-gateway-config` | Gateway port or token missing from config |
| `skipped-stop-token` | Agent replied with DONE or HEARTBEAT_OK — loop idle until next user message |

## Agent Workspace Structure

A workspace for an autonomous agent needs these files:

```
workspace-{agentId}/
├── AGENTS.md       # Startup sequence, memory system, behavior rules
├── SOUL.md         # Identity and core values
├── WORK.md         # Execution loop (pick task → execute → verify → wrap up)
├── TASKS.md        # Task queue (Pending / In Progress / Done)
├── PROGRESS.md     # Project state — must be updated at end of every session
├── HEARTBEAT.md    # Heartbeat checklist (empty file = skip)
└── ARTIFACTS/      # Work outputs (screenshots, code, analysis)
```

**Session startup sequence (defined in WORK.md):**

```
1. git log --oneline -20     understand what was done recently
2. read PROGRESS.md          current project state
3. read TASKS.md             find the next task
4. run init.sh (if present)  start the dev server
5. basic E2E test            catch leftover bugs from last session
6. pick one task, do one task
```

## Two-Phase Workflow for New Projects

Long-running agents restart fresh every session. Structure work in two phases:

**Phase 1 — Init session (first session only)**
1. Create `init.sh` — one command to start the dev server
2. Create `FEATURES.json` — full feature list, every item `"status": "failing"`
3. First git commit
4. Write each feature as a sub-task in TASKS.md

**Phase 2 — Coding sessions (every subsequent session)**
- Read git log + PROGRESS.md to restore context
- Do one feature per session
- Only mark `"status": "passing"` after E2E verification
- Never delete or modify tests to make them pass

## FEATURES.json Pattern (Large Projects)

For projects with 10+ independent features, track verification state in a structured JSON file instead of a plain checklist:

```json
[
  { "id": "user-login",   "description": "User login",    "status": "passing", "verified": "2026-03-20" },
  { "id": "video-upload", "description": "Video upload",  "status": "failing", "verified": null }
]
```

Each session picks one `"failing"` item, implements and verifies it, then updates `status` to `"passing"`.

## Difference from agent-reply-trigger

If you already have the `agent-reply-trigger` plugin installed, this skill provides equivalent functionality with external configuration instead of hardcoded values.

| | agent-reply-trigger | autonomous-loop (this skill) |
|--|--------------------|-----------------------------|
| Message config | Hardcoded in index.ts | Configured in config.json |
| Log prefix | `agent-reply-trigger-` | `autonomous-loop-` |
| Stop file | `agent-reply-trigger.{id}.stop` | `autonomous-loop.{id}.stop` |

Do not enable both plugins for the same agentId — the loop will fire twice per reply.
