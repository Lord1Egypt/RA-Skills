# OpenClaw Update Workflow

Use this file when the user asks to refresh the local OpenClaw docs snapshot, inspect snapshot freshness, or report what changed after an update.

## Goals

- Keep answers grounded in a local snapshot, not memory.
- Make the snapshot version visible through `state/source-lock.json`.
- Rebuild indexes after every sync so routing stays aligned with the current docs tree.

## Commands

Local repo sync:

```bash
python scripts/sync_docs.py --source-path ../openclaw --mode pinned
python scripts/validate_docs.py
python scripts/build_knowledge.py
python scripts/diff_docs.py
```

Remote sync:

```bash
python scripts/sync_docs.py --repo-url https://github.com/openclaw/openclaw --ref main --mode tracking
python scripts/validate_docs.py
python scripts/build_knowledge.py
python scripts/diff_docs.py
```

## Operational Rules

- Prefer `--source-path` when a local checkout exists; it avoids network dependency.
- Run validation before telling the user the refresh succeeded.
- If validation fails, keep the old snapshot and report the failure.
- When asked "what version is this skill based on?", read `state/source-lock.json`.
- When asked "what changed?", read `state/latest-diff.md`.
- Treat upstream branches, tags, and commits as read-only sources.
- Do not push, create PRs, upload this skill folder, or send local skill contents back to GitHub.
- Allowed network activity for refresh is limited to read-only fetch/clone of the upstream OpenClaw repo.
