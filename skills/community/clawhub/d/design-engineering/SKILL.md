---
name: design-engineering
description: Orchestrate iterative design and frontend engineering work through research, planning, sub-agent execution, and validation loops. Use when a visual/UI task requires multiple iterations, when the first implementation needs refinement based on feedback, when choosing between competing technical approaches (Canvas vs SVG vs CSS), or when coordinating sub-agents on design-heavy work. Covers animation architecture decisions, progressive enhancement patterns, performance-aware rendering choices, and the research→plan→execute→validate workflow. Complements frontend-design (which handles aesthetics) by adding engineering discipline, iteration management, and technical decision-making.
version: 1.2.0
---

# Design Engineering

Orchestrate design-heavy frontend work that requires iteration, technical decisions, and validation. This skill is about the *process* — how to research, plan, build, validate, and refine — not the aesthetics (use `frontend-design` for that).

## When to Use
- Visual work that will take multiple iterations to get right
- Choosing between technical approaches (Canvas vs SVG vs CSS, etc.)
- Coordinating sub-agents on parallel design/engineering tasks
- Refining an implementation based on user feedback
- Any frontend work where "build it and ship" isn't enough

## Scope & Safety
- All file operations stay within the user's project directory — no absolute paths outside the project root
- Sub-agents operate within the project scope defined by the orchestrator and must not access files outside it
- Sub-agent outputs (file writes, research findings) are confined to the project working directory
- No credentials or external services are required
- Playwright (when used for screenshots) connects only to `localhost` dev servers — never to external URLs
- No data is exfiltrated or transmitted to external endpoints; all work is local

## The Iteration Loop

Every design-engineering task follows this cycle:

```
Research → Plan → Approve → Execute → Validate → Feedback → Refine
```

### 1. Research Phase
Before touching code, understand the problem space. Spawn 2-3 research sub-agents in parallel with different lenses:

- **Inspiration/reference** — find examples of what we're trying to achieve
- **Technical approaches** — what tools/techniques solve this class of problem
- **Constraints** — performance, browser support, accessibility, progressive enhancement

Research agents should write findings to files within the project's working directory so context is preserved across iterations.

### 2. Plan Phase
Synthesize research into a concrete plan. Present to user for approval before executing. The plan should include:

- Architecture decision with rationale (not just "use X" but "use X because Y fails at Z")
- Layer/component breakdown
- What gets removed, what gets added, what stays
- Pre-mortem: "what would cause this to fail?"
- Estimated sub-agent tasks
- **Horizon estimate:** Count estimated steps across all sub-agents. If > 40 steps total, decompose into sub-phases of ≤ 20 steps. If 20–40 steps, insert a midpoint quality checkpoint (screenshot + integration check before proceeding). Under 20 steps, execute directly. This prevents quality collapse on complex design tasks.

### 3. Execute Phase
Dispatch sub-agents with focused, context-minimal tasks. Key rules in `references/subagent-patterns.md`.

### 4. Validate Phase
After sub-agents complete, the orchestrator MUST validate. Build check is necessary but not sufficient. Check integration points — see `references/validation-checklist.md`.

### 5. Feedback → Refine
Ship to user for review. Expect 2-5 iterations on visual work. Each iteration:
1. Screenshot the live result (use Playwright if available)
2. Identify specific issues from feedback
3. Make targeted fixes (don't rebuild from scratch each time)
4. Validate and redeploy

## Technical Decision Framework

When choosing between rendering approaches, read `references/rendering-decisions.md`. Quick heuristic:

| Need | Use |
|------|-----|
| Static decorative pattern | CSS `background-image` with SVG data URI |
| <100 authored animated elements | Inline SVG + CSS animations |
| Procedural generation, >100 elements, full-page coverage | Canvas 2D |
| 3D, heavy particle systems, post-processing | Three.js/WebGL (last resort — heavy) |

## Progressive Enhancement Stack

Every visual enhancement must degrade gracefully:
1. CSS baseline (always works, no JS)
2. JS-enhanced layer fades in on top
3. `prefers-reduced-motion` → skip animations entirely
4. Low-end device detection → reduce complexity
5. Light/dark theme awareness

## Glass-Panel Pattern

For content floating over animated backgrounds:
```css
.card {
  background: color-mix(in srgb, var(--bg-card) 50-60%, transparent);
  backdrop-filter: blur(8-12px);
  -webkit-backdrop-filter: blur(8-12px);
}
```
Lets animation show through while keeping text readable. Adjust blur and opacity based on background intensity.

## References
- `references/subagent-patterns.md` — How to dispatch and validate sub-agent work
- `references/validation-checklist.md` — Post-execution checks that catch integration bugs
- `references/rendering-decisions.md` — Canvas vs SVG vs CSS decision guide with production lessons
