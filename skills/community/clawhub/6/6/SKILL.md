---
name: multiverse-architect
description: Explore and compare multiple parallel solution designs ("universes") before coding, then converge on a single, well-justified approach. Use when problems are ambiguous, have many trade-offs, or the user is unsure which direction to take.
---

# Multiverse Architect

Design software as if exploring parallel universes: generate several distinct solution paths, explore each briefly, then choose and refine the best one with clear reasoning and trade-offs.

This skill is intentionally **imaginative yet practical**. It turns vague or high-stakes problems into a structured exploration of alternatives before writing or modifying code.

---

## When to Use This Skill

Use **Multiverse Architect** when:

- The task is **ambiguous** or has many possible approaches.
- There are **important trade-offs** (performance vs simplicity, DX vs UX, short-term vs long-term).
- The user says things like:
  - "不确定应该怎么实现" / "I'm not sure which way is better."
  - "有没有别的方案？" / "Are there other options?"
  - "我们要不要用某某框架？" / "Should we use framework X?"
- The change impacts **architecture, data models, or cross-cutting behavior**.

Do **not** use this skill for:

- Trivial bug fixes with an obvious solution.
- Purely mechanical changes (renaming, formatting, small copy edits).

---

## Core Principles

1. **Parallel universes, not random variants**
   - Each "universe" is a **coherent, internally consistent design**, not a tiny tweak.
   - Differences must be **meaningful** (architecture style, data shape, ownership boundaries, flow of control).

2. **Shallow first, deep later**
   - Start with **coarse-grained sketches** of each universe.
   - Only go deep on the one that is ultimately chosen.

3. **Explicit trade-offs**
   - For each universe, list **pros, cons, and risks**.
   - Always tie trade-offs back to the user’s actual constraints (team skills, deadlines, performance, etc.), inferred from context when not stated.

4. **Reversible decisions**
   - Prefer designs that **keep options open** and make it easier to pivot later.
   - Call out which choices are **hard to change** vs **easy to change**.

---

## Workflow Overview

Follow this 4-phase workflow:

1. **Clarify the problem** (what must be true, what is flexible)
2. **Generate 3–4 universes** (distinct solution designs)
3. **Evaluate and converge** (pick one, maybe merge good ideas)
4. **Produce a concrete implementation plan**

Use this process **before** writing or modifying code for large or ambiguous tasks.

---

## Phase 1: Clarify the Problem

When this skill is activated, start by constructing a concise problem summary and constraints list in your own words.

### 1.1 Problem Snapshot

Produce a short snapshot with this structure:

```markdown
## Problem snapshot
- Goal: [...]
- Existing context: [...]
- Hard requirements: [...]
- Soft preferences: [...]
- Unknowns / assumptions: [...]
```

Guidelines:

- **Goal**: Describe the user-visible outcome, not the implementation.
- **Existing context**: Mention relevant tech stack, files, or patterns already in use.
- **Hard requirements**: Things that must not break or be violated.
- **Soft preferences**: Things that are "nice to have" (DX, style, etc.).
- **Unknowns / assumptions**: State assumptions you will proceed with; adjust later if proven wrong.

### 1.2 Sanity Check

Silently check:

- Is the problem actually **simple** with a single obvious path?
  - If yes, **reduce this skill** to a quick single-universe justification and proceed with normal implementation.
- Otherwise, continue to Phase 2.

---

## Phase 2: Generate Universes

Create **3 to 4** distinct universes (solutions). Fewer than 3 is allowed only when the space is clearly narrow.

### 2.1 Universe Template

For each universe, use:

```markdown
### Universe X – [Short name]

**Core idea**: One-sentence summary of the approach.

**Architecture sketch**:
- Key components / modules
- How data flows
- How responsibility is divided

**How it would look in this project**:
- Key files to touch or create
- Rough APIs / interfaces
- How it fits existing conventions (or why it intentionally diverges)

**Pros**:
- [...]

**Cons / risks**:
- [...]

**Most suitable when**:
- [...]
```

### 2.2 Encourage Genuine Diversity

When generating universes:

- Intentionally vary:
  - **Where complexity lives** (frontend vs backend, infra vs app logic).
  - **Data contracts** (rich objects vs thin DTOs, normalized vs denormalized).
  - **Control flow** (event-driven vs request/response, imperative vs declarative).
