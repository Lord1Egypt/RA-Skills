---
name: Feature Planning AutoPilot
description: A general-purpose feature development planning skill. Used to generate executable, verifiable, and iterative development plans before coding, and to automatically capture lessons learned after each conversation.
license: MIT
---

# Feature Planning AutoPilot

This Skill standardizes the "analyze first → plan next → implement last" approach. It applies to frontend, backend, full-stack, API integration, SQL migrations, and mobile page refactoring tasks.

## 1) When to Use

Activate this Skill when the user expresses any of the following intentions:

- "Analyze before writing code"
- "Give me a plan first" / "Break it into steps" / "Execute in phases"
- "Ensure correctness and feasibility"
- "Create a reusable implementation blueprint"

## 2) Expected Outputs

Every planning session must produce the following four deliverables:

1. **Scope Definition**: Clearly state what is and is not included in this task.
2. **Execution Plan**: 3–9 verifiable steps in clear sequence.
3. **Risks & Rollback**: Key risk points and a minimal rollback strategy.
4. **Acceptance Checklist**: Actionable verification items (APIs, pages, logs, builds, tests).

## 3) Standard Workflow (Must Follow in Order)

### Phase A – Quick Clarification

- Restate the goal in 1–2 sentences
- Confirm constraints: tech stack, directory, whether API/DB changes are allowed, timeline
- If information is missing: ask at most 1–3 key questions; default when possible

### Phase B – Context Scan

Complete at minimum the following checks before producing a plan:

- Location of relevant pages / APIs / services
- Data sources and state transitions (e.g., `Pending Delivery → Pending Inbound → Completed`)
- Existing similar implementations (prefer reuse)
- List of files likely to be affected

### Phase C – Plan Drafting

Plan requirements:

- 3–9 steps, each with a concise 3–7 word action title
- Every step must be verifiable (has a "definition of done")
- Only 1 step may be `in-progress` at a time
- State prerequisites for external dependencies or database changes

### Phase D – Implementation & Validation

- Execute the plan step by step; update status after each step
- Perform at least one local validation per phase
- Before finishing, run a minimum viable acceptance check (build / key path click-through / API response)

### Phase E – Lessons Captured (Auto-Iterate)

At the end of the conversation, append three categories of experience to `evolution.json`:

- `preferences`: User's preferred output style or delivery format
- `fixes`: Issues encountered this session and how they were resolved
- `custom_prompts`: Strong prompts that can be reused directly next time

Also sync the learnings back into the "Experience Enhancements" section of `SKILL.md`.

## 4) Plan Template (Ready to Reuse)

```markdown
## Feature Development Plan (AutoPilot)

### 0. Goal & Scope
- Goal:
- Included in this task:
- Excluded from this task:
- Prerequisites:

### 1. Execution Steps
1. [ ] Review current state and dependencies
   - Definition of done: Relevant files and data flow located
2. [ ] Design minimal-change solution
   - Definition of done: Modification points and impact surface confirmed
3. [ ] Implement core changes
   - Definition of done: Core path code complete
4. [ ] Handle edge cases and errors
   - Definition of done: Empty state / failure state / permission state all functional
5. [ ] Verify and regression test
   - Definition of done: Key paths pass, results are reproducible

### 2. Risks & Rollback
- Risk:
- Monitoring signal:
- Rollback method:

### 3. Acceptance Criteria
- [ ] Feature behavior matches requirements
- [ ] No new build errors introduced
- [ ] Key UI / API paths verified
```

## 5) High-Quality Plan Rules (Hard Constraints)

- No "hollow steps" (e.g., "implement feature")
- Never omit "data source" or "state transitions"
- No unrelated large-scale changes (only minimal changes relevant to the task)
- Never skip validation (at least one local check + one result check)
- Never overstate conclusions (explicitly say so when something cannot be verified)

## 6) Common Task Mappings

### A. Mobile Page Optimization

Must include:

- Visual layer (spacing, overflow, readability, tap target size)
- Interaction layer (default state, disabled state, loading state, empty state)
- Data layer (API fields consistent with rendered output)

### B. List / Stats Consistency

Must include:

- Confirm same source API
- Confirm same filtering criteria
- Verify homepage numbers match detail list

### C. State-Driven Workflows (e.g., Inbound)

Must include:

- Define initial state
- Define conditions that trigger state transitions
- Intercept and prompt for invalid states

## 7) Auto-Iteration Protocol

Trigger an experience update for this Skill when any of the following conditions are met:

- User explicitly responds with "this is great" or "this isn't working"
- A build error occurs and is resolved
- A deviation between the plan and the actual implementation is corrected

### Update Structure

`evolution.json` follows this structure:

```json
{
  "last_updated": "ISO_DATETIME",
  "preferences": [],
  "fixes": [],
  "custom_prompts": ""
}
```

### Principles for Writing Learnings

- Preferences → write abstract rules (reusable across projects)
- Fixes → write "trigger condition + resolution approach"
- Prompts → write instructions that can be pasted directly

## 8) Recommended Trigger Commands

- `/plan-auto` — Generate a standard execution plan
- `/plan-auto deep` — Output a full plan including risks and rollback
- `/plan-auto mobile` — Focus on mobile page and interaction refactoring
- `/plan-auto evolve` — Automatically capture learnings at the end of the session

## 9) Experience Enhancements (Synced from evolution.json)

> This section is auto-updated by the iteration process to prevent experience loss.

### User-Learned Best Practices & Constraints

- Plan conclusions must align with the current implementation scope; avoid overreaching beyond applicable scenarios.
- Before presenting an implementation plan, cross-check existing code and database state to ensure the plan is logically sound and actionable.
- Before outputting a plan, clearly define the applicable scope and state transition conditions, and state all necessary prerequisites.
