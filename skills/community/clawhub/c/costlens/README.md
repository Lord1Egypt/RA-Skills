# CostLens

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A token cost monitoring CLI for OpenClaw workflows that turns raw usage events into budget-aware summaries.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-costlens` |
| Runtime | Node.js 18+ |
| Interface | CLI + JavaScript module |
| Main commands | `monitor`, `report`, `budget check` |

## Why this exists

Token usage problems are usually discovered too late, after a workflow has already scaled. CostLens makes spend visible earlier by aggregating model usage, calculating cost, checking budget thresholds, and turning event streams into simple operator-facing output.

## What it does

- Reads JSON event arrays containing prompt and completion token counts
- Applies built-in model rates, with optional per-event overrides
- Summarizes cost by model and by day
- Skips invalid events safely and reports what was ignored
- Checks budget usage and raises warning or critical states
- Exports structured reports for handoff or audit

## Primary workflow

1. Export token events from your workflow logs.
2. Run `costlens monitor` for a quick operational view.
3. Add `--budget` and `--threshold` to enforce spend guardrails.
4. Write a report artifact with `costlens report`.

## Quick start

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/costlens
npm install
node ./bin/costlens.js monitor --events ./fixtures/events.json --budget 0.1 --threshold 75
```

## Commands

| Command | Purpose |
| --- | --- |
| `costlens monitor --events <path>` | Print a live summary table or JSON payload |
| `costlens report --events <path> --out <path>` | Save a full JSON report |
| `costlens budget check --events <path> --budget <amount>` | Return budget status, including critical exits |

## Event shape

```json
{
  "model": "gpt-4.1",
  "promptTokens": 1200,
  "completionTokens": 300,
  "timestamp": "2026-03-10T10:00:00Z"
}
```

## Output behavior

- `monitor` returns exit code `0` for normal or warning states and `2` for critical budget overruns
- `report` writes a JSON artifact with totals, per-model breakdown, per-day breakdown, and budget summary
- Invalid events are skipped instead of crashing the run

## Project layout

```text
costlens/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## Status

The current implementation is built for offline event analysis with built-in model pricing and budget enforcement. It is a practical reporting layer rather than a streaming billing service.
