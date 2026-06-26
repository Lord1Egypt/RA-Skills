---
name: easy-ci-cd
description: Build lightweight, minimal CI/CD scaffolding around a small project. Use when asked to add or simplify GitHub Actions, create a fast CI pipeline, add a minimal Dockerfile, wire basic test/smoke checks, package small release artifacts, or make a repo deploy-ready without adding heavyweight enterprise workflow complexity.
---

# Easy CI/CD

Keep CI/CD boring, fast, and proportionate to the size of the project.

## Workflow

1. Inspect the repo first.
   - Detect language, package manager, test command, and likely runtime command.
   - Read the existing README/config before adding automation.
   - Do not invent build steps the repo does not support.

2. Choose the minimum useful pipeline.
   - Default to one OS and one runtime version.
   - Trigger on `push` and `pull_request` to the main branch unless the repo clearly uses another default branch.
   - Add concurrency with cancel-in-progress for redundant runs.
   - Prefer one job unless the user explicitly wants more.

3. Add only high-value checks.
   - Run the smallest realistic install step.
   - Add a smoke check if it is cheap and meaningful.
   - Run the repo's existing tests if they are available.
   - Prefer fast feedback over exhaustive matrices.

4. Add a tiny release/deploy feature only when it helps.
   - Good defaults: upload test results, upload a source archive on tags, or build a minimal container.
   - Do not add cloud deploy, secrets, registries, or production rollout logic unless the user explicitly asks.

5. Add containerization only when requested or clearly useful.
   - Prefer a common slim base image for the language/runtime.
   - Install only common/lightweight system packages that are likely needed.
   - Keep the default command safe and easy to override.
   - Add a small `.dockerignore`.

6. Verify locally when practical.
   - Run the same cheap checks you put into CI when the environment allows.
   - If full verification is not practical, say so plainly.

7. Update docs minimally.
   - Add 1 short section or a few lines to README if needed.
   - Do not turn a small repo into a manual.

## Guardrails

- Keep YAML readable and short.
- Prefer standard marketplace actions.
- Avoid multi-OS and multi-version matrices unless the project really needs them.
- Avoid long installs and unnecessary services.
- Avoid secret-dependent steps unless the user explicitly provides that direction.
- Match the repository's existing style and naming.

## Good Defaults

### GitHub Actions

For small repos, prefer:
- `actions/checkout`
- language setup action with dependency caching if cheap
- install deps
- smoke check
- test command
- artifact upload if useful

If you need examples, read `references/templates.md`.

### Docker

For small Python repos, prefer:
- `python:<version>-slim`
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`
- small apt install block only if likely needed
- install from `requirements.txt` or project metadata
- safe default `CMD`

## Output Expectations

When reporting back:
- say what was added
- say where it lives
- say how it was verified
- mention anything intentionally left out to keep it minimal
