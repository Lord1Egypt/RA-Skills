---
name: codex-cross-provider-session-repair
description: Repair Codex Desktop sessions that fail after switching model providers or importing/forking old conversations. Use this skill whenever a user mentions an old Codex session becoming invalid, “model provider not found”, “Codex cannot load config.toml”, remote context compaction 404s, “Item with id rs_... not found”, repeated reconnecting during resume, or a migrated Codex conversation that cannot continue—even when the user only asks to inspect or explain the failure. Diagnose the target session across its JSONL rollout, root state_5.sqlite, config.toml, and logs_2.sqlite, then make a target-scoped backup-first repair with verification and restart instructions.
license: MIT
metadata:
  version: "0.7.5"
  repository: "https://github.com/WardLu/skills/tree/main/codex-cross-provider-session-repair"
  maintainer: "Ward Lu"
---

# Codex cross-provider session repair

Compatibility: Requires Python 3.9+ with the standard library; Windows, macOS,
and Linux Codex homes are supported. Stop Codex Desktop before applying file
or database changes. On macOS, the recommended launcher requires Terminal
automation permission so it can close only its uniquely titled repair window.

Use this skill for a damaged or incompatible *saved Codex session*, not for ordinary model/API troubleshooting. The goal is to make one existing conversation resumable while keeping its user-visible history and avoiding broad cache deletion.

## User interaction flow (end-to-end)

The user does not need to memorise CLI flags. A typical session looks like this:

1. **User opens a *new* Codex conversation** (the broken one cannot be used) and provides the session UUID and visible error.
2. **Agent runs the dry-run diagnostic** (see Workflow below). The report shows which failure mode applies and what will be changed.
3. **Agent explains the root cause and gets approval for the write.** After approval, start `scripts/start_repair.py` immediately. On macOS it opens a readable Terminal tab/window and runs the independent worker through a short temporary runner; do not paste the full worker command into the user's shell. The worker is safe whether Codex is still open, is being closed, or was already closed after the approval. Immediately tell the user in the current conversation: `修复任务已启动，最多等待 300 秒；请完全退出 Codex。终端会持续显示进度，完成前不要重新打开。 / Repair started; it may wait up to 300 seconds. Fully quit Codex; follow the Terminal status and do not reopen it before completion.`
4. **Do not reopen Codex until verification says `Verified / 已验证`.** The Terminal shows bilingual states: `Waiting / 等待中`, `Applying / 修复中`, `Verified / 已验证`, or `Failed / 失败`. During the default 300-second wait it prints reminders at about 60, 180, and 240 seconds. The status JSON also exposes `wait_timeout_seconds`, `wait_phase`, `conversation_notice`, and `can_reopen`; only `can_reopen: true` permits reopening. If the current conversation remains available, mirror the wait/reminder status there; after Codex is fully closed, the independent Terminal and status JSON are authoritative.
5. **After verification, relaunch Codex Desktop** (Cmd+Q/reopen on macOS), open the repaired session, and send a short test message.

### Finding the session ID

If the user does not know the UUID, help them find it:

- **From the Codex App UI**: right-click the broken conversation in the sidebar; some versions show the ID in the context menu or in the URL bar.
- **From the filesystem**: list recent rollout files:

  ```bash
  ls -lt ~/.codex/sessions/*/*/rollout-*.jsonl | head -10
  ```

  The UUID is the last segment of the filename (e.g. `rollout-2026-08-02T22-05-32-<UUID>.jsonl`).
- **From the database**: query the threads table for recent sessions:

  ```python
  import sqlite3
  conn = sqlite3.connect("~/.codex/state_5.sqlite".replace("~", str(__import__("pathlib").Path.home())))
  for row in conn.execute("SELECT id, title, model, updated_at FROM threads ORDER BY updated_at DESC LIMIT 10"):
      print(row)
  ```

### One-shot repair command

After Codex Desktop is fully quit, the manual one-shot command can combine all
needed flags in a single `--apply` invocation:

