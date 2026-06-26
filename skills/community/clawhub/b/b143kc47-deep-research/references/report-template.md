# Report Template

Use this as a default. Adapt section names to the user's requested deliverable.

```markdown
# [Research title]

## Executive summary
[3-7 bullets or a short paragraph. State the answer first. Include confidence and the most important uncertainty.]

## Direct answer
[Answer the user's core question. Use evidence IDs like [E0001] for high-impact claims.]

## Key findings

### 1. [Finding]
- Claim: [specific claim] [E0001]
- Why it matters: [decision relevance]
- Confidence: high / medium / low

### 2. [Finding]
...

## Evidence table
| id | source | type | quality | stance | claim supported or contradicted |
|---|---|---:|---:|---|---|
| E0001 | [title / publisher] | paper | 5 | supports | ... |

## Comparison matrix
[Use only when comparing papers, tools, repos, vendors, methods, or options.]

| option | strengths | weaknesses | evidence | fit |
|---|---|---|---|---|

## Contradictions and uncertainty
- [Contradiction or limitation] [evidence IDs for each side]
- [Stale or missing evidence]
- [Assumption made]

## Source-quality notes
[Briefly explain primary vs secondary evidence, source independence, freshness, and any bias concerns.]

## Method appendix
- Effort level: quick / standard / deep / exhaustive
- Hop count: [n]
- Source classes searched: [papers, GitHub, official docs, etc.]
- Counterevidence searched: yes/no; summary
- Files or tools used: [if relevant]
- Remaining open questions: [list]
```

## Claim language

Use calibrated language:

- `shows` only when the source directly demonstrates the claim.
- `suggests` when evidence is partial or context-dependent.
- `claims` when reporting what a source says without endorsing it.
- `likely` when multiple signals align but direct proof is incomplete.
- `unknown` when the searched evidence does not settle the point.

## Evidence table rules

Every row should be specific enough to be checked later. Avoid evidence rows like `web search results show...`. Record the actual source opened, not merely the search query.

## When the user asks for a short answer

Still use the ledger internally for deep research, but compress the final answer:

1. answer first;
2. 3-5 supported findings;
3. one caveat paragraph;
4. compact source list or evidence table.

## When the user asks for an implementation recommendation

Add:

```markdown
## Recommendation
[Recommended option and rationale]

## Adoption risks
[Version, maintenance, security, license, integration, cost]

## Minimum validation plan
[Small test or experiment that would reduce the biggest uncertainty]
```

## When the user asks for literature review

Add:

```markdown
## Literature map
| cluster | representative papers | core idea | limitations |
|---|---|---|---|

## Open research questions
[What remains unresolved across the literature]
```
