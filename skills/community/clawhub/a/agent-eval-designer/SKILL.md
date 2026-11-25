---
name: agent-eval-designer
version: 1.0.0
description: Design a small, honest evaluation set for an agent workflow: tasks, pass criteria, and a scoring rubric a human can run in an hour. Use before shipping or changing any agent.
---

# Agent Eval Designer

## Overview

An agent without evals degrades silently. This workflow builds the smallest eval that still catches real regressions: representative tasks, binary pass criteria wherever possible, and a fixed set that never quietly changes.

## When to use

Before launching an agent workflow, after any prompt/model/tool change, or when quality 'feels' worse and nobody can prove it.

## Workflow

1. **Pick the tasks** — 10-20 real tasks sampled from actual use, including the two most embarrassing past failures
2. **Write pass criteria per task** — observable outcomes ('the summary names the blocker and owner'), not vibes ('good summary')
3. **Include adversarial cases** — at least two: misleading input, missing data, an instruction hidden in content
4. **Freeze the set** — version it; new failures get added as new cases, old cases never get edited to pass
5. **Run and score** — record per-case pass/fail plus the raw outputs; a single aggregate score hides where it broke
6. **Set the ship bar** — e.g. all safety cases pass, >=90% overall; write it down before running

## Guardrails

- Never tune the prompt against the eval set and then report the same set as independent evidence
- Never let the agent grade its own homework without a human spot-check
- Small and run beats large and theoretical

## Output format

An eval pack: task list with criteria, adversarial cases, scoring sheet, ship bar, and the latest run's results.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
