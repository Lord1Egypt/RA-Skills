# Execution Framework (Layer 2)

> **Role**: Universal 4-step execution flow
> **Load Time**: Step 2 (after Pipeline mode confirmed)
> **Note**: Pipeline is "the same process regardless of what you're doing"

---

## Pipeline = Universal Cooking Method

```
No matter if you're making fish-flavored pork or tomato scrambled eggs,
the basic cooking steps are the same:
1. Prepare ingredients
2. Stir-fry
3. Season
4. Plate

Pipeline is the same:
1. Plan
2. Execute
3. Summarize
4. Check
```

---

## 4-Step Execution Flow

### Step 1 — Plan

**Question**: What am I going to do?

```
Pipeline Step 1:
1. Understand task goal
2. Determine specific steps
3. Estimate time and resources
```

### Step 2 — Execute

**Question**: Act according to plan

```
Pipeline Step 2:
1. Execute according to plan
2. Record intermediate results
3. Adjust if problems arise
```

### Step 3 — Summarize

**Question**: What did I produce?

```
Pipeline Step 3:
1. Organize all outputs
2. Merge into unified format
3. Prepare for final output
```

### Step 4 — Check

**Question**: Is the quality acceptable?

```
Pipeline Step 4:
1. Load QUALITY.md
2. Cross-check
3. Return to Step 2 for correction if not passed
```

---

## Gate Mechanism

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
  │           │           │           │
  │    ⚠️ Previous step must be complete    │
  │        before entering next      │
  │           │           │           │
  └───────────┴───────────┴───────────┘
                     │
              Only all passes
              counts as task complete
```

---

## Relationship with WORKFLOWS

**Pipeline is the "cooking method", WORKFLOWS is the "recipe"**

```
Pipeline (method)       WORKFLOWS (content)
────────────────────────────────────────────
Heat pan              Fish-flavored pork ingredients
Add oil               Cut pork strips
Stir-fry              Stir-fry pork
Season                Add seasonings
Plate                 Arrange on plate
```

**Pipeline doesn't care what dish you're making, steps are always the same.**
**Pipeline is responsible for "steps", not "content".**

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
