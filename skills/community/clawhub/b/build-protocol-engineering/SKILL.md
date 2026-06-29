---
name: build-protocol-engineering
description: "Rigorous workflow for software engineering projects (design docs, code, deployment). Use when building a multi-module system, API service, or infrastructure project requiring design documents (D1-DN), code review, testing, and deployment. Inherits core rules from build-protocol (≤2 parallel for tightly-coupled code paths, Audit unmissable, Why This Way), adds engineering-specific: 3-layer consistency check (naming↔business↔data), API contract validation, deployment runbook requirement, rollback plan requirement. Machine-verifies: type consistency across layers, API path matches between frontend/backend, database schema matches TypeScript interfaces, env var consistency across config/code/deployment. Triggers on: 'design document', 'API spec', 'deploy plan', 'multi-service system', 'build service', '做设计文档 / 做系统'."
version: 1.0.1
---

# Build Protocol · Engineering

> Software engineering isn't writing a long document — it's building a system that runs correctly in production.
> This skill enforces the discipline to get there without late-night rollbacks.

## When to Use

**Triggers** (any one):
- Building a multi-module system (3+ services / modules)
- Producing D1-DN design documents before implementation
- Deploying to production (runbook required)
- Any PR merge that changes DB schema, API surface, or auth paths
- Explicit requests: "build service", "做系统", "write design doc", "deploy plan", "API spec"

**Don't use for**:
- Pure knowledge-base / textbook production (use `build-protocol`)
- One-off scripts < 100 lines with no deployment
- Read-only analysis with no code output

## Inherits from build-protocol

All 8 iron rules apply unchanged:

| # | Rule |
|---|---|
| 1 | **Independent Audit unmissable** — use a separate agent or separate context |
| 2 | **Plan before Execute** — no code before architecture is agreed |
| 3 | **≤2 parallel sub-agents** for tightly-coupled work (shared codebase, shared schema); up to 4 acceptable for independent file outputs. Conflict points = N(N-1)/2; 4+ on same code = 75% failure |
| 4 | **Why This Way** — rationale before conclusions in every design doc |
| 5 | **Version + Errata** — every deploy has a changelog; silent changes kill trust |
| 6 | **3-layer consistency** — Naming ↔ Business ↔ Data |
| 7 | **Anti-Sycophancy** — every design doc must have ≥1 "Alternatives Rejected" with honest reasons |
| 8 | **Independent review ≠ self-audit** — the implementer cannot audit their own work |

## Engineering-Specific Iron Rules

| # | Rule | Why |
|---|---|---|
| 9 | **3-layer consistency check before every PR** | Naming drift → runtime errors that grep can't catch |
| 10 | **Deployment runbook required before prod deploy** | "I'll figure it out in prod" = 2 AM rollback |
| 11 | **Rollback plan required before PR merge to main** | Without it, every deploy is a one-way door |

## The 12-Step Engineering Workflow

```
1.  Requirements      → Scope, non-goals, constraints
2.  Design Doc D1     → System architecture + data flow
3.  Design Doc D2-DN  → Per-subsystem: API surface, DB schema, auth
4.  Schema Design     → DB migrations, index plan, partition strategy
5.  API Contract      → Exact request/response shapes (OpenAPI or equivalent)
6.  Plan              → Break into tasks, assign owners, identify critical path
7.  Prepare           → Sub-agent specs (≤3000 chars/task, self-contained)
8.  Execute           → Code + unit tests (≤2 parallel sub-agents)
9.  Review            → PR review by a different agent/context
10. Audit             → Security / performance / 3-layer consistency ⚠️ UNMISSABLE
11. Deploy Runbook    → Step-by-step prod deploy with verification checkpoints
12. Rollback Plan     → Canary + rollback trigger conditions + recovery steps
```

See `references/engineering-workflow.md` for detailed per-step checklists.

## Design Doc Series Standard

Every D[N] must contain — no exceptions:

