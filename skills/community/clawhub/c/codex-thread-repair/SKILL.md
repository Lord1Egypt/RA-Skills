---
name: codex-thread-repair
description: >
  Diagnose and safely repair one local Codex Desktop task selected by its UI title or
  thread ID when recent turns are missing, truncated, merged into an interrupted turn,
  or hidden by damaged rollout ordering. Do not use for broad project/provider
  restoration or ordinary task continuation.
---

# Codex Thread Repair

- **Version**: 1.0.1
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills/tree/main/skills/codex-thread-repair

Repair a specific local task without rewriting its message bodies or replacing the whole Codex state directory.

## Dependencies

- macOS with the Codex desktop app installed as `/Applications/ChatGPT.app`.
- Python 3.10 or newer. The repair script uses only the Python standard library.
- A local Codex state directory containing `state_5.sqlite`, `sqlite/codex-dev.db`, and the selected task's JSONL rollout. It defaults to `$CODEX_HOME` when set, otherwise `~/.codex`.
- Local read/write access to the selected rollout and Codex state. No network access or third-party Python package is required.

## Workflow

1. Resolve `<skill-dir>` as the directory containing this `SKILL.md`; never assume that the current working directory is the skill directory. Resolve and diagnose the user-supplied title or ID while Codex may remain open:

   ```bash
   python3 "<skill-dir>/scripts/thread_repair.py" diagnose "<title-or-id>"
   ```

   Exact UI-title matches come from `local_thread_catalog`; canonical rows and rollout paths come from `state_5.sqlite`. If a title is ambiguous, show the candidates and ask the user for an exact ID. Never choose by recency alone.

2. Read [references/repair-patterns.md](references/repair-patterns.md) when diagnosis is not `healthy` or `supported_ordinal_orphan`. Do not auto-repair an unrecognized structure.

3. For `supported_ordinal_orphan`, explain the detected boundary and prepare one offline launcher:

   ```bash
   python3 "<skill-dir>/scripts/thread_repair.py" prepare "<title-or-id>"
   ```

   Tell the user to press Cmd+Q and then double-click the returned `.command` file. The launcher creates a targeted recovery set, applies the patch atomically, verifies it, and reopens Codex.

4. After Codex restarts, verify both layers:

   ```bash
   python3 "<skill-dir>/scripts/thread_repair.py" verify "<title-or-id>"
   ```

   Also use the Codex task-reading tool to confirm that the formerly hidden recent turns are separate and readable.

5. Keep the backup until the user confirms the UI. If rollback is required, have the user quit Codex and run:

   ```bash
   python3 "<skill-dir>/scripts/thread_repair.py" rollback "<backup-directory>" --reopen
   ```

## Safety boundaries

- Diagnosis and launcher preparation are read-only with respect to Codex state.
- Mutation requires Codex Desktop, its renderer/services, and its app-server to be stopped.
- Resolve the selected rollout to an absolute path under the selected Codex home's `sessions/` directory. Refuse relative paths, symlink escapes, and database paths outside that directory.
- Back up the target rollout plus consistent snapshots of `state_5.sqlite`, `codex-dev.db`, and `.codex-global-state.json` before replacement.
- Preserve the original rollout byte-for-byte in the backup.
- Auto-repair only the narrowly validated ordinal-regression/orphan-turn pattern. Refuse multiple regressions, ambiguous open turns, missing rollouts, malformed JSON, non-contiguous segments, active latest turns, or session-ID mismatches.
- Preserve every original line except the top-level `ordinal` value after the repair boundary; insert exactly one `turn_aborted` event. Verify a normalized content hash before replacement.
- Do not edit SQLite rows for this repair type. For provider mismatches, missing assignments, moved paths, or missing database rows, use `recover-codex-project-chats` instead.
- On any post-replacement verification failure, restore the backed-up rollout automatically.

## Commands

```bash
python3 "<skill-dir>/scripts/thread_repair.py" resolve "<title-or-id>"
python3 "<skill-dir>/scripts/thread_repair.py" diagnose "<title-or-id>"
python3 "<skill-dir>/scripts/thread_repair.py" prepare "<title-or-id>"
python3 "<skill-dir>/scripts/thread_repair.py" apply "<exact-thread-id>" --reopen
python3 "<skill-dir>/scripts/thread_repair.py" verify "<title-or-id>"
python3 "<skill-dir>/scripts/thread_repair.py" rollback "<backup-directory>" --reopen
```

`--codex-home <path>` is a global option and must appear before the subcommand. `prepare --output <path>` selects a new launcher path and refuses to overwrite an existing file. `apply --reopen` and `rollback --reopen` request reopening Codex; failure to reopen is reported as a warning without undoing a successful file operation.

Exit codes are `0` for success or no repair needed, `1` for an operational/safety error, `2` for an ambiguous selector or invalid CLI use, and `3` for an unsupported diagnosis or failed verification.

Report the resolved ID, UI title, rollout path, diagnosis, changed metadata, backup directory, integrity results, and UI verification outcome.

See [CHANGELOG.md](./CHANGELOG.md) for release history.
