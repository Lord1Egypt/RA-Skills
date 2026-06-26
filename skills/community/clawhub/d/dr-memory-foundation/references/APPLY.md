# Apply checklist — dr-memory-foundation

Use this when the user says things like:
- Apply dr-memory-foundation to this workspace
- Initialize memory foundation
- Set up the memory structure

## Goal
Install/normalize the file-based memory layout with minimal user effort.

## Steps
0) Optional fast path: `python3 ./skills/dr-memory-foundation/scripts/install_memory_foundation.py` to copy missing templates.

1) Inspect existing files:
- `MEMORY.md`
- `memory/always_on.md`
- `memory/now.md`
- `memory/open-loops.md`
- `memory/automation.md`
- `memory/topics/*.md`

2) Create missing files from `references/templates/`.

3) Preserve user content:
- Do not delete raw notes.
- Move/merge stable content into topic files if needed.
- Keep `MEMORY.md` small (preferences + indexes only).

4) Ensure these exist after apply:
- `MEMORY.md`
- `memory/always_on.md`
- `memory/now.md`
- `memory/open-loops.md`
- `memory/automation.md`
- `memory/topics/glossary.md`

5) Confirm the result to the user.

## Idempotency rule
If already applied, do not duplicate sections or overwrite user-edited content blindly.
