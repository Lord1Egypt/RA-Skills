---
name: task-board
description: Simple CLI task/project board (kanban)
---

# task-board

A lightweight kanban-style task board that runs entirely from the CLI.

## Usage

```bash
# Add tasks
python3 scripts/tasks.py add "Fix login bug" --priority high
python3 scripts/tasks.py add "Update docs" --priority low

# Move tasks through stages
python3 scripts/tasks.py move 3 doing
python3 scripts/tasks.py move 3 done

# List tasks
python3 scripts/tasks.py list
python3 scripts/tasks.py list --status todo

# Show kanban board
python3 scripts/tasks.py board

# Remove a task
python3 scripts/tasks.py remove 3
```

## Commands

- `add <title>` — Add a new task
- `move <id> <status>` — Move task to a status (todo, doing, done)
- `list` — List tasks (filter with `--status`)
- `board` — Show kanban board view
- `remove <id>` — Remove a task

## Options

- `--priority` — Task priority: `low`, `medium`, `high`
- `--status` — Filter by status
- `--db` — Custom database file path
