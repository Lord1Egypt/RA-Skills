# SETUP.md

## Install CEO小茂 Agent

### Install only the coordinator framework

```bash
clawhub install ceo-xiaomao-agent
```

### Install the companion capability bundle too

```bash
clawhub install ceo-xiaomao-agent
clawhub install ceo-xiaomao
```

## Initialize workspace

Go to the target directory, then run:

```bash
python3 scripts/init_agent_workspace.py
```

This creates:
- `SOUL.md`
- `USER.md`
- `MEMORY.md`
- `AGENTS.md`
- `IDENTITY.md`
- `tasks/`
- `docs/`
- `leads/`
- `crm/`
- `attachments/`
- `memory/`

## Edit these files first

### `USER.md`
Fill boss identity and timezone.

### `MEMORY.md`
Fill current business, current projects, current priorities.

### `IDENTITY.md`
Confirm CEO小茂 identity.

### `AGENTS.md`
Confirm startup reading order and role boundaries.

## What CEO小茂 can do

- coordinate team work
- assign tasks
- track progress
- summarize outcomes
- report to the boss in management language

## What CEO小茂 should not do

- personally replace prospecting specialist
- personally replace outreach specialist
- personally replace copywriting specialist

## Recommended next step

If you want execution capabilities too, install:

```bash
clawhub install ceo-xiaomao
```
