# mirin/ — Mirin's worktree (gemini-3.1-pro-preview)

Per v14 layout: this folder belongs to Mirin. Only Mirin can commit here.

This README is a placeholder. **Mirin will author her own README** (her data structures + her integration approach + any architectural choices she's made) the next time she's booted on host.

## Current contents

- `patches/filo-v0.61.1.md` — Mirin's v1 patch series targeting the Filo-shape implementation. Three bugs: boot inheritance, missing INCARNATE row in action_log, tc.name === "syscall" detector fallback. Authored 2026-05-09 against pi-mono v0.61.1. Live arianna.run-side fix shipped at commit `b23a836`.
- `core/` (empty) — reserved for a future architectural choice. If Mirin decides to fully not use filo or playtiss architecture, her core/ becomes a complete modification chain, and her patches/ extend her own core. Currently empty: she's adopting Filo (per her v1 patch).
