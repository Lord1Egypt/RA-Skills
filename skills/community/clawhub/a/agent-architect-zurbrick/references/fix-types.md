# Fix Types

Choose the smallest intervention that plausibly prevents recurrence.

Default bias: **downshift the fix size** until a larger change is clearly justified.

## 1. No change

Choose this when:
- the evidence comes from one bad run only
- the agent behaved reasonably under ambiguity
- the issue is user preference, not architecture
- the cost of changing the system exceeds the likely benefit

Use language like:
- "No structural change warranted"
- "Treat as isolated execution noise unless it repeats"

## 2. Plain edit

Choose this when:
- one sentence, example, or instruction is wrong or missing
- the right layer is obvious and no new mechanism is needed
- the fix is a direct wording or placement correction

Examples:
- tighten a tone sentence in `SOUL.md`
- add one escalation bullet in `AGENTS.md`
- correct one retrieval pointer in a skill

## 3. Memory tweak

Choose this when:
- a fact belongs in durable memory and is missing
- a recurring correction should be promoted from daily notes to long-term memory
- write/retrieval cadence is the failure, not the governing rule
- memory structure or indexing is slightly off

Before recommending durable promotion, ask:
- is this fact still true?
- is it stable enough to belong in long-term memory?
- would daily or bank memory be safer than immediate durable promotion?

Examples:
- promote a stable preference into `MEMORY.md`
- create a focused `memory/bank/*.md` note for recurring domain context
- add a retrieval reminder to the operating flow

## 4. Rule change

Choose this when:
- the agent needs a standing protocol, boundary, or decision heuristic
- the same judgment failure has happened multiple times
- a memory update alone would not reliably prevent recurrence
- the fix should apply broadly across tasks

Examples:
- require verification before external delivery
- clarify when to ask for approval vs act autonomously
- define a handoff or review gate

Keep rule changes narrow. Avoid turning one incident into a constitution rewrite.

## 5. Skill change

Choose this when:
- the task pattern recurs enough to justify reusable workflow guidance
- an existing skill is too broad, too vague, or missing a key branch
- the agent needs procedural packaging, not just a rule sentence

Examples:
- tighten an existing skill trigger description
- split a bloated skill into lean references
- add a new narrow skill for a repeatable workflow gap

Do **not** choose skill change just because skills feel cleaner than editing core docs.

## Escalation heuristics

Prefer these in order unless the evidence clearly says otherwise:
1. no change
2. plain edit
3. memory tweak
4. rule change
5. skill change

A larger fix must earn itself by showing at least one of these:
- recurrence across tasks
- cross-context benefit
- repeated operator friction
- clear mismatch between current layer and problem type

## What to include in the patch recommendation

For any fix type, specify:
- the exact file or file family
- the smallest meaningful edit
- why this is enough
- what broader changes should be avoided
