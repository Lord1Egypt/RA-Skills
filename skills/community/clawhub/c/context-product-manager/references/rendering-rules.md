# Rendering Rules

Use this reference after the canonical context blueprint exists.

## Canonical-first rule

Always generate the canonical context blueprint before any downstream rendering.

The canonical blueprint is the truth source. Target-specific outputs may adapt wording and order, but they must not silently change:
- objective,
- scope,
- non-goals,
- constraints,
- required deliverables,
- acceptance criteria.

## Required canonical fields

Every full canonical blueprint should include:
- Objective
- Product Intent
- Scope
- Non-goals
- Constraints
- Existing Repo / System Context
- Required Deliverables
- Acceptance Criteria
- Risks
- Open Questions
- Verification Plan

## Codex rendering rules

Optimize for direct execution.

Emphasize:
- first files to read,
- concrete edit boundaries,
- implementation sequence,
- tests and verification commands,
- what not to touch,
- exact deliverables,
- concise report-back expectations.

Style:
- short,
- explicit,
- task-oriented,
- low-fluff.

## Antigravity rendering rules

Optimize for architecture-aware execution.

Emphasize:
- architecture reading priorities,
- design intent,
- invariants / guardrails,
- phased implementation,
- ambiguity handling,
- verification checkpoints,
- what to report after each phase.

Style:
- slightly more explanatory than Codex,
- still high-signal,
- preserve architectural context.

## OpenClaw work packet rules

Generate work packets only when decomposition provides clear value.

Each packet must include:
- objective,
- inputs,
- boundaries,
- expected output,
- done criteria,
- verification,
- dependencies / handoff target.

Avoid performative multi-agent decomposition. If one agent or one handoff is clearly enough, do not split.

## Assumption management rules

Always make these distinctions visible when ambiguity matters:
- Facts
- Assumptions
- Unknowns
- Decisions already made
- Decisions still needed

Do not let a downstream agent inherit guesses as settled requirements.

## Conflict repair rules

If any of the following conflict:
- user description,
- repo reality,
- canonical blueprint,
- Codex handoff,
- Antigravity handoff,
- work packets,

then repair the canonical blueprint first and re-render the downstream outputs.

Do not patch only one branch and let the others drift.

## Quality checks before finalizing

Before sending the rendered outputs, verify:
- nothing new was invented in a downstream variant,
- non-goals are still preserved,
- acceptance criteria still match the original intent,
- repo-specific context stays grounded in actual files or systems inspected,
- required outputs are executable and verifiable.
