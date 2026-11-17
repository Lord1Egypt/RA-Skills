# AIDLC Core Workflow (OpenClaw port)

**PRIORITY**: This workflow OVERRIDES ad-hoc implementation for non-trivial work.

## Adaptive Principle

The workflow adapts to the work. Use full depth for medium/high complexity or ambiguous requests. Collapse gates only when the user explicitly requests a lightweight path or the work is trivial.

## Side effects (read this)

Activating AIDLC **writes local workspace files** under:

```text
{workspace}/aidlc-sessions/<uuid>/
```

including gate markdown, deconfliction reports, `meta.json`, and `APPROVALS.md`.  
Do not put secrets, credentials, or sensitive customer data in gate artifacts.

## Inception Phase (Planning)

Always start here for non-trivial requests.

### Per-gate loop (all gates 0–4)

For **each** gate, the main agent must:

1. **Draft** the gate artifact (use `{baseDir}/templates/gate-*.md` when helpful).
2. **Deconflict** before presenting to the human (see Gate Deconfliction below).
3. **Revise** the draft if deconfliction found material issues (re-run deconfliction after material edits).
4. **Present** the final gate artifact **plus** a short deconfliction summary to the human.
5. **Stop** and wait for exactly:
   - **Approve and Continue**
   - **Request Changes: …**
6. On approval → lock gate into workspace scratch. On request changes → revise only this gate and repeat from step 1.

Do **not** present a gate to the human for approval until deconfliction has run for that draft (or the user explicitly waived it for a lightweight path).

### Gate Deconfliction (required before human present)

**Purpose:** Mitigate contradictions, unresolved questions, missing constraints, and weak option tradeoffs before the human is asked to approve.

**Who:** A dedicated reviewer **subagent** (preferred), or an explicit self-review pass labeled `DECONFLICTION` if subagents are unavailable.

**When:** After the draft for the current gate is ready, **before** presenting Approve/Request-Changes. Also after material revisions from **Request Changes**.

**How (OpenClaw):**

```text
sessions_spawn(
  taskName="aidlc-deconflict-gate-N",
  mode="run",
  context="isolated",   # do not fork full chat unless needed
  task="""You are the AIDLC Gate Deconfliction reviewer (read-only).
Gate: <gate-id>
Session: <uuid>
Objective: <intent>

Read:
- current gate draft (below or path)
- prior locked gates under aidlc-sessions/<uuid>/gates/ (if any)
- APPROVALS.md / meta.json as needed

Do NOT implement code. Do NOT approve the gate. Do NOT modify files unless asked to write the deconfliction report only.

Return a structured report using templates/gate-deconfliction.md sections:
1. Contradictions (internal or vs prior locked gates)
2. Open questions still unresolved
3. Missing constraints / acceptance criteria
4. Option tradeoffs that are under-specified
5. Cross-gate drift
6. Suggested revisions for the main agent (concrete)
7. Residual risks if approved as-is
8. Verdict: clean | issues-found

Current draft:
<paste or path>
"""
)
```

Then `sessions_yield` (or equivalent) until the reviewer completes. Main agent merges useful findings into the gate draft, re-runs deconfliction if the draft changed materially, then presents to the human.

**Output:** Keep the latest report at:

```text
{workspace}/aidlc-sessions/<uuid>/gates/<gate-id>.deconfliction.md
```

**Fail-soft:** If spawn fails, main agent still performs the same checklist inline and labels the section `DECONFLICTION (self-review)` so the human sees it. Never skip the checklist silently.

**Not a substitute for the human gate.** Deconfliction advises; only the human approves.

### Gate 0 — Context Snapshot (ALWAYS)
Produce a short locked snapshot:
- Intent & success criteria
- Greenfield vs brownfield classification
- Constraints & non-negotiables
- Existing assets / code to reuse
- Explicit open questions

Run **Gate Deconfliction**, then present and wait for **Approve and Continue** or **Request Changes**.

### Gate 1 — Assess
- Complexity (Low / Medium / High)
- Key risks
- Dependencies
- Recommended depth of remaining gates

Run **Gate Deconfliction**, then present and wait for approval.

### Gate 2 — Decompose
Break into clear Units of Work with:
- Name / responsibility
- Dependencies between units
- Suggested owner (OpenClaw subagent / human)

Run **Gate Deconfliction**, then present and wait for approval.

### Gate 3 — Design Decisions
Capture the important architectural and design choices with short rationale. Prefer decisions that keep the system simple, secure, and aligned with existing patterns.

Run **Gate Deconfliction** with extra attention to option tradeoffs and contradictions with Gates 0–2, then present and wait for approval.

### Gate 4 — Execution Plan
Produce a concrete, sequenced plan that can be executed by agents. Include:
- Ordered steps
- Which units can run in parallel
- How OpenClaw subagents will be used (including any remaining deconfliction only if a gate is re-entered)
- Verification / acceptance criteria

Run **Gate Deconfliction** (plan vs prior locked decisions), then present and wait for approval.

## Construction Phase

Only after Gate 4 is locked:
- Implement the units
- Prefer parallel OpenClaw subagents where independent
- Keep changes small and verifiable
- Run tests / typecheck / build as appropriate
- Stop and report if a new decision is required — re-enter the appropriate gate (with deconfliction) rather than deciding silently

## Hard Constraints

- Never skip a human gate.
- Never skip Gate Deconfliction before presenting a gate (unless the user explicitly waives it for a lightweight path).
- Never write production code before the Execution Plan is approved.
- Prefer explicit planning mode throughout Inception (no production edits).
- Deconfliction subagents are reviewers only — they do not approve gates or write production code.
- Workspace scratch under `aidlc-sessions/` is the only SoT shipped with this skill.
- This process takes precedence for non-trivial work when the OpenClaw aidlc skill is active.
- Keep the rule files under this skill `references/` editable so the user can evolve the process.
