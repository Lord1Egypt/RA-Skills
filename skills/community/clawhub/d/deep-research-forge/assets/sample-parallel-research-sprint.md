# Sample Parallel Research Sprint

> This is a structural sample. Do not reuse its claims as facts. For a real report, refresh sources, dates, evidence IDs, and confidence.

## Request

Use `$deep-research-forge` with multi-agent parallel execution to research the AI coding IDE market. Split source verification, timeline, competitors, user signals, and dissenting evidence, then synthesize one answer.

## Route

- Selected route: `parallel-research-sprint`
- Final artifact: `research-brief` with reusable evidence notes
- Evidence window: `refresh at execution time`
- Parallel justification: the topic has separable lanes: source verification, timeline, competitive map, user signals, dissent, and decision implications.

## Shared Definitions

- Object: AI coding IDE market
- Scope: developer tools that combine code editing with AI-assisted generation, refactoring, agentic execution, or repository-aware workflows
- Comparison set: dedicated AI coding IDEs, IDE extensions, code assistants in incumbent editors, and agentic coding tools
- Source priority: official product docs and release notes first; repositories, pricing pages, user reviews, issue trackers, and credible reporting second
- Merge risk: feature claims and user sentiment can move quickly; repeated secondary reports may share one upstream source

## Parallel Lanes

| Role | Task | Evidence target | Expected output | Merge risk |
| --- | --- | --- | --- | --- |
| `lead-integrator` | Frame question and synthesize | all lane outputs | one final judgment | over-smoothing conflicts |
| `source-scout` | Verify product facts and source genealogy | official docs, pricing, release notes, filings, repositories | source map and gaps | copied reports counted twice |
| `timeline-analyst` | Explain how the category formed | launch dates, release notes, model capability shifts, ecosystem moves | causal timeline | clean origin myth |
| `competitive-analyst` | Map direct and substitute choices | IDEs, extensions, code assistants, CLI agents | user-job comparison | feature checklist without user choice |
| `user-signal-analyst` | Capture real adoption friction | reviews, issues, forums, social posts, support threads | repeated praise / complaints | channel bias |
| `dissent-reviewer` | Challenge emerging conclusion | negative evidence, security concerns, pricing complaints, lock-in risks | reversal conditions | generic skepticism |

## Specialist Returns

### `source-scout`

```text
Role: source-scout
Task: Verify current product facts and source independence.
Key findings:
- E1 confirms [official feature / availability claim].
- E2 and E3 repeat the same upstream announcement, so they should not count as independent confirmation.
- E4 is a gap: pricing or enterprise availability requires current verification.
Evidence IDs: E1, E2, E3, E4
Confidence: medium
Contradictions: public claims may be older than current product state.
What would change my view: updated official pricing, changelog, or current customer evidence.
Hand-off notes: lead should downgrade repeated media claims unless an independent primary source appears.
```

### `timeline-analyst`

```text
Role: timeline-analyst
Task: Build causal category timeline.
Key findings:
- E5 marks the shift from completion to repository-aware editing.
- E6 marks the shift from chat-in-editor to agentic task execution.
- The path dependency is model capability plus editor workflow integration, not only UX polish.
Evidence IDs: E5, E6
Confidence: medium
Contradictions: origin claims differ by whether the category is defined as "AI autocomplete", "AI IDE", or "agentic coding".
What would change my view: stronger evidence that buyers treat these as separate categories.
Hand-off notes: define category before comparing competitors.
```

### `competitive-analyst`

```text
Role: competitive-analyst
Task: Compare options by user job.
Key findings:
- Dedicated AI IDEs compete on integrated workflow and lower setup cost.
- Extensions compete on staying inside an existing editor.
- CLI / agentic tools compete when the job is long-running repository work.
Evidence IDs: E7, E8, E9
Confidence: medium
Contradictions: feature parity changes quickly; current claims need recency checks.
What would change my view: user data showing one workflow dominates across teams.
Hand-off notes: compare by "solo speed", "team governance", "security", "repo context", and "switching cost".
```

