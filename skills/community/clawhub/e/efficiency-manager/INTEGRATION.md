# Efficiency Manager Integration

## Overview

This document explains how `efficiency-manager` integrates into agent workflows today and how that integration should evolve.

Current reality:
- OpenClaw does not register this skill as a first-class native tool
- integration happens through wrapper scripts and CLI commands

Updated product direction:
- move from local time tracking toward local execution coaching
- keep the current wrapper path, but make the outputs more decision-oriented over time

## Integration Model Today

Current integration pattern:
- agent calls a local script through `exec`
- script returns JSON or formatted text
- agent interprets results and produces the final recommendation

Current file layout:

```text
~/.openclaw/skills/efficiency-manager/
├── scripts/
│   ├── api-wrapper.js
│   ├── efficiency-api
│   └── cli.js
├── lib/
│   ├── storage.js
│   ├── analyzer.js
│   ├── reporter.js
│   └── scheduler.js
├── references/
│   ├── api.md
│   ├── scoring.md
│   ├── scheduling.md
│   ├── data-model.md
│   └── benchmarks.json
├── SKILL.md
└── INTEGRATION.md
```

## Current Public Command Surface

Wrapper commands intended for structured use:
- `add`
- `report`
- `list`

CLI commands available locally:
- `add`
- `start`
- `end`
- `report`
- `analyze`
- `plan`
- `list`
- `delete`
- `config`

## Product Mode Mapping

The updated skill positioning is based on five product modes:
- `log`
- `review`
- `suggest-next`
- `plan-day`
- `weekly-review`

How they map today:

| Product mode | Current support | Integration note |
|---|---|---|
| `log` | `add`, `start`, `end` | stable today |
| `review` | `report` | stable today |
| `suggest-next` | no dedicated command | derive in agent layer |
| `plan-day` | `plan` | lightweight only |
| `weekly-review` | weekly `report` | agent should add behavioral synthesis |

Important:
- do not claim that `suggest-next` already exists as a concrete command
- do not describe `plan` as full optimization

## Recommended Agent Usage

### 1. Capture work

Use:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api add \
  -d "写代码" -c work --from 09:00 --to 11:00
```

Use when:
- the user wants to log completed work
- the agent needs to store a clean historical record

### 2. Review time use

Use:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api report -t today
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api report -t week
```

Use when:
- the user asks for a daily, weekly, or monthly review
- the agent needs structured data for a summary

### 3. Inspect raw history

Use:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api list --date 2026-04-02
```

Use when:
- validating storage output
- checking data quality
- debugging unusual report results

### 4. Build a lightweight plan

Use:

```bash
cd ~/.openclaw/skills/efficiency-manager
node scripts/cli.js plan "写代码2h" "开会1h"
```

Use when:
- the user wants a quick ordering of tasks
- exact optimization is not required

Do not overclaim:
- this is not yet a constraint-aware scheduler

## JSON and Parsing Guidance

For wrapper actions:
- prefer structured JSON fields when available
- use `formatted` fields only for display

Agent behavior should prefer:
1. parse the returned JSON
2. extract summary, category breakdown, and suggestions
3. produce a user-facing decision or recommendation

## Shared Storage Rule

All agents should use the same local store:
- `~/.openclaw/efficiency-manager/data/events.json`
- `~/.openclaw/efficiency-manager/config.json`

Do not create:
- per-agent copies
- per-thread copies
- alternate stores for the same history

If an agent updates efficiency history, it should update the shared store instead of keeping the record only in session memory.

## Current Limitations

1. No first-class native tool registration
- integration still depends on local command execution

2. Public wrapper surface is narrower than the product direction
- `suggest-next` and `weekly-review` still need agent-layer synthesis

3. Planning is lightweight
- current `plan` is sequential, not conflict-aware or deadline-aware

4. Scoring is still duration-heavy
- the agent should avoid overclaiming precision from current metrics

## Recommended Integration Direction

### Phase 1

Keep the wrapper model, but align naming and outputs:
- `add` -> `log`
- `report` -> `review`
- `plan` -> `plan-day`

### Phase 2

Add dedicated decision-oriented wrapper actions:
- `suggest-next`
- `weekly-review`

### Phase 3

Strengthen the planner:
- use deadlines
- use available windows
- use stronger slot-fit logic
- return `scheduled`, `deferred`, and `warnings`

## Minimal Integration Principle

Until the code catches up with the product direction:
- promise the stronger product framing
- stay honest about the current command surface
- let the agent supply some decision logic on top of existing reports instead of pretending the command already exists
