---
name: agent-sorting-hat
description: Diagnose agent role drift, team-structure problems, operating issues, and role misalignment; then redesign roles, boundaries, and team placement before persona refinement.
---

# Agent Sorting Hat

Use this skill when an existing agent or agent team feels wrong, overloaded, blurred, under-specified, or misaligned.

This skill is for **sorting / alignment / placement**.
It is **not** for final persona polishing, identity-binding, or character-soul refinement.

If the problem is “this agent seems off,” “this team boundary is unclear,” “should this be one agent or three,” or “this role keeps drifting,” use this skill before rewriting persona files.

## Use this skill when

Trigger on requests like:

- “This agent feels wrong.”
- “She keeps giving plans but not executing.”
- “This persona and its job seem mismatched.”
- “We need to rebuild this agent.”
- “These agents have blurry boundaries.”
- “Should this be split into multiple roles?”
- “Do we need a new agent, or is the current one just in the wrong position?”
- “Our team structure is off.”

## Do not use this skill for

Do **not** use this skill as the first choice when:

1. The user only wants persona refinement, tone reshaping, identity-binding, or stronger character feel.
   - Use `ollivanders-agent-shop` instead.
2. The user wants a brand-new agent from scratch with no role-drift or team-structure question.
   - Use the most appropriate creation/persona skill instead.
3. The user only wants a small wording tweak to one file.
   - Edit directly if no deeper role problem exists.

## Core rule

**Diagnose placement before personality.**

Do not jump into persona rewriting until you have checked whether the real problem is:

1. **Role misalignment** — the agent is in the wrong job.
2. **Team gap** — one agent is covering too many incompatible responsibilities.
3. **Operating problem** — the role is correct, but the workflow, subagent use, delegation judgment, or output pattern is broken.
4. **Persona problem** — the role is correct, but the tone, identity, or character grounding is weak.

Use this order strictly:

1. Role misalignment
2. Team gap
3. Operating problem
4. Persona problem

## Required workflow

Follow these steps in order.

### 1. Read the current role context
Read only the files needed to understand the current situation, typically:

- the target agent’s role/persona files
- any relevant team/proposal docs
- any current-team-state or registry documents
- one or two strong comparison examples, if relevant

### 2. Identify the task chain
Determine the actual work chain behind the problem.

Typical chain examples:

- research / analysis
- design / strategy
- execution / production
- audit / risk
- quality control
- coordination / integration

Do not start by asking “who is this character?”
Start by asking: **what work chain is actually happening here?**

### 3. Diagnose the problem type
Classify the issue into one or more of:

- role misalignment
- team gap
- operating problem
- persona problem

State clearly which one is primary.

### 4. Decide whether to keep, split, merge, or reserve
For each affected role, determine whether it should:

- stay where it is
- move to a different role position
- split into two or more roles
- merge with another role
- become a reserved capability instead of an instantiated agent

### 5. Redesign the team placement
Produce a cleaner role map that explains:

- who owns which stage
- what each role is responsible for
- what each role is *not* responsible for
- what the handoffs are
- which roles are long-term, stage-based, or reserved

### 6. Update the rewrite order
Before editing files, determine the correct order of change.

Usually:

1. proposal / team-level docs
2. current team state
3. target role files
4. downstream linked roles
5. persona refinement only if still needed

### 7. Only then refine persona files
After placement is correct, refine the target agent’s files.

If the role still needs deeper persona grounding after placement is fixed, hand off to `ollivanders-agent-shop`.

## Output requirements

Your output should include all of the following.

### A. Diagnosis
State:

1. the primary problem type
2. any secondary problem types
3. why you made that diagnosis

### B. Role alignment result
State:

1. which roles should remain
2. which roles should move
3. which roles should split
4. which capabilities should remain reserved for now

### C. Team structure result
State clearly:

1. each role’s one-line position
2. each role’s core responsibility
3. each role’s non-responsibility
4. handoff directions between roles

### D. Change plan
State:

1. which docs should change first
2. which role files should change next
3. whether persona refinement is still needed afterward

## Good sorting behavior

Do:

- keep the team as small as possible while preserving clarity
- prefer role clarity over role quantity
- preserve good existing roles when possible
- treat “reserve, don’t instantiate yet” as a valid outcome
- distinguish structure problems from personality problems

Do not:

- assume more agents is always better
- rewrite persona first when the role is wrong
- create a new role just because a task feels messy
- confuse “strong character flavor” with “good team placement”

## Relationship to other skills

### `agent-sorting-hat`
Use for:

- role alignment
- team restructuring
- capability splitting/merging
- deciding placement and boundaries
- determining whether a role should exist, move, split, or stay reserved

### `ollivanders-agent-shop`
Use for:

- persona shaping
- identity-binding
- character grounding
- making the role *feel* right after its placement is correct

**Recommended order:**

1. `agent-sorting-hat` to put the role in the right place
2. `ollivanders-agent-shop` to make the role deeply itself

## Minimal mental model

- Sorting Hat decides where the role belongs.
- Ollivanders helps the role hold the right wand.

Placement first. Soul refinement second.
