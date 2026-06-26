# Command Reference — Discord Task Tracker

## Syntax

All commands are natural language phrases. Run via:

```
uv run python scripts/task_manager.py "<command>"
```

## Commands

### Add a task
```
add task <description>
track task <description>
todo <description>
```
**Example:** `add task Finish the Discord integration`

### List all tasks
```
list tasks
my tasks
task list
```
Shows numbered task list with status indicators:
- ⬜ = pending
- ✅ = completed (auto-removed after completion)

### Complete a task
```
complete task <number>
task done <number>
done <number>
```
**Example:** `complete task 1`

### Delete a task
```
delete task <number>
```
**Example:** `delete task 2`

## Task Storage

- File: `tasks.json` in the skill directory
- Format: JSON array of `{"id": N, "text": "...", "done": bool}` objects
- Task IDs are sequential and may shift after deletions/completions

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (task not found, unknown command) |
