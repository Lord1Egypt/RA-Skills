# foreman · Chapter 1 · Dispatch

## 0. Preconditions

- **Before any batch dispatch (2+ tasks)**: run `bash <skill-dir>/fleet-check.sh`. Any FAIL gets fixed the way the script says or routed around explicitly — never skipped silently. A single task does not need it.
- Confirm the repo root has a `BRIEFING.md` — the subcontractor briefing: why the stack was chosen, naming conventions, known traps, forbidden zones. If there isn't one, spend five minutes writing it before dispatching anything.
- Confirm `.foreman/` is in `.gitignore`.
- While scanning `.foreman/`, watch for two escalation signals worth reporting to the user unprompted: **forgotten overdue tasks while 3+ batches are in flight**, and **the same kind of task being dispatched twice within a week** (that second one means the work wants a standing rule, not another one-off dispatch).

## 1. Exemption check (objective: two questions and a clock)

1. Can you write a **task-specific assertion command** for this task? A generic `npm test` does not count.
2. If you can't → do a **5-minute spike** to probe the interface, then come back to question 1.
3. Still can't = it is exploratory work → exempt it: the main session does it directly. But **start a clock on disk first**:
   `.foreman/exempt-<slug>.json` ← `{"started_at": "<now>", "deadline_at": "<now+30min>"}`
   The next time foreman runs and sees it overdue → **force the dispatch**. The spike's findings go straight into the work order's "Must comply with" section; those 30 minutes were reconnaissance, not waste.

## 2. Assemble the work order

- Use the template at `<skill-dir>/work-order.md`. All sections plus the allowed-paths whitelist get filled in — including "Commit before you deliver".
- Reference `BRIEFING.md` **by path** ("read BRIEFING.md at the repo root before starting"), never inline its full text.
- Every order declares an **allowed-path whitelist**. Across parallel tasks, both the paths and the shared interface surface (schemas, route tables, shared types, lockfiles, migrations) must be mutually exclusive. Anything that overlaps gets serialized instead.
- A task estimated over an hour splits into two rounds: interface skeleton first → main session confirms the direction → then release the full implementation.
- Tag every verification command `persistent` (becomes a long-lived regression test after merge) or `one_shot` (retired after merge). **Commands with side effects** (migrations, seeds, one-time tokens) run only in final CI; the builder's self-check and your intake re-run use a side-effect-free preflight variant.

## 3. Dispatch

```bash
BE=$(bash <skill-dir>/backend-health.sh pick) || { echo "no usable backend in the pool — stop and report"; exit 1; }
WT=$(bash <skill-dir>/worktree-setup.sh "$(pwd)" <slug>) || { echo "worktree setup failed — see the error above"; exit 1; }

handoff new --backend "$BE" --slug <slug> --write <<'__HF_EOF__'
[full work order]
__HF_EOF__
handoff run --backend "$BE" --cwd "$WT" ~/.handoff/tasks/<RUN_ID>.prompt.md   # run in background
```

`handoff` is a public CLI (`uv tool install handoff-cli==4.0.2 && handoff init` — pin the version you reviewed; upgrade deliberately, not implicitly); configure your backends in `~/.handoff/config.yaml`.

**`--cwd "$WT"` is not optional.** Without it the worker runs in *your* working directory. That has happened for real: a dispatched task switched branches and committed directly in the main session's own checkout, and the main session's HEAD went with it. `worktree-setup.sh` builds `~/foreman-worktrees/<slug>` on branch `work/<slug>`, reuses a clean one for the same slug, and refuses a dirty one or a leftover branch — it never deletes uncommitted work. Don't hand-write `git worktree add`: an invariant that lives only in prose gets copied out of the example by the next person.

### The worker pool

Pick backends from a pool, in order, by **who still has quota and whether the task suits them — not by which IDE the foreman runs in**. Set the order with `FOREMAN_POOL` (names as in your handoff config). An example shape:

| Order | Backend (your name for it) | Paid by | Notes |
|---|---|---|---|
| 1 | a Claude-type backend | an existing Claude subscription | no API key; relies on the claude CLI's login (see below) |
| 2 | `codex` | a ChatGPT subscription | its probe spends one minimal request |
| 3 | `cursor` | a Cursor subscription | see "Cursor through handoff" below |
| last | `deepseek` | pay-as-you-go API key | the overflow outlet: never throttled by a subscription |

Probe cost, failure classes, and cooldowns are documented in the header of `backend-health.sh`; `backend-health.sh status` shows the table.

