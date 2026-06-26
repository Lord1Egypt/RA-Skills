---
name: discord-task-tracker
description: "Track tasks in Discord using natural language. Add, list, complete, and delete tasks via chat commands. Triggers: add task, track task, todo, my tasks, task list, complete task, delete task, task done"
---

# Discord Task Tracker

Track your tasks directly from Discord with natural language commands.

## Commands

| Command | Description |
|---------|-------------|
| `add task <description>` | Add a new task |
| `list tasks` / `my tasks` / `task list` | Show all tasks |
| `complete task <task number>` | Mark a task as done |
| `delete task <task number>` | Remove a task |

## Examples

```
add task Finish the Discord bot integration
list tasks
complete task 1
delete task 2
```

## How It Works

- Tasks are stored in `tasks.json` in the skill directory
- Task numbers are assigned sequentially; use `list tasks` to see current numbers
- Completed tasks are removed from the list
- All task operations reply directly in the Discord channel
