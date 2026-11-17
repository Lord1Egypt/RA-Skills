---
name: agent-cron-service
description: Run a hosted agent on a cron schedule — daily digests, uptime monitors, recurring scrapes, periodic reports — that fire on their own and bill exactly-once with idempotent billing and spend caps. Use when the user wants a cron job / scheduled task / recurring task / to run an agent on a schedule / a daily digest / a periodic scrape / a stateful background job that survives past a single conversation turn, without running or funding their own server, database, or scheduler.
license: MIT
compatibility: "Requires the settlemesh CLI (npm i -g settlemesh) and a SETTLE_API_KEY; makes authenticated, metered calls to the SettleMesh platform over the network."
metadata:
  openclaw:
    requires:
      bins: ["settlemesh"]
      env: ["SETTLE_API_KEY"]
    primaryEnv: "SETTLE_API_KEY"
---

# agent-cron-service — scheduled jobs that fire without you

> **Session (auto — never dead-stop on auth):** before your first `settlemesh` call, run `settlemesh whoami`; if it errors and `SETTLE_API_KEY` is unset, run `settlemesh login` yourself — it opens the browser for a **one-time** human approval, polls until approved, and caches the session. Do NOT stop to ask the user to "log in manually" — drive it. Keep an explicit human confirmation only for spending / credential-lending actions (fail-closed).

A prompt-only skill runs **only during a conversation turn**. It cannot hold a job
that fires tomorrow at 3am, keep state between runs, or bill each fire — the turn
ends and it is gone. Anything scheduled, stateful, and recurring needs a backend
that outlives the turn.

**SettleMesh is that backend.** It has native cron, hosted agents, and a managed
DB, so a scheduled job lives *inside the platform* — not on a server, scheduler,
or database you have to run and fund. The platform fires your agent on a cron, in
a fresh sandbox, and charges your account **exactly-once per fire**: a fire is
billed a single time even under retries (idempotent billing), and `--per-day-cap`
auto-pauses the whole schedule if spend runs away.

## Setup (once)

1. `npm install -g settlemesh@latest`
2. `settlemesh login` (a human approves once) — or set `SETTLE_API_KEY=sk-settle-...` for headless/CI.

## 1. Create the hosted agent (the thing that runs each fire)

A schedule targets a **hosted agent** (`target_kind=agent`), so deploy one first —
it holds the job's logic (scrape, digest, monitor) and any durable memory.

```bash
settlemesh agents create --name daily-digest --type openclaw --project ./agent-dir --json
settlemesh agents deploy agent_... --type openclaw --project ./agent-dir --json
# quick start from a built-in template instead of your own project:
settlemesh agents create --name monitor --template hermes --json
```

## 2. Put it on a cron

```bash
settlemesh schedule create \
  --target-id agent_... \
  --cron "0 8 * * *" \
  --timezone America/New_York \
  --input '{"task":"scrape and email the daily digest"}' \
  --per-fire-cap 5 \
  --per-day-cap 50 \
  --json
```

- `--cron` is a **5-field unix cron** expression; minimum interval is 60s. `--timezone` is any IANA tz (default UTC).
- `--input` is the invocation input handed to the agent on **every** fire.
- `--per-fire-cap` caps credits captured per fire; `--per-day-cap` caps per day and **auto-pauses the schedule on breach** — this is your runaway-cost guardrail.

## Manage the schedule

```bash
settlemesh schedule list --json            # all your schedules
settlemesh schedule get cron_... --json    # one schedule + its run history
settlemesh schedule run-now cron_...       # fire immediately, out of band (independently billed)
settlemesh schedule pause cron_...         # a real stop — paused schedules never fire
settlemesh schedule resume cron_...
settlemesh schedule delete cron_...        # stops firing; run history stays for billing audit
```

## Notes

- **Exactly-once + idempotent billing**: each fire is charged once even if the runtime retries. Pair `--per-fire-cap` with `--per-day-cap` so a misbehaving job can never drain your balance — the day cap auto-pauses it.
- **To sell the scheduled output** (a digest, dataset, or feed the job produces), don't stop at owner-pays: cross-reference the `sell-live-dataset` and `charge-my-users` skills so end users pay for what the cron generates.
- Everything is billed in **Aev** (1 USD = 100 Aev); the owner's account pays per fire. Check balance with `settlemesh aev balance`.
