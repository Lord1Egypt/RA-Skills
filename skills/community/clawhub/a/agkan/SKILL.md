---
name: agkan
description: Use when managing tasks with the agkan CLI tool - creating, listing, updating tasks, managing tags, blocking relationships, or tracking project progress with the kanban board.
---

# agkan

## Overview

`agkan` is an SQLite-based CLI task management tool. It is optimized for collaboration with AI agents.

**7 Statuses:** `icebox` → `backlog` → `ready` → `in_progress` → `review` → `done` → `closed`

---

## Quick Reference

### Agent Guide

```bash
# Display a comprehensive guide for AI agents (overview, commands, workflows)
agkan agent-guide
```

### Task Operations

```bash
# Create task
agkan task add "Title" "Body"
agkan task add "Title" --status ready --author "agent"
agkan task add "Subtask" --parent 1
agkan task add "Title" --file ./spec.md  # Read body from file
agkan task add "Title" --blocked-by 1,2  # Set tasks that block this task
agkan task add "Title" --blocks 3,4      # Set tasks that this task blocks
agkan task add "Title" --assignees "alice,bob"  # Set task assignees (comma-separated)

# List tasks
agkan task list                    # All tasks
agkan task list --status in_progress
agkan task list --tree             # Hierarchical view
agkan task list --root-only        # Root tasks only
agkan task list --tag 1,2          # Filter by tags
agkan task list --dep-tree         # Dependency (blocking) tree view
agkan task list --sort title       # Sort by field (id / title / status / created_at / updated_at), default: created_at
agkan task list --order asc        # Sort order (asc / desc), default: desc
agkan task list --assignees "alice,bob"  # Filter by assignees (comma-separated)
agkan task list --all              # Include all statuses (including done and closed)

# Get details
agkan task get <id>

# Search
agkan task find "keyword"
agkan task find "keyword" --all  # Include done/closed

# Update (positional argument form - backward compatible)
agkan task update <id> status in_progress

# Update (named option form - v1.6.0+)
agkan task update <id> --status in_progress
agkan task update <id> --title "New Title"
agkan task update <id> --body "New body text"
agkan task update <id> --author "agent"
agkan task update <id> --assignees "alice,bob"
agkan task update <id> --file ./spec.md  # Read body from file
agkan task update <id> --status done --title "Updated Title"  # Multiple options

# Count
agkan task count
agkan task count --status ready --quiet  # Output numbers only

# Update parent-child relationship
agkan task update-parent <id> <parent_id>
agkan task update-parent <id> null  # Remove parent

# Delete task
agkan task delete <id>
```

### Blocking Relationships

```bash
# task1 blocks task2 (task2 cannot be started until task1 is complete)
agkan task block add <blocker-id> <blocked-id>
agkan task block remove <blocker-id> <blocked-id>
agkan task block list <id>
```

### Tag Operations

```bash
# Tag management
agkan tag add "frontend"
agkan tag list
agkan tag delete <tag-id-or-name>
agkan tag rename <id-or-name> <new-name>

# Tag tasks
agkan tag attach <task-id> <tag-id-or-name>
agkan tag detach <task-id> <tag-id-or-name>
agkan tag show <task-id>
```

### Metadata Operations

```bash
# Set metadata
agkan task meta set <task-id> <key> <value>

# Get metadata
agkan task meta get <task-id> <key>

# List metadata
agkan task meta list <task-id>

# Delete metadata
agkan task meta delete <task-id> <key>
```

#### Priority (priority)

Task priority is managed with the `priority` key:

```bash
agkan task meta set <task-id> priority <value>
```

| Value | Meaning |
|-----|------|
| `critical` | Requires immediate attention. Blocking issue |
| `high` | Should be prioritized |
| `medium` | Normal priority (default) |
| `low` | Work on if there is time |

**When to set priority:** Priority is set during the planning phase (`agkan-planning-subtask`), at the same time the task is moved from `backlog` to `ready`. This is the responsibility of the planning skill. Skills that select tasks for execution (e.g., `agkan-run`) read this value to determine which task to work on next.

---

## Tag Priority

When selecting or tagging tasks, use the following priority order:

| Priority | Tag Name |
|----------|----------|
| 1 | bug |
| 2 | security |
| 3 | improvement |
| 4 | test |
| 5 | performance |
| 6 | refactor |
| 7 | docs |

