---
name: foreman
description: Dispatch-and-acceptance control desk for farming coding work out to background agents. Probes which worker backend is actually usable, gives each task its own git worktree, sends it to a worker agent via the handoff CLI, takes delivery only as a real commit inside a path whitelist, then gates the merge behind an acceptance protocol whose core rule is that the builder may never touch the tests, assertions, or CI config that judge it. Be aware before using it — it sends repository content to the worker backends you configure; its probes read your local agent login status and may make one minimal request to a backend; and the optional caged worker starts a Docker container, passes DEEPSEEK_API_KEY into it, and lets the worker skip permission prompts inside that container. Use it when batching implementation work out to background agents, or when accepting code that someone else — human or agent — built.
metadata:
  openclaw:
    requires:
      bins:
        - git
        - python3
        - handoff
      config:
        - ~/.handoff/config.yaml
    primaryEnv: DEEPSEEK_API_KEY
    envVars:
      - name: DEEPSEEK_API_KEY
        required: false
        description: Only for the deepseek backend probe (sent to DeepSeek's balance endpoint) and the optional caged worker (passed into the container). Use a dedicated key with a low spending limit.
      - name: FOREMAN_POOL
        required: false
        description: Worker backends to try, in order (names from ~/.handoff/config.yaml). Default deepseek.
      - name: FOREMAN_PROBE_<NAME>
        required: false
        description: Your own probe command for a backend without a built-in probe; run with sh -c.
      - name: FOREMAN_STATE_DIR
        required: false
        description: Where the backend health table is kept. Default ~/.local/state/foreman.
      - name: FOREMAN_WORKTREE_ROOT
        required: false
        description: Where per-task git worktrees are created, and the only place the caged worker will mount from. Default ~/foreman-worktrees.
      - name: FOREMAN_PROMPT_ROOT
        required: false
        description: The only directory the caged worker accepts prompt files from. Default ~/.handoff/tasks.
      - name: FOREMAN_WORKER_IMAGE
        required: false
        description: Immutable sha256 reference of the caged worker image.
      - name: FOREMAN_DOCKER_CONTEXT
        required: false
        description: Docker context holding the worker image.
      - name: FOREMAN_HARDENING_CMD
        required: false
        description: Your dynamic acceptance checker, if any (verify.md).
---

# foreman — thin router

## What this skill touches (trust boundary)

Farming work out to another agent necessarily means handing something a credential and your code, so here is exactly what that involves:

- **Sends repository content to the worker backends you configured** in `~/.handoff/config.yaml` (or, for the caged worker, to the endpoint in `foreman-cworker.sh`). The skill's own scripts send nothing else — no telemetry, no phone-home. What a worker agent does with network access is up to that agent: this skill does not restrict it (see the caged-worker note below).
- **Writes** `.foreman/` inside your repo (task and batch state; it must be gitignored), worktrees under `~/foreman-worktrees/` (override with `FOREMAN_WORKTREE_ROOT`), and a backend health table under `~/.local/state/foreman/` (override with `FOREMAN_STATE_DIR`).
- **Reads** `~/.handoff/` — the dispatcher's own task directory — to locate what a worker delivered.
- **Probes backends before dispatch** (`backend-health.sh`, all probes listed in its header): `claude auth status` and `cursor-agent status` read local login state only; the `deepseek` probe sends `$DEEPSEEK_API_KEY` to DeepSeek's own balance endpoint; the `codex` probe makes one minimal request. Probes you define yourself with `FOREMAN_PROBE_<NAME>` run as you wrote them.
- **`foreman-cworker.sh` starts a Docker container, passes `$DEEPSEEK_API_KEY` into it** as that worker's own API credential, and runs the worker with `--dangerously-skip-permissions` — inside the container only. That is the entire point of the caged worker: it receives one key and one mounted worktree, and nothing else — not your home directory, not your other repos, not your primary agent login. The key is read from your environment at call time, is never stored by this skill, is visible only to processes inside the cage, and is gone when that container exits. **The container's network is not restricted**, so anything running inside it could reach other hosts with that key: use a dedicated key with a low spending limit. The script refuses to start unless the mount is a git-registered task worktree under `FOREMAN_WORKTREE_ROOT` and the image is pinned by an immutable id (`FOREMAN_WORKER_IMAGE`), and it runs the container with all capabilities dropped, `no-new-privileges`, and a read-only root filesystem.
- **Runs the verification commands you wrote** in each work order. This skill never invents commands; what you put in a work order is what runs.

## Entry decision (settle this first, then read the matching chapter)

- **Step 0 — is the foreman on a strong enough model?** The foreman is the judge: it writes work orders, runs the intake checks, decides on rework, and merges. If the current session is on a small or fast tier, tell the user to switch to their strongest general model before continuing. Don't push genuinely hard reasoning out to workers either — that kind of task shouldn't be farmed out at all.
- **Default (there is work to farm out)**: read `dispatch.md` in this directory and run the dispatch chapter. Once every delivery has passed intake, **automatically** read `verify.md` and enter the acceptance chapter — do not wait to be asked again.
- **User says "just dispatch, skip acceptance for now"**: run `dispatch.md` only and stop at intake.
- **`/foreman verify`, or acceptance only** (including code somebody else handed you): read `verify.md` directly.

## Global invariants (both chapters, ahead of any playbook)

1. **Probe before dispatch.** `backend-health.sh pick` chooses a usable backend; if the whole pool is down, stop dispatching and report — never force it. Infrastructure failures (`auth` / `quota` / `config` / `net`) **do not count as rework rounds**: they say nothing about the quality of the work, and mixing them into the rework count misreads "the channel is down" as "the builder can't do the job".
2. **State goes to disk.** Always under `.foreman/` — one `<task_id>.json` per task, one `batch.json` per batch. First action on every entry into foreman: scan `.foreman/` for overdue and unsettled tasks and reconcile them before starting anything new.
3. **One shared escalation budget.** The same `error_fingerprint` showing up a second time → escalate immediately. Dispatch reworks plus acceptance repairs reaching **4 rounds combined** → circuit-break and report to the user.
4. **The measuring instruments are protected.** If a builder's diff touches tests, assertions, or CI config → reject the delivery. No exceptions. This is the only mechanism in the entire scheme that prevents a *consistent* false green: a builder that can edit the ruler can always make the work measure up.
5. **Judge on data, not exit codes.** Acceptance tooling routinely exits 0 no matter what it found. Read only the manifest/findings that *this* run newly generated.
6. **The main session only judges and merges.** Executable work gets farmed out to a separate process, picked from the **worker pool** (`dispatch.md` §3). Prefer backends paid for by a subscription you already have, **chosen by which one still has quota, not by which IDE the foreman happens to run in**; when one is exhausted or its login fails, move down the pool, and end on a pay-as-you-go backend that doesn't run out. Farming out buys two things: an isolated context, and a builder that can't reach the ruler.
