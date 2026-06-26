---
name: agent-cost-eval-kit
description: Agent Token Cost Signal Kit — Find token waste, repeated calls, and risky routing changes before they become real cost.
version: 2.4.4
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tokensave, eval, cost-signal, token-change, waste, triage]
    related_skills: [waste-audit, agent-routing-waste-audit]
---

# Agent Token Cost Signal Kit

Find token waste, repeated calls, and risky routing changes before they become real cost.

## Features

- 🔍 **Token Waste Check**
  Finds agents that may be using too many tokens for the work they do.

- 🔁 **Repeated Call Signal**
  Spots retries, loops, repeated tool calls, or duplicate scheduled jobs.

- 🧠 **Routing Risk Check**
  Flags model or routing changes that may increase token use.

- 🧾 **Evidence Before Action**
  Avoids judging from one noisy run or mixed workloads.

- 🛠 **Clear Next Step**
  Tells you whether to watch, investigate one path, keep status quo, or consider rollback.

## Install

```
openclaw skills install agent-cost-eval-kit
```

```
openclaw skills install agent-cost-eval-kit --global
```

```
openclaw skills install agent-cost-eval-kit --global --force
```

## Activation

```
eval cost change for [My_Agent]
```

```
eval token change for [My_Agent]
```

```
check token waste for [My_Agent]
```

## What You Will Get

- Status
- What was checked
- Waste signal
- Risk level
- Recommended next action

## Status Labels

- **No Clear Waste**
  No meaningful token waste is visible from the available evidence.

- **Watch Only**
  There may be waste, but evidence is not strong enough to act.

- **Investigate One Path**
  One specific agent, job, route, or task path looks suspicious.

- **Keep Status Quo**
  The current setup looks better than the previous one. Do not rollback or make more changes yet.

- **Rollback Candidate**
  A recent change may have increased token use or reduced reliability. Review before rollback.

- **Unsafe to Decide**
  The workflow is too risky, mixed, or under-sampled to make a safe judgment.

## Output Format

Every result starts with a status label, then gives the priority item, reason, evidence, risk level, and next action.

```text
Status: Investigate One Path

Fix First:
daily_empty_signal_reminder

Reason:
Recent runs repeatedly returned NO_REPLY or produced no useful downstream action while still starting a full agent loop.

Evidence:
- Recent scheduled runs repeatedly returned NO_REPLY
- The job still consumed tokens on each run
- The upstream signal source appears empty or inactive

Risk:
Medium

Next Action:
Do read-only verification first. Confirm whether the reminder still has a valid upstream signal source before pausing, reducing frequency, or adding pre-agent filtering.
```

A short output is not waste by itself. Waste means the task consumed tokens without producing useful downstream value.

## What This Will Not Do

It will not:

- calculate exact provider billing without full pricing and usage data
- treat token count as exact dollar cost
- judge from one noisy run
- compare unrelated task types as the same workload
- promise lower cost with equal quality
- edit configs, switch models, disable jobs, or delete cron tasks
- require API keys, private keys, secrets, credentials, or full private logs

This skill is read-only. It may recommend an action, but it will not ask to immediately disable, edit, delete, switch, or change production configs.

Redact sensitive data before pasting logs.

