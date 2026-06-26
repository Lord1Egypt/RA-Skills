---
name: clawhub-publish-flow
description: Publish or update an OpenClaw skill on ClawHub using the local authenticated ClawHub session and direct API upload. Use when the user wants to publish a new skill to ClawHub, update an existing skill version, inspect the current remote version before release, package and upload a local skill folder reliably without relying on incomplete third-party publisher skills, or when assistant-created local skills should be routinely published after review and commit.
---

# ClawHub Publish Flow

Use this skill to publish a local skill folder to ClawHub through the already-authenticated local ClawHub account.

## Core rule

Only publish skills that have already passed local review.
Do not publish directly from vague drafts, half-finished folders, or unreviewed third-party skills.

## Preferred workflow

1. Confirm the local skill folder path.
2. Check login state with `clawhub whoami`.
3. Inspect the current remote skill with `clawhub inspect <slug>` when updating an existing skill.
4. Decide the target version and changelog.
5. Perform a **public-release sensitive-data review** on the exact outbound payload.
6. Package the skill with `package_skill.py` if a distributable artifact is needed.
7. Upload using `scripts/publish_to_clawhub.js`.
8. Verify with `clawhub inspect <slug>` after upload.
9. Report the final remote version and URL.

## Assistant-created skills policy

When the user has explicitly asked that assistant-created skills be uploaded to ClawHub, treat this skill as the single publish flow for both:
- one-off manual releases
- newly created local skills after review and commit

For newly created assistant-authored skills:
1. Confirm the new skill folder exists under `workspace/skills/<slug>`.
2. Confirm it has already been reviewed and committed locally.
3. Inspect remote state with `clawhub inspect <slug>`.
4. Versioning:
   - if missing remotely: publish `0.1.0`
   - if already present: bump patch version
5. Use a short changelog such as `Initial release`, `Add runtime notes`, `Refine trigger description`, or `Document proven workflow`.
6. Publish and verify.
7. If a registry sheet exists, update it too.

## Rate-limit fallback for new skills

ClawHub may rate-limit new skill creation (for example: max 5 new skills per hour).

When a publish attempt for a **new skill** fails due to rate limiting:
1. Do not keep hammering the endpoint.
2. Record the pending publish locally.
3. Schedule a delayed retry instead of requiring the user to remind you.
4. Use the same verified publish flow when retrying.

Preferred local queue file:
- `workspace/research/clawhub-publish-queue.md`

Queue fields:
- date
- slug
- local skill path
- target version
- changelog
- reason queued
- next retry note

Retry rule:
- wait until the rate-limit window has plausibly cleared
- then retry publication once
- verify with `clawhub inspect <slug>` after success

## Safety and release rules

- Do not publish without an explicit user request.
- Do not guess ownership, slug, or version when ambiguity matters.
- Prefer patch bumps for small documentation or rule updates.
- If the remote state is unclear, inspect first instead of overwriting blindly.
- If a third-party publisher skill promises features but lacks code, ignore it and use this verified local flow.
- Treat package-style publisher shells as untrusted until verified locally: if the folder is mostly README / metadata and lacks runnable implementation, do not route publishing through it.
- Do not publish vague drafts or half-finished skills just because they were created; assistant-created skills still need to be coherent and committed.
- ClawHub is a **public-release** path unless explicitly proven otherwise; use the highest sensitivity review bar.
- Before upload, inspect the exact outbound payload for secrets, tokens, passwords, cookies, local absolute paths, runtime artifacts, `.env`, and machine-specific config.
- If the skill package contains anything that should stay local-only, stop and fix the package before publishing.

## Required local assumptions

This skill expects:
- local `clawhub` CLI installed and authenticated
- local ClawHub config present under the current user
- a real skill directory containing `SKILL.md`
- Node available for the publish script

## Scripts

Use `scripts/publish_to_clawhub.js` for the actual API upload.

Arguments:
```bash
node scripts/publish_to_clawhub.js --skill-path <path> --slug <slug> --version <version> --changelog <text>
```

Optional:
```bash
--display-name <name>
--tag <tag>   # repeatable
```

## References

Read `references/release-checklist.md` before publishing when the release is important or public.

## Output style

Report with this structure:
- skill
- local path
- prior remote version (if any)
- target version
- upload result
- verification result
- final URL
- risks or follow-ups
- whether publication succeeded immediately or was queued for delayed retry

Keep it short and operational.
