---
name: convex-deploy-env-doctor
description: Validate and fix Convex deployment configuration for skills/apps. Use when debugging Convex URL/callback/env issues, OAuth callback mismatches, .site vs .cloud confusion, or backend connectivity problems before publish/deploy. Do not use for non-Convex stacks. Success = clear pass/fail checks, exact fixes, and verified runtime URL consistency.
---

# Convex Deploy + Env Doctor

## Workflow

1. Detect project config surface
- Check `.env`, `.env.example`, runtime defaults in source, README/SKILL docs.
- Extract all Convex URLs and callback URLs.

2. Validate URL consistency
- Ensure one canonical backend URL intent (`.cloud` for API by default).
- Flag mixed `.site`/`.cloud` usage and explain where each is appropriate.
- Ensure callback URLs match provider/app configuration.

3. Validate required env vars
- Check required/optional env keys and whether docs match runtime usage.
- Flag hidden defaults that route data unexpectedly.

4. Connectivity sanity check
- Run lightweight checks (lint/build and safe HTTP reachability if possible).
- Confirm configured backend is HTTPS and syntactically valid.

5. Output
- Return:
  - ✅ Passing checks
  - ❌ Failing checks
  - exact file-level patches required
  - post-fix verification commands
  - explicit data-routing disclosure (what endpoints/services were touched)

## Output format

Use `references/output-template.md`.

## Guardrails

- Never print secrets.
- Prefer minimal patch release changes.
- Keep docs and runtime behavior aligned.
- Include file+line evidence for each failing check.
