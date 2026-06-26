# Repository Guide

This repository is a meta-skill for generating character skills.

## Layout

- `SKILL.md` is the product entrypoint.
- `docs/` stores contracts, safety rules, and evidence rules.
- `prompts/` stores phase-specific prompt guides.
- `tools/` stores deterministic helpers.
- `characters/` stores generated child skills.
- `versions/` stores repository-level contract snapshots.

## Editing Rules

- Keep `SKILL.md` as high-level navigation, not a dumping ground for every rule.
- Put detailed policy and schema material in `docs/`.
- Keep `canon`, `persona`, and `style_examples` clearly separated everywhere.
- When changing prompt behavior, update the related docs if the contract changes.
- When changing tool interfaces, update `versions/contracts.md`.

## Validation

- Prefer `python -m compileall tools` for a fast syntax pass.
- Use temporary directories when smoke-testing `skill_writer.py` and `version_manager.py`.
- Do not add README-style files unless explicitly requested.