This is the canonical definition. All skills refer to this table.

---

## JSON Output

Use the `--json` flag when machine processing is needed:

```bash
agkan task list --json
agkan task get 1 --json
agkan task count --json
agkan tag list --json

# Combine with jq
agkan task list --status ready --json | jq '.tasks[].id'
```

### JSON Output Schema

#### `agkan task list --json`

```json
{
  "totalCount": 10,
  "filters": {
    "status": "ready | null",
    "author": "string | null",
    "tagIds": [1, 2],
    "rootOnly": false
  },
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "icebox | backlog | ready | in_progress | review | done | closed",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [{ "id": 1, "name": "bug" }],
      "metadata": [{ "key": "priority", "value": "high" }]
    }
  ]
}
```

#### `agkan task get <id> --json`

```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Task Title",
    "body": "Body | null",
    "author": "string | null",
    "status": "backlog | ready | in_progress | review | done | closed",
    "parent_id": "number | null",
    "created_at": "2026-01-01T00:00:00.000Z",
    "updated_at": "2026-01-01T00:00:00.000Z"
  },
  "parent": "object | null",
  "children": [],
  "blockedBy": [{ "id": 2, "title": "..." }],
  "blocking": [{ "id": 3, "title": "..." }],
  "tags": [{ "id": 1, "name": "bug" }],
  "attachments": []
}
```

#### `agkan task count --json`

```json
{
  "counts": {
    "icebox": 0,
    "backlog": 0,
    "ready": 2,
    "in_progress": 1,
    "review": 0,
    "done": 8,
    "closed": 5
  },
  "total": 16
}
```

#### `agkan task find <keyword> --json`

```json
{
  "keyword": "Search keyword",
  "excludeDoneClosed": true,
  "totalCount": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "body": "Body | null",
      "author": "string | null",
      "status": "ready",
      "parent_id": "number | null",
      "created_at": "2026-01-01T00:00:00.000Z",
      "updated_at": "2026-01-01T00:00:00.000Z",
      "parent": "object | null",
      "tags": [],
      "metadata": []
    }
  ]
}
```

#### `agkan task block list <id> --json`

```json
{
  "task": {
    "id": 1,
    "title": "Task Title",
    "status": "ready"
  },
  "blockedBy": [{ "id": 2, "title": "...", "status": "in_progress" }],
  "blocking": [{ "id": 3, "title": "...", "status": "ready" }]
}
```

#### `agkan task meta list <id> --json`

```json
{
  "success": true,
  "data": [
    { "key": "priority", "value": "high" }
  ]
}
```

#### `agkan tag list --json`

```json
{
  "totalCount": 3,
  "tags": [
    {
      "id": 1,
      "name": "bug",
      "created_at": "2026-01-01T00:00:00.000Z",
      "taskCount": 2
    }
  ]
}
```

---

## Typical Workflows

### Icebox Review (agkan-icebox)

Icebox holds ideas and candidates that are not yet ready for planning. Review them periodically to decide whether to promote or close each one.

```bash
# Review icebox tasks
agkan task list --status icebox

# Promote to backlog when requirements become clear
agkan task update <id> status backlog

# Close if no longer needed
agkan task update <id> status closed
```

**Icebox → Backlog conditions:**
- Requirements or background are now clear enough to plan
- External blockers have been resolved
- Circumstances have changed and the task is now relevant

**Icebox → Closed conditions:**
- The need no longer exists
- A duplicate already exists in a later stage
- Superseded by another approach

### Receiving Tasks as an Agent

```bash
# Check assigned tasks
agkan task list --status ready
agkan task get <id>

# Start work
agkan task update <id> status in_progress

# Complete
agkan task update <id> status done
```

### Structuring Tasks

```bash
# Create parent task
agkan task add "Feature Implementation" --status ready

# Add subtasks
agkan task add "Design" --parent 1 --status ready
agkan task add "Implementation" --parent 1 --status backlog
agkan task add "Testing" --parent 1 --status backlog

# Set dependencies (Design → Implementation → Testing)
agkan task block add 2 3
agkan task block add 3 4

# View overall structure
agkan task list --tree
```

---

## Configuration

Place `.agkan.yml` in the project root to customize the DB path:

```yaml
path: ./.agkan/data.db
```

Or use environment variable: `AGENT_KANBAN_DB_PATH=/custom/path/data.db`