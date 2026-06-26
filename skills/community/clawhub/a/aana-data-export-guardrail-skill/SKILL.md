# AANA Data Export Guardrail Skill

Use this skill before an OpenClaw-style agent exports, downloads, shares, syncs, copies, uploads, emails, or publishes files, records, datasets, reports, logs, messages, or account data.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or export data on its own.

## Core Principle

Data export should be narrow, authorized, necessary, privacy-safe, and reversible where possible. Broad or sensitive exports require explicit approval and review.

## Required Checks

- exact dataset, files, records, fields, date range, and recipient/destination
- reason the export is necessary
- private data, secrets, personal data, customer data, logs, account records, and regulated information
- authorization, ownership, and sharing permission
- format, redaction, retention, and deletion expectations
- whether a smaller summary, aggregate, or filtered export is enough

## Export Risk Classes

Treat these as higher risk:

- bulk exports, cross-account exports, full inboxes, full logs, full databases, all records, and wildcard file exports,
- external destinations, public links, shared drives, vendor uploads, email attachments, and third-party sync targets,
- personal data, customer records, payment data, health/legal/financial data, HR/student records, secrets, credentials, and incident logs,
- exports with unclear retention, deletion, access control, or audit requirements.

## Scope And Minimization Rules

Do not export more than the task requires. Prefer field-level filtering, date ranges, aggregates, redacted summaries, or counts when full records are unnecessary.

Ask before broad, recursive, bulk, cross-account, external, public, or regulated exports.

## Destination And Retention Rules

Verify who will receive the export, where it will be stored, how long it should persist, and whether the user has authority to share it. If retention is unknown, ask before exporting sensitive data.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `export_type`
- `scope_status`
- `destination_status`
- `privacy_status`
- `approval_status`
- `export_risks`
- `blocker_reason`
- `safe_alternative`
- `recommended_action`

Do not include full records, secrets, logs, customer data, account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If export is narrow, necessary, authorized, and privacy-safe, proceed.
- If scope, recipient, fields, or purpose are unclear, ask.
- If sensitive data is included, redact, narrow, or route to review.
- If broad, bulk, cross-account, or external export is requested, require approval.
- If export is unauthorized, excessive, or privacy-violating, block.

## Output Pattern

```text
AANA data export gate:
- Export: files / records / dataset / logs / report / messages / account_data
- Scope: narrow / broad / bulk / cross_account / unknown
- Destination: local / user / external / public / unknown
- Privacy: clear / needs_redaction / sensitive / regulated
- Approval: approved / required / unclear / denied
- Decision: proceed / narrow / ask / redact / request_approval / route_to_review / block
```
