---
name: akievo
description: "Persistent project planning for AI agents. Create, manage, and track long-term goals using structured Kanban boards that survive session resets."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: ["AKIEVO_API_KEY"]
    primaryEnv: "AKIEVO_API_KEY"
    mcpServers:
      akievo:
        url: "https://mcp.akievo.com"
        transport: "http"
        headers:
          Authorization: "Bearer {{AKIEVO_API_KEY}}"
---

# Akievo — Agent Plan Mode

You have access to Akievo, a structured project management system. Use it as your **persistent memory and planning layer** for long-term goals. Akievo boards survive session resets — they are your source of truth.

## Core Principles

1. **Always check before creating.** At the start of every session, call `list_boards` to find existing plans before creating new ones.
2. **One board per goal.** Each major goal or project gets its own board. Prefix agent-created boards with `[Agent]` (e.g., `[Agent] Launch SaaS Product`).
3. **Lists are phases.** Use lists to represent sequential phases or categories (e.g., "Research", "Build", "Launch", "Done").
4. **Cards are tasks.** Each actionable step is a card. Include clear titles and descriptions.
5. **Respect human edits.** The human may add, remove, reprioritize, or comment on cards. Always re-read the board before acting. Never undo or override human changes.

## Session Start Pattern

Every time a new session begins:

1. Call `list_boards` to find boards prefixed with `[Agent]`
2. If a relevant board exists, call `get_board` with its ID to load the full state
3. Read the board's `project_memory` field for context (goal, timeline, assumptions)
4. Identify the next unblocked, incomplete task
5. Report status to the user: what's done, what's next, any blockers

## Creating a New Plan

When the user describes a new goal:

1. Call `list_workspaces` to find available workspaces
2. Use `create_board_with_tasks` to scaffold the entire plan in one call:
   - Break the goal into 3–6 phases (lists)
   - Each phase gets 3–8 concrete tasks (cards)
   - Add checklists for tasks with sub-steps
   - Set priorities: `critical`, `high`, `medium`, `low`
   - Set due dates when the user provides a timeline
3. Create dependencies between tasks that have a natural order using `bulk_create_dependencies`
4. Present the plan to the user and ask for feedback before proceeding

## Working on Tasks

When executing on a plan:

1. Pick the next unblocked, highest-priority incomplete card
2. Work on it (using your other tools — coding, research, writing, etc.)
3. Add progress updates as comments using `add_comment`
4. When done, call `complete_card` to mark it finished
5. If blocked, call `block_card` with a clear reason
6. Move to the next task

## Updating the Plan

As work progresses, the plan may need adjustment:

- **Add new tasks:** `create_card` in the appropriate list
- **Update details:** `update_card` to change title, description, priority, or due date
- **Reorder:** `move_card` to shift tasks between phases
- **Add sub-tasks:** `add_checklist_item` for granular steps
- **Never delete cards** without asking the user first

## Progress Reporting

When the user asks for a status update:

1. Call `get_board` to get current state
2. Count completed vs total cards per list
3. Highlight blocked items and their reasons
4. Identify upcoming due dates
5. Suggest next actions

## Important Safety Rules

- **Never delete a board** without explicit user confirmation
- **Never archive cards** without asking
- **Always re-read the board** before making changes (the human may have edited it)
- **Log your work** — add comments to cards explaining what you did and why
- **Stay scoped** — only modify boards you created or were explicitly asked to manage
