---
name: digital-employee-builder
description: "Build a runnable Agent digital employee from a business codebase or business-function description. Input a business system/module (source code, API docs, or functional spec); output a complete digital-employee workspace — AGENTS.md (operating rules), SOUL.md (persona), IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md, an MCP server wrapping business capabilities, per-workflow Skills — plus steps to onboard, run, and verify it in OpenClaw (default) or other harness frameworks (Claude Code, Cursor, custom). Triggers: digital employee, business-code-to-agent, turn a business system into an agent, SOUL.md, AGENTS.md, OpenClaw agent workspace, agent-ify a business function."
---

# Digital Employee Builder (Business Code → Digital Employee)

Turn a business capability into an agent employee with identity, rules, tools, and a runtime.

## Overall Workflow (execute in order)

```
Business input → 1. Interactive analysis (incl. interface-gap proposals) → ⛔ Gate 1: capability & proposal sign-off → 2. Role modeling → 2.5 Plan proposal → ⛔ Gate 2: plan sign-off → 3. Workspace → 4. MCP wrapping → 5. Skills (with scripts) → 6. Onboarding & verification
```

## Confirmation Gates (hard stops)

Gates 1 and 2 are **stop-and-wait points, not notifications**. At each gate: present the artifact in the conversation, let the user add/remove/adjust, and re-present after every revision round. Only an explicit approval ("approved / looks good / go ahead") unlocks the next step — silence or ambiguous replies mean not approved. Only after approval may the artifact be written into the workspace (`docs/business-capabilities.md` — plus `docs/business-api-proposals.md` when interface gaps exist — for Gate 1, `docs/employee-plan.md` for Gate 2) — create the workspace directory ahead of step 3 if needed to hold these approved docs. Never start generation (steps 3–6) before Gate 2 approval.

## Core Principle 1: Runtime Self-Containment (highest priority)

The employee workspace gets deployed standalone into the OpenClaw/harness runtime — **the business codebase does not exist on that machine**. Therefore:

- Nothing in the workspace (scripts, skills, config) may reference business source code via `sys.path`, absolute paths, or relative paths (e.g. `../../service`) — source code is read at build time for porting; at runtime there is zero source dependency.
- **Default to porting the business logic fully into the script** (Pattern C) so the script itself is the implementation: zero network dependency, immune to business-API flakiness, timeouts, and interface changes. Only when the user explicitly confirms a reliable runtime channel should you fall back to calling the deployed API (Pattern A) or a published SDK package (Pattern B).
- After generation, verify in a clean environment without the business codebase (see the step-6 checklist).

## Core Principle 2: Deterministic Logic Lives in Code

Prompts are suggestions; code is the guardrail. Route every capability point through this table before wrapping:

| Capability shape | Packaging | Why |
|---|---|---|
| Single atomic call, no branching (queries, one-step writes) | MCP tool (step 4) | Thin wrapper suffices; no flow to enforce |
| Fixed-order multi-step flows with validation/branching/rollback (refunds, approvals, reconciliation) | **Executable script in the skill's `scripts/`** (step 5), ported/orchestrated from the business code — or, when the user opts for MCP-only packaging, a **composite tool** in the MCP server (step 4) | Ordering, validation, and exception branches are enforced by code — the model cannot skip steps |
| Steps requiring comprehension, judgment, or content generation (interpreting reports, drafting replies) | Prompt orchestration in SKILL.md | That is the model's job anyway |
| Any capability whose business-side interface is missing or inadequate | **Modification proposal** in `docs/business-api-proposals.md` (Core Principle 3), then build against the approved contract | The builder never modifies business code; contract-first keeps the build unblocked |

A common failure: writing a multi-step business flow as prose steps in SKILL.md and letting the model call tools step by step — the model may skip steps, reorder them, or drop validations. **Whatever if/else, state machines, and validation rules exist in the business code must still exist as code after wrapping.**

