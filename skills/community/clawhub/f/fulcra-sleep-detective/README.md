# Fulcra Sleep Detective

**Status: retired.**

This repository used to package an experimental sleep-analysis skill. That work has been folded into the broader Fulcra skill family, especially `fulcra-context`. The old helper scripts and autonomous monitoring guidance have been removed so this package no longer encourages background collection or retention of sensitive health, calendar, or location data.

## What to use instead

- `fulcra-context` for user-consented sleep, biometric, activity, calendar, location, and metric-catalog reads.
- `fulcra-annotations` for user-approved annotation writes.
- `fulcra-agent-teams`, `fulcra-memory`, and `fulcra-tracking` for coordination, memory, and event-tracking workflows.

## Privacy model

Sleep data is sensitive. Calendar and location data can reveal private routines and relationships. Agents using Fulcra should:

1. Get consent for the current request.
2. Read the smallest useful time window and metric set.
3. Prefer summaries and trends over raw records.
4. Avoid background polling, proactive alerts, exported files, screenshots, public examples, or durable storage unless the user explicitly approves that exact workflow.
5. Use synthetic data for public demos and documentation by default.

## Safe setup

Follow the current `fulcra-context` onboarding path.

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

## License

MIT License - Copyright 2026 Arc
