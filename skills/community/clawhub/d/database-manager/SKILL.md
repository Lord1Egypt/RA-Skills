---
name: Database Manager
slug: database-manager
version: 1.0.0
homepage: https://clawic.com/skills/database-manager
description: Plan, operate, and recover relational databases with schema governance, safe migrations, backup drills, and incident response playbooks.
changelog: Initial release with schema governance rules, migration safety checks, backup recovery workflows, and on-call response templates.
metadata: {"clawdbot":{"emoji":"🗄️","requires":{"bins":[],"config":["~/database-manager/"]},"os":["linux","darwin","win32"],"configPaths":["~/database-manager/"]}}
---

## Setup

On first use, read `setup.md` for local initialization, activation preferences, and operating defaults.

## When to Use

User needs a reliable database operating system for schema design, query hygiene, migration rollout, and recovery readiness.
Agent keeps data work safe by enforcing preflight checks, explicit rollback plans, and incident-ready runbooks.

Use this skill when database changes can affect production reliability, latency, or data integrity.

## Architecture

Memory lives in `~/database-manager/`. See `memory-template.md` for the base structure.

```
~/database-manager/
├── memory.md                  # Durable context and operating preferences
├── inventory.md               # Systems, engines, owners, and critical datasets
├── standards.md               # Naming, indexing, and schema conventions
├── migrations.md              # Planned and executed migration records
├── backups.md                 # Backup schedule, retention, and restore drills
├── incidents.md               # Incident timeline, mitigations, and follow-up
└── archive/
    ├── migrations-YYYY-MM.md  # Closed migrations by month
    └── incidents-YYYY-MM.md   # Closed incidents by month
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory template | `memory-template.md` |
| Inventory and ownership model | `inventory-and-governance.md` |
| Query operations and change windows | `query-operations.md` |
| Migration and release controls | `migration-and-release.md` |
| Backup and recovery workflows | `backup-and-recovery.md` |
| Incident response sequence | `incident-playbook.md` |
| Reusable templates | `templates.md` |

## Core Rules

### 1. Never Change Production Without a Preflight Packet
Every schema or data change must include:
- intent
- blast radius
- rollback path
- verification query set

Skipping preflight creates unbounded operational risk.

### 2. Separate Read Validation from Write Execution
Validate assumptions with read-only checks first, then run writes in explicit, audited steps.

This prevents accidental broad updates caused by stale predicates or wrong join keys.

### 3. Treat Migrations as Product Releases
Each migration requires:
- owner
- deployment window
- rollback deadline
- post-deploy verification criteria

Schema changes without release discipline are a primary source of prolonged incidents.

### 4. Make Index and Query Trade-offs Explicit
When changing indexes or query plans, state expected impact on:
- read latency
- write throughput
- storage growth

Invisible trade-offs create hidden cost and unpredictable performance regressions.

### 5. Backup Is Not Real Until Restore Is Proven
Do not trust backup status alone.
Run restore drills, validate recovered row counts, and document measured recovery time.

Unverified backups are operationally equivalent to no backups.

### 6. Encode Safety Gates for Destructive Operations
Before `DROP`, `TRUNCATE`, broad `DELETE`, or bulk `UPDATE`:
- confirm table and environment
- capture row count baseline
- require explicit user confirmation
- log exact rollback route

Destructive steps without safety gates can permanently corrupt business data.

### 7. Close Every Incident with Durable Learning
After mitigation:
- capture root cause
- record missing guardrail
- add one concrete prevention change

Without closure rules, the same incident class repeats.

## Common Traps

- Running updates without a restrictive predicate -> unintended mass writes and long rollback windows.
- Shipping migrations without timing and lock analysis -> production latency spikes and blocked transactions.
- Assuming replica lag is harmless -> stale reads and misleading verification outcomes.
- Declaring backup success without restore drills -> false confidence during outages.
- Fixing incidents without permanent guardrails -> repeated operational failures.

## Security & Privacy

**Data that leaves your machine:**
- None by default.

**Data that stays local:**
- Database operating context and records under `~/database-manager/`.

**This skill does NOT:**
- Execute destructive commands without explicit user confirmation.
- Access unrelated credentials or services by default.
- Store secrets in memory files.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `sql` - SQL query authoring and analysis
- `mysql` - MySQL-specific workflows and troubleshooting
- `prisma` - Prisma schema and migration tooling
- `sqlite` - local database workflows and prototyping
- `backend` - backend architecture and service delivery

## Feedback

- If useful: `clawhub star database-manager`
- Stay updated: `clawhub sync`
