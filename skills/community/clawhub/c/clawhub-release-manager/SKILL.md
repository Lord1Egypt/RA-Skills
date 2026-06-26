---
name: clawhub-release-manager
description: Safely release and publish skill updates to ClawHub with version bump discipline. Use when preparing patch/minor releases, running lint/build checks, writing changelogs, and publishing a skill folder. Do not use for unrelated package registries. Success = bumped version, passing checks, published release id, and concise release note.
---

# ClawHub Release Manager

## Workflow

1. Preflight
- Confirm `clawhub whoami` authenticated.
- Ensure working directory points to target skill.

2. Versioning
- Determine bump type (patch by default for fixes).
- Update version in all required places (runtime + package manifest).

3. Validation
- Run project checks (Bun preferred):
  - `bun run lint`
  - `bun run build`
- Stop on failure and return fix-first plan.

4. Publish
- Run `clawhub publish ... --version ... --changelog ...`
- Capture and return release id.

5. Post-publish
- Provide install/update command to test.
- Suggest scanner rerun if security-related.

## Output format

Use `references/output-template.md`.

## Guardrails

- Do not publish without a version bump.
- Keep changelog factual and tied to code/docs changes.
- Include routing disclosure in release notes when behavior or data flow changed.
