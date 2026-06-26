# dead-code-finder — Status

**Status:** Ready
**Price:** $59
**Created:** 2026-03-29

## What It Does
Finds dead code in JS/TS projects: unused exports, unreferenced files, and unused npm dependencies. Pure Python, no external dependencies. Supports path aliases, barrel exports, scoped packages.

## Components
- `scripts/find_dead_code.py` — main scanner (regex-based, no AST parser needed)
- Tested on synthetic project with mixed used/unused code

## Next Steps
- [x] Published to ClawHub (after April 11 — GitHub account age requirement)
- [ ] Add Python/Go support in v2
- [ ] Add `--fix` mode for auto-removal