```text
python3 <skill_dir>/scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> --fix-provider --provider <current> --fix-model-turn --remove-reasoning all --apply
```

Run the same command without `--apply` afterward. Do not report completion until
the post-repair report has been captured and verified.

## What this skill fixes

Codex stores continuation state in several layers:

1. the global `config.toml` (current provider defaults);
2. a dated `sessions/**/rollout-*.jsonl` file (the conversation event stream);
3. the root `state_5.sqlite` `threads` row (the desktop index and provider snapshot); and
4. `logs_2.sqlite` (diagnostic evidence).

After a provider switch, an old thread can retain a provider in layers 2 or 3 even when the global config is correct. Separately, an imported/forked long thread can contain `response_item` reasoning records that were sent with `store=false` and never persisted by the service. Remote compaction then fails with HTTP 404: `Item with id 'rs_...' not found`.

The second failure is not fixed by changing the provider, deleting `config.toml`, or clearing browser cache. If multiple different `rs_...` IDs fail in succession, remove the non-user-visible local reasoning items in one pass; deleting one ID at a time only exposes the next stale reference.

A third failure occurs when switching to a Gemini-backed model (e.g. `gemini-3.6-flash-high` via a proxy such as CC Switch). Gemini's API rejects requests whose message history ends with a `model`/assistant turn: `Requests ending with a model turn are not supported.` (HTTP 400 INVALID_ARGUMENT). Codex triggers pre-sampling context compaction (`CompHashChanged`) on model switch; if the effective history after `thread_rolled_back` events ends with an assistant message, the compaction request fails and the turn cannot start. This is systemic—every session switched to Gemini that needs compaction will hit it until the JSONL is repaired.

A fourth failure occurs when the current provider/model does not implement
Codex's remote compaction v2. The turn fails with `Error running remote compact
task: Fatal error: remote compaction v2 expected exactly one compaction output
item, got 0 from N output items`. This is not a JSONL corruption: the backend
simply did not return the `type: "compaction"` output item Codex requires. The
report prints a user-friendly hint and the operator should either disable
remote compaction or switch to a provider/model that supports it. The script
offers `--disable-remote-compaction` (requires `--apply` and explicit user
approval) to write `remote_compaction_v2 = false` under `[features]` in
config.toml with a backup; after applying, fully quit and relaunch Codex
Desktop.

A fifth failure occurs when an imported session is pinned to a model that the
current ChatGPT account cannot use, such as `ark-code-latest`. The report
identifies the model in the rollout's structured turn settings and the target
`threads.model` snapshot. Use `--fix-model --model <current-model>` to update
only those target-session values. Pair it with `--remove-reasoning none` when
the session has no stale-reasoning diagnosis; this preserves all local
reasoning records.

## Safety contract

- Work on the requested session ID only. Do not update every thread or every session by default.
- Start with a dry run. Before any write, make a timestamped backup of the JSONL; back up the root SQLite database (including WAL/SHM sidecars) only when changing its provider row.
- Ask the user to fully quit Codex Desktop, including the tray process and its bundled `codex app-server`/service processes, before applying changes. A live process can cache old events or hold a file lock.
- Never treat a task-bound background waiter, a closed tool session, or a returned process exit code without a backup as proof that a repair ran. The independent wait wrapper must end in `verified`.
- Never delete the whole Codex home, all sessions, `config.toml`, auth tokens, caches, or databases as a generic “reset”.
- Preserve every user message, visible assistant message, tool call, tool result, and `event_msg`. Only remove `response_item` records whose payload type is `reasoning`, and only when the diagnosis supports the stale-compaction repair.
- Do not print auth tokens, refresh tokens, API keys, or complete session contents. Redact paths and secrets in reports.
- If the target rollout cannot be found, JSON parsing fails, or a backup cannot be created, stop and report the blocker instead of guessing.

## Workflow

### 1. Identify the target and Codex home

Use the exact session UUID supplied by the user. Resolve `CODEX_HOME` first; on Windows fall back to `%USERPROFILE%\\.codex`, and on macOS/Linux to `$HOME/.codex`. Do not repurpose common environment variables in shell snippets.

Locate the rollout by filename suffix and then confirm its first `session_meta` record contains the requested ID. Do not trust a title or current working directory alone; imported files can contain more than one `session_meta` record.

### 2. Diagnose read-only

Run the bundled script in dry-run mode:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME>
```

