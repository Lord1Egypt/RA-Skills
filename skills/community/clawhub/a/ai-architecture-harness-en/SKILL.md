---
name: ai-architecture-harness
description: Establish and use architectural guardrails for AI-assisted coding to prevent architecture collapse, feature regression, and drift across long multi-turn iterations. Use when the user mentions AI coding, Agent coding, architecture collapse, Harness Engineering, design intent, acceptance rules, golden rules, architecture tests, or wants the codebase to be safer for AI Agent modifications.
---

# AI Coding Architecture Guardrails

## Goal

Help coding Agents modify large or complex projects without breaking existing architecture, core functionality, or long-term design intent.

When using this Skill, treat the repository as the source of truth, but treat human-maintained design intent as the highest-level guidance. Do not rely on long conversation history for critical context; key rules must be captured in repo docs or executable checks.

## Core model

Use a four-layer guardrail model:

```text
1. Human design-intent layer
2. Agent-synced architecture and acceptance docs layer
3. Hard automated constraints layer
4. Human review and golden-rules feedback layer
```

The Agent’s job is not free-form improvisation, but safe execution within clear boundaries and feedback loops.

## Recommended doc layout

When creating or improving guardrails for a project, prefer this minimal structure:

```text
AGENTS.md
docs/DESIGN_INTENT.md
docs/ARCHITECTURE.md
docs/ACCEPTANCE_RULES.md
docs/GOLDEN_RULES.md
docs/ARCHITECTURE_DRIFT.md
```

`DESIGN_INTENT.md` is maintained by humans. It records project goals, core architectural principles, non-negotiable tradeoffs, and historical design decisions. It is the “constitution”; do not let the Agent overwrite human intent with the current implementation.

`ARCHITECTURE.md` records the currently confirmed architecture map. It may be periodically synced by the Agent from code and `DESIGN_INTENT.md`, but accidental drift must not be automatically legitimized.

`ACCEPTANCE_RULES.md` records how to verify core features, architectural commitments, and non-regression behavior.

`GOLDEN_RULES.md` records strong rules distilled from real incidents. Each rule should include incident source, forbidden behavior, required behavior, and how to enforce it automatically.

`ARCHITECTURE_DRIFT.md` records gaps between design intent and current implementation, classified as: aligned with intent, reasonable evolution, technical debt, needs human decision, or violates design.

## Before you start coding

Before any non-trivial code change:

1. Read `AGENTS.md` if it exists.
2. Read `docs/DESIGN_INTENT.md`, `docs/ARCHITECTURE.md`, `docs/ACCEPTANCE_RULES.md`, and `docs/GOLDEN_RULES.md` if they exist.
3. Clarify architectural boundaries and behaviors this change must not break.
4. State the scope of this change before editing.
5. Do not proactively perform large refactors, renames, migrations, or abstraction overhauls unless the user explicitly asks.

If the project has no guardrail docs yet, create a minimal viable set first; do not invent a huge documentation system in one shot.

## Design-intent maintenance workflow

Human design intent is the top anchor. When updating `DESIGN_INTENT.md`:

1. Preserve historical decisions; do not simply overwrite old content.
2. Append new intent with dated decision records.
3. Record *why* something changed, not only *what* changed.
4. Keep it short enough for the Agent to read before coding.
5. Do not allow the Agent to replace human design tradeoffs with implementation convenience.

Recommended format:

```markdown
## YYYY-MM-DD - [Decision title]

Design intent:
[What the system must preserve or evolve toward.]

Rationale:
[Why this direction matters.]

Impact:
- [Constraints future changes must obey.]
- [What the Agent must not break.]
```

## Architecture sync workflow

After a phase of work completes, or before a major task starts, sync architecture docs:

1. Read `DESIGN_INTENT.md`.
2. Inspect relevant code.
3. Compare design intent with current code.
4. Classify each gap:
   - `aligned with intent`
   - `reasonable evolution`
   - `technical debt`
   - `needs human decision`
   - `violates design`
5. Write only confirmed architecture into `ARCHITECTURE.md`.
6. Write unconfirmed or suspicious gaps into `ARCHITECTURE_DRIFT.md`.

Do not assume “current code is the correct architecture.” Current code may already have collapsed or drifted.

## Architecture acceptance tests

Turn architectural commitments into executable checks. For each architectural cornerstone:

1. Identify cornerstone nodes from `ARCHITECTURE.md`.
2. From code, find observable call chains, data flows, or invariants that prove the cornerstone still holds.
3. Write focused unit tests, integration tests, lint rules, or structural checks.
4. Add checks to the normal verification workflow.

Example:

```text
Architectural cornerstone:
PlanAgent must maintain multi-turn persistent memory.

Observable pattern:
After 10 consecutive dialogue turns, retrieve, summarize/update, and persist in the memory-management chain must run.

Acceptance test:
Simulate 10 dialogue turns; assert expected MemoryManager methods were called and results entered persistence or context assembly.
```

Prefer deterministic checks over AI judgment alone:

```text
Type checking > unit tests > integration tests > architecture tests > lint > CI > AI review > prompt reminders
```

AI review is only a semantic supplement, not a core guardrail.

## Hard-constraint priorities

When building guardrails, prioritize preventing:

- Cross-layer calls or imports that violate architectural direction
- Bypassing core service, repository, memory manager, validator, or provider
- Competing duplicate implementations for existing subsystems
- Deleting, weakening, or circumventing regression tests
- Changing external behavior without updating acceptance rules
- Replacing stable abstractions with direct data access
- Unbounded complexity, global state, or hidden side effects

If the project has clear layering, encode allowed dependency direction as tests or lint rules.

## Golden-rules workflow

When existing guardrails fail to stop architecture collapse, feature regression, or drift:

1. Summarize the incident.
2. Determine why existing docs or tests did not prevent it.
3. Add a rule to `GOLDEN_RULES.md`.
4. Add or propose a deterministic check to enforce the rule.
5. Link the rule to tests, lint, CI, or a review checklist.

Recommended format:

```markdown
## [Rule title]

Incident source:
[What happened and when.]

Forbidden behavior:
[What the Agent must not do again.]

Required behavior:
[Correct architectural behavior.]

Enforcement:
- [Tests, lint, CI checks, or review steps.]
```

Do not turn `GOLDEN_RULES.md` into generic advice. Keep it short, high-signal, and grounded in real incidents or high-risk patterns.

## Collapse-risk review

After the Agent completes a meaningful change, before the final reply, check:

1. Did this change alter architectural boundaries?
2. Did it bypass existing abstractions?
3. Did it delete, weaken, or avoid existing tests?
4. Did it change core call chains?
5. Did it introduce competing implementations for an existing subsystem?
6. Did it move responsibilities to the wrong module?
7. Where should human review focus first?

If any answer indicates risk, either fix it or record it as architectural drift needing human decision.

## Output expectations

When the user asks to design guardrails, deliver:

- Minimal set of new documents to add
- Architectural invariants that should be encoded as hard constraints
- First batch of tests, lint, or structural checks to implement
- Golden-rules feedback workflow
- Short rollout plan

When the user asks to apply guardrails to code, read existing docs and tests first, make small scoped changes, and validate with the project’s strongest automated checks.
