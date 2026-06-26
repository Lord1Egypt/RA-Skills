---
name: aegis
description: >
  AI Development Quality Guardian — contract-driven, design-first quality guardrails
  for AI-assisted full-stack development. Five-layer defense: Design → Contract →
  Implementation → Verification → PM. Prevents project chaos at scale.
  Activate when: starting a feature, setting up a project, dispatching coding tasks,
  reviewing PRs, or managing multi-agent workflows. Also triggers on projects with
  a contracts/ directory (implementation guardrails auto-activate).
---

# Aegis — AI Development Quality Guardian

> Five-layer defense for AI-assisted software development.

## Modes

### Lite Mode (Default for small tasks)
- Design Brief only → straight to implementation
- Use when: solo dev, single-service feature, quick fix

### Full Mode (Multi-service / team projects)
- Complete contract-first workflow
- Use when: multiple API boundaries, team collaboration, complex features

---

## Phase 0: Workspace Architecture Detection

Before starting the Aegis workflow, detect the project architecture to choose the right contract strategy.

### Auto-Detection

Scan the workspace for indicators:
- Both `frontend/`/`client/`/`web/` AND `backend/`/`server/`/`api/` directories → **Monorepo**
- `package.json` with workspaces containing both frontend and backend → **Monorepo**
- Only one side present (pure frontend or pure backend) → **Split Workspace**

### If Split Workspace detected, ask the human:
```
Detected: This workspace contains only {frontend|backend} code.
Where does the other side live?

(a) Another repo managed by the same agent (I can access it)
(b) Another repo managed by a different agent/workspace (I cannot access it)
(c) This is actually a monorepo (I missed something)
```

### Architecture Modes

| Mode | Contract Location | Sync Method |
|------|------------------|-------------|
| **Monorepo** | `contracts/` in project root | Direct (same repo) |
| **Multi-Repo, Single Agent** | Lead workspace's `contracts/`, copied to each repo | Copy before dispatch |
| **Cross-Agent, Cross-Workspace** | Dedicated contract repository | Git submodule / package / lead copy-sync |

**Cross-Workspace:** Contract lives in an independent Git repo. Each agent's workspace integrates it as read-only. Contract Change Requests go through the Lead who has merge rights. See `references/multi-agent-protocol.md` for the full protocol.

---

## Phase 1: Design

Before any non-trivial feature, create a Design Brief:

1. Read `templates/design-brief.md` for the template
2. Fill in: Problem Statement, Architecture Overview, Key Decisions, Module Boundaries, API Surface, Known Gaps, Testing Strategy
3. Submit for human review
4. **Gate:** Do not proceed to Phase 2 until Design Brief is approved

**Lite Mode stops here** — proceed to Phase 3 after Design Brief approval.

## Phase 2: Contract (Full Mode)

Define the API contract before writing implementation code:

1. Create/update `contracts/api-spec.yaml` (OpenAPI 3.1) — use `templates/api-spec-starter.yaml` as base
2. Create/update `contracts/shared-types.ts` — use `templates/shared-types-starter.ts` as base
3. Create/update `contracts/errors.yaml` — use `templates/errors-starter.yaml` as base
4. Run `bash scripts/validate-contract.sh <project-path>` to check consistency
5. **Gate:** Contracts must be reviewed before implementation begins

Reference: `references/contract-first-guide.md` for the full contract-first methodology.

## Phase 3: Implementation

### Pre-Coding Checklist (EVERY TIME before writing code)

1. Check if `contracts/` exists in the project root
2. If yes: read `contracts/api-spec.yaml`, `contracts/errors.yaml`, `contracts/shared-types.ts`
3. Read `CLAUDE.md` for project-specific constraints
4. If a Design Brief exists for your task: read `docs/designs/` relevant file

### Hard Rules (violation = PR rejected)

**R1: Contract is the truth**
- All API responses MUST conform to `contracts/api-spec.yaml`
- Response shapes, status codes, field names — all from the spec

**R2: Shared types — import, never redefine**
- `import { User, ApiResponse } from '../contracts/shared-types'`
- NEVER create local types that shadow contract types
- If shared-types doesn't have what you need → file a Change Request (R5)

**R3: Error codes from registry only**
- Use codes defined in `contracts/errors.yaml`
- Never invent ad-hoc error codes
- Need a new code → file a Change Request (R5)

**R4: Contract tests mandatory**
- Every new API endpoint MUST have a contract test
- Contract test = validate real response against OpenAPI spec schema
- Modified endpoints → update contract test

**R5: Never modify contracts directly**
If the contract needs changes:
1. Create `docs/contract-changes/CHANGE-{date}-{description}.md`
2. Include: what, why, which modules affected
3. Continue implementing with the CURRENT contract
4. Human reviews and updates the contract

**R6: CLAUDE.md constraints**
- Read and follow all ⛔ Hard Constraints in CLAUDE.md
- These are project-specific and override general preferences

**R7: Pre-commit checks are mandatory**
- Run lint → type-check → format-check → contract validation before committing
- After ALL code changes, run formatters as a final step
- Never bypass with `--no-verify`

### Quick Reference