The report should include:

- the exact rollout path and line count;
- JSON parse errors (must be zero before repair);
- target `session_meta` provider values;
- the global provider from `config.toml`;
- the target `threads.model_provider` from root `state_5.sqlite` (the important database, when present);
- distinct `rs_...` IDs extracted from target-thread log errors; and
- how many of those IDs are actual local `response_item` reasoning records.

Use Python's built-in `sqlite3` module; do not require the optional `sqlite3` CLI. Treat a missing `sqlite/` child database as normal and do not invent one.

### 3. Select the smallest justified repair

**Provider mismatch.** If the current provider is known and the target session or target DB row still names an old provider, apply a target-only provider repair:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> \
  --provider <current-provider> --fix-provider --apply
```

Update only the target session's `session_meta` payload and the target `threads` row. Never run a global `UPDATE ... WHERE model_provider=...` for a shared Codex home.

**Unsupported saved model.** If the report shows a model such as
`ark-code-latest` that the current account does not support, align only the
target rollout settings and root thread snapshot with the current configured
model:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> \
  --model <current-model> --fix-model --remove-reasoning none --apply
```

This creates a JSONL backup and a database backup when the target row changes.
It does not delete reasoning records or alter the global `config.toml`.

**Stale remote compaction.** If logs show `Item with id 'rs_...' not found` and the IDs map to local `response_item` records with `payload.type == "reasoning"`, use:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> \
  --remove-reasoning stale --apply
```

This removes only the exact stale IDs. If the user has already seen two or more different stale IDs from the same imported/migrated session, or a retry reveals another ID immediately, use the one-pass cleanup:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> \
  --remove-reasoning all --apply
```

`all` means all local `response_item` records whose payload type is `reasoning`; it does not remove `event_msg.agent_reasoning`, visible messages, tool calls, or tool outputs. This is appropriate because those reasoning items are internal model traces and the service has already confirmed that they were not persisted.

Provider repair and reasoning cleanup can be combined in one invocation after the dry-run report confirms both conditions.

For the recommended user-facing execution, start this command immediately after
the user approves the repair. On macOS it opens a visible Terminal window,
shows the final result, and closes its uniquely titled repair window after the
user presses Enter:

```text
python3 <skill_dir>/scripts/start_repair.py --session-id <UUID> \
  --codex-home <CODEX_HOME> --remove-reasoning stale
```

The command passes `--allow-already-stopped` to the worker, so the user may
quit Codex before or after the worker starts. The worker still requires a
stable process-free window and a rollout fingerprint match before writing.
Terminal output and the status file use bilingual labels. The Terminal opens a
120-column by 36-row window, hides the long worker command behind a temporary
runner, and first announces the maximum wait, then reminds the user at about
60, 180, and 240 seconds. `Verified / 已验证` means it is safe to reopen; `Failed / 失败`
means keep Codex closed. The launcher tags the repair window with the session
ID; after the final Enter prompt, it closes that exact window when it contains
only the repair tab and exits its shell. If macOS has not granted Terminal
automation permission, the worker still exits normally and the user can close
the finished window with Command+W. A timeout writes `wait_timed_out: true`
and a conversation-ready next-step message without changing the session.

For advanced use, start the lower-level process-aware worker from a Terminal
that is independent of Codex while Codex is still open:

```text
python3 <skill_dir>/scripts/wait_and_repair.py --session-id <UUID> --codex-home <CODEX_HOME> --remove-reasoning all --status-file /tmp/codex-session-repair-<UUID>.json
```

