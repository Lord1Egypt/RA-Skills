# Engineering Workflow — 12-Step Reference

> Extends the 9-step build-protocol with 3 engineering-specific gates:
> Schema Design (step 4), API Contract (step 5), Deploy Runbook (step 11), Rollback Plan (step 12).

---

## Step 1 — Requirements

**Output**: Requirements doc (can be lightweight — 1 page is fine)

Checklist:
- [ ] Problem statement in ≤3 sentences
- [ ] Explicit non-goals listed (what this project will NOT do)
- [ ] Success criteria defined (measurable, not "it works")
- [ ] Constraints captured: latency budget, scale target, compliance requirements
- [ ] Stakeholders and decision-makers identified

**Exit gate**: Team agrees on scope before architecture begins.

---

## Step 2 — Design Doc D1 (System Architecture)

**Output**: `D1-architecture.md`

Checklist:
- [ ] System context diagram (what external systems connect here)
- [ ] Component diagram (services, databases, queues)
- [ ] Data flow for the primary happy path
- [ ] Authentication boundary clearly marked
- [ ] Why This Way: why this architecture over the 2 most obvious alternatives
- [ ] Open Questions with owners and deadlines

**Exit gate**: D1 reviewed and signed off. No code written before this.

---

## Step 3 — Design Docs D2-DN (Per-Subsystem)

**Output**: One `D[N]-<subsystem>.md` per major subsystem

Checklist for each D[N]:
- [ ] Goal + Non-Goals
- [ ] API surface (exact schema, not pseudocode)
- [ ] DB schema with column types and constraints
- [ ] Error codes and HTTP statuses
- [ ] Auth rules (who can call what)
- [ ] Observability: metrics + log fields + alert thresholds
- [ ] Alternatives Rejected (≥2, with concrete reasons)
- [ ] Migration Plan (if modifying existing system)
- [ ] Rollback Plan (how to undo)

**Exit gate**: All D[N] docs reviewed. API surfaces agreed across subsystem boundaries.

---

## Step 4 — Schema Design

**Output**: Migration files (`001_initial.sql`, `002_add_column.sql`, etc.)

Checklist:
- [ ] Migration files numbered sequentially
- [ ] Each migration is reversible (has `DOWN` path or snapshot strategy)
- [ ] FK order correct: parent tables created before child FK references
- [ ] Indexes on all foreign keys and common WHERE conditions
- [ ] For PG partitioned tables: `ALTER TABLE` targets parent, not partition
- [ ] Column types match TypeScript interface types (NUMERIC → `parseFloat`, BIGINT → `parseInt`)
- [ ] No default values that will cause silent data migration failures

**Exit gate**: Run migrations on a copy of prod data. Zero errors. Zero lost rows.

---

## Step 5 — API Contract

**Output**: OpenAPI spec or equivalent typed schema file

Checklist:
- [ ] Every endpoint has exact request body schema
- [ ] Every endpoint has exact response body schema (including error responses)
- [ ] Error response format is consistent across all endpoints
- [ ] Auth requirements documented per endpoint
- [ ] Rate limits documented
- [ ] Versioning strategy decided (`/v1/` prefix vs header vs none)
- [ ] Breaking vs non-breaking change criteria defined

**Exit gate**: Both frontend and backend teams sign off on the contract before either writes a line of code.

---

## Step 6 — Plan

**Output**: Task breakdown with owners and critical path

Checklist:
- [ ] Tasks broken down to ≤1 day per task
- [ ] Dependencies identified (what blocks what)
- [ ] Critical path identified
- [ ] Sub-agent assignment: each agent gets ≤3000 chars of context
- [ ] Parallel tasks confirmed to have zero shared file writes
- [ ] Estimated total effort vs deadline — are they compatible?

**Exit gate**: Plan reviewed. No task is "TBD". No two parallel tasks touch the same files.

---

## Step 7 — Prepare (Sub-Agent Specs)

**Output**: Per-agent task instructions (self-contained, ≤3000 chars each)