| Section | Requirement |
|---|---|
| Goal | ≤3 sentences; if you can't state it, you don't understand it |
| Non-Goals | Explicitly listed; as important as Goals |
| Architecture Diagram | ASCII or linked image; must be updated when architecture changes |
| API Surface | Exact request/response schema (not "something like {id: ...}") |
| Data Model | DB schema with column types and constraints |
| Error Handling | Named error codes + HTTP status + user-facing message |
| Security | AuthN method, AuthZ rules, trust boundaries |
| Observability | Metrics emitted, log fields, alert thresholds |
| Why This Way | Rationale for key decisions |
| Alternatives Rejected | ≥2 alternatives with concrete reasons for rejection |
| Migration Plan | How existing data/users transition |
| Rollback Plan | How to undo this change if it goes wrong |
| Dependencies | External services, APIs, teams |
| Open Questions | Unresolved items with owners and deadlines |

See `references/design-doc-checklist.md` for the full machine-checkable checklist.

## Machine-Verified Consistency Checks

Before Step 10 (Audit), run `references/audit-script-engineering.sh`:

- **Env var consistency**: `.env.example` ↔ `config/*.ts` ↔ `docker-compose.yml` ↔ k8s ConfigMap
- **DB column naming**: `init.sql` definitions ↔ query layer ↔ TypeScript interfaces
- **API path**: backend route definitions ↔ frontend fetch calls ↔ design doc spec
- **Import paths**: no broken references in the codebase
- **Secrets not in code**: scan for `AKIA`, `sk-`, `ghp_`, hardcoded passwords
- **TODO markers**: all `TODO/FIXME` in `src/` must be tracked issues, not forgotten

**🔴 failures block deploy**. Not suggestions — blockers.

## Rollback / Hotfix Protocol

| Trigger | Action |
|---|---|
| Deploy fails at step N | Stop. Run rollback from step N-1. Do not continue forward. |
| Rollback fails | Escalate immediately. Do not attempt creative fixes in prod. |
| Hotfix needed | Branch from last known-good tag. Patch. Fast-track Audit (L1 + security only). |
| Schema migration breaks | Restore DB from pre-migration snapshot. Investigate before retry. |

**Canary rules**: Route ≤10% traffic to new version first. Wait ≥15 minutes. Check error rate. Proceed or rollback — not both.

## Anti-Patterns

| ❌ Don't | Why |
|---|---|
| Deploy without runbook | "I know what I'm doing" ends careers |
| Merge without rollback plan | Every deploy is now a one-way door |
| Schema change without migration | Silent data corruption is the worst kind |
| Rename variable without grep-verify | One miss = runtime error at 3 AM |
| Add API endpoint without updating D-doc | Drift between docs and code is technical debt you pay with compounding interest |
| Hardcode production secret in code | Git history is forever |
| ALTER TABLE on partition directly (PG) | Only the parent table accepts new columns in partitioned PG tables |
| Parallelize >2 sub-agents on same codebase | Merge conflicts + shared file writes = corrupted state |
| "Mostly works, ship and fix later" | "Later" is another name for "when it breaks in prod" |

## Gotchas

- **PG partition tables**: `ALTER TABLE ... ADD COLUMN` must target the **parent** table, not a partition
- **FK migration order**: child tables' FKs must reference tables created in earlier migrations — order matters
- **Env var naming drift**: `DB_HOST` in `.env.example`, `process.env.DATABASE_HOST` in code = silent undefined at boot
- **SigV4 URL encoding**: `+` encodes to `%2B` in path but `+` (space) in query string — wrong encoder = auth failure
- **`import` vs `require` in mixed TS/JS**: `.js` extension required in ESM `import` even when source is `.ts`
- **Canary traffic split with sticky sessions**: if users are session-pinned, 10% split becomes 0% or 100% per user

## References

- `references/engineering-workflow.md` — 12-step workflow with per-step checklists
- `references/design-doc-checklist.md` — Machine-checkable D[N] sections
- `references/audit-script-engineering.sh` — Bash template for consistency checks

## Related Skills

- `build-protocol` — Parent skill for knowledge/textbook production
- `engineering-discipline` — Coding standards and PR hygiene

---

_Created: 2026-04-30 · Derived from: build-protocol v1.1_
_Validated against: multi-service system post-mortems (schema drift, FK order, env var naming, SigV4 trap)_
