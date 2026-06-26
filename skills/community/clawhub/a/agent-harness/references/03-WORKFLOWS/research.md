# Research Workflow (Step 3 Content)

> **Role**: Pipeline's "specific work content" layer
> **Use Case**: Research, investigation, deep analysis, research reports
> **Load Time**: Pipeline Step 2 execution
> **Combination**: Pipeline + research

---

## Relationship

```
Pipeline (method)       research (content)
──────────────────────────────────────────
Step 1: Plan     ←→   Identify research goal
Step 2: Execute  ←→   Multi-angle research
Step 3: Summarize←→   Synthesize report
Step 4: Check    ←→   Quality verification
```

**Pipeline decides "steps", research decides "what to do at each step"**

---

## 4-Step Research Flow

### Step 1 — Task Decomposition (Pipeline Plan)

**Question**: What to research?

**Operations**:
1. Identify core questions of research topic
2. Decompose into 3-5 sub-topics/dimensions
3. Determine information needs for each dimension

**Output**:
```markdown
## Research Plan

### Topic
{Research Topic}

### Sub-topics
1. {Dimension A}: {Specific Question}
2. {Dimension B}: {Specific Question}
3. {Dimension C}: {Specific Question}
```

### Step 2 — Multi-Angle Research (Pipeline Execute)

**Question**: How to collect information?

**Operations**:
1. Research each sub-topic in parallel
2. Use web_search
3. Use web_fetch for details
4. Record source for each finding

**Information Source Priority**:
| Priority | Source | Use Case |
|----------|--------|----------|
| P0 | Official docs/whitepapers | Technical details, official data |
| P1 | Authoritative media | Industry trends, event analysis |
| P2 | Academic papers | Theoretical basis, research data |
| P3 | Community discussions | Practical experience, user feedback |

### Step 3 — Information Synthesis (Pipeline Summarize)

**Question**: How to form conclusions?

**Operations**:
1. **Deduplication**: Merge duplicate information
2. **Verification**: Cross-validate conflicting information
3. **Extraction**: Extract key facts (FACT) and inferences (INSIGHT)
4. **Gap**: Identify unanswered questions

**Output**:
```markdown
## Research Findings

### Key Facts
- {Fact 1} [Source: {url}]
- {Fact 2} [Source: {url}]

### Insights
- {Inference} [Confidence: High/Medium/Low]

### Knowledge Gaps
- {Unanswered questions}
```

### Step 4 — Report Output (Pipeline Check)

**Question**: Is output quality acceptable?

**Operations**:
1. Load template: `04-TEMPLATES/research-report.md`
2. Output in template format
3. Self-check: Executive summary/sources/confidence/gaps

**Checklist**:
- [ ] Executive summary complete
- [ ] Each finding has source
- [ ] Confidence assessed
- [ ] Knowledge gaps identified

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