Each sub-agent instruction must include:
1. **Goal**: one sentence
2. **Output**: exact file path + format
3. **Content**: key information provided directly (don't make the agent read large files)
4. **Constraints**: what NOT to do
5. **Acceptance criteria**: measurable completion conditions

**Exit gate**: All specs reviewed by coordinator. No spec has "see the design doc for details" — key info is inline.

---

## Step 8 — Execute (Code + Tests)

**Output**: Code + unit tests

Rules:
- ≤2 sub-agents writing code in parallel at any time
- Jitter second sub-agent start by 1-3 seconds (avoid thundering herd)
- Each sub-agent writes to separate modules / files (zero shared write targets)
- Unit test coverage for all error paths (not just happy path)
- No TODO/FIXME without a tracking issue number

**Exit gate**: All tests pass. No broken imports. No hardcoded secrets.

---

## Step 9 — Review (PR Review)

**Output**: PR review comments + approval

Rules:
- Reviewer must be a different agent / context than the implementer
- Review checklist (minimum):
  - [ ] Does code match the D[N] API contract exactly?
  - [ ] Are all error paths handled?
  - [ ] Are secrets / credentials handled via env vars?
  - [ ] Are DB queries using the correct column names from the schema?
  - [ ] No `console.log` / debug artifacts left in
- Reviewer states at least 1 concern or improvement, even for clean PRs

**Exit gate**: PR approved by reviewer who was not the implementer.

---

## Step 10 — Audit ⚠️ UNMISSABLE

**Output**: Audit report with 🔴 / 🟡 / 🟢 findings

Run `references/audit-script-engineering.sh` first (machine checks), then human audit:

Security audit:
- [ ] Auth bypasses (unauthenticated routes that should be protected)
- [ ] SQL injection / query injection
- [ ] Secrets not in code
- [ ] Input validation on all external-facing parameters

Performance audit:
- [ ] N+1 queries (loop that calls DB per row)
- [ ] Missing indexes on common WHERE conditions
- [ ] Unbounded queries (no LIMIT clause)

Consistency audit (use script):
- [ ] Env var names consistent across all config files
- [ ] DB column names consistent from SQL → query layer → TypeScript interface
- [ ] API paths consistent: backend route ↔ frontend fetch ↔ design doc

**Exit gate**: All 🔴 findings fixed. 🟡 findings either fixed or deferred with tracking issue. Deploy is blocked until this step passes.

---

## Step 11 — Deploy Runbook

**Output**: `runbook-v<N>.md`

A runbook is not documentation — it is a step-by-step operational script with:
- [ ] Pre-deploy checklist (env vars set, DB migrated, smoke test passing on staging)
- [ ] Numbered deploy steps (not "deploy the service" — exact commands)
- [ ] Verification checkpoint after each step (what to check to confirm success)
- [ ] Rollback trigger: exactly what condition means "stop and roll back"
- [ ] Who to notify at each stage
- [ ] Estimated time per step

**Exit gate**: Runbook dry-run on staging. Another person reads the runbook and can execute it without asking questions.

---

## Step 12 — Rollback Plan + Canary Deploy

**Output**: Rollback plan doc + canary deploy execution

Canary rules:
1. Route ≤10% traffic to new version
2. Monitor for ≥15 minutes: error rate, latency P99, DB query time
3. If any metric exceeds threshold → roll back immediately; do not "wait and see"
4. If stable → route 50%, wait 15 min → 100%

Rollback plan must specify:
- [ ] Rollback trigger conditions (exact thresholds, not "if something looks wrong")
- [ ] Rollback steps (numbered, exact commands)
- [ ] DB rollback strategy (if schema migration was included)
- [ ] Communication plan (who gets notified when rollback is triggered)

**Exit gate**: System is healthy at 100% traffic for ≥30 minutes. Runbook archived with the release.

---

_Reference for: build-protocol-engineering SKILL.md Step 12_
_Last updated: 2026-04-30_
