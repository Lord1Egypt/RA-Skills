---
name: agent-memory-os
description: Stop agents from "forgetting, mixing projects, and rotting over time" by giving them a practical memory operating system: global memory, project memory, promotion rules, validation cases, and a maintenance loop.
---

# Agent Memory OS

**Build an agent that gets more organized over time instead of more chaotic.**

Turn an agent's memory from **"a pile of chat history"** into a **long-term working memory operating system**.

## What problem this solves

A lot of agents look impressive in short conversations, then collapse under real work:
- they forget what matters
- active projects pollute long-term memory
- useful lessons never become reusable rules
- the system looks good for a week, then decays

This skill exists to fix that.

It helps the agent move from:
- "I remember fragments"

to:
- **"I have a stable global brain, project-specific working brains, reusable lessons, validation logic, and a maintenance loop that keeps the whole system healthy."**

## What makes this different

This is not just:
- note-taking guidance
- a vector-search recipe
- a memory dump strategy

It is a workflow for building an agent memory **system** with:
- separation of concerns
- promotion paths for reusable knowledge
- validation cases
- operational maintenance rules

## Use this skill when

The user says or implies things like:
- "My agent keeps forgetting"
- "Once projects pile up, everything gets messy"
- "I want long-term memory for my AI agent"
- "I need project memory separated from global memory"
- "I want reusable lessons, not just logs"
- "I want to share or standardize an agent memory setup"

## Example trigger prompts

This skill should feel natural on prompts like:
- "Help me design long-term memory for my coding agent."
- "My AI assistant keeps mixing projects and forgetting context."
- "I need a reusable memory architecture for multi-project agents."
- "How do I separate durable agent memory from active project memory?"
- "Help me turn chat history into a reusable working-memory system."

## What the user gets

By the end of this workflow, the user should have:
1. a memory architecture that separates global and project concerns
2. a minimum project-memory structure
3. routing and promotion rules
4. validation cases to prove the system works
5. a maintenance runbook so it does not decay immediately

## Privacy and publishing rule

When using this skill for sharable/public output:
- never expose real user names, private IDs, workspace-specific secrets, session paths, internal message IDs, or private document URLs
- rewrite examples into generalized patterns
- replace personal/project-specific references with neutral placeholders
- do not bundle private memories, raw chat excerpts, or personally identifying workflow traces into the skill

If the user explicitly wants a public/shareable version, treat **privacy-preserving abstraction** as mandatory, not optional.

## Recommended workflow

### Step 0 — Decide whether to use a full memory system
Not every agent needs this full setup.

Read `references/architecture-decision-guide.md` when the user is unsure whether they need a full global / project / bridge system, or whether a simpler setup is enough.

### Step 1 — Diagnose the real memory problem
Classify the user's issue before proposing architecture.

Typical failure modes:
- **single-brain overload**: everything is dumped into one place
- **project pollution**: local project state contaminates long-term memory
- **retrieval confusion**: the agent doesn't know where to look first
- **knowledge stagnation**: lessons never graduate into reusable rules
- **maintenance decay**: the structure exists but slowly becomes stale

Read `references/failure-modes.md` when you need a sharper diagnosis rubric.

### Step 2 — Choose the architecture
Default recommendation: a **three-part system**
- **global memory** for durable rules, preferences, SOPs, stable principles
- **project memory** for local complexity and active work
- **bridge/promotions** for candidate → promoted → canonical evolution

Read `references/architecture.md` when you need the design rationale.

### Step 3 — Create the minimum working structure
For each project, start with 5 files:
- `PROJECT.md`
- `STATUS.md`
- `DECISIONS.md`
- `ASSETS.md`
- `LESSONS.md`

Use the bundled templates in:
- `assets/project-templates/`
- `assets/bridge-templates/`

### Step 4 — Define routing and promotion rules
Make sure the agent knows:
- what belongs to global memory
- what stays project-local
- what becomes a candidate for reuse
- what evidence is required before promotion

Read:
- `references/routing.md`
- `references/promotion.md`

### Step 5 — Validate with concrete cases
Do not stop at design. Test the system with at least 3 case types:
- **continuous project execution**
- **interruption and recovery**
- **cross-project reuse**

Use measurable criteria: recovery accuracy, unnecessary follow-up questions, reuse success, structure completeness, etc.

Read `references/validation.md` for a compact validation model.

### Step 6 — Add a maintenance runbook
A memory system is not done when designed. It is done when it can be maintained.

Define:
- when to update daily logs
- when to update project status
- when to record lessons
- when candidates get promoted
- when to deprecate outdated rules
- how often to review global/project/bridge memory

Read `references/maintenance.md` when writing or reviewing the runbook.

## Minimal success path

A good first run of this skill usually looks like:
1. identify the dominant failure mode
2. choose the global/project/bridge architecture
3. create the 5 core project files
4. define one promotion rule and one routing rule
5. validate with one interruption-recovery case and one reuse case
6. write a simple maintenance rhythm

If the agent can recover better, reuse more, and stay cleaner over time, the system is working.

## Packaging guidance

Keep the public skill:
- short in SKILL.md
- practical in workflow
- generalized in examples
- private details removed

Do **not** include:
- personal identifiers
- real workspace paths tied to an individual
- raw private conversation excerpts
- internal-only document links
- unredacted project-specific evidence

Read `references/publish-checklist.md` before publishing or sharing widely.

## Output style for public-facing use

If the user wants something that attracts attention, write with this shape:
- start from a painful, recognizable problem
- name the failure mode clearly
- present the architecture as a relief pattern
- show a small, concrete workflow
- prove it with validation cases
- end with operational simplicity, not abstract theory

Make it feel like a **usable system**, not an academic essay.
