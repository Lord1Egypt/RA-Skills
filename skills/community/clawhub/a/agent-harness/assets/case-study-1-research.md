# Case Study 1: Deep Research Task

## Trigger
"Research AI Agent market trends"

## Execution Flow

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4 ──→ Step 5
   │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼
01-DECISION  02-PIPELINE 03-WORKFLOW 04-TEMPLATE 05-QUALITY
  Decision    Framework    research   Report      Quality
                                      Template    Check
```

---

### Step 1 — Decision Tree

**Read**: `references/01-DECISION.md`

**Decision**:
```
Task = Research task?
↓
Yes
↓
Pipeline + research
```

**Output**:
```
Final Decision: Pipeline + WORKFLOWS/research
```

---

### Step 2 — Execution Framework

**Read**: `references/02-PIPELINE.md`

**Understand**: Universal 4-step execution flow

```
Pipeline = Cooking method (same for all dishes: prep→cook→plate→taste)

Step 1: Plan
Step 2: Execute
Step 3: Summarize
Step 4: Check
```

---

### Step 3 — Specific Workflow

**Read**: `references/03-WORKFLOWS/research.md`

**Execute**:
```
Pipeline Step 1 (Plan) ──→ research Step 1: Task Decomposition
                    │
                    ├── Identify topic: AI Agent market trends
                    ├── Decompose dimensions: Tech/Business/Competition/Trends
                    └── Output: Research plan

Pipeline Step 2 (Execute) ──→ research Step 2: Multi-angle Research
                    │
                    ├── Tech dimension: search + collect
                    ├── Business dimension: search + collect
                    └── ...

Pipeline Step 3 (Summarize) ──→ research Step 3: Information Synthesis
                    │
                    ├── Deduplicate and verify
                    ├── Extract facts
                    └── Identify gaps

Pipeline Step 4 (Check) ──→ research Step 4: Report Output
                    │
                    └── Cross-check with quality checklist
```

---

### Step 4 — Output Template

**Read**: `references/04-TEMPLATES/research-report.md`

**Fill**:
```markdown
# Research Report: AI Agent Market Trends

**Date**: 2026-04-07

## Executive Summary
{3-5 sentences of core findings}

## Research Findings
### Key Facts
- {fact} [Source: {url}]

### Insight Inferences
- {inference} [Confidence: High]

## References
| # | Source | Reliability |
|---|--------|-------------|
| 1 | {url} | High |

## Next Steps
- {recommendation}
```

---

### Step 5 — Quality Check

**Read**: `references/05-QUALITY.md`

**Check**:
- [ ] Executive summary is complete
- [ ] Every finding has a source
- [ ] Confidence levels are marked
- [ ] Knowledge gaps are identified

---

## Complete Dialogue Example

```
User: Research AI Agent market trends

Agent:
[Pre-Execution Check]
Q1: Multi-step? → Yes
Q2: Research task? → Yes
Final Decision: Pipeline + WORKFLOWS/research

[Step 1] Load 01-DECISION.md
→ Combination confirmed: Pipeline + research

[Step 2] Load 02-PIPELINE.md
→ Understood: 4-step execution framework

[Step 3] Load 03-WORKFLOWS/research.md
→ Started research flow...

[Step 4] Load 04-TEMPLATES/research-report.md
→ Output report per template

[Step 5] Load 05-QUALITY.md
→ Quality check passed
```
