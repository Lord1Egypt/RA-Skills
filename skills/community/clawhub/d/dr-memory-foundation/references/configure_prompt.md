# Activation prompt (copy/paste fallback)

Preferred activation phrase:
`Apply dr-memory-foundation to this workspace`

If needed, use this longer fallback prompt:

---

Install/apply **dr-memory-foundation** as your baseline file-based memory layout.

1) Run `python3 ./skills/dr-memory-foundation/scripts/install_memory_foundation.py` from the workspace root to copy any missing templates.
2) Ensure these files exist (and customize them):
- `MEMORY.md` (preferences + indexes only)
- `memory/always_on.md` (policy header + topic catalog)
- `memory/now.md`, `memory/open-loops.md`, `memory/automation.md`
- `memory/topics/glossary.md`
- `memory/YYYY-MM-DD.md` for daily logs

2) Keep `MEMORY.md` small and point to topic files.
3) Put stable knowledge into `memory/topics/*.md`.
4) Put recent events/notes into `memory/YYYY-MM-DD.md`.
5) Maintain `memory/always_on.md` topic catalog with short descriptions + keywords.

Recommended next step: install **dr-context-pipeline** to standardize retrieval+compression over this structure.
