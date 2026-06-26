---
name: project-bootstrap
description: Bootstrap new projects with predictable structure and validation commands.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: execution
---

# SKILL: project-bootstrap

## Purpose
Initialize a new project with a predictable structure, quality gates (lint/test), and safe configuration defaults.

## When to Use
- Starting a new service/app/library.
- Creating a new package inside a monorepo.
- You need a repeatable baseline for contributors/CI.

## Inputs
- `project_type` (required, enum: `backend|frontend|library|contract|cli`).
- `stack` (required, string): e.g., â€œnode-tsâ€, â€œpython-fastapiâ€, â€œnextjsâ€.
- `name` (required, string): project/package name.
- `path` (required, string): target directory.
- `constraints` (optional, string[]): repo rules, linting, deployment constraints.

## Steps
1. Confirm target directory and ensure it is safe to create/modify.
2. Select a template that matches repo conventions; prefer minimal dependencies.
3. Scaffold project structure (src/tests/config/docs).
4. Configure:
   - lint/format (if repo uses them)
   - unit test runner
   - env/config examples (`.env.example`), never real secrets
5. Add a README with:
   - how to run locally
   - how to test
   - key design decisions
6. Run deterministic validation commands (install + test + build).

## Validation
- Project builds/runs locally (basic smoke check).
- Tests execute and pass (even if minimal).
- No secrets or machine-specific paths are committed.

## Output
- Created file tree
- Commands to run (`install`, `dev`, `test`, `build`)
- Configuration contract (env vars and defaults)

## Safety Rules
- Never modify global tooling on the machine unless explicitly requested.
- Pin versions where the repo requires it.
- Do not auto-deploy; bootstrap is local by default.

## Example
Bootstrap a TS backend:
- `project_type`: `backend`
- `stack`: `node-ts`
- Output: `apps/api/` with `pnpm test` and `pnpm dev` working.
