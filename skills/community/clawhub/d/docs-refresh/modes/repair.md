# Repair Mode

Use this mode when the collector reports `doc_system_mode=repair`, or when manual routing shows that an existing docs system has a broken map or authority surface.

The repository has a docs system, but its navigation or authority surfaces are stale enough that content edits alone would deepen drift.

## Focus

- Repair `AGENTS.md`, `ARCHITECTURE.md`, index pages, broken authority pointers, or missing cross-links before expanding content.
- Restore a usable map first, then update the smallest authoritative document that owns the changed fact.

## Repair Triggers

- Split docs directories exist but the expected index pages are missing.
- Navigation docs are the active drift signal in a repository that already has a docs system.
- The repository layout implies a docs system, but the collector cannot infer usable preferred targets.

## Working Rule

- Do not patch around a broken map by stuffing more truth into leaf pages. Repair navigation and authority first, then continue with normal convergence.
- Missing `AGENTS.md` alone is not `repair`.
- Sparse docs alone are not `repair`.
