---
name: fulcra-sleep-detective
description: Retired Fulcra sleep-analysis skill. Route new work to fulcra-context and keep all sleep, biometric, calendar, and location reads explicit, bounded, and user-approved.
homepage: https://fulcradynamics.com
---

# Fulcra Sleep Detective

This skill is retired. Its earlier experimental scripts were merged into the broader Fulcra skill family and are no longer shipped here.

Use `fulcra-context` for current sleep, biometric, activity, calendar, location, and metric-catalog reads. Use `fulcra-annotations` only when the user explicitly asks to record an event or create an annotation.

## Current Routing

- Sleep analysis, recovery context, readiness, and trends: use `fulcra-context`.
- Writes, check-ins, ratings, notes, and annotation buttons: use `fulcra-annotations`.
- Cross-agent coordination, handoffs, and team state: use `fulcra-agent-teams`.
- Persistent agent memory workflows: use `fulcra-memory`.
- Lightweight event tracking: use `fulcra-tracking`.

## Privacy Boundary

Sleep and biometric data are sensitive personal context. Calendar and location data can identify people, places, routines, and private obligations. Before using any Fulcra data:

1. Ask for consent unless the user has already granted it for the current request.
2. Read only the smallest metric set and time window needed.
3. Prefer summaries, trends, and aggregates over raw records.
4. Do not retain, export, screenshot, publish, or forward Fulcra records without explicit approval for that exact destination.
5. Do not run background monitoring, scheduled polling, proactive alerts, or persistent files from this retired skill.
6. Use synthetic data for public examples, demos, tests, and documentation unless the user explicitly approves real data for that artifact.

## Safe Setup

For new work, install or use `fulcra-context` and follow its current onboarding flow.

CLI-first environments:

```bash
uv tool run fulcra-api --help
uv tool run fulcra-api auth login --get-auth-url
uv tool run fulcra-api user-info
```

Restricted environments:

```text
https://mcp.fulcradynamics.com/mcp
```

Never print, paste, log, or share access tokens, refresh tokens, credential files, raw private records, or direct capability URLs.

## First Useful Flow

When a user asks about sleep, do this with `fulcra-context`:

1. Confirm the request and time window.
2. Check whether Fulcra data is fresh enough for the question.
3. Read only the needed sleep and recovery metrics.
4. Add calendar, location, medication, supplement, nutrition, or activity context only if the user asked for that correlation or explicitly approves it.
5. Answer with concise interpretation and uncertainty. Say when data is missing or stale.

## Deprecated Commands

The old commands `sleep-theory`, `sleep-alert`, `sleep-context`, and `sleep-insights` are retired. Do not invoke or recreate them from this package. Use bounded `fulcra-context` reads instead.

## Links

- Fulcra Platform: <https://fulcradynamics.com>
- Developer Docs: <https://fulcradynamics.github.io/developer-docs/>
- Current Context Skill: <https://clawhub.ai/arc-claw-bot/skills/fulcra-context>
- Annotation Skill: <https://clawhub.ai/arc-claw-bot/skills/fulcra-annotations>
