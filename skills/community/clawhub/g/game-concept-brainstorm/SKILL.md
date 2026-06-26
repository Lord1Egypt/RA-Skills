---
name: game-concept-brainstorm
description: Turn a vague game idea into a sharp fantasy, design pillars, player verbs, and acceptance bar before implementation begins. This is the proper “brainstorm” stage, not endless ideation.
license: MIT
compatibility: Claude Code and Codex. Best results with file read/write access.
metadata:
  author: game-superpowers
  version: "1.1.0"
  domain: game-development
---

# Game Concept Brainstorm

## Goal
Increase build success by locking the game fantasy before architecture or implementation.

## Deliverables
- `docs/game-studio/concept-brainstorm.md`
- `docs/game-studio/requirements.md`

Use `./shared/templates/concept-brainstorm.md`.

## Use when
- the request is exciting but blurry
- the user asks for “make it good” or “make it fun”
- the team needs to protect the core fantasy from being flattened during implementation

## Workflow
1. Restate the player fantasy in one sentence.
2. Lock the primary verb, the reward loop, and the first 30-second promise.
3. Define 3-4 design pillars.
4. Separate must-haves from experiments.
5. Prefer decisive defaults over endless questions.
6. Feed the result into `game-requirements-brainstorm`, `game-scope-profile`, and `game-ux-flow-designer`.

## Important
This is not for random ideation.
It is for increasing the chance that the first serious build actually feels like the intended game.
