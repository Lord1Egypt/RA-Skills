---
name: game-audit-scorecard
description: Summarize audit findings into a structured multi-dimensional scorecard for UI/UX, feedback, mechanics, scope completeness, maintainability, and live risk.
license: MIT
compatibility: Claude Code and Codex. Best results with file read/write access; shell/build access improves evidence quality.
metadata:
  author: game-superpowers
  version: "1.1.0"
  domain: game-development
---

# Game Audit Scorecard

## Goal
Normalize audit findings into a structured scorecard that future sessions can read, compare, and build from.

## Deliverables
Create or update:
- `docs/game-studio/audit/scorecard.json`
- `docs/game-studio/audit/audit-summary.md`

Use:
- `./shared/templates/audit-scorecard.md`
- `./schemas/audit-scorecard.schema.json`
- `./shared/reference/audit-confidence-and-evidence.md`

## Required dimensions
- `ux_flow`
- `hud_readability`
- `feedback_design`
- `audio_feedback`
- `game_feel`
- `mechanics_clarity`
- `scope_completeness`
- `production_readiness`
- `architecture_health`
- `live_risk`

## Important
Scores should be justified by written evidence.
Do not give false precision.
Use consistent severity language and explain uncertainty where runtime evidence is missing.

