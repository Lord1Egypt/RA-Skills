# Lane Diagnosis

Use this reference to decide which lane is actually weak.

Pick the **causal lane**, not the loudest symptom.

## 1. Persona / tone lane

Choose this lane when the agent:
- sounds wrong even when facts and process are fine
- is too stiff, too chatty, too generic, too passive, too abrasive, or off-brand
- fails to match the intended identity, audience, or communication stance
- keeps making stylistic choices that conflict with the desired voice

Usually belongs in:
- `SOUL.md`
- identity/tone docs
- a small wording edit in an always-loaded persona file

Do **not** choose persona when the real problem is:
- missing constraints
- weak escalation rules
- memory failure
- lack of a reusable workflow

## 2. Rules lane

Choose this lane when the agent:
- repeatedly makes the same judgment error
- violates escalation boundaries or autonomy limits
- skips verification, review, handoff, or QA steps
- handles ambiguity poorly because the operating rule is weak or absent
- needs a clearer protocol, checklist, or decision rule

Usually belongs in:
- `AGENTS.md`
- `OPERATIONS.md`
- guardrail, QA, review, or protocol files

Do **not** choose rules when the issue is just tone or one missing fact.

## 3. Memory lane

Choose this lane when the agent:
- forgets user preferences, commitments, blockers, or recent context
- repeats mistakes that should have been stored as durable lessons
- stores information in the wrong place or cannot retrieve what it already has
- has no clean separation between daily state, durable facts, and deep reference
- needs a write/retrieval habit more than a new rule or skill

Usually belongs in:
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`
- `memory/bank/*.md`
- memory procedure docs or retrieval instructions

Do **not** choose memory when the issue is that the agent never had a workflow for the task.

## 4. Skills lane

Choose this lane when the agent:
- keeps re-solving the same repeatable job from scratch
- needs reusable procedural knowledge, examples, or bundled references
- has a broad skill that should be split or a narrow gap that deserves a small new skill
- would benefit from a better tool-routing pattern or a reusable workflow wrapper

Usually belongs in:
- an existing skill's `SKILL.md`
- a skill's `references/` files
- a new narrow skill directory only if repetition and reuse are real

Do **not** choose skills when a plain edit to a core rule or persona file would solve the issue faster.

## Misclassification traps

### Tone problem that is really rules
The agent sounds hesitant because it lacks an escalation policy or decision rule.

### Rules problem that is really memory
The rule exists, but the agent does not retain the learned exception, preference, or standing instruction.

### Memory problem that is really skills
The agent is not forgetting; it never had a reusable workflow for the task category.

### Skills problem that is really rules
A skill is being proposed just to compensate for weak base operating discipline.

## Tie-breakers

If two lanes look plausible, ask:
1. If I changed only one thing, which lane would most reduce recurrence?
2. Is the problem about **how the agent is**, **how it decides**, **what it remembers**, or **how it repeats work**?
3. Would a local file edit solve this faster than adding a new reusable layer?

Prefer naming:
- **one primary lane**
- **one secondary lane max** only when it materially affects the recommendation

Heuristic:
- if the rule exists but is not followed, check **memory** before adding a second rule
- if the same workflow keeps being reinvented, check **skills** before storing more facts
- if the style problem disappears once authority is clear, patch **rules** before persona