Script-porting patterns and engineering standards: `references/script-encapsulation.md` — required reading for step 5.

## Core Principle 3: Never Modify Business Code — Propose, Agree, Build Against the Contract

The build pipeline is **read-only against the business codebase**. When a capability cannot be packaged because the business side lacks the needed interface (no flow-level endpoint for a Pattern A / composite-tool flow, a query the system computes but never exposes, missing idempotency keys), do not work around it — and never patch the business code yourself. Instead:

1. Draft a **modification proposal** (format: `references/business-api-proposals.md`): the interface to add (REST endpoint / MCP server / SDK module) with the full parameter contract — request/response schemas, error codes, auth, idempotency.
2. Get explicit user confirmation at Gate 1; approved proposals are written to `docs/business-api-proposals.md` (revisions are re-presented like any gate artifact).
3. Build the employee side **against the approved contract immediately**, with the client behind a stub backend switchable by env var — the build never blocks on the business team.
4. The business team implements and deploys on their own schedule; on deployment, flip the stub off and re-run the live smoke test. The proposal doc tracks each item's lifecycle (`proposed → approved → implemented → deployed → verified`).

Pattern C ports rarely trigger this (scripts are self-contained); API-consuming routes and data-sync needs do.

## Step 0: Confirm Inputs & Target

Confirm three things before starting (ask the user if missing):

1. **Business input**: a codebase path, API docs, or a functional description — any one suffices. With only a functional description, build the MCP part as stub tools plus integration notes, and record the proposed interfaces in `docs/business-api-proposals.md` (Core Principle 3).
2. **Employee positioning**: name, who it serves, one-sentence mandate. If the user doesn't provide these, do NOT ask here — step 2.5 will propose them for confirmation at Gate 2.
3. **Target harness**: OpenClaw by default. If the user names another framework (Claude Code, Cursor, custom harness), read `references/harness-adapters.md`.
4. **Runtime access channel**: how will the employee's runtime environment reach the business system? **Default is full porting (Pattern C), which needs no network channel** — only consider Patterns A/B when the user explicitly states the runtime can reliably reach the business API/SDK; in that case confirm network reachability and credential provisioning. When Pattern C involves data residency (script-managed storage replacing the business database), confirm data ownership and sync strategy with the user.

## Step 1: Interactive Business Analysis

Work through the business code interactively and produce a **business capability inventory** — the basis for every artifact that follows. Interaction protocol:

1. **Read first, ask second**: read the business code/docs thoroughly before asking anything (prefer CodeGraph when the repo is indexed, plus API docs and READMEs). Never spend the user's time on questions the code can answer.
2. **Ask as you go**: the moment you hit ambiguity — an endpoint's purpose is unclear, business rules contradict, a capability's inclusion is questionable — ask immediately with AskUserQuestion. Every question must carry your own inference as the default option; never throw an open-ended question at the user.
3. **Extract the inventory**:
   - **Capability points**: HTTP routes / service methods / CLI commands / cron jobs. For each: name, inputs, outputs, side effects (read vs. write), and **packaging route** (MCP tool / script / prompt, per the routing table above; for multi-step flows also record the source file and function location in the business code for step-5 porting).
   - **Role boundaries**: what this employee should do and must never do (write ops, money movement, deletions default to "requires human confirmation").
   - **Domain terms & rules**: state machines, enums, core business rules (e.g., "an order can be cancelled only before payment").
   - **Credentials & dependencies**: databases, third-party APIs, internal service URLs — record only how they are referenced; never write secrets into any artifact.
   - **Interface gaps**: for any capability point whose chosen packaging route needs a business-side interface that doesn't exist or is inadequate (a flow with no flow-level endpoint, a query not exposed, missing idempotency keys), draft a modification proposal per Core Principle 3 — proposed interface, full parameter contract, rationale, alternatives considered.
