# AANA Meeting Summary Checker Skill

Use this skill when an OpenClaw-style agent may summarize a meeting, create notes, extract action items, assign owners, set dates, list decisions, or share meeting follow-ups.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or run a checker on its own.

## Core Principle

Meeting summaries should stay grounded in the transcript, notes, chat, agenda, calendar invite, or other available evidence. The agent should not invent decisions, owners, dates, commitments, attendees, or claims.

The agent should separate:

- transcript-backed facts,
- inferred summaries,
- uncertain or missing details,
- proposed action items,
- confirmed action items,
- unsupported claims that need evidence,
- follow-ups that need user or participant confirmation.

## When To Use

Use this skill before:

- producing meeting notes or summaries,
- extracting decisions, risks, blockers, or open questions,
- assigning action item owners,
- assigning due dates or timelines,
- attributing claims to people,
- sending meeting follow-ups,
- updating docs, tickets, tasks, CRM records, calendars, project plans, or public notes from meeting content.

## Summary Status

Classify the proposed meeting output:

- `ready`: grounded, scoped, and ready to share.
- `needs_transcript`: source transcript, notes, chat, or evidence is missing.
- `needs_owner_confirmation`: owner assignments are inferred or unclear.
- `needs_date_confirmation`: due dates, timelines, or meeting dates are missing or inferred.
- `needs_claim_evidence`: claims, decisions, or commitments lack transcript support.
- `needs_redaction`: private or sensitive content should be removed.
- `needs_review`: high-impact, customer-facing, legal, financial, HR, medical, or public notes need review.
- `block_share`: unsafe, unauthorized, private, or materially unsupported summary.

## AANA Meeting Summary Loop

1. Identify the meeting source: transcript, notes, chat, agenda, calendar event, recording, or user-provided summary.
2. Identify the requested output: summary, minutes, action items, decisions, follow-up email, ticket updates, or public notes.
3. Check evidence: each material claim, decision, action item, owner, and date should trace to available evidence.
4. Check attribution: do not assign statements or commitments to people unless supported.
5. Check owners: mark owners as confirmed, inferred, missing, or needs confirmation.
6. Check dates: mark dates as confirmed, inferred, missing, or needs confirmation.
7. Check privacy: remove sensitive personal, account, customer, HR, legal, health, financial, or confidential content not needed.
8. Check audience: internal notes, participant follow-up, customer email, task tracker, or public page.
9. Choose action: accept, revise, ask, retrieve, request confirmation, route to review, or block sharing.

## Required Checks

Before sharing or applying meeting notes, verify:

- meeting source,
- output type,
- evidence status,
- action item status,
- owner status,
- date status,
- claim attribution status,
- privacy status,
- audience and sharing scope,
- recommended action.

## Evidence Rules

Do not present as fact unless supported:

- decisions,
- commitments,
- action items,
- owners,
- due dates,
- deadlines,
- budgets,
- approvals,
- risks,
- blockers,
- technical claims,
- customer statements,
- policy statements,
- legal, medical, financial, HR, or compliance implications.

If evidence is missing, label the item as unclear or ask for confirmation.

## Action Item Rules

For each action item, include:

- task,
- owner,
- due date or timing,
- source evidence or confidence,
- status: confirmed, inferred, missing owner, missing date, or needs confirmation.

Do not assign an owner because a person was mentioned nearby. Do not invent due dates from urgency language unless the transcript clearly states one.

## Attribution Rules

Do not attribute a statement to a person unless the source supports it.

Use neutral language when attribution is uncertain:

- "The group discussed..."
- "The notes mention..."
- "Owner unclear..."
- "Date not stated..."
- "Needs confirmation..."

## Privacy Rules

Before sharing notes, remove or minimize:

- private personal details,
- customer or account data,
- employee, HR, candidate, student, patient, legal, financial, or support details,
- secrets, credentials, internal URLs, private links, or incident details,
- unrelated transcript content,
- off-topic chat or side remarks.

Use redacted summaries when full transcript details are not needed.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `meeting_source`
- `output_type`
- `summary_status`
- `evidence_status`
- `action_item_status`
- `owner_status`
- `date_status`
- `claim_attribution_status`
- `privacy_status`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If notes, action items, owners, dates, and claims are grounded and privacy-safe, accept.
- If source evidence is missing, ask for transcript, notes, chat, or meeting context.
- If owners or dates are inferred, request confirmation or mark them clearly.
- If claims are unsupported, revise or retrieve evidence.
- If private content appears, redact before sharing.
- If the output affects customers, HR, legal, medical, financial, compliance, public docs, or executive reporting, route to review.
- If the summary is unauthorized, privacy-violating, or materially unsupported, block sharing.
- If a checker is unavailable or untrusted, use manual meeting-summary review.

## Output Pattern

For meeting-summary work, prefer:

```text
AANA meeting summary check:
- Source: transcript / notes / chat / agenda / calendar / user_summary / unknown
- Output: summary / minutes / action_items / decisions / follow_up / task_updates
- Evidence: sufficient / partial / missing / conflicting / unknown
- Action items: confirmed / inferred / missing / needs_confirmation / none
- Owners: confirmed / inferred / missing / unclear
- Dates: confirmed / inferred / missing / unclear
- Claims: supported / partial / unsupported / attribution_unclear
- Privacy: clear / needs_redaction / sensitive / unknown
- Decision: accept / revise / ask / retrieve / request_confirmation / route_to_review / block
```

Do not include this check in the user-facing answer unless confirmation, review, redaction, or an evidence boundary needs to be explained.
