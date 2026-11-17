# Script Encapsulation of Business Code

How to extract business-code workflows into executable skill `scripts/`. Required reading before generating script-driven skills in step 5.

## Contents

- [Runtime Reality: No Business Codebase](#runtime-reality-no-business-codebase)
- [Why Prompts Are Not Enough](#why-prompts-are-not-enough)
- [Three Packaging Patterns](#three-packaging-patterns)
- [Porting Checklist](#porting-checklist)
- [Script Engineering Standards](#script-engineering-standards)
- [Writing the SKILL.md Thin Shell](#writing-the-skillmd-thin-shell)
- [Testing Requirements](#testing-requirements)

## Runtime Reality: No Business Codebase

The employee workspace is deployed into the OpenClaw/harness runtime — **the business source code does not exist on that machine**. This sets hard constraints:

- Scripts must not use `sys.path.insert`, `os.chdir` into a source tree, or any absolute/relative path pointing at the business repo (e.g. `../../service`). Source code is reference material **at build time**; it does not exist **at runtime**.
- **The default is to port the business logic fully into the script** (Pattern C), making the script itself the implementation: zero network dependency, immune to business-API flakiness, timeouts, expired credentials, and interface changes — an API is an inherently unreliable external dependency, so eliminate it when you can.
- Only when the user explicitly confirms a reliable runtime channel should you fall back to the other two: **the deployed business API** (Pattern A, network calls) or **an SDK formally published to a package registry** (Pattern B, pip/npm release).
- The choice is driven by the "runtime access channel" confirmed in step 0.

## Why Prompts Are Not Enough

Having the model execute a multi-step flow by calling tools per prose steps in SKILL.md fails in three ways:

1. **Skipped/reordered steps**: the model may jump straight to the write call, bypassing validation.
2. **Lost validations**: boundary checks in the business code (amount caps, state machines, idempotency keys) get simplified or dropped when paraphrased into prose.
3. **Non-reproducibility**: the same request takes different paths on different runs; failures can't be attributed.

The fix: all deterministic logic (ordering, validation, branching, rollback) goes into scripts; the model only decides "should this flow run" and "what parameters to pass."

## Three Packaging Patterns

**Pattern C is the default**; A/B apply only when the user explicitly confirms a reliable runtime channel.

### Pattern C: Full Porting (default)

Port the flow's business logic completely into the script so it runs standalone with zero network dependency:

- Port line by line against the source function; **keep every if/else, validation, and exception branch** — no "simplification." Replace data access with script-managed storage (e.g. SQLite/JSON under the workspace `data/`) or another channel confirmed at build time.
- Porting covers more than the happy path: every validation function, enum/state-machine definition, money calculation, and error code the flow touches in the source comes along.
- Note provenance in a header comment: `# Ported from src/services/refund.py::process_refund (lines 45-132)`.
- Register the mapping (script ↔ source file ↔ port date) in `docs/business-capabilities.md`; sync the script when the source changes.
- Data ownership must be confirmed with the user at port time: is the script-managed data a read-only replica/cache of business data or an independent ledger, and whether/how it syncs with the business database.

### Pattern A: API Orchestration (optional — when the user confirms the API is reliable)

When the business system runs as a service reachable from the runtime and the user explicitly accepts the API dependency, the script orchestrates HTTP/RPC calls in a fixed order, freezing order and validation into code:

```python
order = api("GET", f"/orders/{args.order_id}")
if order["status"] != "paid":                       # validation in code, not in the model's memory
    fail("INVALID_STATE", f"order status is {order['status']}; only paid orders are refundable")
if amount > order["amount"]:
    fail("AMOUNT_EXCEEDED", "refund exceeds order amount")
api("POST", "/refunds", json={...})
```

- API base URL and credentials come from env vars (`BUSINESS_API_BASE`, `BUSINESS_API_TOKEN`); zero hardcoding in scripts.
- If the API (or one of its endpoints) exists only as an approved proposal in `docs/business-api-proposals.md`, code against the contract with a stub backend behind an env var (e.g. `BUSINESS_API_STUB=true`) until the business side deploys — format and lifecycle in `references/business-api-proposals.md`.
- When the business API lacks flow-level endpoints (e.g. no "refund" endpoint, only low-level CRUD), the multi-step CRUD orchestration and its validations belong in the script — that is exactly why the script exists.

### Pattern B: Published SDK Dependency (optional — when the vendor ships a formal package and the user confirms it)

When the capability is published as a proper pip/npm package (installable from a registry, not a source checkout), the script declares the dependency and calls the SDK:

```python
# Deps: pip install {{business-sdk}}==1.2.3   (from a package registry, not a local path)
from {{business_sdk}} import Client

client = Client(base_url=os.environ["BUSINESS_API_BASE"], token=os.environ["BUSINESS_API_TOKEN"])
```

- Only formally released registry versions are accepted; `pip install /path/to/repo`, `npm link`, and sys.path injection are **all forbidden**.
- Validations and branches still get filled in at the script layer (when the SDK only provides atomic calls).

## Porting Checklist

For every scripted flow, verify against the source business code:

- [ ] All precondition checks ported (state machine, permissions, amount/quantity bounds, duplicate-submission guards)
- [ ] Every branch has a handler; no "allow by default"
- [ ] Write-operation ordering matches the source (especially order-sensitive sequences like charge-then-notify)
- [ ] The source's transaction boundary has an equivalent (commit only when all steps succeed; on failure, run compensation/rollback or report exactly how far execution got)
- [ ] Retry, timeout, and rate-limit policies from the source are preserved
- [ ] **The script contains no path references to the business source and runs standalone away from the repo**

## Script Engineering Standards

1. **Interface**: explicit `argparse` parameters with help text; `--dry-run` is mandatory (dangerous flows show dry-run output to the user before real execution).
2. **Output**: results as JSON on stdout (`{"ok": true, "data": {...}}` or `{"ok": false, "error": {"code": "...", "message": "..."}}`) for model parsing; logs/progress go to stderr.
3. **Exit codes**: 0 = success; non-zero = failure, with code semantics documented in SKILL.md (e.g., 2 = bad arguments, 3 = business validation failed, 4 = external dependency error).
4. **Idempotency**: re-runs must not cause duplicate side effects — dedupe via business order numbers/idempotency keys, or check prior processing before acting.
5. **Credentials**: injected via env vars; no hardcoding in scripts.
6. **Dependencies**: list deps and install commands in a header comment; only formal PyPI/npm releases — local-path dependencies are forbidden.
7. **Size**: keep a single script under ~300 lines; beyond that, split into multiple skills or extract shared modules into `scripts/lib/`.

## Writing the SKILL.md Thin Shell

A script-driven skill's SKILL.md covers exactly four things:

1. Trigger scenarios (in both frontmatter description and body)
2. Run command and parameter table (including dry-run usage)
3. Meaning of the output JSON fields
4. Exit/error codes and remedies (e.g., `INVALID_STATE → tell the user the current status; do not retry`)

No "first do X, then do Y" — the flow lives in the script; repeating it in SKILL.md creates a second implementation that will drift.

## Testing Requirements

Actually run every script before delivery:

1. **Clean-environment test**: copy the script (or the whole workspace) into a directory/container without the business codebase and confirm it starts standalone — this directly verifies runtime self-containment.
2. Happy path once (test environment or mocked business interface).
3. `--dry-run` once (dangerous flows).
4. At least one validation-failure branch (confirm the non-zero exit code and error message).

Mocking: patch the business client with `unittest.mock`, or run a local HTTP stub returning canned responses. Record test commands and results in `docs/harness-setup.md`.