- **Failure classes**: `ok` / `auth` / `quota` / `config` (unknown model, invalid parameter) / `net`. Cooldowns: `quota` uses the recovery time from the error, or defaults to tomorrow; `config` 6 hours; `net` 10 minutes; **`auth` never cools down** (a login can be fixed at any moment). After fixing a config, `backend-health.sh mark <backend> ok` thaws it immediately.
- **Fallback rule**: every class except `ok` is an **infrastructure failure, not a failed delivery** — move down the pool and redispatch, **without counting a rework round or touching the circuit breaker**, and add `backend_fallback: [<from>, <to>, <reason>]` to the task state file. A failure that only shows up mid-dispatch gets recorded with `backend-health.sh mark <backend> <class> [recover-at]` so the next `pick` skips it.
- **Why probing exists**: in one day, three dispatches failed after being sent — a subscription backend that looked logged out, an API key that looked invalid, a model that the account no longer accepted. The task was out, the worktree built, the time spent, and none of it had anything to do with the quality of the work, yet each would have entered the rework loop. The probe moves those failures in front of the dispatch.
- **Backend names can lie about models.** Many handoff configs keep a backend named after one model while its default is another (with `--pro` selecting the stronger one), because renaming a backend breaks `handoff resume` for old runs. Read the config, not the name.

### Logins and credentials that bite

