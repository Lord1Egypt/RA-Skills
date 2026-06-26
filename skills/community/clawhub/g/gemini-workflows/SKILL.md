---
name: gemini-workflows
description: Use Gemini CLI for deep thinking, planning, workflow design, and non-code desktop task orchestration.
---

# Gemini Workflows: Planning + Deep Thinking

## Routing Rule
- Planning, strategy, analysis, synthesis: gemini
- Web search (direct Google): gemini
- Research + code review: gemini
- Code implementation, refactors, tests: Claude CLI (daedalus-code skill)

## Commands
gemini   # deep planning
flash    # fast iteration

## Prompt Template
Goal: <objective>
Context: <constraints, tools, timeline>
Deliverable: <format: checklist/table/plan>
Decision criteria: <ranking logic>
Output style: concise, actionable, execution-ready

## Handoff to Claude
1. Freeze scope + acceptance criteria
2. Hand to Claude via daedalus-code skill
3. Require validation outputs before completion
