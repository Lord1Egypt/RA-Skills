# Migration Guide - Decide

## v1.0.1 Decision Logging Update

This update keeps the same home folder, `~/decide/`, but changes the model from loose preference tracking to structured decision memory.

### Before

- `~/decide/memory.md`
- local notes mixed across confidence or exception concepts
- no formal setup flow for workspace AGENTS and SOUL files

### After

- `~/decide/memory.md`
- `~/decide/decisions.md`
- `~/decide/domains/`
- packaged guides stay in the skill: `components.md`, `confidence.md`, `exceptions.md`, `setup.md`, `memory-template.md`

## Safe Migration

1. Create the new local files without deleting anything:
```bash
mkdir -p ~/decide/domains
touch ~/decide/decisions.md
```

2. Keep the existing `~/decide/memory.md` file exactly as it is.

3. Move durable decision rules and always-ask boundaries into the matching sections of the new memory template.

4. Move individual examples, choices, and outcomes into `~/decide/decisions.md`.

5. If old local notes are specific to one project, client, or technical area, place them in `~/decide/domains/<domain>.md`.

6. Apply any AGENTS or SOUL additions as small snippets only. Do not replace whole sections.