- Avoid fake variation like:
  - "With comments" vs "without comments".
  - Only changing naming or minor patterns.

---

## Phase 3: Evaluate and Converge

Once universes are defined, **compare and pick**.

### 3.1 Comparison Matrix

Construct a compact comparison:

```markdown
## Universe comparison

| Universe | Complexity | Performance | DX / Maintainability | Risk | Notes |
|---------|------------|-------------|----------------------|------|-------|
| U1      | low/med/high | ...       | ...                  | ...  | ...   |
| U2      | ...        | ...         | ...                  | ...  | ...   |
| U3      | ...        | ...         | ...                  | ...  | ...   |
```

Adjust columns as needed (e.g., "Scalability", "Time-to-implement").

### 3.2 Choose (or Hybridize) a Universe

Then produce:

```markdown
## Decision

- Chosen universe: [Ux or Hybrid of Ux + Uy]
- Main reasons:
  - [...]
  - [...]
- Borrowed ideas from other universes:
  - From [Uy]: [...]
  - From [Uz]: [...]
```

Guidelines:

- If combining, **name the hybrid** and clearly state which pieces come from which universe.
- Explicitly justify **why the rejected universes were rejected** (too complex, too brittle, misaligned with constraints, etc.).

---

## Phase 4: Implementation Plan

Turn the chosen universe into a concrete plan that you will then execute using normal tools and workflows.

### 4.1 Plan Template

Use this:

```markdown
## Implementation plan (Multiverse Architect)

### Scope
- Files to modify:
  - [...]
- New files / modules:
  - [...]
- Out-of-scope:
  - [...]

### Steps
1. [...]
2. [...]
3. [...]

### Safety checks
- [ ] Existing behavior covered by tests or manual checks
- [ ] Data migrations (if any) are planned
- [ ] Rollback strategy is identified (what to revert if needed)
```

### 4.2 Execution Mode

After the plan is created:

- Proceed with actual implementation **outside** this skill, using standard coding behavior.
- If the user changes constraints mid-way, **revisit**:
  - Either adjust the current universe.
  - Or briefly spin up **one new alternative universe** to re-evaluate.

---

## Mini-Mode: Lightweight Multiverse

For **medium-sized** decisions (too big to be trivial, too small for full multiverse), use this compressed flow:

1. Write a 1-paragraph problem snapshot.
2. Sketch **2 universes** with only:
   - Core idea
   - 2–3 pros
   - 2–3 cons
3. Choose one in 3–4 bullet points.
4. Write a short 3–5 step implementation outline.

Then continue as usual with coding.

---

## Examples

### Example A – Choosing a State Management Strategy

User: "我们要不要把这个 React 项目的状态全部换成 Zustand，还是继续用 Redux？"

Apply this skill:

1. Snapshot problem (current Redux usage, pain points, team familiarity).
2. Generate universes like:
   - U1: "Stay on Redux but modernize (Toolkit, RTK Query)."
   - U2: "Hybrid: key global state in Redux, local / view state in Zustand."
   - U3: "Full migration to Zustand with new patterns."
3. Compare along learning curve, migration risk, DX, library ecosystem.
4. Choose and produce a concrete migration (or non-migration) plan.

### Example B – Designing a Feature Flag System

User: "需要一个开关系统来灰度发布新功能，但不确定要做多复杂。"

Universes might be:

- U1: Config-file-based flags with a simple in-process helper.
- U2: Centralized flag service + SDK-like helper.
- U3: Database-backed flags with admin UI.

Then:

1. Evaluate based on team size, deployment frequency, and risk tolerance.
2. Choose U1 + tiny piece of U2 (clear abstraction boundary).
3. Output a focused plan touching specific modules/files.

---

## Summary Checklist for Using This Skill

Before leaving Multiverse Architect mode, verify:

- [ ] A clear **problem snapshot** has been written.
- [ ] At least **2–3 genuinely distinct universes** have been explored.
- [ ] A **comparison** table or bullet list exists.
- [ ] A single approach (or hybrid) has been **explicitly chosen**.
- [ ] There is a concrete, step-based **implementation plan** connected to the codebase.

Once all are satisfied, proceed to implement using the chosen design.

