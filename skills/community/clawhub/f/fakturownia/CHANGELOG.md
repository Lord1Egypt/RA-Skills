# Changelog

All notable changes to the `skills/fakturownia` bundle are documented in this file.

## 0.6.7 - 2026-04-20

- Removed binary installation instructions from the generated root and shared skills so agents no longer receive `curl | bash` bootstrap guidance.
- Kept the readiness flow focused on local verification, authentication, and an authenticated smoke test before API calls.

## 0.6.5 - 2026-04-17

- Added explicit bootstrap guidance to the root bundle and shared skill so agents verify binary availability, authenticate with `auth login`, and verify access before making API calls.
- Kept the bootstrap flow concrete with `fakturownia --version`, `fakturownia auth status --json`, and `fakturownia account get --json` smoke-test steps.

## 0.6.4 - 2026-04-17

- Added marketplace publishing metadata with a bundle-local `manifest.json`.
- Added a repo-root `llms.txt` index that points agents and registries to the canonical docs and generated skill bundle.
- Prepared the generated bundle for GitHub-backed skill registries that ingest from `skills/fakturownia`.

## 0.6.3 - 2026-04-17

- Synced the generated skill bundle with the `v0.6.3` CLI release.
- Published the current bundle root, subskills, and recipe indexes for GitHub-based installation.
