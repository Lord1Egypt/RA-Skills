# AGENTS.md

This file provides guidance to Codex and other coding agents when working in this repository. `CLAUDE.md` remains the Claude Code companion file; keep durable repo rules aligned between the two, but do not make Codex depend on Claude-specific tool behavior.

## What this repo is

A Buck Mason personal-shopping skill: markdown, JSON, examples, templates, and deterministic helper scripts. There is no application server or compiled artifact. The agent that loads `SKILL.md` becomes a Buck Mason stylist that talks to the public `pima.io/mcp/buckmason/*` endpoints and selected Buck Mason `/api/*` order/return endpoints.

## Codex surfaces

- `AGENTS.md` is the repo-editing guide for Codex.
- `SKILL.md` is the runtime skill entry point. Keep it lean and point to `references/` for deeper contracts.
- `agents/openai.yaml` is OpenAI/Codex skill UI metadata. Regenerate or update it when the skill name, description, user-facing prompt, or branding changes. Its `default_prompt` must mention `$buck-mason-stylist`.
- `CLAUDE.md` is still useful for Claude-specific publishing and sandbox notes.
- `clawhub.json` is the ClawHub listing/runtime manifest.

## Build, test, and validation

There is nothing to compile. Use targeted validation for the files you touch:

- `python -m pytest tests/` runs the unit and smoke tests for the script bundle.
- `python -m py_compile scripts/*.py scripts/lib/*.py` checks Python syntax.
- `bash -n scripts/deploy-lookbook.sh` checks the deploy wrapper.
- `python -c 'import json; json.load(open("clawhub.json"))'` checks manifest JSON.
- Before publish, visually scan the YAML frontmatter at the top of `SKILL.md` for parser-breaking edits and confirm `clawhub.json#version` matches `SKILL.md` frontmatter `version:`.

Node >= 20.12 is required for `clawhub`; `.tool-versions` pins `nodejs 20.20.2`.

## Versioning

Every substantive change to prompt content, references, scripts, or the MCP contract bumps the version in all three places in the same commit:

1. `clawhub.json#version`
2. `SKILL.md` frontmatter `version:`
3. The commit message, following the existing `vX.Y.Z: <summary>` pattern

If you skip this, ClawHub installs can continue serving the previous skill version.

## Editing rules

- `SKILL.md` is the entry point. When changing a workflow, update both its prose in `SKILL.md` and the matching deeper reference file.
- When adding a reference, script, template, or example, add a one-line entry in both `SKILL.md` "Files in this skill" and `README.md` "Files".
- Keep repo-only docs out of runtime skill instructions. `README.md`, `PUBLISHING.md`, `SECURITY.md`, `CLAUDE.md`, and `AGENTS.md` are for maintainers and reviewers.
- Preserve the opt-in gates. Anything touching money, photos, email, or shipping address needs an explicit user opt-in path and matching `SECURITY.md` / `clawhub.json` updates.
- Do not genericize the skill. Buck Mason store names, product taxonomy, brand tone, and the `https://pima.io/mcp/buckmason/...` host are intentional.
- Prices from Pima are cents; customer-facing output is dollars with a `$`.
- Purchases go through the MCP checkout endpoint only: `POST /mcp/buckmason/checkout` for fully agent-driven MPP. Do not invent `/api/*` purchase paths.
- Only use MPP after same-turn user opt-in with the total restated in plain English and a Link approval handled through `link-cli`.
- Never persist a Stripe SPT, full PAN, or CVV. SPTs are one-time-use.

## Manifest and permissions

`clawhub.json` has load-bearing flat arrays for listing UI compatibility plus sibling detail maps for scanners and reviewers. When adding env vars, binaries, CLIs, or network hosts, update the flat list and the matching details map together. Mirror the same runtime requirements in `SKILL.md` frontmatter under `metadata.openclaw`.

External hosts the skill speaks to must be declared under `permissions.network`. Operator-driven alternatives that are only documented, not invoked by this skill, belong under `permissions.network_alternatives_documented_only`.

## Scripts

The scripts in `scripts/` are the deterministic spine. Keep fragile logic there instead of re-explaining it in prose. Scripts should not make LLM calls internally; agent workflows can call LLM/image APIs around deterministic script steps.

Current high-value checks:

- `scripts/build-html-lookbook.py`
- `scripts/deploy-lookbook.sh`
- `scripts/validate-lookbook.py`
- `scripts/score-calendar-event.py`
- `scripts/discover-weekly-candidates.py`
- `scripts/run-headless-lookbook.py`
- `scripts/verify-face.py`
- `scripts/inject-voting-ui.py`

## Publishing

Publish with `clawhub skill publish . --version <semver>` from the repo root after validation and the lockstep version bump. Visibility comes from `clawhub.json#visibility`; do not add a publish `--visibility` flag.

Do not push, publish, deploy, or transfer ownership unless the user explicitly asks.
