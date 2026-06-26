---
name: cron-job-token-auditor
slug: cron-job-token-auditor
displayName: Cron Job Token Auditor
description: >-
  Audits OpenClaw Gateway cron jobs from jobs.json (or CLI), classifies scheduled workloads by
  token cost (agent turns vs deterministic work), and suggests when OS timers plus scripts and
  openclaw message send could replace recurring LLM runs. Use when optimizing token spend, reviewing
  cron schedules, or comparing Gateway cron to systemd-style automation. Read-only: never edits cron
  or migrates jobs automatically.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://docs.openclaw.ai
---

# Cron Job Auditor

This skill guides **read-only** reviews of **OpenClaw Gateway cron jobs** so the user can spot **token-saving** opportunities—typically moving **purely mechanical** recurring work to an **OS-scheduled script** (systemd timer, launchd, etc.) that calls **`openclaw message send`** without running the model on every tick.

## Hard boundaries

- **Do not** edit `jobs.json`, systemd units, or user scripts **unless the user explicitly asks** for a draft or a diff to apply themselves.
- **Do not** claim guaranteed savings; give **confidence levels** (high / medium / low).
- **Do not** assume paths: default is often `~/.openclaw/cron/jobs.json` — confirm or use `openclaw cron` / docs if the install differs.

## When to apply this skill

- User asks to **audit**, **review**, **optimize**, or **reduce tokens** for **cron**, **scheduled jobs**, or **recurring OpenClaw** tasks.
- User shares or points to **`jobs.json`** (or pastes JSON).

## What to read

1. **`jobs.json`** (or user-provided excerpt): each job’s `name`, `enabled`, `schedule`, `payload`, `delivery`, `agentId`.
2. Prefer **`openclaw cron` / `openclaw cron list`** (or current CLI) when available — aligns with the live Gateway.
3. **`REFERENCE.md`** in this skill folder for glossary and checklist language.

## Classification (per job)

- **`payload.kind: agentTurn`** → counts as **LLM-invoking** for each run (unless documentation says otherwise for this version).
- Extract a **short summary** of the **message** / instructions (first ~200 chars + ellipsis if long). Do not reproduce secrets or API keys; redact chat IDs as `***`.

## Heuristics — “script candidate”

Flag as **candidate** only when **medium or high** confidence:

| Signal | Suggests |
|--------|----------|
| Same task could be a shell/Python script + one message | Possible migration |
| Prompt needs **search**, **summarization**, **judgment**, **variable tool use** | Usually **keep** agent cron |
| Only **fetch fixed URL**, **run CLI**, **grep**, **template message** | Stronger candidate |

**Patterns** (map each candidate to one):

- **A — CLI + send**: e.g. `some-cli … \| …` then `openclaw message send …`
- **B — HTTP + send**: `curl`/`fetch` + parse + send (no LLM).
- **C — Hybrid**: data from script; **optional** rare agent run for exceptions only (document separately).

## Output format — use this template every time

```markdown
## Cron Job Auditor — Summary

- **Source**: (path or CLI)
- **Jobs scanned**: N (enabled: M)
- **Likely LLM per run**: (count of agentTurn-style jobs, or “unknown” if schema unclear)

## Per-job table

| Job name | Enabled | Schedule | Payload kind | LLM? | Confidence (migration) | Notes |
|----------|---------|----------|--------------|------|------------------------|-------|

## Candidates for OS timer + script (no auto-migration)

For each row with confidence **medium** or **high**:

### 1. `<job name>`

- **Why it costs tokens**: …
- **Suggested pattern**: A / B / C (one paragraph)
- **Prerequisites**: …
- **Manual steps** (numbered):
  1. Implement script at `…` (user path)
  2. Test with dry-run / manual run
  3. Add systemd timer (or launchd) — user edits unit files
  4. **Disable or remove** the Gateway cron entry to avoid duplicate sends
  5. Verify with checklist in REFERENCE.md

## Not recommended for migration

| Job | Reason |
|-----|--------|

## Low-confidence items

(Brief list — what would be needed to decide.)

```

## Tone

- Clear, cautious, actionable. Prefer **numbered steps** over prose walls.
- Link to **OpenClaw Cron** documentation when reminding users how Gateway scheduling works.

## Related

- Users who already moved jobs to OS scripts often keep **`openclaw message send`** for delivery only — that path avoids **per-tick** LLM usage for the poll itself.
