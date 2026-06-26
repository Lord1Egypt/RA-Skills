---
name: agent-audit-log
description: Lightweight operational audit logging for AI assistants, agent workspaces, and personal automation systems. Use when you need a structured way to record high-value actions such as installs, config changes, updates, repository operations, external publishing, secret injection, deletions, export-safety checks, and follow-up risks. Also use when designing or improving an audit trail with JSONL logs, risk levels, target indexes, human summaries, and open-item tracking.
---

# Agent Audit Log

Create and maintain a lightweight audit trail for high-value actions.

## Core rule
Log only actions that matter for safety, traceability, or later review. Do not turn the audit log into noise.

## Default layers
1. Raw fact log (`YYYY-MM-DD.jsonl`)
2. Date summary (`index.json`)
3. Target/project index (`by-target.json`)
4. Risk index (`by-risk.json`)
5. Human-readable summary (`latest.md`)
6. Export-safety events (`export_safety_check`)
7. Open items (`open-items.json`)
8. Status transition history (`open-items-history.json`)

## Read references as needed
- Read `references/schema.md` for the log schema and event fields.
- Read `references/risk-model.md` for how to classify low / medium / high risk.
- Read `references/export-safety.md` before logging publish/export actions.
- Read `references/open-items.md` when tracking unresolved risks or follow-up work.
- Read `references/examples.md` when you need concrete event, export-safety, or open-item examples.

## Use scripts as needed
- Use `scripts/init_audit.sh` to create the basic audit directory and starter files.

## Operating rules
- Do not store plaintext secrets in audit logs.
- Prefer concise, human-readable summaries.
- Record target, result, and non-sensitive references.
- Use `warn` when something needs attention but did not fail.
- Use open items for follow-up risk, not for routine noise.
