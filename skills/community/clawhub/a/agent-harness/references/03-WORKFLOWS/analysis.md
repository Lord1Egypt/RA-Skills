# Analysis Workflow (Step 3 Content)

> **Role**: Pipeline's "specific work content" layer
> **Use Case**: Multi-dimensional analysis, competitive analysis, comparative evaluation
> **Load Time**: Pipeline Step 2 execution
> **Combination**: Pipeline + analysis

---

## Relationship

```
Pipeline (method)       analysis (content)
──────────────────────────────────────────
Step 1: Plan     ←→   Dimension Decomposition
Step 2: Execute  ←→   Data Collection
Step 3: Summarize←→   Cross-dimension Comparison
Step 4: Check    ←→   Conclusion Verification
```

---

## 4-Step Analysis Flow

### Step 1 — Dimension Decomposition (Pipeline Plan)

**Question**: From what angles to analyze?

**Operations**:
1. Clarify analysis goal
2. Identify key dimensions (3-7)
3. Define evaluation criteria

**Output**:
```markdown
## Analysis Dimensions

### Analysis Goal
{Core Question}

### Dimension Definitions
| Dimension | Definition | Standard |
|-----------|------------|----------|
| A | {Definition} | {Standard} |
| B | {Definition} | {Standard} |
```

### Step 2 — Data Collection (Pipeline Execute)

**Question**: Data for each dimension?

**Data Classification**:
| Type | Reliability |
|------|-------------|
| Primary data | High |
| Official public | High |
| Authoritative third-party | Medium |
| Community/reviews | Medium-Low |

### Step 3 — Cross-Dimension Comparison (Pipeline Summarize)

**Question**: Patterns across dimensions?

**Analysis Types**:
| Type | Method |
|------|--------|
| Advantage analysis | Find outstanding items across dimensions |
| Disadvantage analysis | Find weak items across dimensions |
| Comparison matrix | Build scoring matrix |

**Output**:
```markdown
## Cross-Dimension Comparison

### Scoring Matrix
| Subject | Dimension A | Dimension B | Total |
|---------|-------------|-------------|-------|
| X       | 8           | 7           | 15    |
| Y       | 6           | 9           | 15    |
```

### Step 4 — Conclusion Output (Pipeline Check)

**Question**: Final conclusion and suggestions?

**Output**:
```markdown
## Analysis Conclusions

### Core Conclusion
{1-3 sentences}

### Actionable Suggestions
1. **{Suggestion 1}**: {Description}
2. **{Suggestion 2}**: {Description}

### Confidence Assessment
- Confidence: {High/Medium/Low}
- Uncertainty: {Description}
```

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
