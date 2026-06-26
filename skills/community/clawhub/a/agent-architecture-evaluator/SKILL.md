---
name: agent-architecture-evaluator
description: Use when evaluating, testing, and optimizing an agent architecture or multi-agent system. Best for reviewing planning, routing, memory, tool use, reliability, observability, cost, and system-level failure modes.
version: "1.0.0"
---

# Agent Architecture Evaluator

Version: `1.0.0`

## Overview

This skill reviews the architecture of an agent system, not just its prompts or its attached skills.

Use it for architectures involving components such as:

- planner / executor splits
- routers and specialists
- tool-use layers
- memory systems
- human approval gates
- multi-agent coordination

## Use this skill when

- A user wants to assess an existing agent architecture.
- Reliability, latency, cost, or coordination problems appear to be architectural.
- A team needs a structured architecture review and optimization roadmap.
- You need system-level test scenarios rather than single-skill evals.

## Do not use this skill when

- The problem is one isolated skill.
- The task is to create a new skill from scratch.
- The main need is portfolio review across many related skills.

Use `agent-test-measure-refine` or `agent-skill-portfolio-evaluator` in those cases.

## Output contract

Always produce these named outputs:

- `architecture_inventory`
- `failure_mode_map`
- `architecture_test_plan`
- `optimization_roadmap`
- `measurement_plan`
- `architecture_recommendation`

## Review dimensions

Evaluate at least these dimensions:

1. `component clarity`
2. `routing correctness`
3. `memory usefulness`
4. `coordination reliability`
5. `cost and latency efficiency`
6. `observability and debuggability`

## Quick start

1. Map the current architecture.
2. Identify critical paths and failure-prone handoffs.
3. Define architecture-level test scenarios.
4. Identify bottlenecks in routing, memory, tools, or coordination.
5. Recommend the smallest structural changes with the highest leverage.

## Workflow

### 1. Build the architecture inventory

Capture:

- components
- responsibilities
- inputs and outputs
- state or memory boundaries
- human approval points
- observability signals

### 2. Map failure modes

Look for:

- planner produces unusable tasks
- router sends work to the wrong specialist
- memory pollutes current decisions
- tool calls are slow, redundant, or poorly validated
- multi-agent handoffs lose context
- approval gates appear too late

### 3. Design system tests

Cover:

- happy path
- degraded upstream input
- partial component failure
- tool unavailability
- stale or noisy memory
- high-latency coordination
- rollback or recovery behavior

See `references/architecture-review-framework-v1.0.0.md`.

### 4. Prioritize architectural changes

Prefer:

- clarifying responsibilities before adding components
- removing weak indirection
- tightening interface contracts
- adding observability before adding complexity
- isolating state when cross-contamination is likely

### 5. Define measurement

Recommend concrete metrics where available:

- task success rate
- retry rate
- fallback rate
- cost per successful task
- latency by stage
- human intervention rate

## Anti-patterns

- adding new components to hide unclear ownership
- keeping weak memory because it sounds sophisticated
- optimizing one stage without measuring system impact
- blaming prompts for structural routing failures

## Resources

- `references/architecture-review-framework-v1.0.0.md` for system review steps.
- `references/optimization-patterns-v1.0.0.md` for architecture optimization guidance.
- `assets/architecture-review-template.md` for the final report structure.
- `assets/example-architecture-review.md` for a realistic filled review.
- `assets/architecture-input-example.json` for structured input.
- `scripts/render_architecture_review.py` to normalize a structured architecture review into Markdown.