- **Three separate logins exist for the claude CLI.** A desktop app's own login, the default `claude` CLI login, and the login *keyed by `CLAUDE_CONFIG_DIR`* are not shared. handoff launches claude-type backends with `CLAUDE_CONFIG_DIR` set, so it reads the keyed entry: log in with `CLAUDE_CONFIG_DIR=$HOME/.claude claude auth login`. A plain `claude auth login` writes a different entry that handoff never sees, and the app working fine proves nothing about the CLI.
- **Two claude-type backends need different `CLAUDE_CONFIG_DIR`s.** If a subscription backend and an API-key backend (e.g. DeepSeek through its Anthropic-compatible endpoint) share one, the CLI sends the subscription OAuth token to the API-key endpoint, which answers 401 "api key is invalid". **The error points at the key; the real cause is the login leaking across channels** — replacing a perfectly good key twice won't fix it. Fix: in the API-key backend's `env` block, set `CLAUDE_CONFIG_DIR: ~/.handoff/claude-config-<name>` explicitly (handoff only injects its default when you don't). Diagnostic tip: DeepSeek echoes the last four characters of the key it received in that 401 — compare them with your config.
- **Unattended alternative**: `claude setup-token` issues a long-lived token used via `CLAUDE_CODE_OAUTH_TOKEN`, bypassing the keychain. It is a plaintext long-lived credential: keep it in a mode-600 file, never in a global shell export.

### Cursor through handoff

No handoff code change is needed. handoff deep-merges per-backend fields over the type defaults (lists are replaced wholesale), and `command`, `session_flags`, `continue_id_flags` and `resume_flags` are all overridable — so a backend of `type: claude` with `command: cursor-agent` works. `cursor-agent` has no `--dangerously-skip-permissions` or `--append-system-prompt`: use `--force` to skip confirmations, and put the system prompt into the prompt body itself. **`--force` means the worker runs commands and edits files without asking anyone** — that is what makes background dispatch possible, and it is also why it must only ever run with `--cwd` pointing at a task worktree, never your main checkout, and why every delivery still goes through intake before it is merged. The same holds for any backend configured to skip permission prompts. Unverified: whether the model weighs an inlined system prompt the same as a separate system layer — only that it is sent and followed.

### Caged dispatch (optional; for sensitive repos or when you want a hard blast radius)

The caged worker sees only the mounted worktree — the host `$HOME`, your other repos, and your primary agent login are all invisible to it, so `--dangerously-skip-permissions` only ever applies inside the cage. **Because your subscription login is invisible in there, the cage can't use subscription quota — it runs on an API key.**

Build the worker image once. The Dockerfile is inlined here deliberately, so this step depends on nothing but Docker. **Everything that ends up holding your code and your key is pinned**: the base image by digest, the agent CLI by exact version. Bump them on purpose, after reviewing the new versions — never by rebuilding against whatever is newest.

```bash
docker build -t foreman-worker - <<'DOCKERFILE'
FROM node:22.19-slim@sha256:4a4884e8a44826194dff92ba316264f392056cbe243dcc9fd3551e71cea02b90
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates ripgrep \
    && rm -rf /var/lib/apt/lists/* \
    && npm i -g @anthropic-ai/claude-code@2.1.270 \
    && useradd -m worker
USER worker
WORKDIR /work
ENTRYPOINT ["claude"]
DOCKERFILE
export FOREMAN_WORKER_IMAGE=$(docker image inspect -f '{{.Id}}' foreman-worker)   # immutable id; record it
```

Then dispatch into the cage (set `FOREMAN_DOCKER_CONTEXT` if the image lives in a non-default Docker context — some runtimes switch the default context when they start):

```bash
bash <skill-dir>/foreman-cworker.sh "$WT" ~/.handoff/tasks/<RUN_ID>.prompt.md > result-file &
```

The script refuses to start unless the worktree is a git-registered worktree directly under `FOREMAN_WORKTREE_ROOT` (so never `$HOME`, `/`, your main checkout, or a symlink leading elsewhere), the prompt is a regular file inside `~/.handoff/tasks` (override with `FOREMAN_PROMPT_ROOT`), and `FOREMAN_WORKER_IMAGE` is an immutable reference. It runs the container with all capabilities dropped, `no-new-privileges`, and a read-only root filesystem (only `/work`, `/tmp` and the worker's home are writable). **It does not restrict the network.** The API endpoint in the script is configuration, not a boundary: code inside the cage could still reach other hosts with the key. Give the cage its own key with a low spending limit; if you need a hard boundary, put the container on a network whose only exit is an allowlisting proxy for the API host.

Limits: the worktree must live under your home directory (container VMs usually share only `~`); there is no handoff lifecycle (`tail`/`list`), so results land in the redirected file and you run it in the background; and **git doesn't work inside the cage** (the worktree's `.git` points at the host repository, which isn't mounted). So the cage can't satisfy "commit before you deliver" itself: once the delivery header is in, the **main session** commits the worker's changes in that worktree as `<task_id>: delivered by caged worker`, and intake check 0 then runs against that commit.

### State on disk

- Task state at `.foreman/<task_id>.json`:
  `{task_id, attempt_id, handoff_run_id, backend, worktree, branch, dispatched_at, deadline_at, rework_count, repair_rounds, error_fingerprint, backend_fallback, status}`
  `handoff_run_id` is the basename of the `.prompt.md` path that `handoff new` prints (that command pre-allocates the run and echoes the path, not a bare id). Write it at dispatch time and update it with `attempt_id` on every redispatch — the batch → task → delivery audit chain closes through that field.
  `worktree` / `branch` are what `worktree-setup.sh` returned and created; intake runs against those two fields instead of guessing paths.
- Batch state at `.foreman/batch.json`: `{batch_id, members[], integration_sha: null, total_rounds: 0}`

## 4. Intake (four checks; failing any one is a rejection)

0. **The commit really exists**: does `git -C <worktree> log --oneline <base>..<branch>` show at least one commit? **Judging "did it change anything" from `git diff` on the working tree does not count.** Uncommitted edits are silently dropped when the integration branch merges `<branch>` — every other check passes and nothing fails until verification re-runs on the integrated result. That has been reproduced for real: the builder edited the files, ran verification green, never committed, and `git merge` was a no-op, leaving the integration branch on the old code. No commit = no delivery; send it back.
1. **Delivery header**: a JSON blob of ≤300 tokens (model / commands / exit codes / passed count / first failure summary / log path / committed sha). Locate the delivered artifacts through `handoff_run_id` from the state file — `~/.handoff/tasks/<handoff_run_id>.result.md` and `.out.txt`. **Never guess by recency (`ls -t` and friends)**: on a reworked task with the same slug you will pick up the previous attempt's files. No delivery header = not a delivery; read `result` and `out` to tell a failure apart from a lost result.
2. **Diff boundary**: are the paths touched by `git diff --name-only <base>..<branch>` (commit level, not the working tree) a subset of the allowed paths? Out of bounds → reject, and redispatch that task serialized.
3. **The ruler is untouched**: does that diff touch tests, assertions, or CI config? If it does → reject (global invariant 4).

- After all four checks, the main session re-runs the verification commands itself (side-effect-free variant) as a spot check.
- Results must correspond to the current `attempt_id`. A delivery from a stale attempt is void — discard it.

## 5. Rework and escalation

- Rejected: extract the `error_fingerprint` into the task state file, increment `rework_count`, update `attempt_id`, revise the work order with the failure evidence attached, and redispatch.
- **Infrastructure failures are not rework** (see §3 fallback rule).
- **Stale-ruler conflict** (the builder delivered red, did not touch the ruler, and the failure is a test encoding behavior the spec has since removed): this is not builder error and **does not count as a rework round**. The trusted side (the main session) fixes the ruler in its own commit, with the message noting `Ruler update by trusted side` — every change to the measuring instruments needs its own auditable provenance.
- **Escalation ladder — climb one rung at a time, don't jump straight to the breaker**:
  1. the backend's default model
  2. same fingerprint a second time → the same backend with `--pro` (its stronger model), redispatched with the failure evidence attached
  3. still red → a stronger backend from another vendor, or pull the task back to the main session
- **Batch `total_rounds` ≥ 4** → circuit-break and report to the user with the evidence; stop escalating automatically. Genuinely high-risk tasks may skip the ladder and go to the strongest backend from the start.

## 6. Exit

- All deliveries accepted → merge each task branch into the integration branch, write `integration_sha` into `batch.json` → **automatically read `verify.md` and enter the acceptance chapter**. Do not wait for an instruction.
- In "dispatch only" mode, stop here and remind the user that acceptance has not been done.
