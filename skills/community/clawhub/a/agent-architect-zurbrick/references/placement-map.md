# Placement Map

Use this map to say **where the patch belongs** once the lane is identified.

## Persona / tone

Typical homes:
- `SOUL.md`
- `IDENTITY.md`
- other always-loaded tone/persona files

Good patch shapes:
- one clarifying tone paragraph
- one anti-pattern list item
- one identity or pressure-behavior sentence

Avoid:
- stuffing workflow rules into persona files
- using voice edits to compensate for weak guardrails

## Rules

Typical homes:
- `AGENTS.md`
- `OPERATIONS.md`
- `QA.md`
- guardrail or protocol documents

Good patch shapes:
- one decision rule
- one escalation boundary
- one review or verification gate
- one workflow checkpoint

Avoid:
- edits to Constitutional Principles in `AGENTS.md` — those are immutable unless Don gives explicit written approval
- broad rewrites triggered by a narrow failure

## Memory

Typical homes:
- `MEMORY.md` for durable facts
- `memory/YYYY-MM-DD.md` for daily state and work logs
- `memory/bank/*.md` for deep domain context
- memory procedures when the issue is write/retrieval cadence

Good patch shapes:
- promote one durable fact
- prune or relocate duplicated context
- add a retrieval reminder or storage rule

Avoid:
- creating memory sprawl for one-off details
- treating memory as a replacement for missing workflow guidance

## Skills

Typical homes:
- an existing skill's `SKILL.md`
- an existing skill's `references/`
- a new narrow skill folder only when reuse is real

Good patch shapes:
- tighten frontmatter trigger language
- split optional detail into one new reference
- add one missing branch to a reusable workflow
- create one narrow skill with a sharp non-scope

Avoid:
- mega-skills
- dashboards, registries, or lifecycle machinery
- skills that compensate for a missing base rule

## Quick routing rule

If the fix changes **how the agent sounds**, patch persona.
If it changes **how the agent decides**, patch rules.
If it changes **what the agent retains or recalls**, patch memory.
If it changes **how the agent repeatedly executes a task category**, patch skills.
