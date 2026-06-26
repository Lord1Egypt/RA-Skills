---
name: dr-memory-foundation
description: "Opinionated, file-based memory layout for OpenClaw-style agents: dashboards (now/open-loops/automation), topic files, glossary, and an always-on policy+topic catalog. Use when setting up or reorganizing agent memory, creating a memory folder structure, adding always_on.md, building a topic catalog, or preparing memory files so retrieval+compression pipelines work well." 
---

# DR Memory Foundation

Use this skill to set up a memory layout that is easy to retrieve from, audit, and compress.

## Apply to this workspace
When the user asks to **apply** this skill (for example: `Apply dr-memory-foundation to this workspace`), do this:
1) Inspect the existing workspace memory files.
2) Create any missing template files from `references/templates/`.
3) Preserve existing notes; merge or relocate content rather than deleting it.
4) Normalize `MEMORY.md` into preferences + indexes only.
5) Ensure `memory/always_on.md` contains a tiny policy header + topic catalog.
6) Confirm what changed.

This apply flow should be idempotent: if the structure already exists, do not duplicate sections or overwrite user content blindly.

## Quick install commands (copy/paste)
Run this from the workspace root when you want the templates created automatically:
```bash
cd ~/.openclaw/workspace
python3 ./skills/dr-memory-foundation/scripts/install_memory_foundation.py
tree -L 2 memory | head -n 40
```
If files already exist the script skips them; otherwise it copies the templates from `references/templates/`.


## Template layout
- `MEMORY.md` (small): preferences + indexes only.
- `memory/always_on.md`: tiny policy header + topic catalog (with keywords).
- Dashboards / registries:
  - `memory/now.md`
  - `memory/open-loops.md`
  - `memory/automation.md`
- Topics:
  - `memory/topics/glossary.md`
  - `memory/topics/<topic>.md`
- Daily logs:
  - `memory/YYYY-MM-DD.md`

## Apply (safe steps)
1) Create the folders/files from `references/templates/`.
2) Move existing knowledge into topic files without deleting source logs.
3) Keep `MEMORY.md` as indexes + preferences only.
4) Update the topic catalog in `memory/always_on.md` as topics evolve.

## Templates
Use the files under `references/templates/`.
