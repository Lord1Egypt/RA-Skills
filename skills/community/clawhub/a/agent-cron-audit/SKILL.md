---
name: agent-cron-audit
description: "Read-only health audit for recurring / scheduled AI agent jobs. Finds silent failures, duplicate active jobs, retry loops, over-frequent schedules, stale automations, risky model usage, and context bloat. Evidence first. Manual verification before any change."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [openclaw, agent, cron, audit, scheduled-jobs, read-only, health]
    related_skills: [waste-audit, agent-cost-eval-kit]
---

## Features

- 🩺 Cron Health Audit: Inspects recurring / scheduled AI agent jobs for silent failures, duplicate active jobs, retry loops, over-frequent schedules, stale automations, risky model usage, and context bloat.
- 🔇 Silent Failure Detection: Flags jobs that complete "successfully" but produce no useful output, no downstream action, repeated empty replies, or stuck retries.
- ♻️ Duplicate / Retry Loop Detection: Identifies multiple active schedules that run the same effective task, and jobs whose failure count keeps rising despite restarts.
- ⏱️ Schedule Hygiene: Calls out schedules that are too frequent, too aggressive for the model, or that re-run before the previous run's downstream work has settled.
- 🧱 Context Bloat Signal: Flags recurring runs that drag in oversized context, old conversation history, or full private logs into every loop.
- 🧾 Evidence-First Output: For every finding, shows what was checked, the signal, and a confidence label (High / Medium / Low) before any next step.
- 🛠 Manual Verification Prompt: Produces a copy-paste prompt for the user's agent so the human can verify findings safely.
- 🔒 Read-Only Safety: Does not edit, disable, delete, restart, enable, upload, or auto-fix any job.

## Install

For shared OpenClaw agents, install into the global managed skills directory:

```bash
openclaw skills install agent-cron-audit --global
```

To upgrade an existing shared install:

```bash
openclaw skills install agent-cron-audit --global --force
```

Then test with:

```bash
audit agent cron jobs
```

## Activation

Primary activation phrase:

```bash
audit agent cron jobs
```

Also activate for:

- `check recurring agent jobs`
- `check scheduled agent jobs`
- `find silent failures in agent cron`
- `check stale automations`
- `check duplicate active agent jobs`
- `check retry loops`

Do not activate this skill for:

- general OpenClaw setup
- provider / API key debugging
- normal one-off job execution
- pricing-only questions
- dashboard / report / export requests
- automatic fix or job disabling requests

## What This Skill Audits

This skill is the entry point for **recurring / scheduled AI agent job health**.

It looks at the schedule, run history, model choice, and output of recurring jobs, then groups findings by risk:

- **Silent failures** — job finishes without error but produces no useful downstream work
- **Duplicate active jobs** — two or more schedules effectively run the same task
- **Retry loops** — repeated failures, restarts, or fallback chains with no recovery
- **Over-frequent schedules** — interval shorter than the task or downstream consumer can absorb
- **Stale automations** — schedule still active but upstream signal, target, or recipient no longer valid
- **Risky model usage** — a model that is too strong, too weak, or too context-heavy for the recurring task
- **Context bloat** — recurring runs that repeatedly pull in oversized context, old history, or full private logs

The output is **evidence**, not an action. This skill does not change any job.

## What You Will Get

Every audit returns six sections, in this order:

### 1. Fix First

The single most likely health risk in the current cron set, with:

- Job
- Why it looks risky
- Evidence
- Confidence: High / Medium / Low
- Recommended next step (always manual verification first)

### 2. Top Cron Health Findings

Up to 5 ranked findings. For each:

- Job
- Health signal
- Evidence
- Why it matters
- Confidence: High / Medium / Low

### 3. Evidence

Raw observations the audit relied on, with secrets, IDs, and private payloads already redacted as `<redacted>`.

### 4. Manual Verification Prompt

A copy-paste prompt the user can hand to their own agent to verify a finding safely:

```text
Read only. Inspect recurring/scheduled AI agent jobs for silent failures,
duplicate active jobs, retry loops, over-frequent schedules, stale
automations, risky model usage, and context bloat. Do not edit, disable,
restart, delete, or change any job. Do not upload logs. Redact secrets and
IDs. Return top findings with evidence, likely cause, manual verification
steps, and recommended human priority.
```

### 5. What Not To Do Yet

A short list of actions the skill deliberately does **not** recommend at this stage, for example: do not disable a job, do not change a schedule, do not switch the model, do not delete run history.

### 6. Related Skill, If Relevant

If the main issue is recurring **token waste** rather than general cron health:

```text
Try: openclaw skills install waste-audit --global
```

If the main issue is **routing / model / cost change risk** rather than general cron health:

```text
Try: openclaw skills install agent-cost-eval-kit --global
```

These are pointers, not a funnel. Pick the one that matches the actual problem.

## Safety

- 🔒 **Read-only first.** Never edit, disable, delete, restart, or auto-fix a job as the first recommendation.
- 🚫 **No auto-apply.** Always surface evidence and let the owner decide.
- ✏️ **Edit as last resort.** Changing a job schedule, prompt, or config should only be suggested after manual verification confirms the finding.
- 🔑 **No secrets exposed.** Never show raw tokens, API keys, bot tokens, Telegram chat IDs, private server paths, or raw private payloads in examples or evidence.
- 📋 **Redact before sharing.** Use `<redacted>`, `<redacted-id>`, or similar placeholders for anything that could identify a private resource.
- 🌐 **Local-first.** All inspection happens locally. This skill does not upload logs, call external LLMs, or send telemetry.
- ❓ **No precise savings claim.** This skill does not promise exact cost reduction, percentage savings, or dollar amounts. It surfaces health risk, not a bill.

## Out Of Scope

This skill will not:

- Calculate exact provider billing or dollar savings
- Treat token count as exact dollar cost
- Edit configs, switch models, disable jobs, delete cron tasks, or restart agents
- Require API keys, private keys, secrets, credentials, or full private logs
- Make network calls or call external LLMs
- Provide a dashboard, report, export, or backend service
- Replace `waste-audit` (token waste) or `agent-cost-eval-kit` (cost change triage)

## When To Pick A Different Skill

| Main problem | Use this skill |
| --- | --- |
| Recurring token waste on a known job | `waste-audit` |
| Suspected cost / model / routing change after a deployment | `agent-cost-eval-kit` |
| General cron health of recurring agent jobs (this card) | `agent-cron-audit` |
| One-off job execution, provider setup, API key debugging | (not this skill) |

## Feedback / Free Second Look

If `agent-cron-audit` flags a finding and you are not sure whether it is real, you can DM me on X: @BeeGeeEth.

When you do, send only the redacted "Top Cron Health Findings" and "Evidence" sections. Do not include secrets, API keys, private logs, wallet data, full config files, or production credentials.
