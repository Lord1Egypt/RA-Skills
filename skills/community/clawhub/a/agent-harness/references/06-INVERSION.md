# Inversion (Requirements Clarification Workflow)

> **Role**: When requirements are unclear, gather requirements before action
> **Use Case**: Fuzzy requirements, unclear goals, missing key information
> **Load Time**: When Decision Tree determines "requirements unclear"

---

## Core Principle

**⚠️ Gate: DO NOT start building until all phases are complete**

Before requirements collection is complete, prohibited from executing any substantive work.

---

## 3-Phase Flow

### Phase 1 — Problem Discovery

**Goal**: Figure out what the user really wants to solve

**Operations**:
1. Ask one question at a time
2. Wait for user response before next question
3. Follow up key details (background/purpose/constraints)

**Output**:
```markdown
## Requirements Understanding

### Core Problem
{One-sentence description of what user wants to solve}

### Key Details
- {Detail A}
- {Detail B}
- {Detail C}
```

---

### Phase 2 — Technical Constraints

**Goal**: Clarify objective constraints

**Operations**:
1. Confirm tech stack/platform/tool constraints
2. Confirm data/permissions/resource constraints
3. Confirm time and quality requirements

**Output**:
```markdown
## Constraints

### Technical Constraints
- {Constraint A}

### Resource Constraints
- {Constraint A}

### Time/Quality Constraints
- {Constraint A}
```

---

### Phase 3 — Synthesis & Confirmation

**Goal**: Generate complete action plan, wait for user confirmation before execution

**Operations**:
1. Combine Phase 1 + Phase 2, generate complete plan
2. Describe clearly: what to do → how to do → what to output
3. Wait for user confirmation before execution phase

**Output**:
```markdown
## Action Plan

### Goal
{One-sentence goal}

### Execution Steps
1. {Step 1}
2. {Step 2}
3. {Step 3}

### Output
{Deliverable description}

---
Please confirm if this plan meets your expectations. I will begin execution after confirmation.
```

---

## Quick Execution Checklist

```
Inversion Quick Execution Checklist:
□ Load inversion.md
□ Send Phase 1 first question
□ Wait for user response
□ Follow up key details (1-3 questions)
□ Enter Phase 2: Confirm constraints
□ Enter Phase 3: Generate plan and request confirmation
□ Begin execution only after confirmation
```

---

_Last updated: 2026-04-07 by neltharion11 | https://github.com/neltharion11/skill-agent-harness_
