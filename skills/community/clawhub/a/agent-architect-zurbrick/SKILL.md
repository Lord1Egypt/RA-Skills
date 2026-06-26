---
name: agent-architect
description: >
  Audit and improve an agent at the right layer: persona/tone, constitutional
  and operating rules, memory architecture, or skill portfolio / reusable
  workflows. Use when an agent feels off, brittle, repetitive, forgetful,
  over-scoped, or uneven and the question is which lane is actually weak and
  what the smallest justified fix is. Helps decide whether to make a plain
  edit, tighten a rule, adjust memory, change a skill, or do nothing.
---

# Agent Architect

Use this skill to diagnose **where an agent problem belongs** before changing
anything.

This is a narrow architecture audit skill. It does not run a governance program,
build a dashboard, or redesign the whole agent unless the evidence clearly earns
that conclusion.

Recommendations from this skill are **diagnostic only**. Do not apply patches
without reviewing whether the lane assignment and fix type actually match the problem.

## Use when

- an agent sounds wrong, acts off-brand, or drifts in tone
- an agent keeps making the same operating mistake
- an agent forgets key context, commitments, or prior corrections
- an agent keeps solving repeatable problems ad hoc instead of through a skill or workflow
- the real question is **which layer should change** rather than how to patch the symptom
- deciding whether the fix belongs in `SOUL.md`, `AGENTS.md` / operations files,
  memory files, or a skill directory

## Do not use when

- the user already knows the exact file and exact edit to make
- the task is routine skill authoring with no architecture diagnosis needed
- the request is to build a whole new agent system, dashboard, registry, or governance framework
- the issue is a one-off execution failure better solved by fixing the local task directly
- there is not enough evidence yet to distinguish signal from a single bad run

## The four lanes

1. **Persona / tone** — identity, voice, style, stance, response texture
2. **Rules** — constitutional constraints, operating rules, decision protocols,
   escalation boundaries, workflow habits
3. **Memory** — what is stored, when it is written, how it is retrieved,
   where durable facts vs daily state live
4. **Skills** — reusable workflows, narrow procedural packages, tool-routing,
   repeatable playbooks

Read `references/lane-diagnosis.md` before assigning a lane.

## Default workflow

1. **Start from the symptom, not the fix**
   Capture the failure pattern, repeated friction, or observed weakness.

2. **Check whether this is recurring or isolated**
   If it is a one-off, prefer a local fix or no change.

3. **Assign the primary lane**
   Read `references/lane-diagnosis.md` and choose the lane causing the failure.
   If multiple lanes contribute, name one primary lane and at most one secondary lane.
   Only recommend a secondary-lane patch if the primary-lane fix would clearly fail without it.
   Otherwise, note the secondary lane as context only.

4. **Choose the smallest justified fix type**
   Read `references/fix-types.md` and prefer, in order:
   - no change
   - plain edit
   - memory tweak
   - rule change
   - skill change

   Do not escalate to a larger fix just because it feels more architectural.
   Weak evidence should bias toward no change or a local edit. Structural changes need recurrence,
   cross-context benefit, or repeated operator friction.

5. **Say where the patch belongs**
   Point to the layer or file family directly:
   - persona → `SOUL.md`, identity/tone docs
   - rules → `AGENTS.md`, `OPERATIONS.md`, guardrails, QA/protocol docs
   - memory → `MEMORY.md`, `memory/*.md`, memory procedures, retrieval paths
   - skills → a specific skill's `SKILL.md`, `references/`, or a new narrow skill only if earned

6. **State what not to touch**
   Avoid collateral edits, broad rewrites, and cross-lane churn unless clearly necessary.

7. **Use the output format exactly**
   Keep the answer short, decisive, and patch-oriented.

8. **Log meaningful architecture recommendations**
   If the diagnosis leads to a real structural recommendation, log the lane, fix type,
   and short symptom summary to daily memory so future audits can see what changed and why.

For a fast pass before recommending any change, read `references/audit-checklist.md`.

## Output format

### Human-readable
1. **Diagnosis** — what is actually going wrong
2. **Lane** — persona / rules / memory / skills
3. **Recommended fix type** — plain edit / rule change / skill change / memory tweak / no change
4. **Smallest justified patch** — exact change and where it belongs
5. **Risks / what not to touch** — nearby changes that would be overreach

### Structured option

```yaml
diagnosis: short summary of what is actually wrong
lane: persona|rules|memory|skills
secondary_lane: none|persona|rules|memory|skills
fix_type: no_change|plain_edit|memory_tweak|rule_change|skill_change
patch_target: exact file or file family
smallest_patch: concise patch recommendation
risks:
  - overreach to avoid
  - adjacent file or lane not to touch
```

## Works well with

- **`skill-builder`** — when the result is "tighten or add a narrow skill"
- **memory-architecture skills such as `cognition`** — when the issue is durable storage, retrieval shape, or memory-system design beyond a local tweak
- **`battle-tested-agent`** — when the diagnosis suggests reliability hardening patterns across memory, delegation, or verification
- **`openclaw-guide`** — when the issue is really OpenClaw routing, config, session behavior, or platform mechanics rather than the agent itself

## References

- `references/lane-diagnosis.md` — how to identify the weak lane and avoid misclassification
- `references/fix-types.md` — how to choose the smallest justified intervention
- `references/audit-checklist.md` — fast audit pass before recommending any patch
- `references/placement-map.md` — where each kind of fix usually belongs
- `references/worked-examples.md` — compact examples for common mixed-lane failures and one do-nothing case

## Output style

Be crisp. Route the problem to the right layer. Prefer the smallest justified patch over architectural theater.
