---
name: business-agent-launchpad
description: Use when a user wants to initialize OpenClaw, Hermes, or another agent harness for ordinary business or office work. Guides plain-language business interviews, recommends agent roles, object-based Markdown memory, tool permissions, model tiers, free/paid upgrade paths, and generates starter workspaces with the `agent-launchpad` CLI.
version: 0.1.0
author: Andy Ren
license: MIT
tags: [agent, onboarding, openclaw, hermes, memory, office, business]
category: productivity
---

# Business Agent Launchpad

Use this skill when the user wants a first-run business setup for OpenClaw, Hermes, or a similar agent harness.

The goal is to translate ordinary business language into:

- scenario and workflow description
- agent roles and operating rules
- object-based Markdown memory
- tool and permission plan
- model tier and escalation plan
- free vs paid cost choices
- OpenClaw/Hermes starter artifacts

## First Check

Verify the CLI exists:

```bash
agent-launchpad doctor
```

If it is not installed, find the project folder and install it:

```bash
npm install -g .
```

Then re-run:

```bash
agent-launchpad doctor
```

## Recommended Flow

For a non-technical user, run the interview:

```bash
agent-launchpad interview --out ./first-business-agent
```

For a quick preset:

```bash
agent-launchpad generate --preset sales --tier free --runtime both --out ./sales-agent
```

Available scenario keys:

- `sales`
- `admin`
- `finance`
- `legal`
- `project`
- `hr`
- `customer_service`
- `executive_assistant`
- `procurement`

Available tiers:

- `free`: Markdown memory and local tools first
- `local_plus`: local semantic memory with a small embedding model
- `cloud_plus`: paid models, hosted embeddings, and stronger document understanding
- `team`: shared memory, permissions, audit, and business-system integration

## How To Choose

Use `free` when the user is just starting, wants transparency, or lacks API keys.

Use `local_plus` when the user has many documents and cares about privacy.

Use `cloud_plus` when document quality, long-context reasoning, OCR, or lower setup friction matters more than API cost.

Use `team` when multiple people share memory or the workflow touches customer records, HR, finance, contracts, CRM, ERP, or audit requirements.

## After Generation

Open the generated `README.md`, then inspect:

- `route-map.md`
- `cost-and-model-plan.md`
- `permission-plan.md`
- `tool-plan.md`
- `memory/index.md`
- `openclaw/` or `hermes/`

Verify:

```bash
agent-launchpad verify ./first-business-agent
```

## Safety Rules

- Do not let the generated agent send messages, submit forms, delete files, change CRM/accounting records, approve payments, or store sensitive data without explicit user approval.
- Keep Markdown object memory as the human-readable source of truth.
- For paid models, hosted embeddings, cloud OCR, or managed vector databases, explain the benefit and tradeoff before enabling them.
- Treat legal, finance, HR, customer-impacting, and executive work as review-support workflows, not autonomous decision workflows.
