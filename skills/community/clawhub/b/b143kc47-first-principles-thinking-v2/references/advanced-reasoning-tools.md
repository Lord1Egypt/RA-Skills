# Advanced Reasoning Tools for First-Principles Thinking

Use this reference for Deep or Exploration depth, high-stakes decisions, factual
research, or any task where the user asks for more accurate reasoning or richer
brainstorming. Do not load it for simple mechanical tasks.

---

## 1. Compact Tool Plan

Before analysis, select only the tools justified by the problem.

```markdown
### Tool Plan
- Accuracy: [mechanism map / assumption ledger / evidence grounding / Fermi / solver]
- Divergence: [ToT / GoT / morphological matrix / contradiction analysis / debate]
- Verification: [self-consistency / CoVe / backward check / sensitivity / red team]
- Budget: [Quick / Standard / Deep / Exploration]
```

Rule: if the tool will not change the answer, do not use it.

---

## 2. Mechanism Map Template

```markdown
### Mechanism Map
- Actors / systems:
- Objective function or incentive for each actor:
- Inputs:
- Outputs:
- Stocks / flows:
- Bottleneck:
- Causal chain: A -> B -> C
- Mediators:
- Confounders:
- Feedback loops:
- Boundary conditions:
- Falsifying observation:
```

Use text arrows. Avoid decorative diagrams unless the user asks.

---

## 3. Assumption Ledger v2 Template

```markdown
| Assumption | Category | Evidence | Confidence | Fragility | Failure if false | Fastest test | Verdict |
|------------|----------|----------|------------|-----------|------------------|--------------|---------|
| ...        | technical / business / resource / historical / behavioral / data | ... | low / medium / high | ... | ... | ... | keep / modify / discard / investigate |
```

Promotion rules:
- Promote to `[TRUTH]` only if it passes the Ground-Truth Test.
- Promote to `[CONSTRAINT]` only if the source, threshold, and cost of
  violation are explicit.
- Elevate to User Checkpoints if falsehood would reverse the conclusion.

---

## 4. Least-to-Most Decomposition

```markdown
| Subproblem | Why it matters | Intermediate output | Status |
|------------|----------------|---------------------|--------|
| ...        | ...            | variable / constraint / mechanism / test / risk | solved / bounded / unknown |
```

Good subproblems are causally useful. Bad subproblems are just outline headings.

---

## 5. Fermi / Dimensional Check

```markdown
### Quantitative Sanity Check
- Proxy equation:
- Variables:
  - x = low / base / high
  - y = low / base / high
- Unit check:
- Result range:
- Dominant variable:
- Does this change the recommendation? yes / no / uncertain
```

Use ranges rather than fake precision. State when a number is a placeholder.

---

## 6. Evidence Grounding

Use when claims depend on facts, data, papers, recent information,
user-provided sources, observable behavior, or domain-specific sources.

```markdown
### Evidence Grounding
Load-bearing facts to verify:
1. ...
2. ...

Evidence retrieved:
- Source / evidence / tool result:
- What it supports:
- What it does not support:

Inference boundary:
- Source-supported:
- Inferred:
- Unknown:
```

Never let retrieved claims bypass the Claim Ledger. Retrieved facts enter as
`[CLAIM]` until they pass the Ground-Truth Test or are cited as source-supported.

---

## 7. Chain-of-Verification

```markdown
### Verification Questions
1. Which claim is most likely false?
2. Which number, date, source, or fact needs external evidence?
3. Which assumption would flip the answer?
4. What observation would falsify the conclusion?
5. What is the strongest counterexample?

### Verification Answers
- Q1: ...
- Q2: ...

### Revision
- Changed:
- Confidence adjustment:
```

---

## 8. Self-Consistency and Backward Check

```markdown
### Independent Paths
- Path A: [mechanism / economic / physical / causal]
- Path B: [operational / implementation / behavioral]
- Path C: [constraint / risk / adversarial]

### Comparison
| Path | Conclusion | Unique assumption | Weakest link |
|------|------------|-------------------|--------------|

### Backward Check
If conclusion C is true, the following must also be true:
- ...
Are these present in the ledger? yes / no / unknown
```

Do not use voting if all paths share the same fragile premise.

---

## 9. Sensitivity Analysis

```markdown
### Sensitivity
| Variable / assumption | Plausible range | Does recommendation flip? | Test |
|-----------------------|-----------------|---------------------------|------|
| ...                   | ...             | yes / no / maybe          | ...  |

Highest-value next information:
- ...
```

If the recommendation is knife-edge, say so and lower confidence.

---

## 10. Structured Brainstorming Pack

### 10.1 Tree of Thoughts

```markdown
| Option | Core mechanism | Novelty | Feasibility | Risk | Test | Score |
|--------|----------------|---------|-------------|------|------|-------|
```

Generate 3-5 options, expand the top 2, keep the runner-up.

### 10.2 Graph of Thoughts

```markdown
Nodes:
- Assumptions:
- Constraints:
- Mechanisms:
- Resources:
- Analogies:
- Risks:
- User/customer behaviors:

Edges:
- Enables:
- Conflicts with:
- Depends on:
- Amplifies:
- Reduces:

Synthesized intersections:
1. Constraint + resource -> idea
2. Risk + mechanism -> safer variant
3. Analogy + bottleneck -> non-obvious option
```

### 10.3 Morphological Matrix

```markdown
| Dimension | Variants |
|-----------|----------|
| User / actor | ... |
| Job-to-be-done | ... |
| Mechanism | ... |
| Constraint | ... |
| Resource | ... |
| Channel / implementation path | ... |
| Failure mode | ... |
```

Combine variants into at least 10 raw concepts for Exploration depth. Filter by
feasibility, novelty, and mechanism fit.

### 10.4 Contradiction Analysis

```markdown
Contradiction: more X without more Y
Resolution patterns:
- Separate in time:
- Separate in space:
- Modularize:
- Invert:
- Automate / self-service:
- Change the unit of analysis:
```

### 10.5 Multi-Perspective Debate

Roles:
- First-principles mechanist: explains why the option works from primitives.
- Operator: attacks implementation complexity, maintenance, and sequencing.
- Skeptic / red team: attacks assumptions, incentives, security, and failure modes.
- Creative strategist: looks for non-obvious combinations and reframings.

Each role must critique at least one other role. The synthesis must preserve the
strongest objection, not smooth it away.

---

## 11. Formalization / Solver Trigger

When a problem has hard constraints, equations, schedules, Boolean logic,
optimization, or combinatorics, translate prose into variables before answering.

```markdown
Variables:
- ...
Constraints:
- ...
Objective:
- minimize / maximize / satisfy:
Infeasibility means:
- ...
```

Use approved calculation, solver, spreadsheet, or symbolic-math tools when available and useful.
If not available, still keep the variable/constraint representation in the answer.

---

## 12. Final Convergence Checklist

A Deep or Exploration answer is complete only when it has:

- A mechanism map
- A ledger of truths, claims, assumptions, constraints, and unknowns
- At least two genuinely different paths or concepts
- One quantitative or constraint sanity check when magnitudes matter
- A falsifier or fastest experiment
- Sensitivity / confidence calibration
- A short statement of what evidence would change the conclusion
