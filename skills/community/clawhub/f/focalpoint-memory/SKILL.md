---
name: focalpoint-memory
description: "FocalPoint — AI cognitive operating system. Memory + attention management + workflow orchestration. Workbench prepares context before tasks. Three-Province review ensures quality. Never lose track of projects again."
version: "0.3.4"
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

# FocalPoint — AI Cognitive Operating System

Your AI forgets everything between conversations. FocalPoint fixes that.

**Not just memory — cognitive infrastructure.** FocalPoint tracks your projects, prepares context before tasks, uses a Three-Province review system for quality decisions, and proactively alerts you about stuck work.

## The Problem

AI agents are stateless. Every conversation starts from zero — no memory of your projects, decisions, or progress. You waste time re-explaining context and manually tracking what's stuck.

Existing solutions only go halfway:

| Tool | What it does | What it doesn't do |
|------|-------------|-------------------|
| **Mem0 / Zep** | Remembers conversations | Doesn't track tasks or alert you |
| **LangGraph / CrewAI** | Orchestrates agents | No persistent cognitive layer |
| **Claude / OpenAI memory** | Remembers preferences | Doesn't manage work or deadlines |

**They remember what was said. FocalPoint manages what needs to be done.**

## What You Get

- **Structured memory** — Goal > Project > Milestone > Task hierarchy with status lifecycle
- **Workbench** — One call prepares goal, knowledge, context, subtasks, and role prompt
- **Proactive alerts** — Heartbeat detects blocked, stale, and at-risk tasks automatically
- **Knowledge documents** — Attach design docs to nodes; child tasks inherit parent knowledge
- **Role-based thinking** — Strategy, Review, and Execution roles see filtered perspectives
- **Three-Province review** — Parallel review by two reviewers before execution; max 3 rejections then escalate
- **Full-text search** — FTS5 search across titles, narratives, and knowledge documents
- **GitHub + Notion sync** — Issues and pages auto-sync as FocalPoint nodes
- **Zero dependencies** — Runs 100% locally on SQLite. No vector DB, no Redis, no cloud.

## Competitive Comparison

| Capability | Mem0 | Zep | Letta | CrewAI | Claude | **FocalPoint** |
|---|---|---|---|---|---|---|
| Persistent memory | Yes | Yes | Yes | Yes | Yes | **Yes** |
| Task lifecycle management | - | - | - | Partial | - | **Yes** |
| Dependency graph (DAG) | - | - | - | - | - | **Yes** |
| Proactive alerts | - | - | - | - | - | **Yes** |
| Knowledge docs + inheritance | - | - | - | - | Partial | **Yes** |
| Role-based context | - | - | - | Partial | - | **Yes** |
| Decision review workflow | - | - | - | - | - | **Yes** |
| Full-text search | Vector | Vector | Vector | - | - | **FTS5** |
| MCP native | - | - | - | - | Proprietary | **Yes** |
| Self-hosted, zero deps | Partial | Partial | Yes | Yes | - | **Yes** |

No competitor combines structured task management + proactive alerts + knowledge inheritance + role-based context + review workflow in a single MCP-native package.

## Setup

### 1. Install
```bash
pip install focalpoint
```

### 2. Add MCP server
```yaml
# openclaw.yaml
mcp_servers:
  fpms:
    command: focalpoint
```

### 3. Restart OpenClaw

That's it. 22 tools are now available.

## How It Works

### Architecture: Brain-Spine Model

```
Brain (LLM)              Spine (FocalPoint engine)
  |                         |
  | -- Tool Call -->        | Validate -> Write SQLite -> Narrative -> Audit
  |                         |
  | <-- Context ---         | Assemble L0/L1/L2 -> Trim -> Inject prompt
```

- **Brain** = LLM. Only reads context and issues Tool Calls.
- **Spine** = Deterministic engine. All logic here. LLM never touches storage directly.

### Storage: Pure SQLite

```
SQLite           <- Single source of truth
events.jsonl     <- Audit trail
narratives/*.md  <- Append-only logs
knowledge/{id}/  <- Design documents
```

No vector database. No Redis. No PostgreSQL. One SQLite file is everything.

## Work Mode

### Workbench — prepare before you work

```
You: "Work on the payment system task"
AI calls activate_workbench(node_id, role="execution")
-> Returns: goal, knowledge docs, context bundle, sorted subtasks,
   suggested next step, and execution role prompt
-> AI enters role, reads background, starts working
```

### Three Roles

| Role | Focus | Sees |
|------|-------|------|
| **Strategy** (Maker) | Should we do this? Priority? | Decisions + feedback |
| **Review** (Reviewer) | Any risks? Historical lessons? | Risk notes + progress |
| **Execution** (Engineer) | How to build it? Acceptance criteria? | Technical details + progress |

