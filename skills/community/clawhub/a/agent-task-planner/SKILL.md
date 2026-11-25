---
name: agent-task-planner
version: 1.0.0
description: Break a goal into an ordered, checkpointed task plan an agent can execute without supervision drift. Use when starting any multi-step job, automation, or project and you want the plan written before work begins.
---

# Agent Task Planner

## Overview

Turns a one-line goal into an execution plan: decomposed steps, dependencies, checkpoints where a human should glance, and explicit stop conditions. Planning only — it does not execute the steps.

## When to use

At the start of any task with more than ~5 steps, any delegated agent job, or whenever a previous run drifted off-scope.

## Workflow

1. **Restate the goal** — one sentence, with the measurable end state
2. **List constraints** — time, budget, tools allowed, things that must NOT happen
3. **Decompose** — break the goal into steps of 15-60 minutes each; no step may contain the word 'and then figure out'
4. **Order by dependency** — mark which steps block others and which can run in parallel
5. **Add checkpoints** — after every 3-5 steps, define what 'still on track' looks like and what evidence proves it
6. **Define stop conditions** — the specific signals that mean halt and ask a human instead of improvising
7. **Write the plan down** — a numbered list the executing agent can re-read after any context loss

## Guardrails

- Never plan steps that spend money, send messages, or delete things without flagging them as approval-gated
- If a step's input is unknown, the plan must include a discovery step — never assume the input exists
- Keep the plan to one page; a plan nobody re-reads is not a plan

## Output format

A numbered plan with: goal statement, constraints, steps with dependencies marked, checkpoints, stop conditions, and the approval-gated steps flagged.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