Then fully quit Codex Desktop. The wrapper prints bilingual status labels and
atomically updates the same status file. It announces the configured wait
limit and emits periodic reminders. If Codex reappears during the stability
window or the rollout changes while waiting, it stops without writing and
reports `Failed / 失败`.

**Gemini model-turn compaction.** If the dry-run report shows `Model-turn compaction: RISK` or `logged-error`, the effective history ends with an assistant message and Gemini compaction will fail. Use:

```text
python scripts/repair.py --session-id <UUID> --codex-home <CODEX_HOME> \
  --fix-model-turn --apply
```

This removes `thread_rolled_back` event records so that previously rolled-back turns (which typically contain the trailing user message) become effective again. If the last effective message is still `assistant` after rollback removal, a dummy `user` message is appended to satisfy Gemini's requirement. The repair can be combined with `--fix-provider` and `--remove-reasoning` in the same invocation.

### 4. Verify the file and database

Run the script again without `--apply`, or use its `--verify` output. Confirm:

- every remaining JSONL line parses;
- zero stale IDs remain as local reasoning items;
- provider values agree with the chosen current provider when provider repair was requested;
- the target `threads.model` and all structured rollout model settings agree with the chosen model when model repair was requested;
- the backup path is reported; and
- a new backup was created by this apply, not just a zero exit code; and
- no unrelated session was changed;
- the `Model-turn compaction` line shows `ok` (not `RISK`) and `last_role=user` when `--fix-model-turn` was applied.

The report labels log-derived IDs as `Historical remote stale IDs (from logs)`.
That list may remain after a successful repair because it is historical evidence.
The decisive fields are `Stale IDs present as local reasoning: []` together with
`Local reasoning records: 0`. The raw `rs_...` text may still occur inside a
historical `task_complete` error event; that text is not a `response_item`
submitted for compaction and does not need to be deleted.

### 5. Reload and test

Tell the user to fully quit and relaunch Codex Desktop, then open the exact session. A page refresh is insufficient because the desktop process caches the event stream. A safe smoke test is a short prompt that asks for a confirmation only; do not resume the user's old project task automatically.

If compaction succeeds and the error changes to authentication, transport, or provider availability, stop treating it as a session-file problem and diagnose that separate issue. If a new stale ID appears after a clean reload, re-run the dry-run report before changing anything else.

## Bundled tools

Install this skill with `npx skills add WardLu/skills --skill codex-cross-provider-session-repair --global --agent codex --yes`, or use the platform installer documented in `README.md`.

- `scripts/repair.py` — deterministic, backup-first diagnosis and target-scoped repair.
- `scripts/start_repair.py` — recommended consent-to-terminal launcher; opens a readable 120×36 Terminal tab/window on macOS, hides the long worker command behind a temporary runner, and starts the worker even when Codex was already closed.
- `scripts/wait_and_repair.py` — process-aware wait/apply/verify wrapper for use from an independent Terminal. It fails closed if Codex was not detected initially, reappears during the stability window, or changes the rollout while waiting.
- `tests/test_repair.py` — offline tests using temporary fake Codex homes and SQLite databases.
- `tests/test_wait_and_repair.py` — offline tests for process lifecycle, rollout race protection, status files, and end-to-end verification.
- `README.md` — installation, upgrade, release, and troubleshooting guide.

## Documentation

The English installation and maintenance guide is `README.md`; Simplified Chinese users can use the synchronized `README.zh-CN.md` guide.

## Report format

Give the user a concise result with: root cause, exact target session, files changed, backup paths, verification counts, whether the independent process-aware run reached `verified`, whether an independent smoke test reached `Context compacted`, and the one required restart step. When the wait ends in a timeout, explicitly state that the configured wait limit was reached, no files were changed, and the user must fully quit Codex before retrying. Never include credentials or full JSONL lines.
