---
name: fpms-memory
description: "Cognitive memory engine — gives your AI persistent work tracking, proactive risk alerts, and cross-conversation continuity. Never lose track of projects again."
version: "0.2.0"
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://github.com/jeff0052/founderOSclaudecode"
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: focalpoint
        bins: [focalpoint]
---

# FPMS — Focal Point Memory System

Your AI forgets everything between conversations. FPMS fixes that.

**Not just memory — attention management.** FPMS tracks your projects, detects stuck tasks, and loads the right context at the right time.

## What You Get

- **Cross-conversation memory** — Start Monday, continue Wednesday, review Friday
- **Structured work tracking** — Projects → Tasks → Subtasks with status lifecycle
- **Proactive alerts** — "Task X has been blocked for 3 days"
- **Smart context loading** — Only loads what fits your token budget
- **GitHub sync** — Issues auto-sync as FPMS nodes

## How It's Different From Other Memory Tools

| | Mem0/Zep | **FPMS** |
|--|---------|----------|
| Remembers conversations | Yes | Yes (via prompt rules) |
| Tracks tasks & projects | No | **Yes** |
| Alerts you about stuck work | No | **Yes (heartbeat)** |
| Manages token budget | No | **Yes (L0/L1/L2)** |
| Parent-child task hierarchy | No | **Yes** |
| GitHub integration | No | **Yes** |

**Other tools remember what was said. FPMS manages what needs to be done.**

## Setup

### 1. Install
```bash
pip install focalpoint
```

### 2. Add MCP server to openclaw.yaml
```yaml
mcp_servers:
  fpms:
    command: focalpoint
```

### 3. Restart OpenClaw

That's it. 18 tools are now available in your conversations.

## Use Cases

### Project tracking
```
You: "Create a project for the product launch with 3 tasks"
(Next day)
You: "What's the launch status?"
AI:  "3 tasks: 1 done, 1 active, 1 blocked. The blocked task
      is waiting on design review — it's been 2 days."
```

### Decision memory
```
You: "We're going with Stripe for payments"
(Two weeks later)
You: "Why did we pick Stripe?"
AI:  "You decided on March 15 — better API and lower international fees."
```

### Risk detection
```
AI automatically runs heartbeat and finds:
  - Deploy task BLOCKED for 4 days
  - Docs update STALE — no activity for a week
  - Bug fix AT RISK — deadline is tomorrow
```

## Available Tools (18)

| Tool | What it does |
|------|-------------|
| `bootstrap` | Load memory context (call at conversation start) |
| `heartbeat` | Scan for risks: blocked, stale, at-risk tasks |
| `create_node` | Create a project/task/goal |
| `update_status` | Change status (inbox/active/waiting/done/dropped) |
| `append_log` | Record decisions, progress, links |
| `get_context_bundle` | Get token-budgeted context payload |
| `search_nodes` | Find tasks by status, parent, source |
| `get_node` | Get full details of a work item |
| `shift_focus` | Switch AI attention to a specific task |
| `expand_context` | See parent, children, dependencies |
| `update_field` | Update title, summary, deadline, etc. |
| `attach_node` / `detach_node` | Move tasks in hierarchy |
| `add_dependency` / `remove_dependency` | Manage task dependencies |
| `unarchive` | Restore completed/dropped tasks |
| `set_persistent` | Protect tasks from auto-archive |
| `get_assembly_trace` | Debug context assembly |

## Automatic Memory Rules

Follow these rules in EVERY conversation:

1. **Conversation start** → Call `bootstrap` to load memory
2. **User mentions a task/project/goal** → `create_node`
3. **User makes a decision** → `append_log` to the relevant node
4. **Task progresses** → `update_status`
5. **Before conversation ends** → `append_log` key takeaways
6. **Every ~10 min** → `heartbeat` to check for risks

## Requirements

- Python 3.10+
- No external services — runs 100% locally on SQLite

## Links

- [GitHub](https://github.com/jeff0052/founderOSclaudecode)
- [PyPI](https://pypi.org/project/fpms/)
- [Full Documentation](https://github.com/jeff0052/founderOSclaudecode/blob/main/docs/USAGE-GUIDE.md)
