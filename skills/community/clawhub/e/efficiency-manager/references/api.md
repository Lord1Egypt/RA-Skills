# API Reference

This skill currently has two command surfaces:
- wrapper commands for agent-friendly JSON flows
- CLI commands for richer local interaction

## Wrapper Commands

Preferred when the caller wants structured JSON.

Path:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api
```

Currently exposed actions:
- `add`
- `report`
- `list`

Examples:

```bash
efficiency-api add -d "写代码" -c work --from 09:00 --to 11:00
efficiency-api report -t today
efficiency-api list --date 2026-04-02
```

Internal actions that exist in the wrapper but are not exposed as the public shell entrypoint:
- `analyze`
- `delete`
- `config`

Use those only when the direct Node entrypoint is acceptable:

```bash
cd ~/.openclaw/skills/efficiency-manager
node scripts/api-wrapper.js analyze -c work
```

## CLI Commands

Path:

```bash
~/.openclaw/skills/efficiency-manager/scripts/cli.js
```

Current CLI capabilities:
- `add`
- `start`
- `end`
- `report`
- `analyze`
- `plan`
- `list`
- `delete`
- `config`

Examples:

```bash
efficiency start "写代码"
efficiency end "写代码"
efficiency report week
efficiency plan "写代码2h" "开会1h"
```

## Mode Mapping

Conceptual mode to current command support:

- `Log`
  Use `efficiency-api add` or `efficiency start/end`

- `Review`
  Use `efficiency-api report` or `efficiency report`

- `Suggest Next`
  No dedicated command yet
  Derive from task input plus current history and heuristics

- `Plan Day`
  Use `efficiency plan` today
  Treat it as a lightweight planner, not a full constraint-aware scheduler

- `Weekly Review`
  Use weekly `report` plus an action-oriented synthesis

## Compatibility Direction

Recommended future public action names:
- `log`
- `review`
- `suggest-next`
- `plan-day`
- `weekly-review`

Recommended alias mapping:
- `add` -> `log`
- `report` -> `review`
- `plan` -> `plan-day`
