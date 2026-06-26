---
name: creative-agent-os-north-star
description: Review or shape product and architecture decisions for a lightweight creative agent OS. Use when comparing runtimes, cloud execution, agent system shape, coding-engine adapters, skills, or multimodal product direction against the user's north-star principles.
version: 0.1.1
---

# Creative Agent OS North Star

Use this skill when the work risks drifting away from the intended product shape.

## Core test

Before proposing or implementing anything, check:

1. Does this stay lightweight?
2. Does this help ordinary users, not just agent power users?
3. Does this keep the coding engine replaceable?
4. Does this fit cloud sandbox execution better than local-only assumptions?
5. Does this make adding domain agents easier rather than harder?

## Default reference frame

- runtime: learn from Nanobot
- cloud execution: learn from Open Inspect / background-agents
- system shape: learn from OpenClaw
- coding engine: adapter, never hard-coded

Read `references/north-star.md` when you need the full criteria.

## What to do

- call out drift early
- prefer thinner orchestration over heavy frameworking
- separate product shape from engine implementation
- preserve room for multimodal apps, skills, memory, and CLI bridges

## Output style

When reviewing a proposal, answer in this order:

1. what matches the north star
2. what drifts from it
3. the smallest correction that gets back on track
