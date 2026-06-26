# AANA Ticket Update Checker Skill

Use this skill before an OpenClaw-style agent updates support tickets, GitHub issues, Linear, Jira, CRM cases, bug reports, tasks, or customer-visible status fields.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or update tickets on its own.

## Core Principle

Ticket updates should be accurate, scoped, evidence-backed, privacy-safe, and authorized before changing state or customer-visible text.

## Required Checks

- exact ticket, project, repository, customer, or case
- update type: comment, status, owner, priority, label, due date, escalation, close, reopen, or customer reply
- evidence for facts, reproduction steps, test results, policy claims, and status
- private data, logs, credentials, account records, and internal notes
- owner, priority, SLA, due date, and escalation authority
- whether the update is internal-only or customer-visible

## Ticket Risk Classes

Treat these as higher risk:

- customer-visible comments, public issue comments, ticket closure, severity changes, SLA changes, escalation changes, and ownership transfers,
- refund, billing, legal, security, outage, incident, compliance, HR, or medical/support-related updates,
- logs, screenshots, account records, customer identifiers, internal notes, or private reproduction data,
- claims about root cause, fix status, test results, deployment status, policy, or expected timeline.

## Evidence Rules

Do not update a ticket with unsupported claims about:

- root cause,
- fix shipped,
- tests passed,
- customer eligibility,
- billing/refund decisions,
- policy exceptions,
- deployment status,
- severity or priority.

Retrieve evidence or mark the update as tentative before changing status or posting externally.

## Visibility Rules

Internal notes can include more diagnostic context than customer-visible replies, but still require minimization. Customer-visible updates must be concise, accurate, non-speculative, and free of internal notes or unrelated data.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `update_type`
- `evidence_status`
- `visibility_status`
- `privacy_status`
- `approval_status`
- `ticket_risks`
- `blocker_reason`
- `safe_alternative`
- `recommended_action`

Do not include full logs, customer records, secrets, internal notes, or unrelated ticket history when a redacted summary is enough.

## Decision Rule

- If facts and scope are clear and the update is low-risk, proceed.
- If evidence, owner, status, priority, or visibility is unclear, ask or retrieve.
- If customer-visible text or irreversible status changes are involved, require approval.
- If private data appears, redact.
- If the update is unauthorized, unsupported, or misleading, block.

## Output Pattern

```text
AANA ticket gate:
- Update: comment / status / owner / priority / close / reopen / customer_reply
- Evidence: sufficient / partial / missing / conflicting
- Visibility: internal / customer_visible / public / unknown
- Privacy: clear / needs_redaction / sensitive / unknown
- Approval: approved / required / unclear / denied
- Decision: proceed / revise / ask / retrieve / redact / request_approval / block
```