| Situation | Action |
|-----------|--------|
| Need a new endpoint | Check api-spec.yaml first |
| Need a new type | Check shared-types.ts → if missing, Change Request |
| Need a new error code | Check errors.yaml → if missing, Change Request |
| API response doesn't match spec | Fix code, not spec |
| Spec seems wrong | Change Request, implement per current spec |
| No contracts/ directory | Hard rules don't apply — standard development |

## Phase 4: Verification

After implementation, validate quality:

1. Run contract tests — `bash scripts/validate-contract.sh <project-path>`
2. Run frontend tests — `pnpm test` (if frontend exists)
3. Run backend integration tests — HTTP E2E against real server + real DB
4. Generate gap report — `bash scripts/gap-report.sh <project-path>`
5. Review: are all Design Brief items implemented?
6. Review: do all endpoints have contract + integration tests?
7. **Gate:** All tests must pass before PR/MR

### Testing Hierarchy

```
E2E Test          ← Playwright (real browser + real backend)
Integration Test  ← Real HTTP server + real DB (no mocks)
Contract Test     ← Validate against api-spec.yaml (NO mocking the contract)
Frontend Test     ← Vitest + React Testing Library + MSW (contract-typed mocks)
Unit Test         ← Mock external deps, test pure logic
```

### Frontend Testing (when project has frontend)

- **Stack:** Vitest + React Testing Library + MSW
- **Required coverage:** API clients (normal/error/auth), data hooks (loading/success/error), key components
- **MSW handlers:** must mock every backend endpoint with data matching `contracts/shared-types.ts`
- **CI gate:** `pnpm test` must pass — same blocking power as backend tests

### Backend Integration Testing (HTTP E2E)

- **Every endpoint** must have: happy path (200) + bad request (400) + not found (404) + auth failure (401)
- **Real database** — isolated test DB, not mocks. Transactions or migrations for clean state.
- **Mutation verification** — POST/PUT/DELETE → GET to confirm state change
- **CI pipeline:** `lint → type-check → unit → frontend-test → contract → integration → route-coverage → build → E2E`

### Consumer-Driven Route Coverage

Integration tests must cover what the frontend calls, not just what the backend implements.

- **Full mode:** `verify-route-coverage.sh` cross-references frontend API calls with backend routes. Every consumer route needs a backend handler + integration test.
- **Degraded mode:** If no frontend manifest or scannable frontend code exists, CI warns but does not fail. Provider-driven tests remain the baseline.
- **Cross-workspace:** Frontend agent exports `consumer-routes.yaml` to the contract repo. Backend CI validates coverage against it.
- **Route manifest:** `contracts/route-manifest.yaml` — declares every API route the frontend consumes. Auto-generated or manual.

Run after integration tests in CI:
```bash
bash scripts/verify-route-coverage.sh <project-path>
```

### Test Strategy = Design Artifact

Full-stack features require a complete testing strategy **in the Design Brief** before coding begins.

Reference: `references/testing-strategy.md` for the full testing pyramid and standards.

## Phase 5: PM

Track progress and enforce quality gates:

1. Update `docs/designs/<feature>/implementation-summary.md` — use `templates/implementation-summary.md`
2. Mark Design Brief items as completed
3. Note any contract Change Requests filed during implementation
4. Release readiness check: all gates passed?

---

## Project Setup

Initialize Aegis in any project:

```bash
bash scripts/init-project.sh /path/to/project
```

This creates:
- `contracts/` — API spec, shared types, error codes (stack-aware)
- `docs/designs/` — for Design Briefs
- `.aegis/` — portable validation scripts
- `CLAUDE.md` — from Aegis template (if not existing)
- `docker-compose.integration.yml` — auto-detects your database

Set up guardrails (pre-commit hooks + CI):

```bash
bash scripts/setup-guardrails.sh /path/to/project --ci github  # or --ci gitlab
```

---

## Multi-Agent Protocol

When multiple agents work on the same project:
- Each agent reads contracts before starting
- Contracts are the synchronization point — not code
- Change Requests prevent concurrent contract modifications

**Cross-Workspace:** When agents operate in separate workspaces, contract lives in a dedicated repository. Each agent integrates via submodule/package/copy-sync and treats `contracts/` as read-only. Integration testing is orchestrated externally.

Reference: `references/multi-agent-protocol.md`

## File Structure

```
~/.claude/skills/aegis/          # ← You are here (CC skill)
├── SKILL.md                     # This file
├── templates/                   # Project templates
│   ├── design-brief.md
│   ├── claude-md.md
│   ├── api-spec-starter.yaml
│   ├── shared-types-starter.ts
│   ├── errors-starter.yaml
│   ├── contract-test-example.ts
│   ├── docker-compose.integration.yml
│   ├── implementation-summary.md
│   └── route-manifest-starter.yaml  # Consumer route manifest template
├── scripts/                     # Automation
│   ├── init-project.sh          # Initialize Aegis in a project
│   ├── setup-guardrails.sh      # Pre-commit + CI setup
│   ├── detect-stack.sh          # Auto-detect language/framework
│   ├── validate-contract.sh     # Validate contract consistency
│   ├── gap-report.sh            # Design Brief vs implementation gaps
│   ├── generate-types.sh        # Generate types from OpenAPI spec
│   └── verify-route-coverage.sh # Consumer-driven route coverage check
└── references/                  # Deep-dive guides
    ├── contract-first-guide.md
    ├── testing-strategy.md
    └── multi-agent-protocol.md
```
