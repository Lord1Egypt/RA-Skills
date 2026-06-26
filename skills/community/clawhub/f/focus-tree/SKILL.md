---
name: focus-tree
description: Maintain persistent focus on active work with hierarchical task tracking. Prevents the agent from forgetting mid-project context, drifting between topics, or asking "what were we doing?" after compaction. Extracts decisions, TODOs, constraints, blockers, and sub-agents into tree structure.
homepage: https://github.com/openclaw/focus-tree
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":["node"]}}}
---

# Focus Tree

Session content focus tree with checklist tracking. Extracts decisions, TODOs, constraints, and context into a single-root hierarchical structure for better conversation alignment and task management.

## Core Principles

1. **Alignment** — Maintain synchronized understanding between agent and user. The FOCUS.md serves as a shared source of truth that both parties can reference.

2. **Focus** — Keep the agent anchored to the current task. Prevents drifting between topics or losing track after session compactions.

3. **Planning** — Enable structured, step-by-step task execution. Break down complex work into manageable hierarchical sub-tasks with clear progress tracking.

## When to Read FOCUS.md

- **Every session start** (before responding to first message)
- **After every compaction** (if context feels thin, read it)
- **When the user asks about current work** ("what are we doing?", "where were we?")

## When to Write/Update FOCUS.md

Agents update FOCUS.md directly using file tools when:

| Trigger | Action | Example |
|---------|--------|---------|
| **user_request** | User says "start new project" | Write new FOCUS.md with Focus Point and TODOs |
| **task_complete** | User says "task done" | Edit TODO line: `☐` → `✅` |
| **priority_shift** | User changes priorities | Edit Focus Point line |
| **new_project** | Starting new focused project | Write new FOCUS.md, archive old if exists |
| **heartbeat** | Heartbeat check reveals blockers | Edit Status line, add Blockers section |

**Additional actions:**
- **When work is DONE** — append to `FOCUS-LOG.md` and clear/write new FOCUS.md
- **Before compaction memory flushes** — ensure FOCUS.md reflects current state

## Rules

1. **One focus at a time.** If the user pivots, archive the old focus first.
2. **Keep it short.** FOCUS.md should be <50 lines. It's a resume point, not a journal.
3. **📖 Context is sacred.** Always update it before stopping work. Future-you reads this first.
4. **Don't duplicate memory files.** FOCUS.md tracks *what we're doing now*. Daily memory files track *what happened*. Different jobs.
5. **Archive when done.** Append completed focuses to `FOCUS-LOG.md` with completion date and outcome, then clear FOCUS.md.
6. **Read it, don't ask.** If FOCUS.md exists, read it and resume. Don't ask "what were we working on?" when the answer is in the file.

## File Roles

Focus Tree uses three distinct files for different purposes:

| File | Purpose | When to Update |
|------|---------|----------------|
| **FOCUS.md** | **Current work state** — What we're doing NOW | Every task change, status change, or context shift |
| **FOCUS-LOG.md** | **Completed work history** — Archive of finished focuses | Only when archiving a completed/blocked focus |
| **MEMORY.md** | **Long-term curated memory** — Important insights, lessons, preferences | Periodically distill from daily notes |

**Key principle:** FOCUS.md tracks *what we're doing now*. Daily memory files track *what happened*. FOCUS-LOG tracks *what we finished*. Different jobs.

## FOCUS.md Structure

Focus Tree uses a hierarchical tree structure. Here's the complete format:

```markdown
# FOCUS.md - Current Focus

🎯 **Focus Point**: [Task Name]

**Started:** [Date]
**Status:** [active/paused/blocked]

📝 TODOs
☐ [Task 1]
☐ [Task 2]

📖 Context
[Current context/notes]
🚧 [Blocker if any]
```

### Tree View

Hierarchical structure showing nesting levels:

```
🎯 Focus Point (Root)
├── 📌 Decisions
├── 📝 TODOs (max 2 levels)
│   ├── ✅ Level 1 task
│   │   ├── Level 2 sub-task (no icon)
│   │   └── Level 2 sub-task
│   └── ⏳ Level 1 task
├── ⚠️ Constraints
├── 🤖 Sub-Agents
└── 📖 Context
    └── 🚧 Blockers
```