Same data, different thinking modes. The role prompt guides the AI's perspective.

### Three-Province Review — quality decisions

For major decisions (new features, architecture changes, tech choices):

```
Strategy produces requirements
    |
Review + Engineer review in parallel
|-- Review: checks risks, historical lessons -> approve/reject
|-- Engineer: evaluates feasibility -> approve/reject
    |
Both approve -> proceed to execution
Either rejects -> revise and resubmit
    |
> 3 rejections -> escalate to human
```

### Knowledge Documents — persistent design context

```
You: "Save this architecture doc to the project"
AI calls set_knowledge(project_id, "architecture", content)
-> Child tasks inherit parent knowledge automatically
-> AI reads project overview without you re-explaining

Types: overview | requirements | architecture | custom names
```

### Log Categories

```
append_log(node_id, content, category="decision")   # Decision records
append_log(node_id, content, category="feedback")    # User/market feedback
append_log(node_id, content, category="risk")        # Risks and lessons
append_log(node_id, content, category="technical")   # Technical details
append_log(node_id, content, category="progress")    # Progress updates
append_log(node_id, content, category="general")     # Default
```

Different roles see different categories. Strategy sees decisions + feedback. Execution sees technical + progress.

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
AI:  append_log(node_id, "Chose Stripe — better API, lower fees", category="decision")
(Two weeks later)
You: "Why did we pick Stripe?"
AI:  Searches decisions -> "You decided on March 15 — better API and lower fees."
```

### Risk detection
```
AI automatically runs heartbeat and finds:
  - Deploy task BLOCKED for 4 days
  - Docs update STALE — no activity for a week
  - Bug fix AT RISK — deadline is tomorrow
```

### Full-text search
```
You: "Find everything related to caching decisions"
AI:  search_nodes(query="caching decisions")
-> Finds nodes by title, narrative content, and knowledge docs
```

## Available Tools (22)

### Write (11)
| Tool | What it does |
|------|-------------|
| `create_node` | Create a project/task/goal/milestone |
| `update_status` | Change status (inbox/active/waiting/done/dropped) |
| `update_field` | Update title, summary, deadline, etc. |
| `attach_node` / `detach_node` | Move tasks in hierarchy |
| `add_dependency` / `remove_dependency` | Manage task dependencies |
| `append_log` | Record decisions, progress, risks (with category) |
| `unarchive` | Restore completed/dropped tasks |
| `set_persistent` | Protect tasks from auto-archive |
| `set_knowledge` | Attach knowledge documents to nodes |

### Read (5)
| Tool | What it does |
|------|-------------|
| `get_node` | Get full details of a work item |
| `search_nodes` | Find tasks by filters or full-text search |
| `get_knowledge` | Read knowledge with parent inheritance |
| `delete_knowledge` | Delete a knowledge document |
| `get_assembly_trace` | Debug context assembly |

### Cognitive (4)
| Tool | What it does |
|------|-------------|
| `bootstrap` | Load memory context (call at conversation start) |
| `heartbeat` | Scan for risks: blocked, stale, at-risk tasks |
| `activate_workbench` | Prepare working context with role + knowledge |
| `get_context_bundle` | Get role-filtered, token-budgeted context |

### Review (1)
| Tool | What it does |
|------|-------------|
| `sansei_review` | Three-Province parallel review |

### Runtime (1)
| Tool | What it does |
|------|-------------|
| `shift_focus` | Switch AI attention to a specific task |

## Automatic Memory Rules

Follow these rules in EVERY conversation:

1. **Conversation start** -> Call `bootstrap` to load memory
2. **Before starting a task** -> `activate_workbench` to prepare context
3. **User makes a decision** -> `append_log` with category="decision"
4. **Risk identified** -> `append_log` with category="risk"
5. **Task progresses** -> `update_status`
6. **Design conclusions** -> `set_knowledge` to persist for future sessions
7. **Before conversation ends** -> `append_log` key takeaways
8. **Every ~10 min** -> `heartbeat` to check for risks

## Stats

| Metric | Value |
|--------|-------|
| Tests | 665 |
| MCP Tools | 22 |
| External dependencies | 0 (pure SQLite) |
| Cold start | < 100ms |
| Supported LLMs | Any (via MCP protocol) |
| Platforms | Claude Desktop, OpenClaw, any MCP client |

## Requirements

- Python 3.10+
- No external services — runs 100% locally on SQLite

## Links

- [GitHub](https://github.com/jeff0052/founderOSclaudecode)
- [PyPI](https://pypi.org/project/focalpoint/)
