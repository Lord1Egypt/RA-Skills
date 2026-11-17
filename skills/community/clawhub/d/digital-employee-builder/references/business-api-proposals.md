# Business-Code Modification Proposals

The builder never modifies the business codebase (Core Principle 3 in SKILL.md). When packaging is blocked because the business side lacks an interface, the gap becomes a modification proposal in `docs/business-api-proposals.md` — the contract the employee side builds against and the business team implements against. Required reading when step 1 surfaces interface gaps.

## Contents

- [When a Proposal Is Required](#when-a-proposal-is-required)
- [Proposal Format](#proposal-format)
- [Contract Minimums](#contract-minimums)
- [Lifecycle](#lifecycle)
- [Employee-Side Rules](#employee-side-rules)

## When a Proposal Is Required

Draft a proposal when a capability point's chosen packaging route needs a business-side interface that does not exist or is inadequate:

- A multi-step flow packaged via Pattern A / composite MCP tool, but the API only offers scattered CRUD (no flow-level endpoint) or misses a needed query
- A query the business system computes but does not expose over any interface
- Missing idempotency keys / state fields the employee side needs to operate safely
- A subsystem the user wants exposed as its own MCP server or SDK package

Pattern C full ports rarely need proposals (scripts are self-contained) — the exception is data residency: if script-managed storage must sync with the business database, propose the export/sync interface here.

Never route around a missing interface with sys.path hacks, direct DB access from the employee side, or screen scraping — propose the interface instead.

## Proposal Format

One section per proposal (template: `assets/workspace/business-api-proposals.md.tmpl`):

| Field | Content |
|---|---|
| ID / title | Stable ID (e.g. `BP-001`) referenced by the capability inventory and the MCP tool list |
| Status | Lifecycle state (see below) |
| Source capability point | The inventory entry this proposal unblocks |
| Current state | What exists today and why it is insufficient — cite endpoints, tables, or source files |
| Proposed change | The interface to add: REST endpoint (`POST /refunds`), query exposure, MCP server module, SDK package |
| Contract | The full agreement (see Contract Minimums) |
| Rationale & alternatives | Why this shape; what was rejected and why (e.g. "Pattern C port rejected: refund records must stay in the business DB") |
| Employee-side impact | Which MCP tools / scripts depend on it; the stub plan |
| Confirmed by / date | Who approved it at Gate 1 and when |

## Contract Minimums

Every proposed interface must pin down, at minimum:

1. **Shape**: HTTP method + path, or MCP tool name, or SDK module + function.
2. **Request**: every parameter's name, type, constraints, valid values/enums, required vs. optional.
3. **Response**: success schema field by field; list endpoints include pagination fields.
4. **Errors**: enumerated error codes with meaning (e.g. `INVALID_STATE`, `AMOUNT_EXCEEDED`, `DUPLICATE`) and HTTP status mapping.
5. **Side effects**: reads vs. writes, state transitions, downstream triggers (notifications, callbacks).
6. **Auth**: which credential env vars the employee side will hold (variable names only, never values).
7. **Idempotency**: idempotency-key parameter or natural dedupe key; safe-retry semantics.
8. **Non-goals**: what the interface explicitly will not do — prevents scope creep on the business side.

## Lifecycle

`proposed → approved → implemented → deployed → verified` (plus `rejected` / `dropped`, with a note)

- **proposed**: drafted during step 1, presented at Gate 1.
- **approved**: user confirmed at the gate — employee-side build starts against the contract (stub-backed).
- **implemented / deployed**: business team reports progress; update the doc as it lands.
- **verified**: stub flipped off, live smoke test passed (step-6 checklist).

The doc is the single source of truth for the contract. If the deployed reality drifts from the contract, update the proposal and the employee-side code together — never silently patch one side.

## Employee-Side Rules

1. MCP tools and scripts implement the approved contract verbatim — parameter names, response fields, error codes.
2. Stub backends live behind an env var (e.g. `BUSINESS_API_STUB=true`) with canned responses derived from the contract's response schema; stubbed tools are recorded in TOOLS.md and `docs/harness-setup.md`, and marked `contract-pending: <proposal-id>` in the plan.
3. On deployment: flip, re-run the live smoke test, mark the proposal `verified`. Until then, demo and verification runs use stub mode and say so.