### `user-signal-analyst`

```text
Role: user-signal-analyst
Task: Identify repeated user praise and pain.
Key findings:
- E10 shows repeated praise for flow speed and fewer context switches.
- E11 shows repeated complaints around cost, trust, privacy, and brittle agent behavior.
- Social sentiment is noisy and should be treated as user_signal, not market proof.
Evidence IDs: E10, E11
Confidence: low to medium
Contradictions: enthusiastic individual developers may not represent enterprise adoption.
What would change my view: stable survey, retention, or enterprise rollout evidence.
Hand-off notes: preserve user signal separately from product facts.
```

### `dissent-reviewer`

```text
Role: dissent-reviewer
Task: Test the optimistic category story.
Key findings:
- E12 suggests incumbents can absorb many AI IDE features into existing editors.
- E13 suggests security / compliance can slow enterprise adoption.
- E14 is a gap: durable willingness to pay remains under-verified.
Evidence IDs: E12, E13, E14
Confidence: medium
Contradictions: individual productivity stories conflict with organizational governance concerns.
What would change my view: evidence of repeat enterprise expansion and policy-safe deployments.
Hand-off notes: final answer should include a monitor / experiment path rather than a pure GO verdict.
```

## Evidence Ledger Sample

| ID | Lane / role | Claim | Status | Source | Upstream / group | Reliability | Implication |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | source / source-scout | Official product capability claim requires current verification. | gap | official docs / release notes | group-product-facts | unknown | verify before comparing features |
| E2 | source / source-scout | Secondary articles repeat one upstream announcement. | reported_claim | media | upstream-announcement-1 | medium | do not count as independent proof |
| E5 | timeline / timeline-analyst | Category definition changes depending on whether the focus is autocomplete, IDE, or agentic work. | inference | analysis | group-category-definition | medium | define category before judgment |
| E10 | user-signal / user-signal-analyst | Users often praise flow speed and fewer context switches. | user_signal | community / review | group-user-praise | low | useful but not market proof |
| E12 | dissent / dissent-reviewer | Incumbent editors may absorb AI IDE features. | inference | product / ecosystem evidence | group-incumbent-risk | medium | lowers confidence in standalone category durability |

## Parallel Execution Summary

| Role | Main contribution | Evidence IDs | Confidence | Open issue |
| --- | --- | --- | --- | --- |
| `source-scout` | separated primary claims from repeated reports | E1-E4 | medium | current pricing / availability |
| `timeline-analyst` | reframed category as workflow evolution | E5-E6 | medium | category boundary |
| `competitive-analyst` | compared by user job instead of features | E7-E9 | medium | fast-changing feature parity |
| `user-signal-analyst` | separated praise / complaints from proof | E10-E11 | low-medium | channel bias |
| `dissent-reviewer` | identified incumbent, security, and willingness-to-pay risks | E12-E14 | medium | enterprise durability |

## Lead Integrator Synthesis

- Accepted: The market should be analyzed as competing workflows, not only products.
- Rejected or downgraded: repeated articles that trace to one announcement; broad claims based only on social enthusiasm.
- Still unresolved: enterprise adoption durability, willingness to pay, and which workflows become default.
- Final confidence: medium if current sources confirm the product facts; low if the source base is mostly secondary or stale.

## Example Final Judgment

The AI coding IDE market is best understood as a workflow transition from autocomplete to repository-aware and increasingly agentic development. The strongest near-term opportunity is not "the IDE with the most features", but the tool that fits the user's switching-cost tolerance, governance needs, and preferred coding loop.

Recommended next move for a team: run a time-boxed experiment rather than making a category-wide adoption call. Measure task completion speed, review burden, privacy / compliance fit, and whether developers keep using it after novelty fades.

## Reversal Conditions

This view should change if:

- incumbent editors ship equivalent integrated workflows with lower switching cost.
- dedicated AI IDEs show strong retention and enterprise expansion.
- security or privacy constraints make agentic workflows unusable in the target organization.
- model or pricing changes materially alter cost-performance.
