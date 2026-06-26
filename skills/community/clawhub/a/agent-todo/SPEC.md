# agent-todo Specification

## Positioning

`agent-todo` is a **local-first execution queue** for OpenClaw agents.

It is not a shared reminder board anymore. Each agent owns its queue inside its own workspace, heartbeat only consumes local work, and cross-agent routing happens explicitly through `dispatch`.

## Design Goals

1. **Install and use immediately**
   - single-workspace mode must work after install
   - no extra registry required for the default path

2. **Align heartbeat, workspace, and memory**
   - each workspace keeps its own queue
   - each agent heartbeat only consumes its own queue
   - execution context stays inside the same workspace

3. **Support multi-agent routing without heavy central config**
   - discover workspaces from `~/.openclaw/openclaw.json`
   - read each workspace's `.agent-todo/local.json` when dispatching

4. **Avoid schema drift**
   - runtime storage uses JSON instead of Markdown tables

## Runtime Layout

```text
<workspace>/
  .agent-todo/
    tasks.json
    local.json
  HEARTBEAT.md
```

### `tasks.json`

```json
{
  "version": 2,
  "tasks": [
    {
      "id": "uuid",
      "title": "Review unread notification logic",
      "status": "pending",
      "task_type": "coding",
      "source": "chat:direct",
      "next_action": "Inspect unread notification generation",
      "success_criteria": "No duplicate notifications",
      "result": "",
      "deadline": "",
      "owner_agent_id": "coding",
      "created_by_agent_id": "coding",
      "claimed_at": "",
      "last_attempt_at": "",
      "blocked_reason": "",
      "parent_id": "",
      "depends_on": [],
      "created_at": "2026-03-24T00:00:00+08:00",
      "updated_at": "2026-03-24T00:00:00+08:00",
      "completed_at": "",
      "tags": []
    }
  ]
}
```

### `local.json`

Optional self-declared identity:

```json
{
  "agent_id": "coding",
  "label": "Coding Agent"
}
```

If missing, the runtime falls back to the current workspace entry inside `openclaw.json`; if still unresolved, it uses `local`.

## Workspace Discovery

Use `~/.openclaw/openclaw.json` as the only discovery source for agent workspaces.

### Discovery flow

1. Read `agents.defaults.workspace`
2. Read `agents.list[*].workspace`
3. Deduplicate paths
4. When dispatching, inspect `<workspace>/.agent-todo/local.json`
5. Match `agent_id`

### Why this design

- no duplicate workspace registry
- no drift between OpenClaw and agent-todo
- keeps the model aligned with how OpenClaw already stores agents

## Command Model

### Local commands

- `init`
- `doctor`
- `setup-heartbeat [--write] [--all] [--dry-run]`
- `add`
- `plan`
- `list`
- `show`
- `report`
- `run-pending --claim`
- `done`
- `block`
- `unblock`
- `cancel`

### Cross-agent command

- `dispatch --to-agent <agent_id>`

`add` always writes to the current workspace. `dispatch` always writes to a discovered target workspace.

## Heartbeat Strategy

`setup-heartbeat` manages a block inside `HEARTBEAT.md`:

```md
<!-- agent-todo:begin -->
AGENT_TODO_WORKSPACE=/path/to/workspace bash ./skills/agent-todo/script.sh run-pending --claim
<!-- agent-todo:end -->
```

When the skill lives outside the target workspace, `setup-heartbeat` must bind the target workspace explicitly via `AGENT_TODO_WORKSPACE=...` so `run-pending` reads the correct local queue.

### Rules

- if the block is missing: append it
- if the block exists: update it in place
- never overwrite unrelated user content in `HEARTBEAT.md`
- `--all` applies the same append-or-update logic to every discovered workspace

## Selection Rules for `run-pending`

1. ignore `done`, `cancelled`, `blocked`
2. require all `depends_on` tasks to be done
3. prefer child tasks over standalone/parent tasks
4. prefer `running` over `pending`
5. among pending tasks, prefer earlier deadline, then earlier creation time

## Reporting

Keep source-aware reports:

- `forum:#...` → forum reply format
- `chat:...` → direct-chat reply format
- others → generic report format

## Error Handling

### Dispatch target not found

Fail fast with a clear error.

### Duplicate `agent_id`

Fail fast and show conflicting workspaces.

### Missing local identity

Allow local mode. Only dispatch requires target discovery.

## Non-Goals

- no shared global TODO file
- no central agent registry owned by agent-todo
- no whole-file overwrite of `HEARTBEAT.md`
