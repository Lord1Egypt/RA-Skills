---
name: aport-handoff
description: >
  Package completed work for handoff to another agent or a human.
  Every item in the handoff must have a verified APort decision.
  The handoff document is verifiable — not a summary of what you
  think you did, but proof of what APort confirmed you delivered.
license: Apache-2.0
compatibility: Any AI agent or coding assistant with HTTP access
metadata:
  author: uchibeke
  version: 1.0.0
  tags: ai-agent, handoff, decisions, multi-agent, aport, verification
---

# /aport-handoff — Verified Work Package

A handoff is a promise. This skill makes that promise verifiable.
Every item in an APort handoff is backed by a signed APort decision.
The recipient — human or agent — can independently verify every claim.

## When to use this skill

- When passing work to another agent in a pipeline
- When completing your part of a multi-agent workflow
- When handing a feature to a human for final review
- When a sprint or milestone is complete and needs sign-off
- When onboarding a new agent to a codebase you've been working on

## Prerequisites

You must have an APort passport and completed tasks with ALLOW decisions.
Tasks without verified decisions cannot be included in a verified handoff.

If you don't have a passport:
- **Web:** https://aport.id
- **CLI:** `npx aport-id`
- **Agent skill:** Read https://aport.id/skill and follow the instructions

## Step 1 — Identify what to hand off

Ask the user or determine from context:
- What is the scope? (PR, feature, sprint, project)
- Who is the recipient? (human, another agent, a team)
- What time window? (today, this week, this sprint)

## Step 2 — Fetch verified decisions for the scope

```
GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
```

Filter to decisions where `allow: true` within the relevant time window.
Only ALLOW decisions are included in a handoff.
DENY decisions indicate incomplete work — surface these separately as blockers.

## Step 3 — Build the handoff document

```markdown
# Handoff — [SCOPE] — [DATE]
**From:** [YOUR AGENT NAME] (aport.id/passport/YOUR_SLUG)
**To:** [RECIPIENT]
**APort verification:** All items below have signed decisions

---

## Completed Work

### [task description or title]
**Summary:** [from verification context]
**Output type:** [code / document / analysis / plan]
**Completed:** [decision created_at]
**Decision:** [decision_id] — verify at https://aport.io/api/verify/decisions/get/[decision_id]

Evidence provided:
- [criterion 1]: [evidence string from attestation]
- [criterion 2]: [evidence string from attestation]

---

[repeat for each completed item]

---

## Not Included (Incomplete)

The following tasks were attempted but not verified complete:

| Task | Last attempt | Blocked on |
|------|-------------|------------|
| [description] | [time] | [reason code from deny decision] |

These require attention before they can be handed off.

---

## What the recipient needs to know

[Contextual notes — dependencies, known issues, next steps, decisions made]
[Write this section yourself based on what the recipient needs]

---

## Verification

All decisions in this handoff are cryptographically signed by APort.
Verify any decision:
  GET https://aport.io/api/verify/decisions/get/DECISION_ID

Issuing agent passport:
  https://aport.id/passport/YOUR_SLUG
```

## Step 4 — Deliver the handoff

Offer to deliver the handoff document through available channels:
- Save to a file (e.g. `handoff-[date].md`)
- Open a GitHub issue or PR description
- Post to Slack or Discord (with user permission)
- Send via any messaging tool available as an MCP tool

Always save a local copy regardless of delivery method.

## What makes a handoff invalid

A handoff is invalid if:
- It includes tasks without APort decisions
- It claims completion for tasks still showing DENY
- The decision_ids cannot be verified at the APort API
- The issuing agent's passport is suspended

If any of these conditions apply, surface them clearly rather than
including unverified items in the handoff.

## Tone

Handoffs are functional documents. No padding.
State what was done, what wasn't done, and what the recipient needs to know.
The decision trail is the credibility — the prose is just navigation.

## Links

- Create a passport: https://aport.id (web) or `npx aport-id` (CLI) or https://aport.id/skill (agent)
- Your decisions: GET https://aport.io/api/verify/decisions/YOUR_AGENT_ID
- Verify a decision: GET https://aport.io/api/verify/decisions/get/DECISION_ID
- Your passport: https://aport.id/passport/YOUR_SLUG
