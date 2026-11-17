---
name: fde-prd-writer
description: "Stage 3 of FDE Delivery Loop. Turn an approved problem-discovery package and POC engagement charter into an English POC PRD specification handoff for engineering, QA, deployment, Agent Skill design, and POC execution. Use to write, improve, or review POC PRDs, functional requirements, acceptance criteria, test scenarios, scope decisions, and downstream handoffs. Do not use for initial discovery, customer commitments, prototype construction, or production operations."
---

# FDE PRD Writer | POC Specification Handoff

Turn an aligned customer problem and POC agreement into a PRD package that engineering can implement, QA can accept, and downstream teams can continue delivering.

## Confirm upstream readiness

Before starting, confirm the presence of:

1. The Customer Problem-Discovery Package from `fde-problem-discovery`.
2. The POC Engagement Charter from `fde-engagement-charter`.

When either is missing, state the gap and return to the corresponding upstream stage. Do not fill the PRD with unvalidated assumptions.

## Writing process

1. **Lock the problem and outcome**: Extract target users, real workflow, business outcomes, success criteria, and explicit non-goals.
2. **Design the minimum closed loop**: Define scope, functions, exceptions, permissions, data, and dependencies around user tasks. Replace vague terms such as “intelligent” and “easy to use” with observable behavior.
3. **Write testable specifications**: Number each requirement. Define trigger, preconditions, main flow, exception flow, acceptance criteria, and evidence.
4. **Complete downstream handoffs**: Identify the inputs and open risks required by Deployment Architecture, Agent Skill Design, POC Run, and Adoption and Value.
5. **Run quality checks**: Use [references/prd-quality.md](references/prd-quality.md). Rewrite or mark as open anything that cannot be implemented, tested, or traced.

## Method selection principles

Treat KANO, SWOT, JTBD, user stories, and Mermaid as decision and communication tools:

- Use a method only when it improves a scope, priority, risk, or workflow decision.
- Convert every conclusion back into concrete evidence, requirements, and acceptance criteria.
- Use Mermaid to clarify complex flows, states, or system relationships, not as decoration.

See [references/method-selection.md](references/method-selection.md) for method selection and [references/upstream-downstream-contracts.md](references/upstream-downstream-contracts.md) for lifecycle boundaries.

Load `references/user-stories.md`, `references/test-scenarios.md`, and`references/prd-style.md` only when needed. Interviewing, discovery, and product strategy belong to Problem Discovery or Productization and are not the default starting point for this skill.

## Output

Use [templates/prd-skeleton.md](templates/prd-skeleton.md) to produce the **POC PRD Specification Handoff Package**. Default to English in this edition. Produce another language only when the user explicitly requests it.

Before delivery, run `node scripts/validate-traceability.js <prd.md>`to check structural traceability and orphan identifiers across` FR → AC → TS`. The script detects identifier and relationship gaps only; it cannot decide whether a requirement, acceptance criterion, or test is correct for the business.

## Boundary

This skill does not replace Problem Discovery, the POC Charter, Deployment Architecture, Agent implementation, real execution, or value review. Its responsibility is to give those downstream activities a reliable, traceable, and acceptable specification.
