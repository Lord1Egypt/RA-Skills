# Agent Dispatch Cards

Use these cards when `parallel-research-sprint` is active. Pick only the roles needed for the current question.

Each role must return evidence IDs, confidence, contradictions, and hand-off notes. Specialist roles should not write polished final prose unless the lead-integrator asks for a reusable asset pack section.

## `lead-integrator`

Owns:

- research question and scope
- lane selection
- shared definitions
- evidence merge
- final artifact

Do:

- assign non-overlapping lanes.
- define the evidence window and source priority.
- deduplicate upstream sources before synthesis.
- decide which findings are accepted, downgraded, or left as gaps.

Avoid:

- letting every lane write its own final answer.
- hiding unresolved conflict behind a smooth consensus.

Return:

```text
Role: lead-integrator
Research question:
Parallel lanes:
Merge judgment:
Accepted:
Rejected or downgraded:
Unresolved gaps:
Final confidence:
```

## `source-scout`

Owns:

- primary sources
- source genealogy
- recency checks
- duplicated secondary reports

Do:

- find original sources before aggregators.
- mark whether multiple reports share one upstream claim.
- identify missing primary evidence that should exist.

Avoid:

- counting reposts, summaries, or copied databases as independent confirmation.
- treating PR claims as neutral evidence.

Return:

```text
Role: source-scout
Task:
Primary sources found:
Repeated / non-independent sources:
Evidence IDs:
Gaps:
Confidence:
Hand-off notes:
```

## `timeline-analyst`

Owns:

- origin
- phase changes
- path dependencies
- contested history

Do:

- explain why each stage changed, not only when it happened.
- connect historical choices to current strengths and constraints.
- mark disputed dates or origin claims.

Avoid:

- making a clean origin story when the record is messy.
- listing dates without causal interpretation.

Return:

```text
Role: timeline-analyst
Task:
Stage map:
Path dependencies:
Contested points:
Evidence IDs:
Confidence:
Hand-off notes:
```

## `competitive-analyst`

Owns:

- direct competitors
- indirect competitors
- substitutes
- user choice logic
- ecosystem position

Do:

- compare by user job, switching cost, trust, price, workflow, and distribution.
- include substitutes that solve the same job differently.
- identify likely future challengers.

Avoid:

- producing only a feature checklist.
- assuming category boundaries from vendor positioning.

Return:

```text
Role: competitive-analyst
Task:
Competitor / substitute set:
User choice logic:
Strongest comparison dimension:
Evidence IDs:
Confidence:
Hand-off notes:
```

## `user-signal-analyst`

Owns:

- reviews
- GitHub issues
- forum threads
- social feedback
- repeated complaints and praise

Do:

- separate common signal from loud outlier.
- preserve user language when it clarifies the job-to-be-done.
- mark channel bias.

Avoid:

- treating social virality as broad market proof.
- over-indexing on one community.

Return:

```text
Role: user-signal-analyst
Task:
Repeated praise:
Repeated complaints:
Channel bias:
Evidence IDs:
Confidence:
Hand-off notes:
```

## `dissent-reviewer`

Owns:

- negative evidence
- contradictions
- alternative explanations
- reversal conditions

Do:

- look for the strongest case against the emerging conclusion.
- name what would make the current answer wrong.
- separate evidence-based objections from generic skepticism.

Avoid:

- adding token opposition that does not change confidence.
- flattening all risks into equal weight.

Return:

```text
Role: dissent-reviewer
Task:
Strongest objection:
Contradictory evidence:
Alternative explanation:
Reversal conditions:
Evidence IDs:
Confidence:
Hand-off notes:
```

## `decision-analyst`

Owns:

- verdict
- confidence
- risk
- monitoring threshold
- next action

Do:

- apply `decision-rubric.md`.
- recommend `EXPERIMENT`, `HOLD`, or `MONITOR` when evidence is not strong enough for `GO`.
- make reversal conditions measurable.

Avoid:

- giving high confidence without user context.
- jumping from weak evidence to an irreversible action.

Return:

```text
Role: decision-analyst
Task:
Verdict:
Confidence:
Key assumptions:
Risks:
Monitoring thresholds:
Evidence IDs:
Hand-off notes:
```
