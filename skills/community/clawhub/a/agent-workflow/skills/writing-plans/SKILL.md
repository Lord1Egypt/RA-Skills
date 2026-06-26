---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step task, before starting execution. Trigger when a design document or spec is ready and needs to be broken into actionable steps. Do not trigger without a prior design or spec, and do not trigger during execution."
---

# Writing Plans

## Overview

Write comprehensive execution plans assuming the executor has zero context about this project and unfamiliar with its conventions. Document everything they need to know: which areas to touch for each task, what to produce, what to verify, how to confirm success. Give them the whole plan as bite-sized tasks. Avoid redundancy. Only do what's necessary. Define acceptance criteria before execution.

Assume they are capable, but know almost nothing about this project's domain or toolset.

**Announce at start:** "I'm using the writing-plans skill to create the execution plan."

**Context:** This should be run after a design spec has been approved (created by the brainstorming skill).

**Save plans to:** `docs/plans/YYYY-MM-DD-<task-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent areas, it should have been broken into sub-specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per area. Each plan should produce working, verifiable output on its own.

## Work Structure

Before defining tasks, map out which areas will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each area should have one clear responsibility.
- Prefer smaller, focused deliverables over large ones that do too much.
- Areas that change together should be planned together. Split by responsibility, not by technical layer.
- In existing projects, follow established patterns.

This structure informs the task decomposition. Each task should produce self-contained output that makes sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Define the acceptance criteria for this output" — step
- "Produce the minimal output that meets the criteria" — step
- "Verify output against criteria" — step
- "Record progress / save result" — step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Task Name] Execution Plan

> **For executors:** Use agent-workflow:subagent-driven-execution (recommended) or agent-workflow:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this produces]

**Approach:** [2-3 sentences about the approach]

**Key Resources:** [Key references, tools, or inputs needed]

---
```

## Task Structure

```markdown
### Task N: [Component Name]

**Produces:**
- `exact/path/or/description/of/output`

**Inputs / References:**
- [What this task needs to get started]

- [ ] **Step 1: Define acceptance criteria**

What does "done" look like for this task?
- Criterion A: ...
- Criterion B: ...

- [ ] **Step 2: Produce output**

[Exact description of what to create/write/do, with enough detail that no guessing is needed]

- [ ] **Step 3: Verify against criteria**

Check each criterion:
- [ ] Criterion A met?
- [ ] Criterion B met?

- [ ] **Step 4: Record progress**

Save result to [location]. Note any decisions made.
```

## No Placeholders

Every step must contain the actual content an executor needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate handling" / "handle edge cases" (without specifying which)
- "Similar to Task N" (repeat the content — the executor may be reading tasks out of order)
- Steps that describe what to do without showing how
- References to outputs not defined in any task

## Remember
- Exact locations always
- Complete content in every step — if a step produces output, describe it fully
- Exact verification steps with expected outcomes
- Avoid redundancy. Only do what's necessary. Define acceptance criteria first.

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that addresses it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Consistency check:** Do the names, formats, and references you used in later tasks match what you defined in earlier tasks?

If you find issues, fix them inline. No need to re-review — just fix and move on.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Sequential Execution** — Execute tasks in this session using executing-plans, with checkpoints for review

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use `agent-workflow:subagent-driven-execution`

**If Sequential Execution chosen:**
- **REQUIRED SUB-SKILL:** Use `agent-workflow:executing-plans`
