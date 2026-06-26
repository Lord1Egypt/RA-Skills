# Case Study 2: Multi-Agent Coordination Task

## Triggers
"Help me analyze the competitive landscape of three products simultaneously"
"Task decomposition" / "multi-agent" / "parallel execution"

## Execution Flow

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4 ──→ Step 5
   │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼
01-DECISION  02-PIPELINE 03-WORKFLOW 04-TEMPLATE 05-QUALITY
  Decision    Framework    subagent   Summary     Quality
                                      Template    Check
```

---

## Detailed Steps

### Step 1 — Decision Tree

**Decision**:
```
Task = Multi-step? → Yes
Task type = Coordination (multi-agent)?
↓
Yes
↓
Pipeline + subagent
```

---

### Step 2 — Execution Framework

**Read**: `references/02-PIPELINE.md`

```
Pipeline = Cooking method

Step 1: Plan ──→ Cook three dishes today
Step 2: Execute ──→ Three pans cooking simultaneously
Step 3: Summarize ──→ Put three dishes together
Step 4: Check ──→ Taste and score
```

---

### Step 3 — Specific Workflow

**Read**: `references/03-WORKFLOWS/subagent.md`

```
Pipeline Step 1 (Plan) ──→ subagent Step 1: Task Analysis
                    │
                    ├── Complexity: 3 products, >5 steps → needs decomposition
                    ├── Parallelism: 3 analyses can run in parallel → suits multi-agent
                    └── Decision: Start multi-agent coordination

Pipeline Step 2 (Execute) ──→ subagent Step 2-3: Decompose + Parallel
                    │
                    ├── Create Sub-task A: Analyze Product A
                    ├── Create Sub-task B: Analyze Product B
                    ├── Create Sub-task C: Analyze Product C
                    │
                    ├── Start Sub-A (independent session)
                    ├── Start Sub-B (independent session)
                    ├── Start Sub-C (independent session)
                    │
                    └── Wait for all to complete

Pipeline Step 3 (Summarize) ──→ subagent Step 4: Result Merge
                    │
                    ├── Collect Sub-A results
                    ├── Collect Sub-B results
                    ├── Collect Sub-C results
                    │
                    ├── Cross-comparison
                    ├── Identify differences
                    └── Generate comprehensive report
```

---

### Step 4 — Output Template

**Load**: `references/04-TEMPLATES/analysis-report.md`

---

## Complete Dialogue Example

```
User: Help me analyze the competitive landscape of Product A, B, and C

Agent:
[Pre-Execution Check]
Q1: Multi-step? → Yes
Q2: Coordination task? → Yes
Final Decision: Pipeline + WORKFLOWS/subagent

[Step 1] Combination confirmed: Pipeline + subagent

[Step 2] Load 02-PIPELINE.md
→ Understood: Plan→Decompose→Parallel→Merge

[Step 3] Load 03-WORKFLOWS/subagent.md
→ Started execution...

[Step 3.1] Task analysis
→ Decision: decompose into 3 sub-tasks

[Step 3.2] Launch 3 sub-agents in parallel
→ Sub-A: Analyze Product A
→ Sub-B: Analyze Product B
→ Sub-C: Analyze Product C

[Step 3.3] Wait for completion, merge results
→ Comprehensive conclusion: {competitive landscape analysis}

[Step 4] Output per template

[Step 5] Quality check
```

---

## Difference from Research Task

| Dimension | Research Task | Coordination Task |
|-----------|---------------|-------------------|
| WORKFLOW | research | subagent |
| Step 2 | Multi-angle information collection | Launch multiple sub-agents |
| Sub-tasks | Parallel search of different dimensions | Parallel analysis of different products |
| Merge | Information synthesis | Result merging |
