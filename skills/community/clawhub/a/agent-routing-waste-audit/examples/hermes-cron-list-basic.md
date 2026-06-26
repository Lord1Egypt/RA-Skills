# Hermes Cron List — Basic Example

Paste this as input to test the Agent Routing Waste Audit skill:

```
5233cac535ea [active]
    Name:      hermes-health-watchdog
    Schedule:  */5 * * * *
    Repeat:    ∞
    Next run:  2026-05-29T21:00:00+08:00
    Deliver:   local
    Last run:  2026-05-29T20:55:14.739199+08:00  ok

760c41123c8f [active]
    Name:      vps-disk-daily-check
    Schedule:  0 9 * * *
    Repeat:    ∞
    Next run:  2026-05-30T09:00:00+08:00
    Deliver:   local
    Last run:  2026-05-29T09:00:39.464607+08:00  ok
```

## Expected Audit Result

### Initial Finding

One high-priority audit candidate found.

---

### Top Routing / Waste Candidate

| Field | Value |
|---|---|
| **Name** | hermes-health-watchdog |
| **ID** | 5233cac535ea |
| **Why flagged** | Runs every 5 minutes (~288 runs/day). A health watchdog that runs an LLM on every tick is a high-frequency waste candidate. |
| **Estimated frequency** | ~288 runs/day |
| **Confidence** | High (schedule parseable, frequency is compounding) |
| **Evidence depth** | Level 1 |

---

### Lower-Priority Candidates

| Name | ID | Why lower priority | Estimated frequency |
|---|---|---|---|
| vps-disk-daily-check | 760c41123c8f | Runs once/day at most | ~1 run/day |

---

### Missing Evidence

- model / provider used
- whether LLM is invoked every run
- whether normal "ok" runs are useful or routinely discarded
- token usage per run

---

### Suggested Manual Check

Inspect whether `hermes-health-watchdog` can become **script-first / LLM-only-on-anomaly** — i.e. run a lightweight script every 5 minutes that only escalates to an LLM when a real anomaly is detected, rather than running an LLM on every tick.

---

### Copy-Paste Prompt for Your Agent

```
Please inspect this agent run for possible routing waste.

Run: hermes-health-watchdog (5233cac535ea)
Flagged because: Runs every 5 minutes (~288 runs/day). A health watchdog that invokes an LLM on every scheduled tick is a high-frequency waste candidate.
Evidence depth so far: Level 1 — schedule and last-run status available; model, token usage, and prompt summary not yet available.

Do not edit, disable, delete, or mutate anything yet.

Inspect and report:
1. whether this job invokes an LLM every run, or only on anomaly
2. whether normal "ok" runs actually needed an LLM
3. whether script-first / anomaly-only / silent-on-ok is a safer and cheaper policy
4. the safest manual next step, with no changes applied yet

Redact secrets. Do not expose raw private payloads.
```
