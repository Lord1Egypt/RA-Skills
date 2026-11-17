# Output Schemas

Use only the schemas required by the request. Keep identifiers stable so the profile can be updated when new evidence arrives.

## Architect method profile

```markdown
# [Architect / practice] method profile

Scope: [period, geography, building types, question]
Evidence coverage: [projects and source types]
Known gaps: [missing or weak evidence]

## Persistent concerns
- [Concern]: [documented / observed / interpreted / provisional] — [citations]

## Periods and changes
- [Period]: [what changed and possible conditions] — [citations]

## Method-card index
| ID | Method | Dimension | Period | Confidence |
|---|---|---|---|---|
```

## Method card

```markdown
### M-[NN] [Verb-led method name]

- Status: documented | observed | interpreted | provisional
- Confidence: high | medium | low
- Scope: [career period / project type / geography]
- Design problem: [problem this method addresses]
- Trigger conditions: [when it becomes relevant]
- Operations: [repeatable spatial, organizational, tectonic, or representational moves]
- Effects: [documented intent and/or observed result, clearly separated]
- Tradeoffs: [what the move costs or makes harder]
- Failure conditions: [when it should not be used]
- Counterexample: [project or evidence that limits the claim]
- Evidence: [source IDs with page, timestamp, drawing, or URL]
- Project questions: [questions that transfer the method without copying form]
```

## Project application matrix

```markdown
| Method card | Why relevant now | Possible project operation | Test / drawing needed | Conflict or risk | Decision owner |
|---|---|---|---|---|---|
```

## Comparative lens

```markdown
| Project question | Architect A method | Architect B method | Shared ground | Key difference | Current-project implication |
|---|---|---|---|---|---|
```

Compare methods at the same analytical level. Do not compare one architect's quote with another architect's photograph as if they were equivalent evidence.

## Audit table

```markdown
| Claim or card | Evidence status | Problem | Required correction or research |
|---|---|---|---|
```

Common problems include unsupported intention, single-project generalization, missing period, collaborator erasure, image-only inference, citation drift, and style-label substitution.

## Bounded research backlog

```markdown
| Priority | Missing evidence | Why it matters | Preferred source | Stop condition |
|---|---|---|---|---|
```

Use a stop condition such as “one architect-authored statement plus drawings from two additional projects.” Do not create an open-ended reading list.

## Compact response

For an early design conversation, return only:

1. One-sentence scope and limitation
2. Three relevant method cards
3. One application matrix
4. Three counter-lens questions
5. Evidence gaps and next decision
