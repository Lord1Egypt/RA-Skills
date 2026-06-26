# Migration Guide - Escalate

## v1.0.1 Setup and Memory Update

This update keeps the same home folder, `~/escalate/`, but clarifies what belongs in the user's live memory versus the packaged skill guides.

### Before

- `~/escalate/memory.md`
- possible local notes mixed with `boundaries.md` or `patterns.md`
- no formal setup flow for the workspace AGENTS and SOUL files

### After

- `~/escalate/memory.md`
- `~/escalate/decisions.md`
- `~/escalate/domains/`
- packaged guides stay in the skill: `boundaries.md`, `patterns.md`, `setup.md`, `memory-template.md`

## Safe Migration

1. Create the new local files without deleting anything:
```bash
mkdir -p ~/escalate/domains
touch ~/escalate/decisions.md
```

2. Keep the existing `~/escalate/memory.md` file exactly as it is.

3. If old escalation notes live in loose sections or ad-hoc files, copy durable boundaries into the matching sections in the new memory template.

4. Move recent examples, corrections, and trust adjustments into `~/escalate/decisions.md`.

5. If old local files named `boundaries.md` or `patterns.md` exist inside `~/escalate/`, keep them for reference and merge them gradually. Do not delete or rename them unless the user explicitly asks for cleanup.

6. Apply any workspace AGENTS or SOUL additions as small snippets only. Do not replace whole sections.
