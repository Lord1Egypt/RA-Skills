# Feishu Task Workbench Implementation

## Goal

Mirror the stable Weixin task-workbench interaction model for Feishu via `openclaw-lark`, while keeping task registries isolated per channel.

## Required runtime behavior

The Feishu version must match the Weixin version on these points:

- treat task commands as a first-class workbench protocol
- use `sessions_spawn` to create one dedicated session per task
- use `sessions_send` to continue the active task session
- use `sessions_history` to summarize task progress when needed
- use `scripts/task_registry.py` as the single source of truth for persisted task state
- keep Feishu and Weixin registries fully separate

## Capability gate

Do this on the first task command in a session:

1. confirm `sessions_spawn` is available
2. confirm `sessions_send` is available
3. confirm `sessions_history` is available

If any are missing:

- stop immediately
- do not create or mutate the registry
- explain that the host is missing required cross-session capabilities
- point to `tools.allow`, `tools.agentToAgent.enabled=true`, and `tools.sessions.visibility=all`

Do not degrade silently into registry-only mode.

## Registry layout

Use per-account per-peer isolation:

```text
tasks/feishu/<account>/<peer>.json
```

Examples:

```text
tasks/feishu/main/ou_xxx.json
```

Feishu and Weixin must never share the same root path.

## Quick start

Initialize:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json init
```

Create a task after `sessions_spawn` returns a session key:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json add "周报" --session-key <sessionKey> --make-current
```

List tasks:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json list
```

Switch task:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json switch 2
```

Show current task:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json show
```

Update task summary/status:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json update 2 --status in_progress --summary "已完成结构设计"
```

Close/archive:

```bash
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json close 2 --summary "终稿已确认"
python3 scripts/task_registry.py --registry tasks/feishu/<account>/<peer>.json archive 2 --summary "已归档备查"
```

## Canonical workflow

### Create task

1. user sends `新建任务：<title>`
2. call `sessions_spawn`
3. persist the task with `add --session-key ... --make-current`
4. reply with task id and current task

### List tasks

1. call `list`
2. render compact task list
3. mark current task

### Switch task

1. call `switch <id>`
2. confirm switch
3. later plain-text messages route to the new current task

### Continue task

1. call `show`
2. route the user message with `sessions_send`
3. when helpful, update status to `in_progress`
4. reply with a task header

### Summarize task

1. call `summarize <id>`
2. optionally pull recent task context with `sessions_history`
3. reply in the format: progress / output / blockers / next step
4. optionally write back a refreshed summary

### Close or archive task

1. call `close` or `archive`
2. preserve history and summary
3. if the current task closes, let the registry pick the next active task or clear `currentTaskId`

### Task status

When the user sends `任务状态`:

1. call `show`
2. call `list`
3. report current task id, title, status
4. include `sessionKey` and registry path only for debugging

## Response rules

For any reply that belongs to a concrete task, prepend:

```text
[任务:#2 周报]
```

Keep user-facing responses short and operational.

## Acceptance standard

Treat the Feishu skill as fixed only if all of these hold:

1. `任务列表` is recognized as workbench control flow
2. `新建任务：周报` creates a dedicated task session plus registry entry
3. `切到 #<id>` changes the default routing target
4. plain-text follow-up goes to the current task via `sessions_send`
5. `总结 #<id>` can use `sessions_history`
6. Feishu writes under `tasks/feishu/...`
7. Weixin writes under `tasks/weixin/...`
8. the two channels do not share registry files
