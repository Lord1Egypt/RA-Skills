---
name: byterover-metrics
description: ByteRover usage metrics report. Runs the metrics script to summarise query and curate activity — counts, durations, file changes, and quota errors. Accepts one or more project directories via --cwd to report per-project stats. Use when asked to report ByteRover health, usage stats, or activity for specific projects.
---

# ByteRover Metrics Report

## When to Use
- Daily health check on ByteRover query/curate activity
- When asked "how is ByteRover doing?" or "show usage stats"
- When asked for metrics on a specific project or list of projects
- Scheduled cron jobs that report overnight/daily metrics

## When NOT to Use
- Querying or curating knowledge (use `brv query` / `brv curate` directly)
- Listing stored memories (use `brv search`)

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--cwd` | path | current directory | Project directory to run `brv` against. Pass once per project. Supports `~` expansion. |
| `BRV_SINCE` | env var | `24h` | Lookback window (e.g. `48h`, `7d`) |
| `BRV_CMD` | env var | `brv` | Path to the `brv` binary — set in non-interactive environments (cron, CI) where `brv` may not be on PATH |

## How to Run

**Single project:**
```sh
npx tsx metrics.ts --cwd=~/my-project
```

**Multiple projects — run once per `--cwd`:**
```sh
npx tsx metrics.ts --cwd=~/project-a
npx tsx metrics.ts --cwd=~/project-b
npx tsx metrics.ts --cwd=~/project-c
```

**Change the lookback window:**
```sh
BRV_SINCE=48h npx tsx metrics.ts --cwd=~/my-project
```

**Non-interactive / cron environments:**
```sh
BRV_CMD=$(which brv) npx tsx metrics.ts --cwd=~/my-project
```

When the user provides a list of project paths, run the script once per path and present each as a separate section in your response.

## Output Rules

- Output ONLY the formatted metrics summary below — nothing else
- Do NOT narrate reasoning, thinking steps, or tool call decisions
- Do NOT show intermediate commands, execution logs, or script output verbatim

## Response Format

After running the script, present the output in a clean summary:

1. **Query Activity** — executed in window, completed vs errors, avg duration
2. **Curate Activity** — executed in window, files added/updated/merged, errors
3. **Quota Warnings** — highlight any ⚠️ quota or rate-limit errors with their IDs
4. **Status line** — one-sentence overall health (e.g. "✅ All good — 12 queries, 3 curations, no errors")

If reporting multiple projects, show one summary block per project, then a combined status line at the end.

If the script exits with a non-zero code or produces no output:
- Show the error message
- Suggest running `brv status` to diagnose the daemon