### Field Reference

| Field | Prefix | Required | Description |
|-------|--------|----------|-------------|
| **Focus Point** | `🎯` | ✅ Yes | Root task name |
| **TODOs** | `☐/⏳/✅` | ✅ Yes | Task checklist |
| **Context** | `📖` | ✅ Yes | Active state + blockers |
| Decisions | `📌` | ❌ No | Key decisions made |
| Constraints | `⚠️` | ❌ No | Limitations/requirements |
| Sub-Agents | `🤖` | ❌ No | Spawned agents status |
| Started | - | ❌ No | Start date |
| Status | - | ❌ No | active/paused/blocked |

## Usage

Focus Tree operates on `FOCUS.md` and `FOCUS-LOG.md` directly.

### Option 1: CLI Script (recommended)

```bash
node scripts/focus.mjs init "Project Name"    # Initialize
node scripts/focus.mjs add-todo "Task"        # Add task
node scripts/focus.mjs done 1                 # Mark done
node scripts/focus.mjs status active          # Update status
node scripts/focus.mjs archive "Outcome"      # Archive
```

### Option 2: Direct File Operations

```bash
read /path/to/workspace/FOCUS.md
edit /path/to/workspace/FOCUS.md
  old: "☐ Incomplete task"
  new: "✅ Completed task"
```

## Context Section Details

The 📖 **Context** section serves as the "Active State" — it's the resume point after compaction.

**What to include:**
- What was the last thing done
- What's the next action
- Any blockers or waiting

Always update Context before stopping work. Future-you will read this first.

## Content Parsing

When editing FOCUS.md, agents should use these section prefixes:

| Section | Prefix | Example | Placement |
|---------|--------|---------|-----------|
| Decisions | `📌` | `📌 Decided to use Node.js` | Optional section after TODOs |
| TODOs | `☐/⏳/✅` | `☐ Implement feature` | Required section |
| Constraints | `⚠️` | `⚠️ Must use TypeScript` | Optional section after TODOs |
| Blockers | `🚧` | `🚧 Waiting for API key` | Inside 📖 Context section |
| Context | `📖` | `📖 Current status...` | Required section (last) |
| Sub-Agents | `🤖` | `🤖 label — task — status` | Optional section before Context |

## Display Format

- **TODOs Level 1**: Icon prefix
  - `✅` = completed
  - `⏳` = in progress
  - `☐` = pending
- **TODOs Level 2**: Plain list, no icon prefix
- **Decisions**: prefix `📌`
- **Constraints**: prefix `⚠️`
- **Context**: prefix `📖`

## FOCUS-LOG.md Format

Append-only log of completed focuses:

```markdown
# Focus Log

## [Project Name] — COMPLETED YYYY-MM-DD
**Duration:** X hours/days
**Outcome:** One-line result

## [Project Name] — ARCHIVED YYYY-MM-DD
**Duration:** X hours/days
**Outcome:** Partial completion note
**Status:** incomplete
```

## Integration with AGENTS.md

Add to your session-start routine, after reading SOUL.md and USER.md:

- Read `FOCUS.md` if it exists → resume work or acknowledge status
- If no `FOCUS.md` exists → check `MEMORY.md` for recent context
- Proceed with current focus or start new

## Integration with HEARTBEAT.md

Focus Tree provides dedicated heartbeat integration:

**Heartbeat triggers:**
- Check current FOCUS.md status
- Detect blockers → edit 📖 Context section, add `🚧 [blocker description]`
- Update Status line if needed

**HEARTBEAT.md format:**
```markdown
# HEARTBEAT.md

Focus Tree Trigger-based Updates

## Trigger Conditions
1. **User request** — User explicitly says "start new task"
2. **Heartbeat check** — Check FOCUS.md status, update Blockers

## Execution Flow
1. Read FOCUS.md
2. Detect task status (if blocked, edit FOCUS.md to add Blockers)
3. Write/Edit FOCUS.md as needed

## No Auto-extraction
- Do not auto-extract tasks from conversation
- Only update on explicit trigger conditions
```
