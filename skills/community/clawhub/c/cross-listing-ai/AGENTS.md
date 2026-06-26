# AGENTS.md

## Purpose

This repository is a docs-only skill package for `Cross Listing AI`. Use this file as a router to the real source-of-truth docs instead of adding long guidance here.

## Source Of Truth

- `README.md`: repo overview, structure, and publish entrypoints
- `SKILL.md`: root skill contract and non-negotiable behavior
- `references/`: workflow, extraction, pricing, final output, and marketplace rules
- `agents/openai.yaml`: OpenAI-style agent metadata used by registries and tooling

## Task Routing

- Skill behavior changes: update `SKILL.md` first, then the affected files under `references/`
- Metadata changes: update `agents/openai.yaml` and any matching public copy in `README.md`
- Release and publish work: use the scripts under `scripts/` or the aliases in `package.json`

## Safe Verification

- `npm run test`

## Release Commands

- `npm run publish:clawhub -- <version> [changelog] [tags]`
- `npm run publish:skills`
- `npm run publish:all -- <version> [changelog] [tags]`
- Run the skills.sh entrypoint only from a clean local `main` checkout that already matches `origin/main`
- Direct entrypoints also work: `scripts/publish-clawhub.sh`, `scripts/publish-skills.sh`, `scripts/publish-all.sh`

## Freshness Rules

- Keep this file short and index-like
- Add durable detail to repo-local docs, not here
- Update this file only when the repo layout, source-of-truth docs, or release entrypoints change
