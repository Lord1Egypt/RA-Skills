---
name: agent-routing-waste-audit
description: Paste an agent job, cron, routing, or run summary and get an immediate read-only audit of possible routing, retry, fallback, or model-assignment waste.
version: 1.2.2
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [routing, tokensave, agent, audit, retry, fallback, waste, cross-agent, cron]
    related_skills: [waste-audit]
---

# Agent Routing Waste Audit

Read-only routing waste audit for agent workflows: catch overpowered models, retry loops, fallback cost escalation, sub-agent overuse, and unclear local/cloud split before they compound.

## What It Checks

Use this when you want to check whether an agent workflow is wasting tokens or cost through:

- overpowered models for simple tasks
- retry loops that keep burning tokens
- fallback chains that increase cost without recovery
- sub-agents assigned to unnecessarily strong models
- unclear or wasteful local/cloud model split
- recurring jobs that may no longer justify their model tier

The audit can review pasted job lists, routing logs, cron metadata, JSON job output, prompt previews, or agent run summaries.

## Install

Workspace install:

```bash
openclaw skills install agent-routing-waste-audit
```

Install for all local agents:

```bash
openclaw skills install agent-routing-waste-audit --global
```

## Activation

```bash
audit agent routing waste
```

## What You Get

- Ranked routing waste findings based on available evidence.
- Clear separation between evidence-backed findings and missing evidence.
- Manual verification steps before any production change.
- A safe copy-paste prompt for your agent.
- Read-only behavior by default.

## Copy-Paste Prompt for Your Agent

Copy this into your agent:

```
Audit the current or pasted agent job/routing evidence for routing waste.

Use the agent-routing-waste-audit skill.

First use any relevant evidence already available in this conversation, including job lists, JSON output, routing logs, cron metadata, prompt previews, run summaries, retry/fallback traces, model/provider names, or schedule information.

Look for:
- overpowered model choices
- unnecessary retries
- fallback loops or cost escalation
- sub-agent overuse
- unclear local/cloud split
- recurring jobs whose model tier may no longer be justified

Do not modify, disable, delete, reschedule, rewrite, downgrade models, or change routing policies.

If there is not enough evidence, ask me for the single most useful missing input instead of giving me a long checklist.

Return:
1. Decision
2. Top routing waste findings
3. Evidence used
4. Missing evidence
5. Safe manual verification steps
6. Recommended next action
```

## What This Will Not Do

It will not:
- modify jobs or routing rules
- disable, delete, or reschedule anything
- automatically downgrade models or change routing policies
- expose API keys, tokens, secrets, or private logs
- claim savings without evidence
- replace human review before production changes
- audit general cron hygiene unrelated to routing or model-choice waste
