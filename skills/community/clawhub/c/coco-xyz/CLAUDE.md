# CLAUDE.md

Development guidelines for openclaw-hxa-connect.

## Project Conventions

- **TypeScript** — Source in `index.ts`
- **Conventional commits** — `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`
- **English for code** — Comments, commit messages, PR descriptions, and documentation in English

## Release Process

When releasing a new version, **all four files** must be updated in the same commit:

1. **`package.json`** — Bump `version` field
2. **`package-lock.json`** — Run `npm install` after bumping package.json to sync the lock file
3. **`SKILL.md`** — Update `version` in YAML frontmatter to match package.json
4. **`CHANGELOG.md`** — Add new version entry following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

Version bump commit message: `chore: bump version to X.Y.Z`

After merge, create a GitHub Release with tag `vX.Y.Z` from the merge commit.

## Architecture

HXA-Connect channel plugin for OpenClaw — bot-to-bot messaging.

- `index.ts` — Plugin entry point
- `openclaw.plugin.json` — OpenClaw plugin manifest
