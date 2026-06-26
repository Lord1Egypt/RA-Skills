# Intake Framework

Use this reference when you need a disciplined intake pass before writing plan or context.

## Goal
Ask less, read more, and only ask the questions that materially change the plan.

## Four-round intake funnel

### Round 0 — Task typing
Classify the request first:

| Mode | Meaning | What to inspect first |
|---|---|---|
| greenfield | new feature / product idea | goals, user, constraints, expected shape |
| brownfield | change existing repo/system | repo structure, docs, current implementation, constraints |
| repair/refactor | fix or reshape existing behavior | current bug/symptom, boundaries, risk surface |
| orchestration-first | mostly about delegation and work packets | decomposition boundaries, dependencies, done criteria |

### Round 1 — Product truth
Capture the minimum product truth needed to plan well:
- What problem is actually being solved?
- Who benefits or uses it?
- What does success look like?
- What is the hardest constraint?

If one of these is missing, ask the **single** highest-value question.

### Round 2 — Local context inspection
Before asking more questions, read what the repo or workspace can already tell you.

Default inspection order:
1. README / docs / specs / issues
2. repo tree / service boundaries
3. key implementation files
4. current plans / TODO / progress artifacts
5. configs / schemas / APIs / data definitions

## Question strategy

### Ask one question at a time
Do not send a survey. Ask the one question whose answer most changes scope, prioritization, or acceptance.

### Prefer these question orders
1. value / objective
2. scope
3. hard constraints
4. implementation details

### Prefer multiple choice when possible
Multiple choice reduces user effort and ambiguity.

## Internal structuring before drafting

Before generating outputs, internally sort information into:
- Facts
- Assumptions
- Unknowns
- Conflicts
- Decisions needed

If the plan still depends on a guessed answer to a core product question, do not draft the full context yet.

## Stop clarifying when

Start drafting once all of the following are true:
- the objective is clear enough to name,
- an MVP or first phase can be defined,
- key constraints are known,
- acceptance criteria can be written,
- remaining unknowns will not block a useful first-pass plan.

## Trigger conditions for another clarifying question

Ask again only when one of these appears:
- product goal conflict,
- scope conflict,
- trade-off requiring Alan’s judgment,
- repo reality contradicts verbal request,
- acceptance criteria remain ambiguous.

## Repo-aware intake shortcuts

When a request touches an existing codebase, try to extract these before asking Alan:
- main app boundaries,
- key files or packages,
- current workflows,
- likely edit points,
- existing naming and architectural patterns,
- obvious constraints the user may not have mentioned.

## Anti-patterns

Avoid these failure modes:
- asking for information that docs/files already answer,
- turning intake into a long questionnaire,
- discussing implementation before value and scope are clear,
- drafting a context block that hides critical uncertainty,
- treating a large platform request as one phase when it obviously needs decomposition.
