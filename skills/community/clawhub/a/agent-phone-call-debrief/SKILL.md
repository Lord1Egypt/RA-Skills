---
name: agent-phone-call-debrief
displayName: "Agent Phone Call Debrief"
version: "1.0.0"
description: "Debrief after an AI agent phone call — compare outcome to goal, capture commitments, flag escalations, and produce follow-up tasks and CRM-ready notes."
triggerKeywords:
  - agent phone call debrief
  - post call debrief agent
  - after phone call summary
  - call outcome report
  - agent call notes
  - phone call follow up
  - call debrief template
  - polly call summary
  - inbound call debrief
  - outbound call recap
tags:
  - agent-phone-call
  - customer-service
  - booking
  - inbound-call
  - debrief
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Agent Phone Call Debrief

## Purpose

Turn raw **post-call inputs** (transcript, agent summary, user notes, or “the call just ended”) into a structured **debrief** — outcome vs goal, commitments, risks, and next actions. Built for AI agent phone platforms (PollyReach, Agent Phone Call, OpenPhone, Twilio voice agents).

Pairs with **phone-call-prep-brief** (pre-call). This skill handles **after-call**.

Does **not** place calls, record calls, or access telephony APIs.

## When to use

Use when:

- An AI agent finished an outbound or inbound phone call
- The user pastes a transcript or agent-generated call summary
- Booking, support, or scheduling calls need follow-up tasks
- The user asks “how did the call go?” or wants CRM notes

## Safety and boundaries

**Do not** invent facts not present in the provided transcript/summary.

**Do not** request passwords, full payment card numbers, or government IDs.

**Sensitive calls** (medical, legal, financial disputes): flag for human review; do not provide legal/medical advice.

**Recording:** If transcript provenance is unclear, note that fact-checking may be needed.

Mark uncertain extractions with `[unclear]` or `[verify]`.

## Required inputs

Ask only what’s missing:

1. **Call direction** — outbound, inbound, or callback.
2. **Original goal** — from prep brief or one sentence (what success meant).
3. **Call artifact** — transcript, bullet summary, or user recap (required).
4. **Counterparty** — who was called or who called (role/org).
5. **Outcome signal** — user’s gut: success / partial / failed / unknown.

## Workflow

1. Parse artifact for: stated outcome, commitments, dates/times, names, reference numbers, objections.
2. Compare against original goal → **verdict** (met / partial / missed).
3. Output debrief (format below).
4. List **follow-ups** with owner (user / agent / human) and due hints.
5. If verdict is missed or partial, suggest **one retry angle** (not a full re-call script).

## Output format

### Call debrief — {counterparty or role}

| Field | Value |
|-------|-------|
| Direction | outbound / inbound / callback |
| Goal | … |
| Verdict | met / partial / missed |
| Duration | if known |
| Reference #s | confirmation, ticket, reservation ID |

#### What happened (3–5 bullets)

Factual, sourced from transcript. No fluff.

#### Commitments made

| Who | Commitment | When | Confidence |
|-----|------------|------|------------|
| Agent | … | … | high / verify |
| Other party | … | … | high / verify |

#### Risks & escalations

- Promises that exceed authority
- Hostile/abusive interaction
- Compliance issues (recording consent, PII spoken aloud)
- Items marked `[verify]`

#### Follow-up tasks

- [ ] Task — owner — due (relative or date)

#### CRM / ticket note (copy-paste)

≤120 words, third person, past tense.

#### Retry recommendation (if partial/missed)

One paragraph: what to change before a second attempt.

## Quality bar

- **Grounded** — every commitment traces to transcript text.
- **Actionable** — follow-ups have owners, not “monitor situation.”
- **Honest verdict** — partial when only some must-cover items landed.
- **Concise CRM note** — scannable in a ticket system.

## Examples

**Good commitment row:** Agent — “Table for 4 Tuesday 7pm under Taboada” — Tue 7pm — high (confirmed twice in transcript).

**Bad commitment row:** Agent — “Reservation handled” — soon — high (too vague).

**Good follow-up:** `[ ] Email restaurant confirmation screenshot to user — agent — within 1h`

**Bad follow-up:** `[ ] Follow up on reservation`
