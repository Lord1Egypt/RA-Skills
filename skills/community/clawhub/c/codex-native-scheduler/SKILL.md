---
name: codex-native-scheduler
description: Schedule, inspect, retry, pause, resume, stop, and decommission unattended Codex CLI jobs through macOS launchd, Linux systemd user timers, or Windows Task Scheduler. Use when the user wants Codex to run later or recur without a resident daemon, or needs to manage jobs created by codex-schedule.
---

# Codex Native Scheduler

Use the bundled `scripts/codex-schedule` CLI. It stores private state under
`$CODEX_HOME/codex-native-scheduler` and registers only the native backend for
the current platform.

## Workflow

1. Run `scripts/codex-schedule doctor` before the first scheduled job on a host.
2. Confirm the intended working directory, schedule, and whether the prompt may
   write files.
3. Prefer `--workspace worktree` for write-capable recurring jobs. Direct jobs
   can conflict with other jobs using the same directory.
4. Use exactly one prompt source and exactly one schedule:

   ```console
   scripts/codex-schedule create \
     --name weekly-review \
     --cwd "$PWD" \
     --weekly-at mon@09:30 \
     --workspace worktree \
     --prompt-file ./weekly-review.md
   ```

5. Inspect the returned job and native status with `status`. Use `run-now` only
   when the user explicitly wants an immediate manual run.
6. Use `runs` and `run-show` for evidence. Raw JSONL, stderr, final output, and
   snapshots live in the reported run directory.

## Configuration

Pass a Codex profile with `--profile`. Pass any Codex override repeatedly with
`-c key=value`. Do not invent another permission acknowledgement or filter:
Codex receives the values through `codex exec --strict-config` and enforces its
own valid keys, authentication, approval, sandbox, and organization policies.

`new_each_run` is the default session mode. Use `resume_fixed` only when the
task intentionally needs continuity; it forces overlap policy `skip`. Changing
cwd or workspace mode for a fixed session requires `update --reset-session`.
To continue an existing Codex session, create a direct `resume_fixed` job with
`--session-id SESSION_UUID`; its `--cwd` should be the session's working
directory.
Seeded sessions do not inherit the scheduler's default profile and reject
`--profile` and `-c` so the job cannot override the session's model settings.
Profile and Codex overrides remain locked until `update --reset-session`
starts a new session generation.

## Operations

- `pause JOB` unregisters future wakes and leaves an active run alone.
- `resume JOB` registers future wakes again.
- `stop RUN` stops one active run.
- `retry RUN` creates a linked manual run and does not increment schedule count.
- `prune [JOB] --dry-run` previews retention cleanup.
- `delete JOB --yes` permanently deletes job state.
- `decommission` unregisters every job and preserves state before uninstalling.
- `purge --yes` removes state only after decommissioning.

Never enable Linux linger, edit Codex configuration, commit/merge/push a
worktree, or delete a dirty worktree on the user's behalf.

Read [references/semantics.md](references/semantics.md) when exact count,
catch-up, DST, retry, overlap, session, or retention behavior matters.
