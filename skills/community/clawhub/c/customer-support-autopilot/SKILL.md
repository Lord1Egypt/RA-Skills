---
name: customer-support-autopilot
description: Classify customer support tickets, draft accurate responses, suggest macros, and route escalations based on risk, SLA, and business impact.
metadata: {"openclaw":{"emoji":"🎧"}}
---

# Customer Support Autopilot

## Purpose

Improve support response speed and consistency while reducing risk.

## Core capabilities

- classify incoming tickets by intent/severity
- draft response suggestions in brand tone
- propose macro usage and next actions
- route to L1/L2/L3 based on policy
- detect risky cases (legal, security, billing, fraud, abuse)

## Guardrails

- never invent policy promises
- never disclose sensitive internal info
- escalate regulated/high-risk cases immediately
- include reference IDs when available

## Workflow

1. Parse ticket and extract entities.
2. Classify category + urgency.
3. Draft response with confidence level.
4. Recommend escalation path and SLA.
5. Output macro + notes for agent.

## Output format

1. category + severity
2. draft response
3. escalation recommendation
4. SLA target + required follow-up

## Setup

Read [setup.md](setup.md).

## Examples

See [examples.md](examples.md).

