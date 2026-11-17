---
name: "dr-planning-artifacts"
description: "Create handoff-ready product, system, roadmap, architecture, and Azure DevOps planning artifacts."
---

# DR. Planning Artifacts

Use when Daniel is shaping durable planning work before implementation.

Core outcome: produce planning artifacts with enough context that another engineer or agent can understand what is being built without relying on Daniel's or the planner's memory.

## Trigger

Use this skill when Daniel asks to:

- plan a roadmap
- define or refine epics, features, user stories, or tasks
- structure Azure DevOps backlog items
- lock an epic, feature, story, task, roadmap, or planning decision
- capture product, system, or architecture direction
- turn an idea into implementation-ready planning artifacts
- create handoff-ready planning docs
- structure large technical work before coding

## Routing Boundaries

This skill is for planning and handoff artifacts, not execution.

Use this skill when the main question is:

- What are we building?
- Why does it matter?
- What belongs in scope?
- How should the work be decomposed?
- What should a later implementer understand?

Use `dr-checkpoint-implementation` instead when the main task is:

- implement
- build
- fix
- migrate
- deploy
- roll out
- wire up
- validate production behavior

If both apply, use this skill first to shape or lock the planning artifact. Switch to `dr-checkpoint-implementation` only when execution begins.

For tiny obvious tasks, use neither skill; just do the work.

## Non-Goals

Do not use this skill to execute implementation work.

Do not turn every small chat into a formal plan.

Do not bury exact commands, file edits, or test commands inside epics or features. Put exact implementation detail in tasks.

Do not invent unknown detail. Mark assumptions and open questions clearly.

## Planning Principles

1. Treat planning as a durable artifact, not a chat summary.
2. Assume someone else may implement it later.
3. Preserve useful context, rationale, examples, and boundaries.
4. Keep hierarchy clean without making higher levels vague.
5. Push back when a boundary is too broad, overlaps another item, or mixes discovery, validation, rollout, and implementation concerns.
6. Use concrete names and outcomes.
7. Separate what is known from assumptions, open questions, and later decisions.
8. Make acceptance criteria practical when the goal is implementation-ready planning.

## Azure DevOps Hierarchy

Daniel commonly uses this hierarchy:

- Epic: major business or system capability.
- Feature: smaller capability inside an epic.
- User Story: user-facing need or behavior.
- Task: exact implementation work, files, commands, tests, and acceptance specifics.

Preserve this hierarchy unless Daniel explicitly chooses a different structure.

## Artifact Detail By Level

### Epic

Prefer this structure:

- Name
- Meaning
- Purpose / why it exists
- Clear outcome
- In scope
- Out of scope
- Examples
- Success signal
- Dependencies / related areas
- Risks / important boundaries
- Related later epics or features
- Open questions / assumptions

Epics should explain the what and why clearly. They should not contain task-level implementation instructions.

### Feature

Prefer this structure:

- Name
- Capability
- User or business value
- In scope
- Out of scope
- Expected outcome
- Dependencies / related areas
- Risks / boundaries
- Initial user stories, when useful
- Open questions / assumptions

Features should be specific enough to guide story creation without becoming implementation task lists.

### User Story

Prefer this structure:

- As a / I want / so that
- Notes and context
- Acceptance criteria
- Dependencies or related stories
- Edge cases or constraints, when known
- Open questions / assumptions

If Daniel is preparing implementation-ready work, include acceptance criteria by default.

### Task

Prefer this structure:

- Objective
- Exact implementation approach, when enough context exists
- Files or areas likely involved
- Commands, scripts, or tests, when known
- Acceptance specifics
- Validation evidence expected
- Dependencies / blockers

Tasks are where exact how-to detail belongs.

## Locking Behavior

When Daniel says something is locked:

1. Restate the locked version clearly.
2. Preserve the hierarchy and boundaries.
3. Update the appropriate durable place when the active agent has write access and the destination is clear.
4. If the destination is not clear, present the locked artifact and ask where it should be stored.
5. Do not silently rewrite a locked artifact later; propose changes as a revision.

## Quality Bar

A planning artifact is good enough when:

- another engineer or agent can understand the intent without the original chat
- the hierarchy is clean
- the item is not a vague one-liner
- scope and non-scope are clear
- rationale is preserved
- dependencies and risks are visible
- success signal is concrete
- unknowns are marked instead of invented

## Pushback Rules

Push back briefly when:

- an epic is really multiple epics
- a feature mixes unrelated capabilities
- a user story is really a feature or task
- a task lacks enough context to implement safely
- discovery, validation, promotion, rollout, and execution are collapsed into one item
- the artifact is too thin for future implementers

Use this pattern:

1. State the concern.
2. Explain the practical risk.
3. Offer a cleaner split or ask the smallest needed question.

## Handoff To Implementation

When planning is complete and Daniel wants execution:

- keep the locked planning artifact as source context
- convert implementation tasks into checkpoints where useful
- use `dr-checkpoint-implementation` for coding, rollout, validation, and approval gates

The planning artifact should guide execution; it should not replace execution validation.

## Examples

A thin epic title is not enough:

```text
Bad: Stock Research Engine
```

Better:

```text
Epic: Stock Research Engine
Meaning: A system capability that gathers, normalizes, and summarizes stock-related signals so Daniel can review investment ideas without manually checking every source.
Purpose: Reduce repeated manual research and create a durable research trail.
Clear outcome: Daniel can request or receive a structured company snapshot with sources, risks, and next actions.
In scope: source discovery, data capture, summarization, evidence links, watchlist integration.
Out of scope: automated trading, financial advice, portfolio allocation.
Success signal: another agent can create features and stories from this epic without asking what the engine is supposed to do.
```
