---
name: "claude-code-memory"
description: "Use when you want to set up, maintain, or review a Claude Code style layered memory workflow, including `CLAUDE.md` rules, session memory, durable memory, and promotion of stable learnings into instruction files."
---

## Overview

Use this skill when the task involves memory design or memory hygiene for Claude Code or a similar coding agent.

This skill organizes memory into three layers:

1. Instruction memory
2. Session memory
3. Durable memory

The intent is to keep each layer narrow, useful, and easy to trust.

## Before you start

- Identify the host tool's instruction file. For Claude Code this is usually `CLAUDE.md` or `CLAUDE.local.md`. Other common examples are `AGENTS.md` and `.github/copilot-instructions.md`.
- Identify or create a repo-local durable memory directory. The default layout in this skill uses `.agent-memory/`.
- Identify or create the session summary file at `.agent-memory/session/summary.md`.

## Layer 1: Instruction memory

Treat the host instruction file as the rule layer. In Claude Code, this is the `CLAUDE.md` layer.

Put information here only if it is:

- stable
- normative
- broadly applicable across future work
- costly for the agent to rediscover incorrectly

Good candidates:

- test commands
- review expectations
- approval boundaries
- release process rules
- communication style preferences that consistently apply

Do not place transient task state here.

## Layer 2: Session memory

Maintain `.agent-memory/session/summary.md` as the short-lived working notebook for the current thread.

It should answer:

- What is actively being worked on now
- What did the user ask for
- Which files and functions matter
- Which commands have already been run
- Which errors happened and how they were resolved
- What remains next

This layer should be updated during long tasks and before compaction or handoff.

Use this structure:

```markdown
# Session Title

# Current State

# Task Specification

# Files and Functions

# Workflow

# Errors and Corrections

# Key Results

# Worklog
```

Keep it concise but concrete. Prefer file paths, exact commands, and specific failure modes over generic summaries.

## Layer 3: Durable memory

Use `.agent-memory/` for long-lived memories that should survive across conversations.

Store durable memories in topic files and keep `.agent-memory/MEMORY.md` as an index.

Use the following durable memory types:

### `user-profile`

Information about the user's role, goals, background, and level of familiarity.

Examples:

- backend-heavy engineer who wants frontend explanations grounded in systems concepts
- founder who prefers quick trade-off summaries

### `working-style`

Guidance about how to collaborate with this user or team.

Examples:

- run tests before proposing a commit
- avoid long recap paragraphs
- prefer one bundled refactor PR in this codebase

### `project-context`

Important project facts that are not derivable from the repo.

Examples:

- freeze window dates
- stakeholder constraints
- migration rationale
- incident aftermath that still shapes decisions

### `external-reference`

Pointers to systems outside the repo.

Examples:

- which dashboard matters for this codepath
- which Linear board tracks this class of bugs
- which Slack channel owns deployment coordination

## Durable memory format

Each durable memory should live in its own file with frontmatter:

```markdown
---
name: testing-policy
description: Integration tests in this repo must hit a real database
type: working-style
---

Integration tests in this repo must hit a real database.

Why:
A previous production migration failure was missed by mock-based coverage.

How to apply:
When changing data access or migrations, prefer real-db integration coverage over mocks.
```

The index file should stay short:

```markdown
- [Testing Policy](testing-policy.md) - Real database integration tests are expected here
```

## What not to save as durable memory

Do not save these unless there is a strong reason and the non-obvious part is the actual point:

- file structure
- code architecture visible in the repo
- git history
- recent diff summaries
- temporary task state
- obvious commands already documented in project instructions

If it can be recovered cheaply from the current repo, prefer not to save it as durable memory.

## Recall discipline

Never trust durable memory blindly.

Before acting on it:

- verify named files still exist
- grep for named functions or flags
- prefer current repo state over historical memory if they conflict
- update or remove stale memories when you discover drift

## Promotion workflow

When reviewing memory, classify each item:

- Promote to instruction memory
- Keep in durable memory
- Keep only in session memory
- Delete as stale, duplicate, or overfit

Promote into the instruction layer when the item has become a rule.
Keep it in durable memory when it remains useful context but is not a rule.
Keep it only in session memory when it is tied to the present thread.

## Review workflow

When the user asks to review memory:

1. Read the host instruction file such as `CLAUDE.md`
2. Read `.agent-memory/MEMORY.md`
3. Read the most relevant durable topic files
4. Read `.agent-memory/session/summary.md` if current-thread context matters
5. Produce a report with:
   - promotions
   - cleanup
   - conflicts
   - ambiguous items

Do not modify durable memory or instruction files without user approval unless the user explicitly asked you to apply the cleanup.

## File layout used by this skill

```text
.agent-memory/
├── MEMORY.md
├── user/
├── style/
├── project/
├── references/
└── session/
    └── summary.md
```

## References

- Architecture notes: [references/architecture.md](references/architecture.md)
- Host tool mapping: [references/host-tool-mapping.md](references/host-tool-mapping.md)
- Example durable memory files: [examples/persistent-memory/MEMORY.md](examples/persistent-memory/MEMORY.md)
- Example session summary: [examples/session-memory/summary.md](examples/session-memory/summary.md)
