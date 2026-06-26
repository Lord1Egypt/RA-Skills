# Reviewer rubric

Use exactly these reviewer identities and scopes.

## `star_correctness`

### Focus
- behavioral correctness
- control-flow mistakes
- boundary conditions
- error handling and failure paths
- state consistency, idempotency, async or concurrency hazards
- semantic regressions introduced by the diff

### Do not focus on
- naming polish
- general code style
- “could be more elegant” feedback

### Promote to p0 when
- the change is likely to produce incorrect behavior
- an edge case can silently break a key path
- a missing failure guard can corrupt state or produce a bad external result

## `star_architecture`

### Focus
- module responsibilities
- boundary placement
- dependency direction
- cohesion and coupling
- leakage of business logic into the wrong layer
- whether the change makes future modification harder

### Do not focus on
- minor local readability issues
- unit test naming or formatting

### Promote to p1 or p0 when
- the change damages a key system boundary
- the design spreads one concern across too many modules
- the introduced abstraction creates long-term structural drag

## `star_testability`

### Focus
- whether the change can be verified
- whether high-risk paths are covered
- whether regressions would be caught
- whether the chosen test level matches the risk
- whether tests validate behavior instead of incidental implementation details

### Do not focus on
- production-code aesthetics
- broad architecture opinions unless they directly block testing

### Promote to p0 when
- a high-risk change has no realistic validation path
- a missing test leaves a severe regression effectively invisible

## `star_readability`

### Focus
- naming clarity
- control-flow clarity
- excessive nesting or oversized functions
- hidden assumptions and magic values
- comments that fail to explain intent
- cognitive load for future maintainers

### Do not focus on
- requests for whole-system redesign
- cosmetic nits with no maintenance impact

### Promote to p1 when
- understanding or modifying the code is materially harder after this change
- hidden assumptions are likely to cause future mistakes

## `star_simplicity`

### Focus
- unnecessary code growth
- excessive indirection
- premature abstraction
- wrappers or helpers with weak payoff
- speculative configurability or extensibility
- chances to reduce concept count, branch count, file count, or forwarding layers

### Do not focus on
- tiny syntax-level shortening with no maintenance win
- simplifications that would trade away correctness or testability

### Strong heuristics
- an abstraction used only once is suspect
- a configuration layer that outweighs the logic is suspect
- speculative future-proofing is suspect
- a small amount of repetition is often cheaper than a poor abstraction
- reduce concept count before chasing line count

### Promote to p1 when
- the change clearly increases maintenance surface without proportional value
- a simpler shape would preserve behavior with less indirection

## Common reviewer rules

All reviewers must:

- ground each issue in concrete evidence
- explain why it matters
- suggest a practical next step
- stay within their own focus area
- include “keep / do not over-fix” notes when relevant
- avoid low-value noise

## Evidence standard

Each finding should point to a real place in the change, such as:
- file and function
- module and responsibility boundary
- specific test gap
- changed interface and affected usage

## Finding budget

Per reviewer, prefer:
- up to 3 p0 findings
- up to 5 p1 findings
- up to 5 p2 findings

Fewer is better when the change is healthy.
