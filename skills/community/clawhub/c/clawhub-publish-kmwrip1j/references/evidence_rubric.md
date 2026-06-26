# Evidence Rubric

## Purpose

This file defines how to convert extracted text into interpretable MBTI evidence.
It is a rubric, not a hardcoded verdict table.

## Stronger Evidence

Prefer evidence that shows:

- repeated behavior over one-off wording
- actual choices over aspirations
- tradeoffs under pressure
- stable work habits
- similar signals across multiple source types
- the same preference appearing across time, not just in one sentence
- how the user handles the outer world when decisions and commitments become real

## Weaker Evidence

Treat these as weak unless reinforced:

- punctuation style
- message length alone
- single-word preferences
- borrowed personality language
- copied summaries
- generic first-person fillers such as "我觉得" or "I think"
- generic collaboration words such as "我们" or "一起" without clearer context

## Pseudo-Signals

Do not directly score these:

- "be rigorous", "be concise", "don't flatter me"
- requests about markdown, tables, emoji, output style
- build/deploy instructions with no self-description
- assistant-control commands
- stack traces, shell logs, or tool output

They may still be kept as notes if they reveal a pattern indirectly.

## Dimension Hints

### E / I

Look for:

- energy from discussion vs reflection
- thinking out loud vs thinking before speaking
- breadth of contact vs depth of solitude
- best work done outwardly in action vs inwardly in reflection

Do not equate:

- short messages with `E`
- long messages with `I`
- "我觉得" with `I`
- "我们" with `E`

### S / N

Look for:

- concrete operating detail vs abstraction and pattern language
- exact execution requests vs model/frame building
- dependence on prior examples vs speculative possibility-building

### T / F

Look for:

- evaluation through logic, evidence, and tradeoffs
- evaluation through impact, values, and interpersonal consequences

Do not force a binary from politeness alone.

### J / P

Look for:

- closure, commitment, and external structure in dealing with people and situations
- openness, optionality, iterative exploration, and adaptation in dealing with the outer world

Key caution:

- external tools may be compensation, not preference
- a user can maintain a GTD system and still show strong `P` patterns in practice
- for introverts, outward `J/P` behavior often reflects the auxiliary process rather than the dominant one

## Suggested Strength Labels

- `weak`: a plausible but surface-level hint
- `moderate`: a clear behavior or framing pattern
- `strong`: repeated, specific, cross-context evidence

## Chinese Context Adjustments

Borrowed from the spirit of KnowMe's cultural note, but generalized:

- indirectness does not imply introversion
- group language does not automatically imply feeling
- hierarchy-aware phrasing does not automatically imply judging
- tool-centric rigor language does not automatically imply thinking

## Counterevidence

Every axis should preserve opposing evidence when present.

Examples:

- a user may prefer open exploration in ideation but demand closure in shipping work
- a user may describe themselves as private yet visibly think in public when solving problems

Counterevidence is not noise. It is often what differentiates adjacent types.

## Function Hints

Function hints are allowed only after the four-letter candidates are already in range.

- for extraverts, outward behavior may show the dominant process directly
- for introverts, outward behavior often shows the auxiliary more clearly

Therefore:

- functions are a coherence check
- functions are not the primary classifier
