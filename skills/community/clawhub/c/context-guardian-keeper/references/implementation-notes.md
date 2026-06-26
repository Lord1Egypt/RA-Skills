# Implementation Notes

Use Python for the reference module when the host project does not already mandate a different language.

Recommended layout:
- `scripts/context_guardian.py` — reference implementation
- `references/task-state-schema.md` — canonical state contract
- `references/summary-template.md` — structured summary format
- `references/config-example.yaml` — configuration shape
- `references/persisted-task-state.example.json` — persisted state example
- `references/summary-example.md` — markdown summary example
- `references/integration-checklist.md` — host loop integration checklist
- `scripts/test_context_guardian.py` — behavior tests

Practical rule:
- Keep low-value conversation history out of the working bundle once durable state exists.
- Always prefer a fresh checkpoint over guessing.
- For OpenClaw-style hosts, a thin workspace-level wrapper CLI is a good integration pattern: it should reuse the reference module, stay small, and expose only the safest repetitive actions (`status`, `ensure`, `checkpoint`, `bundle`).
- If the host already knows its workspace root, prefer a session-level default (for example `CG_ROOT`) over forcing weak models to repeat a fragile `--root ...` flag on every call.
- Treat `summaries/latest-summary.md` as the canonical runtime alias for the newest summary, even when timestamped summaries are also kept for history.
- If a live host already has legacy task-state files, detect that shape explicitly and require an archival migration step before canonical writes.
