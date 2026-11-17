---
name: agent-uptime-keeper
description: >-
  Keep always-on agents honestly reachable: register each agent endpoint with an
  external heartbeat watch, poll its verdict daily, and escalate when it goes
  dark. Use when running long-lived agents, before promising uptime to a
  counterparty, or after an outage nobody noticed.
version: 1.0.0
metadata:
  triggers: |-
    is my agent still reachable
    set up uptime monitoring for my agent
    agent went dark silently
    prove my agent's uptime
    watch this endpoint
  kind: workflow
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: DDG_AGENT_ID
        required: false
        description: Stable agent identity sent as X-Agent-Id; the watch is keyed to it, so keep it stable across runs.
    homepage: https://agents.daedalusdevelopmentgroup.com
    emoji: "📡"
allowed-tools: Bash, Read
---

# Agent Uptime Keeper

An unattended agent that goes dark is worse than a stopped one: counterparties
keep paying against a URL that no longer answers. This skill gives every agent
endpoint an outside observer and an honest uptime number — so "we are up" is a
measurement, not a hope.

**Endpoints:** `POST /v1/heartbeat/register` ($0.01 per 30-day window),
`POST /v1/heartbeat/status` ($0.01), `POST /v1/heartbeat/alerts` (**free with
the watch**), all on `https://agents.daedalusdevelopmentgroup.com`.

**External cost:** $0.01 per register (covers a 30-day watch) plus $0.01 per
status poll; alerts are free while the watch is active. No account or API key
is required; the paid path needs an x402-capable client. One watch = $0.01 per
month plus $0.01/day to poll — less than the cost of one unnoticed outage.

## Procedure

1. **Pick the reachable surface.** The URL a counterparty actually calls (your
   agent's HTTP endpoint), plus the success condition: status code and, when
   useful, a string the body must contain.
2. **Register one watch per endpoint.**
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/heartbeat/register \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"url":"https://my-agent.example.com/health","interval_seconds":900,
          "expect":{"status_code":200,"contains_text":"ok"}}' > out/watch.json
   ```
   Body: `url`, `interval_seconds` (300..86400, default 900), optional
   `expect`, optional `webhook_url`. Returns `watch_id` and `window_ends_at`.
   Store the `watch_id` next to the agent definition. Re-registering the same
   (identity, url) refreshes the window — it never creates a second watch.
3. **Poll daily.**
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/heartbeat/status \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"watch_id":"<watch_id>"}' > out/status.json
   ```
   Returns `last_verdict`, `last_checked_at`, `uptime_30d` (ok/total),
   `consecutive_fails`, `alert_count`. Treat `consecutive_fails >= 2` as a
   page, not a trend.
4. **Read the alerts, not just the number.** `POST /v1/heartbeat/alerts`
   (free with the watch) returns `went_dark / back_alive / flap` events with
   timestamps — flapping (>=3 flips/24h) usually means a resource leak, not
   network noise.
5. **Report uptime from observations.** Quote `uptime_30d` (ok/total probes)
   and the probe interval in any SLA-ish claim; never extrapolate past the
   watch's lifetime.

## Report schema

```json
{"agent": "name", "watch_id": "...", "url": "https://...",
 "uptime_30d": "287/288", "interval_seconds": 900,
 "last_verdict": "alive", "alerts": [{"ts": "...", "kind": "went_dark"}]}
```

## Failure handling

- `404` on status/alerts = unknown `watch_id` (wrong identity, or the window
  expired): re-register the watch and use the new id.
- `402` = the 30-day window or the daily allowance is exhausted; the body
  carries the exact upgrade path — retry the identical body with payment.
- `503` = the prober backend is unavailable; no charge, retry with backoff.

## Rules

- Register only endpoints you control; a heartbeat watch on someone else's URL is abuse.
- Two consecutive fails before escalating; one failed probe is a packet, not an outage.
- Probe intervals are floors, not promises — a watch can only prove what it observed.
- When you change the agent's URL or success condition, re-register the watch in the same change.

## Not for

- Load testing or capacity planning (this watches reachability, not throughput).
- Watching resources behind authentication the prober cannot reach.
- On-call scheduling or paging policy — this produces the signal, not the roster.

## Example

**Ask:** "Our support agent keeps going quiet overnight — how do we catch it?"

**Before:** outages are found when a customer complains the next morning.

**After:** the endpoint is registered with a 15-minute watch; at 03:10 the
watch flips to dark and the operator's webhook fires; at 03:40 back_alive.
The morning report quotes uptime_30d = 271/288 and the two alert events.

## Version

1.0.0 — initial staged draft (register → daily status → alert-driven escalation).
