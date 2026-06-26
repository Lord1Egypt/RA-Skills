---
name: aport-standup
description: >
  Generate a standup update from your APort policy decisions.
  Shows what you actually shipped — not what you remember shipping.
  Driven by signed APort decisions, not by memory or estimates.
license: Apache-2.0
compatibility: Any AI agent or coding assistant with HTTP access
metadata:
  author: uchibeke
  version: 1.0.0
  tags: ai-agent, standup, decisions, aport, retrospective, accountability
---

# /aport-standup — What Did You Actually Ship?

Most standup updates are written from memory. This one is written from decisions.
APort policy decisions are cryptographically signed records of what you
delivered, when, and what evidence you provided. This skill turns those decisions
into a standup update.

## When to use this skill

- At the start of a work session ("what did I do yesterday?")
- At the end of a work session ("what did I ship today?")
- When a user asks "what have you been doing?"
- Before a team sync or status update
- As input to a weekly retrospective

## Prerequisites

You must have an APort passport. If you don't have one:
- **Web:** https://aport.id
- **CLI:** `npx aport-id`
- **Agent skill:** Read https://aport.id/skill and follow the instructions

You need `APORT_AGENT_ID` in your environment.

## Step 1 — Fetch your recent decisions

```
GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
```

This returns your decision history — every policy verification result,
signed and timestamped.

## Step 2 — Parse the decisions

Each decision includes:
```json
{
  "decision_id": "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",
  "allow": true,
  "policy_id": "deliverable.task.complete.v1",
  "created_at": "2026-03-13T09:00:00Z",
  "agent_id": "ap_...",
  "reasons": [
    { "code": "capability_verified", "message": "...", "severity": "info" }
  ],
  "signature": "..."
}
```

Filter to recent decisions based on the standup window.
Sort by `created_at` descending. Group by policy_id if multiple types present.

## Step 3 — Generate the standup

Format the standup based on what the user needs:

### Daily standup (default)

```
STANDUP — [DATE] — [AGENT NAME]

COMPLETED (verified by APort)
  - [task context from decision] — [decision_id] — [time]
  - [task context from decision] — [decision_id] — [time]

DENIED / IN PROGRESS
  - [decision_id] — blocked on [reason code] — [time of last attempt]

STATS
  - Tasks completed: X
  - Tasks attempted: Y
  - Completion rate: Z%
```

### Weekly summary

```
WEEK OF [DATE RANGE] — [AGENT NAME]

SHIPPED
  [list of allow decisions with context]

BLOCKED
  [list of deny decisions, most recent reason code]

PATTERNS
  [most common deny reason if any — signals systemic issue]

DECISION TRAIL
  [list of decision_ids for audit — one per line]
```

### Team standup (multiple agents)

If the user has multiple agents with APort passports, offer to generate
a combined standup by fetching decisions for each agent_id.

## Step 4 — Highlight blockers

If any tasks were denied in the time window, surface them prominently:

```
BLOCKERS REQUIRING ATTENTION
  - [decision_id] — denied — [reason code]
    This task needs: [what the reason code indicates]
```

Repeated denials on the same policy signal something needs human attention.
A task denied more than 3 times should always be surfaced.

## Step 5 — Offer the decision trail

At the end of any standup, offer:
```
Decision IDs for audit:
  dec_001 — allow — deliverable.task.complete.v1 — 2026-03-13T09:00:00Z
  dec_002 — allow — deliverable.task.complete.v1 — 2026-03-13T11:30:00Z
```

These decision_ids are cryptographically signed. The user or any
auditor can verify them independently at:
```
GET https://aport.io/api/verify/decisions/get/DECISION_ID
```

## Tone

Keep standups factual and brief. No padding. No "I worked hard on".
The decisions speak. The standup reports what the decisions say.

Good: "Implemented OAuth2 refresh token flow — PR #47"
Bad: "Spent significant time working on the authentication system"

## Links

- Create a passport: https://aport.id (web) or `npx aport-id` (CLI) or https://aport.id/skill (agent)
- Your decisions: GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
- Verify a decision: GET https://aport.io/api/verify/decisions/get/DECISION_ID
- Your passport: https://aport.id/passport/YOUR_SLUG
