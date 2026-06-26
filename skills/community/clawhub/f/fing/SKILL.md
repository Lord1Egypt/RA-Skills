---
name: fing
description: Query and troubleshoot Fing Local API monitoring agents for local network device inventory, presence, online/offline state, people/presence where supported, and read-only homelab network checks. Use when Fing Desktop, Fing Agent, or Fingbox local API data is needed.
---

# Fing Local API

Use this skill for read-only Fing local monitoring data. Prefer summaries because device lists reveal private network inventory.

## Helper

Use the bundled helper:

```bash
python3 skills/fing/scripts/fing_helper.py --help
```

Environment defaults:

- `FING_API_HOST` — Fing agent host/IP, default `localhost`.
- `FING_API_PORT` — default `49090`.
- `FING_API_SCHEME` — default `http`.
- `FING_API_KEY` — API key.

The helper also loads `.env` from the current workspace directory.

Examples:

```bash
# Compact health/device summary
python3 skills/fing/scripts/fing_helper.py summary

# Device inventory summary
python3 skills/fing/scripts/fing_helper.py devices

# Raw API wrapper for debugging
python3 skills/fing/scripts/fing_helper.py devices --raw

# People/presence, Fing Desktop only
python3 skills/fing/scripts/fing_helper.py people
```

## Workflow

1. Start with `summary` to verify API reachability and device counts.
2. Use `devices` for inventory, online/offline checks, or finding unknown devices.
3. Use `people` only when Fing Desktop is expected; Fing Agent/Fingbox may return 503 for this endpoint.
4. For proactive checks, alert only on actionable changes: API unreachable, auth failure, unexpectedly low/no visible devices, or important device state changes if Igor has defined watch targets.

## API reference

Read `references/api-summary.md` when endpoint details, response fields, or error meanings matter.

## Safety notes

- Do not expose full MAC/IP/name inventories outside Igor's direct context.
- Do not send detailed device lists proactively unless they indicate a real issue.
- The documented API is local HTTP with API key in query string; avoid logging command lines or URLs containing the real key.
