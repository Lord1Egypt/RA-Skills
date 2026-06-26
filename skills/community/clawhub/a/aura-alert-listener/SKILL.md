---
name: aura-alert-listener
description: High-frequency Aura alert polling and autonomous task/job handling loop with dedupe and quiet no-op behavior. Use when running Aura checks every 5-30 seconds, replacing or supplementing 15-minute cron checks, and when only actionable alerts should wake/notify the human.
---

# Aura Alert Listener

Implement a cheap polling loop that only escalates when alerts are actionable.

## Files in this skill

- `scripts/poll-aura-alerts.mjs` — lightweight poller with state, dedupe, optional auto-ack for `push.*`, and queueing of human-notify events
- `scripts/drain-aura-notify-queue.mjs` — drains queued notifications and prints a concise summary
- `scripts/dispatch-aura-notifications.mjs` — main-session dispatcher: only emits output when `memory/needs-review-memory.flag` exists

## Required env

- `AURA_API_KEY`

## Optional env

- `AURA_BASE_URL` (default: `http://ryan-holmes-2.tail63f286.ts.net:8000`)
- `AURA_STATE_FILE` (default: `./memory/aura-alert-listener-state.json`)
- `AURA_ACK_PUSH` (`1` default; set `0` to disable auto-ack)
- `AURA_NOTIFY_QUEUE_FILE` (default: `./memory/aura-notify-queue.jsonl`)
- `AURA_NOTIFY_FLAG_FILE` (default: `./memory/needs-review-memory.flag`)

## Poll once (cheap check)

```bash
node skills/aura-alert-listener/scripts/poll-aura-alerts.mjs
```

Behavior:
- Fetch `/v1/alerts` and `/v1/agents/settings`
- Persist `checked_at`
- Dedupe alerts by stable IDs
- Print nothing and exit `0` when no new actionable alerts exist
- Print compact JSON when work exists
- Auto-ack `push.*` alerts when `AURA_ACK_PUSH=1`

## Suggested high-frequency cron

Use isolated session so no-op runs stay quiet.

```bash
openclaw cron add \
  --every 10s \
  --name "Aura Alert Listener" \
  --session isolated \
  --message "Run: node skills/aura-alert-listener/scripts/poll-aura-alerts.mjs. If output is empty, send nothing. If output has alerts, apply approval_mode from /v1/agents/settings. In auto/policy-within-limits run claim/execute loop for eligible tasks/jobs; in human mode ask first. Notify human only for approvals needed, policy violations, balance.low, repeated errors, or periodic summaries."
```

## Suggested notifier cron (main session)

Use a separate main-session dispatcher to keep high-frequency polling isolated and quiet. The listener writes a flag file when human-facing updates exist.

```bash
openclaw cron add \
  --every 1m \
  --name "Aura Notify Bridge" \
  --session main \
  --system-event "Run: node skills/aura-alert-listener/scripts/dispatch-aura-notifications.mjs. If output is empty, exit silently with no user-visible reply. If output has text, post it to the human as-is."
```

## Action loop contract (agent side)

When poller returns alerts:
1. Re-fetch authoritative task/job state by ID.
2. For open eligible tasks in `auto` (or `policy` within limits): claim immediately.
3. Continue execution (`accept/submit/deliver/verify` as appropriate).
4. On `409`: skip and continue.
5. On `429`: stop loop and notify human once.
6. Do not notify human for autonomous in-policy actions.

## Notes

- Keep a slower backup cron (e.g., every 15m) for resilience.
- If using webhooks later, keep this listener as fallback.
