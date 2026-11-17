---
name: discussion-cohesion-diagnosis
description: Diagnose cohesion in the Discussion of an English psychology research paper. Covers both (1) local-level cohesion devices — connectives, reference chains, citation as glue — and (2) global-level narrative thread — forward-moving wrap, take-home message, navigational signposting. Triggers on "check Discussion cohesion", "is my discussion connected", "Discussion 衔接", "narrative flow check", etc. Does NOT generate or rewrite prose.
---

# Discussion Cohesion & Narrative-Thread Diagnosis

## Theory basis
*Science Research Writing* Unit 4.1.1 (Wrapping the discussion in a narrative) + 4.2.2 (citation positioning sentence patterns: "We first demonstrated that X, consistent with...", "In contrast...", "In line with this...") + 4.2.2 Q&A "If I decide to 'reboot' the reader, how do I choose which part/s of the article to revisit?" (narrative navigation).

## Two-level rubric

### Level 1 — Local cohesion (device-level)
- **Connectives** — additive (furthermore, in addition), adversative (however, in contrast), causal (therefore, consequently), sequential (then, subsequently). Appropriate density (not over- or under-used).
- **Reference chains** — pronouns (this/these/that), demonstratives, lexical repetition. No broken or ambiguous reference.
- **Citation as glue** — each citation is integrated with a clear relationship word/phrase (confirm / contrast / extend), not dropped as a bare parenthetical.
- **Paragraph topic sentences** — first sentence of each paragraph carries the topic forward; not a generic "Also, ..." chain.

### Level 2 — Global narrative thread (flow-level)
- **Controlling idea** — one message persists from opening to closing.
- **Forward motion** — every paragraph moves the reader closer to the conclusion; no backtracking or side-tracks.
- **Navigational signposting** — explicit "we will return to...", "in the next section...", "this raises the question..." for non-linear moves.
- **Take-home persistence** — the take-home message stated in the opening is reinforced (not contradicted) by the closing.

## What this skill diagnoses

1. **Connective density and variety** — too few = choppy; too many = mechanical
2. **Reference clarity** — does "this" / "these" / "that" have a unique, retrievable referent?
3. **Citation integration** — is each citation tied with a clear relationship word?
4. **Topic sentence quality** — does the first sentence of each paragraph do real work?
5. **Controlling-idea persistence** — is there one main message throughout?
6. **Forward motion** — any stalling or backtracking?
7. **Closing–opening alignment** — does the conclusion echo the take-home stated in the opening?

## Diagnostic signals

| Signal | Means |
|---|---|
| "Also, ..." / "Moreover, ..." / "In addition, ..." opens 4+ consecutive paragraphs | Mechanical connective chain; vary the opening |
| "This suggests..." where "this" could mean 2 prior things | Reference ambiguity |
| "(Smith, 2020; Jones, 2018; Lee, 2019)" dropped without relationship word | Citation as decoration, not glue |
| Paragraph 3 introduces a new sub-topic unrelated to anything earlier | Side-track; breaks forward motion |
| Last sentence contradicts or shifts from the first sentence's claim | Closing–opening misalignment |
| Take-home from the opening is unrecognisable in the closing | Thread lost |

## Output format

```markdown
## Cohesion & Narrative Diagnosis

### Level 1 — Local cohesion
- Connective density: [score] (per 1000 words; corpus baseline = X)
- Reference clarity: [score]
- Citation integration: [score]
- Topic sentence quality: [score]

### Level 2 — Global narrative thread
- Controlling idea: [extracted]
- Forward motion: [pass / concern / fail]
- Take-home persistence: [pass / concern / fail]
- Closing–opening alignment: [pass / concern / fail]

### Top issues (severity: critical / major / minor)
1. ...
2. ...
```

## Academic integrity
Does not generate or rewrite the Discussion. Only diagnoses and suggests.

## References (to be filled in Phase 2)
- `references/rubric.md`
- `references/checklist.md`
- `references/examples/`
