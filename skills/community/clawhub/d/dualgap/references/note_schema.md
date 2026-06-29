# Paper Note And Review Schema

Use this schema when generating notes for a two-direction literature review.

## Per-Paper Note

```markdown
# [Paper title]

## 1. Basic Information
- File:
- Direction:
- Paper type:
- Strictly belongs to this direction:
- Main task:
- Data / benchmark:
- Confidence: high / medium / low

## 2. Background And Motivation
Explain where the problem comes from in this paper's own setting.
Avoid generic statements such as "privacy is important" or "communication is expensive."

## 3. Core Challenge
What specific failure of existing methods does the paper target?
Why is this challenge nontrivial?

## 4. Method: Step-By-Step Mechanism
Describe the algorithm as a procedure.
For FL/distributed papers, include:
- client state
- server state
- uploaded payload
- downloaded payload
- aggregation or routing
- local training
- inference/deployment

For skill discovery/self-evolution papers, include:
- trajectory/data source
- skill representation
- skill generator
- verifier or evaluator
- optimizer/editor
- retrieval/dependency mechanism
- train/evolution phase
- inference/use phase

## 5. Why The Method Could Work
Explain the causal or algorithmic reason, not just the component name.

## 6. Experiments And Evidence
What claims are supported?
Which claims only hold under narrow settings?

## 7. Assumptions And Failure Modes
Separate:
- stated assumptions
- hidden assumptions
- author-noted limitations
- inferred "does not work when..." scenarios

## 8. Implications For The Cross-Direction Research Agenda
State one of:
- directly transferable
- indirect inspiration
- warning / counterexample
- mostly irrelevant

Then give concrete, paper-specific implications.
Do not reuse the same generic paragraph across papers.

## 9. Open Questions To Verify
List testable uncertainties and suggested validation experiments.
```

## Reviewer JSON

The reviewer must return JSON only:

```json
{
  "pass": true,
  "score": 9,
  "failure_reasons": [],
  "rewrite_instructions": [],
  "duplicate_implication": false,
  "needs_pdf_recheck": false,
  "evidence": "Short explanation grounded in the note."
}
```

Set `pass` to false if:

- the method section is too vague to reconstruct the workflow
- the importance section is generic
- the implication section is reusable boilerplate
- assumptions/failure modes are missing
- the note conflates author evidence with inference
- the note does not explicitly state relationship to the cross-direction agenda

## Synthesis Review JSON

Each synthesis document is reviewed by a separate LLM call. A direct pass uses:

```json
{
  "pass": true,
  "score": 9,
  "failure_reasons": [],
  "rewrite_instructions": [],
  "missing_axes": [],
  "over_generic_sections": [],
  "evidence": "Short explanation grounded in the synthesis."
}
```

If the first synthesis review fails and the rewrite passes, the saved JSON uses:

```json
{
  "initial": {
    "pass": false,
    "score": 5,
    "failure_reasons": ["Too generic"],
    "rewrite_instructions": ["Tie every gap to concrete paper evidence"]
  },
  "final": {
    "pass": true,
    "score": 8,
    "failure_reasons": [],
    "rewrite_instructions": [],
    "missing_axes": [],
    "over_generic_sections": [],
    "evidence": "The rewritten document now names mechanisms and validation plans."
  }
}
```

Set `pass` to false if:

- the document is a generic taxonomy rather than a comparison grounded in notes
- research gaps do not say why existing papers fail to solve the problem
- improvement ideas lack concrete mechanisms, target failure modes, or validation plans
- the user's agenda or exclusions are ignored
- author evidence, model inference, and uncertain hypotheses are mixed
