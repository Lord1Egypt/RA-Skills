---
name: clean-codex-archives
description: Safely inspect and remove locally archived Codex conversation data on Windows, macOS, and Linux, including archived rollout JSONL files, archived session rows and related logs in Codex SQLite databases, and stale session_index.jsonl entries. Use when the user asks to clear, purge, delete, or clean archived Codex conversations or their local history metadata.
---

# Clean Codex Archives

Use the bundled `scripts/clean_codex_archives.py` script as the cross-platform entry point. It uses only Python's standard library and preserves active sessions.

## Safety contract

- Resolve the Codex data root from an explicit `--codex-home` argument, then the `CODEX_HOME` environment variable, then the current user's `.codex` directory.
- Treat `state_5.sqlite` as the source of truth. Only rows with `threads.archived = 1` are eligible for deletion.
- Preserve all unarchived threads, their logs, and their session-index entries.
- Run without `--apply` first. Use `--apply` only after the user explicitly authorizes deletion.
- Delete associated logs and goals before deleting archived thread rows, because the archived IDs are needed to select related records safely.
- Delete related `thread_dynamic_tools` and `thread_spawn_edges` rows when those tables are present.
- Remove only `archived_sessions/*.jsonl` files. Do not delete the archive directory itself or unrelated files.
- Rewrite `session_index.jsonl` only after database cleanup, retaining entries whose IDs still exist in `state_5.sqlite` and rejecting malformed JSON instead of silently dropping it.
- If a database is locked, ask the user to close Codex or otherwise stop the process holding the database, then retry.

## Workflow

1. Run a dry run and inspect the counts for archive files, archived threads, related logs, goals, and stale index entries.
2. If the user confirms deletion, rerun with `--apply`.
3. Use `--vacuum` only when the user also wants SQLite files compacted; it may require exclusive database access and is not needed for logical deletion.
4. Verify that archived-thread count is zero, archive-file count is zero, remaining index IDs all exist in the state database, and SQLite `quick_check` reports `ok` for modified databases.

## Commands

```sh
# Inventory only; no changes. Use python3 on Unix-like systems.
python3 ./scripts/clean_codex_archives.py

# Apply the explicitly authorized cleanup.
python3 ./scripts/clean_codex_archives.py --apply

# Use a specific Codex data root.
python3 ./scripts/clean_codex_archives.py --codex-home "$HOME/.codex" --apply

# Optional physical compaction after deletion.
python3 ./scripts/clean_codex_archives.py --apply --vacuum
```

On Windows, use `python` instead of `python3`.
