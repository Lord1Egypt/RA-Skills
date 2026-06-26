---
name: game-build-strategy
description: Decide the AI-native development mode, quality target, task granularity, and refactor policy based on project state and user intent. This skill prevents both over-cautious iteration and reckless live-product rewrites.
license: MIT
compatibility: Claude Code and Codex. Best results with file read/write access.
metadata:
  author: game-superpowers
  version: "1.1.0"
  domain: game-development
---

# Game Build Strategy

## Goal
Choose the right build strategy for the project.
Write `docs/game-studio/build-strategy.md` and `docs/game-studio/quality-target.md`.

Use:
- `./shared/reference/development-modes.md`
- `./shared/reference/quality-targets.md`
- `./shared/templates/build-strategy.md`
- `./shared/templates/quality-target.md`

## Development modes
- `yolo-super`
- `guided-build`
- `refactor-open`
- `surgical-live`

## Quality targets
- `first-playable`
- `polished-prototype`
- `production-feature`
- `live-patch`

## Selection rules
- **greenfield + narrow mechanic spike** -> `yolo-super` + `first-playable`
- **greenfield + serious showcase build** -> usually `yolo-super` or `guided-build` + `polished-prototype`
- **existing product-facing feature work** -> usually `guided-build` or `refactor-open` + `production-feature`
- **shipped or live-risky** -> `surgical-live` + `live-patch`

## Planning policy
Match task size to the mode:
- aggressive modes can use large coherent implementation chunks
- production-feature work can use medium coherent chunks
- live work should use smaller changes with tighter verification

## Guardrail
Do not let “safe” planning ruin the result on low-risk greenfield work.
Do not let “fast” planning justify broad rewrites on live products.
