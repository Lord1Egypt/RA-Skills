---
name: freeze
description: >
  Restrict file edits to a specific directory for the session. Blocks Edit and
  Write outside the allowed path. Use when debugging to prevent accidentally
  fixing unrelated code, or when scoping changes to one module.
  Use when: "freeze", "restrict edits", "only edit this folder", "lock down edits".
---

# Freeze — Restrict Edits to a Directory

Lock edits to a specific directory. Everything outside is read-only.

## How to Use

1. **Ask the user** which directory to lock to (or detect from context — e.g., the directory containing the bug).
2. **Announce:** "Edits restricted to `{dir}/`. Everything else is read-only. Say 'unfreeze' to remove."
3. **Enforce:** Before any Edit or Write, check that the target file is within the locked directory. If not, refuse and remind the user.

## Detection

After activating freeze, note the locked directory in your context. Every edit command should be checked:
- Target file starts with locked dir → proceed
- Target file is outside → "This file is outside the frozen scope (`{locked_dir}/`). Say 'unfreeze' to edit elsewhere."

## Auto-detect for Debugging

When invoked during debugging, auto-lock to the directory containing the affected files:
- If investigating `src/auth/login.ts` → freeze to `src/auth/`
- If the bug spans multiple directories → ask which one to lock
- If genuinely cross-cutting → skip the lock, note why
