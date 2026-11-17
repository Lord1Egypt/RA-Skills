# Operational semantics

## Scheduling and count

Each job uses exactly one of `--at`, `--every`, `--daily-at`, or
`--weekly-at`. Schedules have minute precision. Native timers only wake the
runner; the stored semantic schedule decides which occurrence is due.
Occurrence claims deduplicate repeated native wakes, and multiple missed
occurrences coalesce into one catch-up run without shifting an interval's
anchor.

Daily and weekly schedules use the system's local wall clock. A nonexistent
time in a daylight-saving gap is skipped. A repeated wall time has one
occurrence key and runs at most once.

`--count` includes scheduled runs that actually start, including failed,
timed-out, and stopped runs. Duplicate wakes, `skipped_overlap`, `run-now`, and
manual retry do not increment it. Recurring schedules are indefinite unless
`--count` or `--until` is set.

## Overlap and failure

`--overlap skip` is the default. A new occurrence that finds an active run is
recorded as `skipped_overlap`; it is not queued or counted. `parallel` is
available only with `new_each_run`. `resume_fixed` always serializes. There is
no cross-job lock or global concurrency limit, so direct jobs sharing a
directory may write concurrently.

A Codex launch receives at most three attempts, separated by 5 and 30 seconds.
Retry stops once `turn.started` is observed. Deterministic configuration,
argument, profile, authentication, and permission errors are not retried.
Profiles and repeated `-c key=value` overrides are passed to
`codex exec --strict-config`; the scheduler does not maintain a Codex key
allowlist.

Failed, timed-out, and abandoned runs increment the consecutive-failure
counter. Success resets it. Three consecutive failures pause a recurring job.
A later manual success clears the counter but does not automatically resume a
paused job.

## Sessions and workspaces

`new_each_run` starts a new Codex session. In worktree mode it also creates a
new branch and worktree for each run. `resume_fixed` reuses one session and,
in worktree mode, one persistent branch/worktree generation. Changing prompt,
schedule, profile, or Codex overrides keeps the fixed session. Changing cwd or
workspace mode requires `update --reset-session`.

An existing Codex session UUID can seed a `resume_fixed` job with `--session-id`
in direct mode. The configured cwd should match that session's working
directory.
Seeded sessions do not inherit the scheduler's default profile and cannot set a
profile or Codex override, preventing the job from overriding the session's
model and reasoning settings. This remains enforced during updates until
`--reset-session` starts a new session generation.

Worktree base policy defaults to `latest`. The configured local branch or
explicit `--base-ref` is resolved at run time without fetch or pull. Detached
HEAD falls back to the captured commit. `snapshot` always uses the captured
commit. The scheduler does not commit, merge, push, or automatically remove
dirty or unmerged worktrees.

Direct mode rejects a dirty Git directory unless `--allow-dirty` is explicit.
Worktree mode requires Git; direct mode may run outside Git.

## Runs, retention, and lifecycle

Each run initially stores `run.json`, a job snapshot, prompt snapshot, attempt
records, raw Codex JSONL, stderr, and the final reply when Codex produces one.
Manual retry creates a new run linked by `retry_of` and resumes the captured
session when its workspace remains available. A missing new-session workspace
falls back to a new session; a missing fixed-session workspace or session
fails until the job is explicitly reset.

Retention defaults to forever. Bounded retention may combine age and retained
run count and is applied automatically after terminal runs. `prune --dry-run`
previews the same candidates. Pruning deletes detailed artifacts and leaves a
tombstone containing run identity, status, timestamps, job revision, and retry
link.

`pause` and `resume` apply only to recurring jobs. Pause prevents future wakes
and leaves an active run alone. `stop` terminates one active run. `cancel`
applies only to a pending one-shot. `delete` is permanent, requires
confirmation, and refuses active runs unless `--stop` is supplied.
`decommission` unregisters native jobs while keeping state. `purge --yes`
requires decommissioned jobs and refuses unsafe worktree removal.

## Platform and security boundaries

State lives under `$CODEX_HOME/codex-native-scheduler`. `--state-dir` and
`CODEX_SCHEDULER_STATE_DIR` override it for isolated tests, CI, and canaries;
native registrations retain the absolute selected path. For deletion safety,
`purge --yes` requires that path's final component to be exactly
`codex-native-scheduler`. Other overridden roots remain usable for
non-destructive commands. POSIX directories and files are private; Windows
protection is best effort. Captured environment values are redacted from
ordinary output but are not encrypted on disk.

The scheduler never enables Linux linger and never falls back to cron, at,
nohup, a resident process, or another backend. It adds no separate permission
acknowledgement or organization-policy preflight; Codex remains responsible
for its configuration, authentication, sandbox, approvals, and managed
requirements, and native errors are retained in private run artifacts.
