# Todo Reference

## Task Operations

### Create Task

```bash
dws todo task create --title "<title>" --executors "<userId1,userId2>" [--priority <1|2|3|4>] [--due-date "<date>"] [--description "<desc>"]
```

**Parameters:**
- `--title`: Task title (required)
- `--executors`: Comma-separated user IDs
- `--priority`: 1=Urgent, 2=High, 3=Normal, 4=Low
- `--due-date`: Due date (ISO 8601)
- `--description`: Task description

**Example:**
```bash
dws todo task create \
  --title "Review PR #123" \
  --executors "user123" \
  --priority 2 \
  --due-date "2024-04-01T18:00:00Z" \
  --yes
```

### List Tasks

```bash
dws todo task list [--status <pending|done|all>] [--limit <N>]
```

**Example:**
```bash
# Pending tasks
dws todo task list --status pending --jq '.result[] | {title: .title, due: .dueDate}'

# Count pending
dws todo task list --status pending --jq '.result | length'
```

### Get Task Detail

```bash
dws todo task get --task-id <taskId>
```

### Update Task

```bash
dws todo task update --task-id <taskId> [--title "<new-title>"] [--priority <new-priority>] [--due-date "<new-date>"]
```

### Mark as Done

```bash
dws todo task done --task-id <taskId>
```

### Delete Task

```bash
dws todo task delete --task-id <taskId>
```

## Common Patterns

### Batch Create Todos

See bundled script: `scripts/todo_batch_create.py`

```bash
# From JSON file
python scripts/todo_batch_create.py tasks.json
```

### Daily Todo Summary

See bundled script: `scripts/todo_daily_summary.py`

```bash
python scripts/todo_daily_summary.py
```

### Check Overdue Tasks

See bundled script: `scripts/todo_overdue_check.py`

```bash
python scripts/todo_overdue_check.py
```

### Create Todo for Self

```bash
# First get your userId
dws contact user get-self --jq '.result[0].userId'

# Then create todo
dws todo task create --title "Finish report" --executors "<your-userId>" --yes
```

### Assign Todo to Team

```bash
# Get department members
dws contact dept members --dept-id "dept123" --jq '.result[] | .userId' | tr '\n' ','

# Create with all members
dws todo task create --title "Team task" --executors "user1,user2,user3" --yes
```
