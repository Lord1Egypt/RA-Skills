---
name: flow-pms
description: Interact with FlowDeck Project Management API (projects, cycles, tasks). Use for CRUD + archive/unarchive operations via the FlowDeck REST API through Supabase Edge Functions. Trigger when user asks about project status, cycle progress, task management, or implementing work from a Flow task.
---

# FlowDeck Project Management API

Interact with the FlowDeck project management module via the REST API gateway
(base URL: `https://<supabase_url>/functions/v1/api-gateway`).

## Usage

Run the script using the absolute path (do NOT cd to the skill directory):

```bash
uv run ~/.codex/skills/flow-pms/scripts/flow_api.py <action> <resource> [options]
```

**Important:** Always run from the user's current working directory so any output files are saved where the user is working.

## Actions

| Action       | Description                     | Example                                                       |
|-------------|---------------------------------|---------------------------------------------------------------|
| `list`      | List resources (paginated)      | `uv run ... list projects --limit 50`                         |
| `get`       | Get single resource             | `uv run ... get projects --id <uuid>`                         |
| `create`    | Create resource                 | `uv run ... create projects --data '{"name":"X","prefix":"X"}'` |
| `update`    | Update resource                 | `uv run ... update tasks --id <uuid> --data '{"status":"done"}'` |
| `delete`    | Delete resource                 | `uv run ... delete tasks --id <uuid>`                         |
| `archive`   | Archive project                 | `uv run ... archive projects --id <uuid>`                     |
| `unarchive` | Unarchive project (to on_hold)  | `uv run ... unarchive projects --id <uuid>`                   |

## PMS Resources

| Resource     | Endpoint                                | Notes                      |
|-------------|-----------------------------------------|----------------------------|
| `projects` | `/projects`                              | Project management         |
| `cycles`   | `/projects/{projectId}/cycles`           | Sprints, scoped to project |
| `tasks`    | `/projects/{projectId}/tasks`            | Tasks, scoped to project   |
| `comments` | `/tasks/{taskId}/comments`               | Comments on tasks          |

## Filters for `list`

- `--limit N` (default 50, max 200)
- `--offset N` (default 0)
- `--status` — filter by status enum
- `--priority` — filter task priority (tasks)
- `--cycle-id` — filter tasks by cycle
- `--assignee-id` — filter tasks by assignee
- `--project-id` — parent project ID for scoped resources (cycles, tasks, comments)

## Status/Stage/Priority Enums

### Projects
`briefing`, `planning`, `in_progress`, `review`, `completed`, `post_launch`, `on_hold`, `continuous_support`, `archived`

### Cycles
`draft`, `active`, `completed`, `cancelled`

### Tasks (status)
`backlog` -> `todo` -> `in_progress` -> `in_review` -> `done` / `cancelled`

### Tasks (priority)
`none`, `low`, `medium`, `high`, `urgent`

### Tasks (type)
`feature`, `bug`, `improvement`, `task`

## Core workflows

### Project status update

For prompts like `Me atualize sobre o status do projeto X no flow`:

1. `list projects` to resolve project by name
2. `get projects --id <uuid>` for full details
3. `list cycles --project-id <uuid>` to find active cycle (prefer `status=active`, fallback to latest)
4. `list tasks --project-id <uuid>` to get tasks
5. Summarize: project status, deadline, active cycle progress, task counts by status/priority, risk signals (urgent open tasks, blocked high-priority items)

### Current cycle status

1. Resolve project
2. `list cycles --project-id <uuid>`
3. Pick cycle with `status=active`; mention if none exists
4. `list tasks --project-id <uuid> --cycle-id <uuid>` for task-level detail
5. Report: progress, scope, completed_scope, dates, deadline risk signals

### Create a task

1. Resolve the target project
2. Determine status and cycle from the project's active cycle
3. Include optional fields only when the user specified them or when you need one clarification

**Required fields for project create:** `name`, `prefix`

**Required fields for task create:** only `title` by API, but you MUST at minimum also:
- Resolve the project (ask if missing)
- Check for an active cycle and default `cycle_id` to it
- Check for an assignee

### Implement what is in a task

1. Resolve the project
2. Resolve the task by identifier (e.g. `PRJ-42`) or title
3. Fetch the full task
4. Summarize scope from title, description, type, priority, due date, cycle
5. Use the task content as the implementation brief
6. If code changes are made outside Flow, suggest or perform a task status update afterward

## Mutation safety

Ask for confirmation before:
- Deleting projects, cycles, or tasks
- Broad updates when the target match is ambiguous

Do not ask when the user already clearly requested the destructive action and the target is unambiguous.

## API Key

The script checks for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `FLOWBOARD_API_KEY` environment variable

If neither is available, the script exits with an error message.

## API Key + Base URL Environment Variables

- `FLOWBOARD_API_KEY` — Bearer API key
- `FLOWBOARD_BASE_URL` — API base URL (default: `https://mycivgjuujlnyoycuwrz.supabase.co/functions/v1/api-gateway`)

## Preflight + Common Failures

- Preflight:
  - `command -v uv` (must exist)
  - `test -n "$FLOWBOARD_API_KEY"` (or pass `--api-key`)
- Common failures:
  - `Error: No API key provided.` -> set `FLOWBOARD_API_KEY` or pass `--api-key`
  - `HTTP 401` -> invalid/revoked key
  - `HTTP 404` -> resource not found or doesn't belong to workspace
  - `"quota/permission/403"` -> wrong key, no access, or quota exceeded

## Examples

**List projects in progress:**
```bash
uv run ~/.codex/skills/flow-pms/scripts/flow_api.py list projects --status in_progress --limit 20
```

**Create a task in a project:**
```bash
uv run ~/.codex/skills/flow-pms/scripts/flow_api.py create tasks \
  --project-id <uuid> \
  --data '{"title":"Implementar login social","priority":"high","type":"feature"}'
```

**Move task to in_progress:**
```bash
uv run ~/.codex/skills/flow-pms/scripts/flow_api.py update tasks \
  --id <uuid> --data '{"status":"in_progress"}'
```

**Archive a project:**
```bash
uv run ~/.codex/skills/flow-pms/scripts/flow_api.py archive projects --id <uuid>
```
