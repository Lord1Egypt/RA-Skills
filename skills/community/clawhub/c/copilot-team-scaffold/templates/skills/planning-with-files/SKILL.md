---
name: planning-with-files
description: Implements Manus-style file-based planning for complex tasks. Creates planning files under docs/sessions/<task-slug>/. Use when starting complex multi-step tasks, research projects, or any task requiring >5 tool calls. Now with automatic session recovery after context reset.
user-invocable: true
---

# Planning with Files

Work like Manus: Use persistent markdown files as your "working memory on disk."

## FIRST: Check for Previous Session

**Before starting work**, check for unsynced context from a previous session:

```bash
python3 .github/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"
```

If catchup report shows unsynced context:
1. Run `git diff --stat` to see actual code changes
2. Read current planning files
3. Update planning files based on catchup + git diff
4. Then proceed with task

## Important: Where Files Go

- **Default planning root:** `docs/sessions/`
- **Per-task directory:** create a dedicated subdirectory such as `docs/sessions/<task-slug>/`
- **Planning files:** store `task_plan.md`, `findings.md`, and `progress.md` inside that task subdirectory

| Location | What Goes There |
|----------|-----------------|
| Skill directory (`.github/skills/planning-with-files/`) | Templates, scripts, reference docs |
| `docs/sessions/<task-slug>/` | `task_plan.md`, `findings.md`, `progress.md` |

## Quick Start

Before ANY complex task:

1. **Create `docs/sessions/<task-slug>/`** — Use a short, stable slug
2. **Create `task_plan.md`** — Use [templates/task_plan.md](templates/task_plan.md) as reference
3. **Create `findings.md`** — Use [templates/findings.md](templates/findings.md) as reference
4. **Create `progress.md`** — Use [templates/progress.md](templates/progress.md) as reference
5. **Re-read plan before decisions** — Refreshes goals in attention window
6. **Update after each phase** — Mark complete, log errors

## The Core Pattern

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

## File Purposes

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Phases, progress, decisions | After each phase |
| `findings.md` | Research, discoveries | After ANY discovery |
| `progress.md` | Session log, test results | Throughout session |

## Critical Rules

### 1. Create Plan First
Never start a complex task without `docs/sessions/<task-slug>/task_plan.md`. Non-negotiable.

### 2. The 2-Action Rule
> "After every 2 view/browser/search operations, IMMEDIATELY save key findings to text files."

This prevents visual/multimodal information from being lost.