4. **⛔ Gate 1: capability & proposal sign-off** — hard stop (see Confirmation Gates above):
   - Present the full inventory in the conversation as a table: capability | inputs/outputs | read/write | packaging route | source location.
   - Present every interface-gap proposal with its draft contract (shape, parameters, returns, error codes, idempotency) — the user confirms both the content and that the business team can take it on.
   - Attach explicit inclusion recommendations: what you propose to include, what you propose to exclude and why (e.g., "destructive ops should be excluded or dry-run-only").
   - The user may add, remove, or adjust entries; re-present the updated inventory after each revision round.
   - Only on explicit approval, write the inventory as a table in `docs/business-capabilities.md` and the proposals (when any) in `docs/business-api-proposals.md` — then proceed to step 2.

## Step 2: Role Modeling

Map the capability inventory to the employee's identity using three mapping rules:

- Mandate → SOUL.md Identity/Expertise + AGENTS.md Scope rules
- Boundaries → AGENTS.md approval gates and forbidden zone (dangerous ops require human confirmation)
- Audience → initial entries in USER.md

Persona tone follows the business context: customer-facing → polite and restrained; internal ops → direct and efficient; finance/compliance → rigorous and conservative.

The mapping outputs are a **draft proposal** for step 2.5 — do not write them into any workspace file yet.

## Step 2.5: Plan Proposal (⛔ Gate 2)

Based on the approved capability inventory, present a complete employee plan in the conversation — a hard stop (see Confirmation Gates above). The plan has four blocks:

1. **Employee positioning**: name, audience, one-sentence mandate, persona tone (with reasoning, e.g. "finance context → rigorous and conservative").
2. **Functional scope**: what the employee will do / explicitly will not do (forbidden zone and the operations requiring human confirmation).
3. **MCP tool list**: for each tool — name (verb phrase), read/write, purpose, and the capability point it wraps. Mark tools waiting on an approved proposal as `contract-pending: <proposal-id>` so scope expectations are explicit.
4. **Skills list**: for each skill — name, trigger scenario, shape (script-driven / prompt-orchestrated), and the business workflow it covers.

The user may adjust any block; update the plan and re-present after each revision round. Only on explicit approval of all four blocks, write the plan to `docs/employee-plan.md` in the workspace — it becomes the authoritative spec for steps 3–6. Never start generation before this approval.

## Step 3: Generate the Workspace

Generate everything according to the approved plan in `docs/employee-plan.md` — positioning, scope, and approval gates come from there, not from re-derivation.

Use `assets/workspace/` as templates to generate the full directory (default output: `./digital-employees/<employee-name>/`):

```
<employee-name>/
├── AGENTS.md        # Operating rules: session startup, scope, approval gates, forbidden zone
├── SOUL.md          # Persona: identity, tone, expertise, boundaries
├── IDENTITY.md      # Name, emoji, one-line role
├── USER.md          # Audience profile (initial skeleton)
├── TOOLS.md         # Environment notes: MCP server, ports, credential variable names
├── HEARTBEAT.md     # Periodic tasks (optional; omit if no periodic needs)
├── memory/          # Empty dir; the employee writes daily logs at runtime
├── skills/          # Generated in step 5
├── mcp-server/      # Generated in step 4
├── docs/business-capabilities.md  # Capability inventory from step 1 (Gate-1 approved)
├── docs/employee-plan.md          # Approved plan from step 2.5 (Gate 2)
└── docs/business-api-proposals.md # Business-side modification proposals (Gate-1 approved; omit if no gaps)
```

Template usage notes (templates in `assets/workspace/*.tmpl`; OpenClaw field details in `references/openclaw-workspace.md`):

