# Efficiency Manager API Usage

This document explains the current command surface and how it maps to the updated product direction.

Efficiency Manager is moving from a local time tracker toward a local execution coach.

That means two things are true at the same time:
- the current implementation already supports local logging and review
- the product direction now also includes next-task guidance and realistic day planning

## Quick Start

For agent or script usage, prefer the wrapper entrypoint:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api <action> [options]
```

For richer local interaction, use the CLI:

```bash
cd ~/.openclaw/skills/efficiency-manager
node scripts/cli.js <command> [options]
```

## Product Modes vs Current Commands

Conceptual product modes:
- `log`
- `review`
- `suggest-next`
- `plan-day`
- `weekly-review`

Current implemented command support:

| Product mode | Current command path | Status |
|---|---|---|
| `log` | `efficiency-api add` or `efficiency add/start/end` | implemented |
| `review` | `efficiency-api report` or `efficiency report` | implemented |
| `suggest-next` | derived manually from task inputs plus history | not yet a dedicated command |
| `plan-day` | `efficiency plan` | lightweight implementation |
| `weekly-review` | weekly `report` plus action-oriented interpretation | partially supported |

Recommended future alias mapping:
- `add` -> `log`
- `report` -> `review`
- `plan` -> `plan-day`

## Wrapper Commands

Wrapper path:

```bash
~/.openclaw/skills/efficiency-manager/scripts/efficiency-api
```

### 1. `add`

Use for fast event capture.

```bash
efficiency-api add -d "写代码" -c work --from 09:00 --to 11:00
efficiency-api add -d "阅读《深度工作》" -c study --from 14:00 --to 15:30 -n "第3章"
efficiency-api add -d "开会" -c work --from 10:00 --to 11:30 --date 2026-03-20
```

Parameters:

| Parameter | Short | Required | Meaning |
|---|---|---|---|
| `--description` | `-d` | yes | event description |
| `--category` | `-c` | no | category, auto-detected if omitted |
| `--from` | | yes | start time `HH:MM` |
| `--to` | | yes | end time `HH:MM` |
| `--date` | | no | date `YYYY-MM-DD`, default is today |
| `--notes` | `-n` | no | notes |

Recommended product interpretation:
- treat `add` as the current implementation of `log`

### 2. `report`

Use for day, week, or month review.

```bash
efficiency-api report -t today
efficiency-api report -t week
efficiency-api report -t week --date 2026-03-15
efficiency-api report -t month --date 2026-03
efficiency-api report -t 2026-03-23
```

Parameters:

| Parameter | Short | Required | Meaning |
|---|---|---|---|
| `--type` | `-t` | no | `today`, `week`, `month`, or `YYYY-MM-DD` |
| `--date` | | no | anchor date for week or month reports |

Recommended product interpretation:
- treat `report` as the current implementation of `review`
- for weekly review outputs, add one concrete behavior recommendation instead of only relaying metrics

### 3. `list`

Use for raw inspection and debugging, not as the main product surface.

```bash
efficiency-api list
efficiency-api list --date 2026-03-23
efficiency-api list --category work
efficiency-api list --startDate 2026-03-20 --endDate 2026-03-25
```

Parameters:

| Parameter | Short | Required | Meaning |
|---|---|---|---|
| `--category` | `-c` | no | filter by category |
| `--date` | `-d` | no | filter by date |
| `--startDate` | | no | range start |
| `--endDate` | | no | range end |

Recommended product interpretation:
- keep this as an advanced or support command
- avoid presenting it as a primary user-facing mode

## Internal Wrapper Actions

These actions exist in `api-wrapper.js` but are not exposed as the intended public shell interface:
- `analyze`
- `delete`
- `config`

Direct usage:

```bash
cd ~/.openclaw/skills/efficiency-manager
node scripts/api-wrapper.js analyze -c study
node scripts/api-wrapper.js config
```

Use them carefully:
- `analyze` is useful for debugging and structured analysis
- `delete` and `config` are support tools, not core product moments

## CLI Commands

The CLI currently exposes a broader surface than the wrapper:
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
efficiency report today
efficiency analyze work
efficiency plan "写代码2h" "开会1h" "健身1h"
```

Notes:
- `start/end` are useful for live tracking
- `plan` is available today, but it should be described as a lightweight planner rather than a full scheduler
- `analyze` is best treated as an expert or debugging surface

## Output Format

Wrapper commands return JSON.

Typical success shape:

```json
{
  "success": true,
  "action": "add"
}
```

Typical error shape:

```json
{
  "error": "Error message"
}
```

When using outputs in an agent workflow:
- prefer structured fields over formatted text when both are available
- use formatted text only for user-facing summaries

## Data and Compatibility

Current shared storage:
- `~/.openclaw/efficiency-manager/data/events.json`
- `~/.openclaw/efficiency-manager/config.json`

Compatibility already handled in storage:
- `title` -> `description`
- `from` and `to` plus `date` -> `startTime` and `endTime`
- some Chinese categories -> normalized categories
- timestamps with spaces instead of `T`

## Recommended V2 Surface

These are the target public action names for the next product step:
- `log`
- `review`
- `suggest-next`
- `plan-day`
- `weekly-review`

What should happen before exposing them:
- keep JSON output stable
- align wrapper naming with product modes
- avoid claiming dedicated support until the command exists
