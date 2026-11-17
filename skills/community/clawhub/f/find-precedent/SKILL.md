---
name: find-precedent
description: >
  Part of the Overpowered skill suite.
  Find and compare relevant historical cases—contracts, proposals, projects, incidents, decisions, designs, or exceptions—to inform a current problem without treating similarity as authority. Use when the question is effectively 'have we dealt with something like this before?' or reusable prior work may exist.
compatibility: >
  Requires access to one or more historical knowledge sources through RAG, search, document repositories, or equivalent tools for full functionality.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "1-knowledge"
  version: "0.1.0"
---

# Overpowered / Find Precedent

## Core rule

**Find comparable prior cases, explain why they are comparable, extract reusable lessons, and make material differences impossible to miss. Never convert precedent into authority.**

## Procedure

1. Define the **current case** and the decision the precedent should inform.
2. Extract 3–7 comparison dimensions that actually matter: customer type, requirement, risk, contract shape, architecture, scale, jurisdiction, outcome, etc.
3. Search the most appropriate historical source. If source selection is unclear, use `know-enough` first.
4. Rank candidate precedents by decision-relevant similarity, not wording similarity alone.
5. For each useful precedent, capture:
   - why it is comparable;
   - decision/action taken;
   - known outcome;
   - material differences;
   - what is reusable;
   - what must not be copied blindly.
6. Synthesize patterns across cases. Preserve outliers when they matter.

## Output contract

```text
Current decision: ...

Precedent 1
- Similar because: ...
- What was done: ...
- Outcome: ...
- Material differences: ...
- Reusable: ...
- Do not copy blindly: ...

Pattern across precedents: ...
Limits of analogy: ...
```

## Gotchas

- Semantic similarity is only a candidate-generation signal.
- A signed historical contract does not define current legal policy.
- Old proposals may contain stale features, prices, dates, staffing, or commitments.
- Do not hide cases that contradict the preferred answer.
- If no sufficiently comparable precedent exists, say so.

## Stop condition

Stop when enough comparable cases exist to identify a stable pattern or when further search is unlikely to improve the analogy.
