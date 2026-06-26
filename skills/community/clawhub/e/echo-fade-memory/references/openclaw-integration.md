# OpenClaw Integration

This package supports OpenClaw in the same spirit as the reference skills, but the durable memory backend is `echo-fade-memory`.

## Goal

Use OpenClaw workspace context plus `echo-fade-memory` for:

- persistent recall across sessions
- decision / preference capture
- reminders to store learnings and errors as memories

## Install the Skill Source

From a source checkout, copy this skill into your OpenClaw skills directory:

```bash
cp -r ./skill/echo-fade-memory ~/.openclaw/skills/echo-fade-memory
```

## Install the Hook Source

From a source checkout, copy the OpenClaw hook:

```bash
cp -r ./skill/echo-fade-memory/hooks/openclaw ~/.openclaw/hooks/echo-fade-memory
```

Enable it:

```bash
openclaw hooks enable echo-fade-memory
```

## What the Hook Injects

On `agent:bootstrap`, the hook injects a short reminder telling the agent to:

1. recall before answering
2. store durable preferences / decisions / corrections
3. reinforce reused memories
4. ground fuzzy memories before trusting them

## Runtime Assumption

The hook defaults to:

```bash
http://127.0.0.1:8080
```

In containerized OpenClaw environments, this may be unreachable. In that case, use:

```bash
export EFM_BASE_URL=http://host.docker.internal:8080
```

You can adapt the reminder or your environment to a different URL via `EFM_BASE_URL`.

## Suggested OpenClaw Workflow

### On session start

- Read your usual workspace files
- Recall relevant project memory with a focused query
- Ground anything that looks uncertain

### During work

- Store user preferences immediately
- Store project decisions immediately
- Store debugging lessons that may recur

### During errors

- Treat important failures as memory-worthy if they reveal a project-specific workaround
- Prefer storing a concise fix rather than the full raw log

## Recommended Memory Shapes

| OpenClaw event | Store as |
|----------------|----------|
| User preference | `memory_type=preference`, `importance>=0.9` |
| Project decision | `memory_type=project`, optional `conflict_group` |
| Missing capability | `memory_type=goal`, summary starts with `feature-request:` |
| Debugging lesson | `memory_type=project`, summary starts with `error:` or `learning:` |

## Example

```text
User: "We switched to chromem because we wanted the embedded vector store to stay lightweight and easy to run."

Agent (internal):
1. Store project decision memory
2. Continue task

Later:
User: "Why did we switch to chromem?"

Agent (internal):
1. Recall memory
2. Ground if needed
3. Answer
4. Reinforce the memory
```

## Verification

Check the hook is installed:

```bash
openclaw hooks list
```

Check the skill is visible:

```bash
openclaw status
```

Check the memory service:

```bash
~/.openclaw/skills/echo-fade-memory/scripts/health-check.sh
```