- **One file, one concern**: rules → AGENTS.md, tone → SOUL.md, environment → TOOLS.md. Never duplicate content across files — duplication edited in one place but not the other inevitably creates conflicting instructions.
- **Keep it short**: these files are injected into every session context. Keep AGENTS.md/SOUL.md under ~150 lines each and put critical rules near the top (OpenClaw truncates at 20,000 chars per file by default).
- AGENTS.md must include: a session-startup checklist (read SOUL/USER/today's memory), business scope, the approval-required operation list, and how to escalate on failure or uncertainty.

## Step 4: MCP Wrapping

Wrap exactly the MCP tool list approved in `docs/employee-plan.md` as an MCP server — no additions, no omissions. Templates:

- Python: `assets/mcp-server-python/server.py.tmpl` (FastMCP — preferred, fewest dependencies)
- TypeScript: `assets/mcp-server-ts/server.ts.tmpl` (use when the business system itself is Node/TS)

Wrapping rules:

1. **One capability point = one MCP tool**. Tool names are verb phrases (`query_order`, `create_refund`); descriptions state parameter meanings and side effects.
2. **Read/write tiering**: query tools are open directly; write tools say "confirm with the user before executing" in their description and are mirrored in AGENTS.md's approval list.
3. **Thin wrapper** (atomic tools): each tool only validates params + calls the existing business interface (HTTP client or imported module). Never copy business logic — composite flow tools (rule 6) are the deliberate, disciplined exception.
4. **Credentials via env vars**: the server reads env at startup; TOOLS.md records variable names only.
5. **Generate config snippets**: write the onboarding config for this MCP server into `docs/harness-setup.md` (OpenClaw openclaw.json mcpServers snippet, Claude Code .mcp.json, Cursor mcp.json — formats in `references/harness-adapters.md`).
6. **Composite tools for flows** (when the user opts for MCP-only packaging): a multi-step flow becomes ONE flow-level tool (`process_refund`) whose server code holds the whole orchestration — every validation, branch, ordering, and compensation step from the business code (run the Porting Checklist from `references/script-encapsulation.md` over this code). Requirements:
   - `dry_run` parameter, default `true` for dangerous flows — the server-side equivalent of the script `--dry-run` convention.
   - Never expose the underlying write-CRUD as standalone tools: read CRUD stays open, writes happen only through composite tools, so the model physically cannot hand-assemble a write flow. Mirror "flows go through composite tools only" in AGENTS.md.
   - The server now carries business logic: provenance comments (`# Ported from src/services/refund.py::process_refund`) and mapping registration in `docs/business-capabilities.md`, exactly as script ports do. Flow changes mean editing + redeploying the server — call this trade-off out when the user chooses this route; missing flow-level interfaces on the business side go through Core Principle 3 proposals.
   - Engineering details and example: `references/mcp-integration.md` → Composite Tools.
7. **Contract-first tools** (pending proposals): implement tools waiting on an approved proposal strictly against the contract in `docs/business-api-proposals.md` — parameters, response fields, error codes verbatim. Point the client at a stub backend behind an env var (e.g. `BUSINESS_API_STUB=true`) so the server starts and passes smoke tests before the business side deploys; record stubbed tools in TOOLS.md and `docs/harness-setup.md`. On deployment, flip the env var and re-run the smoke test — the tool definition must not change.

Then actually start the server once (send an initialize request for stdio, or curl a health check for HTTP) and confirm tools/list returns every capability point. If it won't start, fix it — never deliver an MCP server that doesn't run.

## Step 5: Generate Skills (Script-First)

Generate workspace skills per the skills list approved in `docs/employee-plan.md` (templates in `assets/skill-template/`, including `SKILL.md.tmpl` and `scripts/workflow.py.tmpl`). Each skill takes one of two shapes per the routing table:

**A. Script-driven (multi-step deterministic flows — the default)**

```
skills/<workflow-name>/
├── SKILL.md            # Thin shell: triggers, parameters, how to run the script, output interpretation
└── scripts/
    └── <workflow>.py   # Executable ported/orchestrated from business code; holds ALL deterministic logic
```

- Extract scripts from the business code using the patterns in `references/script-encapsulation.md`. **Default is Pattern C: port the business logic fully into the script** (zero network dependency, most reliable); fall back to Pattern A (orchestrate the deployed API) or Pattern B (published SDK) only when the user explicitly confirms a reliable runtime channel. In all three patterns the script must be self-contained — **no sys.path/path references to business source code**. Never deliver a flow as a fresh natural-language description alone.
- Scripts must cover **every validation and branch** the business code has for that flow (state-machine checks, amount caps, duplicate-submission guards); validation failure exits non-zero with a clear error message.
- Dangerous flows ship a `--dry-run` flag (validate only). Approval gates in AGENTS.md still apply: dry-run first, show the user, then execute for real.
- SKILL.md states only: the run command, each parameter's meaning and valid values, the meaning of the script's JSON output fields, and exit codes with their remedies. No prose steps for the model to orchestrate — orchestration already happened inside the script.
- **Run every generated script for real** (test environment or mocked business interface) before delivery; nothing ships that doesn't execute.
- **Contract-first**: if a scripted flow depends on a business interface covered by a pending proposal, code against the approved contract with a stub backend behind an env var (same convention as step 4 rule 7) — or defer that skill to post-deployment; record the choice in the proposal doc.

**B. Prompt-orchestrated (judgment-heavy flows)**

- Anything a single tool call completes gets no skill.
- The body covers steps, exception branches, and which MCP tools are involved.

**Common constraint**: workspace skills reference only this employee's MCP tools, scripts/, and docs/ — no external environment dependencies.

## Step 6: Onboarding & Verification

Provide complete onboarding steps in `docs/harness-setup.md` and verify each item:

**OpenClaw (default)**:
1. Place the workspace at `~/.openclaw/workspace-<employee-name>/` (or register as a standalone agent: `openclaw agents add <employee-name>` pointing at the workspace)
2. Add the MCP server config to openclaw.json
3. Run `openclaw agent prompt` to preview the assembled system prompt; confirm AGENTS/SOUL inject cleanly with no truncation
4. Smoke-test dialogue: ask its identity (verifies SOUL), issue a read-only business request (verifies MCP), trigger a write op (verifies approval gates)

**Verification checklist** (check every item before delivery):
- [ ] Generated MCP tools and Skills match `docs/employee-plan.md` exactly — nothing added, nothing dropped
- [ ] **Clean-environment test**: copy the workspace alone into a directory/container without the business codebase; scripts and MCP server start and run there (no source-path references in scripts)
- [ ] Workspace-wide grep: no `sys.path.insert`, no absolute/relative paths into the business repo, no hardcoded secrets
- [ ] MCP server starts; tools/list is complete
- [ ] Every script actually runs (including --dry-run and at least one exception branch)
- [ ] Spot-check one flow: in-script validations/branches match the source business code, no logic dropped
- [ ] Workspace files within character budgets; no cross-file role mixing
- [ ] Every dangerous operation has a human-confirmation gate
- [ ] All three smoke-test dialogues pass
- [ ] `docs/business-api-proposals.md` (when present) covers every interface gap; each proposal has explicit user confirmation and a current lifecycle status
- [ ] Every contract-pending tool/script runs against its stub; parameters, response fields, and error codes match the approved proposal verbatim
- [ ] Stub-mode flags and the post-deployment flip + live re-verification steps are recorded in `docs/harness-setup.md`

## References

- `references/script-encapsulation.md` — **Core**: script-porting patterns and engineering standards for business code (required reading for step 5)
- `references/business-api-proposals.md` — Modification-proposal format, contract minimums, stub discipline, lifecycle (required reading when the business side lacks interfaces)
- `references/openclaw-workspace.md` — OpenClaw workspace file spec, loading mechanics, character budgets
- `references/harness-adapters.md` — Onboarding formats for Claude Code / Cursor / generic harnesses
- `references/mcp-integration.md` — MCP protocol essentials and wrapping details
