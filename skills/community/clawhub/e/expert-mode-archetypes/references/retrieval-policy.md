# Expert Mode Retrieval Policy v0.3.0-draft

Expert Mode should improve judgement without flooding the context window. Use this policy to decide how much expert/archetype context to load.

## Core rule

Load the smallest amount of archetype context that can materially improve the next reply.

Do not load every dossier just because Expert Mode is active.

## Retrieval levels

### Level 0: Roster only

Use when selecting or reporting available archetypes.

Load:

- `experts/roster.md` only, if available.

Use for:

- deciding which archetypes might be relevant
- avoiding duplicate dossiers
- reporting what exists
- lightweight planning

Do not load full dossiers at Level 0.

### Level 1: Header skim

Use when deciding whether a specific dossier is relevant.

Load only these sections if possible:

- Scope
- Archetype buckets
- Load when
- Do not load when

Use for:

- relevance checks
- choosing between similar archetypes
- confirming whether a dossier should be loaded fully

### Level 2: One lead dossier

Use when one archetype should shape the answer.

Load:

- one complete dossier, usually the lead archetype

Use for:

- focused implementation
- focused critique
- single-domain judgement
- compact expert-mode answers

### Level 3: Small panel

Use when the decision needs tradeoffs or review.

Load:

- 2-3 complete dossiers

Typical combinations:

- builder + stakeholder
- domain expert + risk reviewer
- product strategist + customer researcher + maintainer
- lead expert + adversarial reviewer + translator

Use for:

- design decisions
- risky changes
- launch/readiness review
- project direction choices

### Level 4: Broad panel summary

Use when many archetypes are relevant but full loading would be wasteful.

Load:

- roster
- header skim for several dossiers
- full dossier only for the lead or highest-risk lens

Then summarize the rest from headers/load rules.

Use for:

- strategy planning
- broad project review
- deciding which experts to create next
- large cross-functional work

Avoid loading 6-10 full dossiers unless explicitly necessary.

## Loading heuristics

Load a dossier when at least one is true:

- It changes likely recommendations.
- It reveals failure modes not obvious from the base task.
- It represents the affected user/stakeholder.
- It provides domain-specific source guidance.
- It helps translate expert judgement to the target audience.
- It is needed to resolve disagreement between archetypes.

Do not load a dossier when:

- The answer is routine and low-risk.
- The dossier only repeats general reasoning.
- A more specific dossier is already loaded.
- The user asked for speed and the risk is low.
- The dossier is stale or marked archived/superseded.

## Context exit rule

After answering, do not keep treating a dossier as active unless the next user turn still needs it. Expert Mode is a retrieval pattern, not a permanent personality change.

## Reporting rule

When useful, report briefly:

```markdown
Expert Mode loaded:
- <archetype>: <why>

Not loaded:
- <archetype>: <why>
```

For casual use, skip this report and just answer with the selected lens.

## Conflict rule

If loaded archetypes disagree, summarize only disagreement that affects the decision.

Good:

> Product wants fewer steps; security wants explicit confirmation. Recommendation: keep one extra confirmation only for destructive actions.

Bad:

> Long theatrical debate between fake experts.

## Compression rule

If a dossier is loaded repeatedly, create or update a compact version. Frequently used dossiers should become shorter over time.
