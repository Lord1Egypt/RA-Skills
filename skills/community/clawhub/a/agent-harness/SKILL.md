---
name: agent-harness
description: |
  Agent Work Framework. Unified entry thinking framework + workflow Skill.
  
  Trigger Words (Thinking Modes):
  research, plan, design, think, pattern, process, step, review, score, analyze,
  evaluate, compare, survey, solution, feasibility, summary, deep research,
  research report, task decomposition, multi-agent, parallel execution,
  context compression, long-task planning
---

# Agent Harness

> **One-line summary**: First decide "what combination to use", then execute layer by layer.
> 
> **Core Relationship**:
> ```
> Decision Tree → Choose "Pipeline + which WORKFLOWS"
> Pipeline = Execution Framework (universal)
> WORKFLOWS = Work Content (specific)
> ```

---

## ⚠️ Pre-Execution Check (Must Confirm Each Item)

```
When receiving a task, first answer these questions:

1. [ ] What is the core task? (multi-step / single-step)
2. [ ] Is the requirement clear? (clear → next / unclear → load 06-INVERSION.md)
3. [ ] Does it need multi-step execution? (yes → Pipeline + other)
4. [ ] What is the specific content? (corresponds to which WORKFLOWS)
```

**Response Format**:
```
[Pre-Execution Check]
Q1: xxx → Conclusion
Q2: xxx → Conclusion
...
Final Decision: Pipeline + WORKFLOWS/{name}
Or: Final Decision: Inversion (standalone mode)
```

---

## Layer Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Layer Execution Order                       │
│                                                               │
│  Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4 ──→ Step 5      │
│     │           │           │           │           │        │
│     ▼           ▼           ▼           ▼           ▼        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │Decision│→│Pipeline │→│WORKFLOW│→│Template│→│Quality │     │
│  │01-     │ │02-      │ │03-     │ │04-     │ │05-     │     │
│  │DECISION│ │PIPELINE │ │WORKFLOWS│ │TEMPLATE│ │QUALITY │     │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
│                                                               │
│  Decision Tree decides "which combination",                  │
│  Pipeline decides "universal execution flow",                │
│  WORKFLOWS decides "specific work content"                   │
└─────────────────────────────────────────────────────────────┘
```

### Analogy

```
🍳 Cooking Scenario:
- Decision Tree = Customer orders ("spicy today")
- Pipeline = Cooking method (heat pan first, no matter what)
- WORKFLOWS = Specific recipe (how to make fish-flavored pork)
- Template = Plating style (how to arrange the plate)

💻 Software Scenario:
- Decision Tree = Task classification ("this is a research task")
- Pipeline = Execution flow (decompose first, no matter the research)
- WORKFLOWS = Research method (4-step method)
- Template = Report format (title-abstract-body-conclusion)
```

---

## Execution Flow

### Step 1 — Decision (Load 01-DECISION.md)

```
[Step 1] Read references/01-DECISION.md
         Decide: Pipeline + which WORKFLOWS

Common Combinations:
- Pipeline + research    → Research tasks
- Pipeline + subagent    → Coordination tasks
- Pipeline + context     → Compression tasks
- Pipeline + analysis    → Analysis tasks
```

### Step 2 — Execution Framework (Load 02-PIPELINE.md)

```
[Step 2] Read references/02-PIPELINE.md
         Understand: Universal 4-step execution flow

Pipeline Steps:
Step 1: Plan
Step 2: Execute
Step 3: Summarize
Step 4: Check
```

### Step 3 — Specific Content (Load 03-WORKFLOWS/{name}.md)

```
[Step 3] Read references/03-WORKFLOWS/{corresponding workflow}.md
         Execute: Specific work content

research = 4-step research (decompose→research→synthesize→report)
subagent = 4-step coordination (analyze→decompose→parallel→merge)
context  = 4-step compression (assess→strategy→execute→verify)
analysis = 4-step analysis (decompose→collect→compare→conclude)
```

### Step 4 — Output Template (Load 04-TEMPLATES/{name}.md)

```
[Step 4] Read references/04-TEMPLATES/{corresponding template}.md
         Generate: Structured final output
```

### Step 5 — Quality Check (Load 05-QUALITY.md)

```
[Step 5] Read references/05-QUALITY.md
         Verify: Output quality meets standards
```

---

## Quick Reference: Common Combinations

| Task Type | Combination | Description |
|-----------|-------------|-------------|
| 📝 Deep Research Report | Pipeline + **research** | Multi-step research flow |
| 🤖 Multi-Agent Coordination | Pipeline + **subagent** | Decompose+parallel+merge |
| 📦 Long-Task Compression | Pipeline + **context** | Context management strategy |
| ⚖️ Competitive Analysis | Pipeline + **analysis** | Multi-dimensional comparison |
| ❓ Unclear Requirements | **Inversion** (standalone) | Gather requirements first |

---

## Forbidden Behaviors

- ❌ **Skip Steps**: Go to Step 3 without completing Step 1
- ❌ **Mix Layers**: Treat Pipeline and WORKFLOWS as the same thing
- ❌ **Missing Template**: Output content but format is chaotic
- ❌ **Missing Check**: End without quality verification

---

## Completion Flag

```
[agent-harness execution complete]
✓ Steps 1-5 completed
✓ Combination: Pipeline + WORKFLOWS/{name}
✓ Forbidden behaviors check: Passed
```

---

## File Index

| File | Role | Load Time |
|------|------|-----------|
| `SKILL.md` | Entry + Layer Description | On trigger |
| `references/01-DECISION.md` | Decision Tree | Step 1 |
| `references/02-PIPELINE.md` | Execution Framework | Step 2 |
| `references/03-WORKFLOWS/research.md` | Research Content | Step 3 |
| `references/03-WORKFLOWS/subagent.md` | Coordination Content | Step 3 |
| `references/03-WORKFLOWS/context.md` | Compression Content | Step 3 |
| `references/03-WORKFLOWS/analysis.md` | Analysis Content | Step 3 |
| `references/04-TEMPLATES/research-report.md` | Research Template | Step 4 |
| `references/04-TEMPLATES/analysis-report.md` | Analysis Template | Step 4 |
| `references/06-INVERSION.md` | Requirements Clarification | When unclear |
| `references/05-QUALITY.md` | Quality Check | Pipeline Step 4 |

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
