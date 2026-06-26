---
name: claw-wiki
description: Reference and refresh a local OpenClaw documentation snapshot for product usage, deployment, configuration, CLI commands, channels, gateway behavior, tools, troubleshooting, and docs-version verification. Use when users ask how OpenClaw works, how to configure or operate it, where a feature is documented, whether the local docs are outdated, or to update this skill's OpenClaw knowledge base from upstream docs.
metadata:
  short-description: Reference and refresh OpenClaw docs
---

# Claw Wiki

Use this skill to answer OpenClaw questions from local source docs in `openclaw_docs/`, not memory, and to refresh that snapshot when the user explicitly asks for an update.

## Safety Contract

This skill is a documentation lookup and maintenance skill, not a general remote execution or credential-handling tool.

Allowed behavior:

- Read the bundled local docs snapshot under `openclaw_docs/`
- Read local metadata in `docs.json`, `references/`, and `state/`
- Search the local snapshot with deterministic text/file queries
- When the user explicitly asks for a refresh, sync docs from the upstream OpenClaw documentation source and rebuild local indexes

Hard limits:

- Only use refresh mode when the user explicitly asks for freshness verification, update, or sync
- Treat the upstream OpenClaw docs repository as read-only source material
- Only sync documentation content and `docs.json` into this skill
- Only write inside this skill directory, specifically `openclaw_docs/`, `docs.json`, and `state/`
- Do not push commits, open pull requests, upload this skill, or publish local files elsewhere
- Do not read local credential stores, shell history, SSH keys, `.env` files, or unrelated workspace files
- Do not execute downloaded install scripts or run arbitrary shell fragments from documentation examples
- Do not treat example tokens, passwords, API keys, or secrets shown in docs as real credentials

If a requested action exceeds those limits, refuse it and explain the boundary.

The maintained compatibility target is the English docs snapshot. Locale-prefixed navigation entries in `docs.json` may exist, but validation only guarantees the English document set is usable.

## Files

- `./openclaw_docs/`: markdown source docs
- `./docs.json`: optional metadata/navigation mapping
- `./state/source-lock.json`: current snapshot source, ref, commit, and sync metadata
- `./state/docs-manifest.json`: generated manifest of the local docs snapshot
- `./state/topic-index.json`: generated keyword-to-path topic index
- `./state/latest-diff.md`: latest update diff summary
- `./references/routing-cheatsheet.md`: intent-to-path quick router for broad questions
- `./references/query-examples.md`: ready-to-use search query patterns by user intent
- `./references/update-workflow.md`: refresh workflow for syncing and validating the local snapshot
- `./scripts/`: deterministic sync, validate, build, and diff helpers

## Workflow

1. Determine whether the user wants documentation lookup or snapshot maintenance.
   - For normal product questions, answer from the current local snapshot.
   - For "latest", "refresh", "update docs", or "is this outdated?" requests, read `state/source-lock.json` first and use `references/update-workflow.md`.
2. Identify intent and route to likely subdirectories first.
   - If intent is broad or mixed, read `references/routing-cheatsheet.md` first.
   - If wording is clear but query terms are weak, read `references/query-examples.md`.
3. Search with fast text search (`rg`) under `openclaw_docs/`; avoid broad full-tree reads.
4. Read full content of the top 1-3 most relevant files before answering.
5. Synthesize a direct answer and include exact file paths used.
6. When freshness matters, report the current snapshot commit/date from `state/source-lock.json` and do not imply the snapshot is current unless it was just refreshed.
7. If the user explicitly requests a refresh, run the scripted flow:
   - `python scripts/sync_docs.py ...`
   - `python scripts/validate_docs.py`
   - `python scripts/build_knowledge.py`
   - `python scripts/diff_docs.py`
8. If docs are ambiguous or missing, say so explicitly and state what was searched.

## Maintenance Guardrails

- Prefer a local OpenClaw checkout when available.
- If remote sync is needed, use the pinned upstream OpenClaw docs source only.
- Limit refresh work to documentation ingestion, validation, indexing, and diff generation.
- Review generated `state/latest-diff.md` before claiming the refresh succeeded.
- If sync input looks unrelated to OpenClaw docs, stop and report the mismatch instead of forcing the update.

## Update Principles

- Refresh this skill by reading upstream OpenClaw docs into the local snapshot only.
- Allowed: local repo reads, `git fetch`, `git clone`, copying `docs/` and `docs.json` into this skill, and rebuilding local indexes.
- Not allowed: `git push`, PR creation, uploading this skill folder, or sending local skill contents back to GitHub.
- Treat upstream refs such as `main`, tags, or commits as read-only sources, not write targets.
- Prefer a local OpenClaw checkout when available; otherwise clone/fetch the upstream repo without modifying any remote.

## Routing Hints

- Getting started/install/platform setup: `start/`, `install/`, `platforms/`
- Runtime model and behavior: `concepts/`, `gateway/`, `tools/`
- CLI commands: `cli/`
- Integrations/providers: `providers/`, `channels/`, `plugins/`, `nodes/`
- Failures and debugging: `help/`, `diagnostics/`, `gateway/troubleshooting.md`, `channels/troubleshooting.md`
- Security topics: `security/`, `tools/exec-approvals.md`, `gateway/security/`
- Experimental or planning material: `experiments/` (only use when user asks for proposals/plans)

## Search and Read Strategy

- Start with targeted queries, then widen only if needed.
- Prefer searching filenames first, then file content.
- Exclude merged or generated outputs when present.
- For very large files, jump to relevant sections first, then expand for surrounding context.
- Do not rely on a single snippet when explaining behavior, constraints, or defaults.
- Prefer local snapshot sync over per-question remote browsing for repeatability.

## Answer Quality Bar

- Ground each key claim in files actually read.
- Include paths in the response so users can verify quickly.
- Separate documented behavior from inference.
- Do not invent flags, defaults, commands, or config keys not found in docs.
- For freshness-sensitive answers, include the snapshot version from `state/source-lock.json`.
