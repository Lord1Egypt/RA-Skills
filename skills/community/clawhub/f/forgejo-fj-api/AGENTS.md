# Project

`forgejo-skill` is an OpenClaw skill for self-hosted Forgejo via `fj`, REST API, and local `git` review workflows.
Main product files are Markdown: `SKILL.md`, `README.md`, `references/*.md`, `CHANGELOG.md`.
In this repo, `.md` files are usually shipped skill content, not ancillary docs.

# Changelog

- Inspect staged changes only.
- For changelog-only work, never run `git add`, commit, or push.
- Follow Keep a Changelog `1.1.0`: https://keepachangelog.com/en/1.1.0/
- Update only `## [Unreleased]` unless a specific version is requested.
- When releasing, create or update `## [<version>] - YYYY-MM-DD` from `Unreleased`.
- Keep entries concise, user-facing, actionable, and deduplicated.
- Treat core skill Markdown changes as product changes when they alter capability, setup, workflow, or references.
- Ignore only true ancillary changes such as `docs/`, guides, notes, images, and assets.

# Commit Message

- Propose a commit message only; do not commit.
- Use conventional commits: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `ci`, `build`.
- Keep it concise: `<type>: <summary>`.
- Match the staged changes and any changelog edits exactly.
- Prefer `feat` when the skill gains new user-facing capability or reference coverage.

# Release

- Start from staged changes as source of truth.
- Update affected product docs before changelog updates.
- For releases, stage required doc and changelog edits, create one normal commit, create an annotated tag, then push branch and tag.
