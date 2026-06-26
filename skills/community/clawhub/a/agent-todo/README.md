# agent-todo

> **Local-first execution queue for OpenClaw agents.**
> Each agent keeps its own queue inside its own workspace, claims work during heartbeat, and can dispatch tasks to another agent when needed.

- ClawHub: https://clawhub.com/skills/agent-todo
- 中文说明: [README.zh-CN.md](./README.zh-CN.md)

## What it solves

Chat is good at promises and bad at follow-through.

`agent-todo` turns “I’ll do this later” into executable work:

- each workspace owns its own queue
- heartbeat picks the next task and claims it
- finished work can be reported back to the original source
- tasks can be dispatched across agents discovered from OpenClaw config

## Storage model

Runtime data lives inside the workspace:

```text
<workspace>/
  .agent-todo/
    tasks.json
    local.json   # optional
```

- `tasks.json`: the local execution queue
- `local.json`: optional self-declared identity, e.g. `{"agent_id":"coding","label":"Coding Agent"}`
- workspace discovery source: `~/.openclaw/openclaw.json`

## Quick Start

### Install

```bash
clawhub install agent-todo
cd ~/.openclaw/workspace/skills/agent-todo
chmod +x script.sh todo.sh hooks/*.sh tests/smoke.sh
```

### Initialize local queue

```bash
bash ./script.sh init
```

### Check current status

```bash
bash ./script.sh doctor
```

### Wire heartbeat for current workspace

```bash
bash ./script.sh setup-heartbeat --write
```

### Wire heartbeat for all discovered workspaces

```bash
bash ./script.sh setup-heartbeat --all --write
```

This uses a managed block in `HEARTBEAT.md` and updates that block in place instead of overwriting the whole file. The generated command binds the target workspace explicitly with `AGENT_TODO_WORKSPACE=...`, so shared/external skill installs still read the correct local queue.

### Add a task for the current agent

```bash
bash ./script.sh add "Publish release" \
  --task-type publish \
  --source "forum:#19/reply:88" \
  --next-action "Push GitHub and publish ClawHub" \
  --success-criteria "GitHub and ClawHub updated"
```

### Split a composite goal into steps

```bash
bash ./script.sh plan "Open-source release" \
  --task-type publish \
  --source "chat:direct" \
  --steps "Update README; Push GitHub; Publish ClawHub"
```

### Dispatch a task to another agent

```bash
bash ./script.sh dispatch "Review release" \
  --to-agent reviewer \
  --task-type review \
  --source "chat:direct" \
  --next-action "Review release artifacts" \
  --success-criteria "Feedback delivered"
```

`dispatch` scans workspaces from `~/.openclaw/openclaw.json`, reads each workspace's `.agent-todo/local.json`, and writes the task into the matching target workspace.

### Let heartbeat pick work

```bash
bash ./script.sh run-pending --claim
```

If a task exists, the command prints an `EXECUTE_NOW` brief. If there is no runnable task, it prints `HEARTBEAT_OK`.

### Update task state

```bash
bash ./script.sh block <id> --reason "Need review"
bash ./script.sh done <id> --note "Work completed"
bash ./script.sh report <id>
bash ./script.sh cancel <id> --reason "Handled elsewhere"
```

## Core commands

```bash
bash ./script.sh init
bash ./script.sh doctor
bash ./script.sh setup-heartbeat --write
bash ./script.sh setup-heartbeat --all --write
bash ./script.sh add "Refine release plan" --task-type doc --next-action "Update README and SKILL.md"
bash ./script.sh dispatch "Review release" --to-agent reviewer --task-type review --next-action "Review artifacts"
bash ./script.sh plan "Release" --task-type publish --steps "Update README; Push GitHub; Publish ClawHub"
bash ./script.sh list --status pending
bash ./script.sh show <id>
bash ./script.sh run-pending --claim
bash ./script.sh block <id> --reason "Waiting for review"
bash ./script.sh done <id> --note "README updated and pushed"
bash ./script.sh report <id>
bash ./script.sh cancel <id> --reason "No longer needed"
bash ./script.sh agents list
```

## Statuses

| Status | Meaning |
|---|---|
| pending | queued, not started |
| running | currently being worked on |
| blocked | cannot continue without input or dependency |
| done | completed |
| cancelled | intentionally dropped |

## Testing

```bash
bash tests/smoke.sh
```

## License

MIT License
nse
nse
