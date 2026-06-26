# Contributing

Thanks for improving `speak4bangboo`.

## Scope

This project focuses on Bangboo-style prompt assets and cross-framework compatibility (Cursor, Claude, OpenClaw, and compatible runtimes).

## Contribution rules

1. Keep behavior contract consistent:
   - grunt prefix is decorative,
   - parentheses carry real meaning,
   - safety/factual constraints remain explicit.
2. Keep Chinese and English behavior aligned.
3. Avoid framework-specific drift from `prompts/core-rules.md`.
4. Prefer small, reviewable pull requests.

## Workflow

1. Fork and create a branch from `main`.
2. Make changes with clear file-level intent.
3. Update related docs (`README.md`, `docs/integration.md`, `CHANGELOG.md`) when needed.
4. Open a pull request using the provided template.

## Quality checklist

- [ ] Cursor, Claude, and OpenClaw entry files still point to valid prompt files.
- [ ] `reference-lexicon.md` remains internally consistent.
- [ ] Examples do not break the core behavior contract.
- [ ] No secrets, tokens, or private data added.

## Versioning

This project follows semantic versioning:

- `MAJOR`: breaking behavior contract changes.
- `MINOR`: backward-compatible additions.
- `PATCH`: wording fixes, typo fixes, non-breaking docs updates.
