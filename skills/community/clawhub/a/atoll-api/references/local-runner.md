# Local runner

Read this reference before installing, diagnosing, configuring, or operating `atoll-runner`, its repository bindings, loopback UI, leases, or recovery behavior.

## End-to-end setup

The released runner does not require an Atoll source checkout. It is the
`atoll-runner` binary in `@atollhq/cli`; the machine needs Node.js, Git, a local
checkout of each repository that will receive work, and an authenticated Codex
runtime. On macOS, first confirm that `git --version` succeeds. Apple Git can be
blocked until the operator reviews and accepts the Xcode Command Line Tools
license; do not accept legal terms or enter an administrator password for them.

Install or update the released CLI, then verify that both binaries exist:

```bash
npm install -g @atollhq/cli@latest
atoll --version
atoll-runner --help
```

Create one named Atoll profile per agent identity and organization. Obtain the
agent key from the human operator; never print it, put it in shell history on
their behalf, or copy it into runner configuration. The interactive flow is
preferred when a terminal is available:

```bash
atoll auth setup
atoll auth profiles --json
```

For each profile, discover the project's verified repository mapping and keep
its opaque `repo_ref`. Do not invent a reference or treat a local path as
authorization:

```bash
atoll --profile agent-a repository list --project project-slug --json
atoll-runner --profile agent-a repositories bind repo-ref /absolute/path/to/checkout --issue issue-uuid
atoll-runner --profile agent-a repositories validate repo-ref
```

The issue is authorization evidence for its project; binding does not execute
that issue. The checkout must be a non-bare Git repository whose credential-free
`origin` matches the authorized GitHub repository. The runner uses the checkout
as a verified source and creates isolated worktrees under its private local
state. It does not work directly in the primary checkout, and the released CLI
does not accept a custom worktree root or per-issue working directory.

Before the first start, the authenticated agent has no hosted runner row to
pause. The operator must first remove every eligible assignment from that agent,
or use a dedicated setup agent with no assignments. Do not infer safety from a
quick issue read when another process can assign work concurrently. With this
no-work precondition established, run one bounded real cycle to initialize local
state and register the hosted row:

```bash
atoll-runner --profile agent-a run --once
```

This is not a model test. It is safe only because the agent has no eligible
assigned work. A binding command creates local identity but not runner state or
server presence; `doctor` will not fully pass yet, and `--dry-run` intentionally
does not perform registration. As soon as the runner appears, pause it in
**Workspace Settings → Runners → Manage → Pause new work** and verify that the
fleet row shows **Paused**. Keep it paused while running the read-only checks and
installing the optional macOS service:

```bash
atoll-runner --profile agent-a doctor
atoll-runner --profile agent-a run --once --dry-run
atoll-runner --profile agent-a service install --ui --ui-port 4735
atoll-runner --profile agent-a service status
atoll-runner --profile agent-a status
```

Expected readiness evidence is: `doctor` succeeds, every required repository
binding validates, Codex is authenticated, the service is installed and loaded,
the loopback UI returns HTTP 200 when enabled, and runner status reports Atoll
reachable with no unexpected current or retained job. A dry run is read-only;
after the hosted row is paused it should return no candidate with
`blocked_reason: intake_paused`.

Only after those checks pass should the operator resume **Workspace Settings →
Runners → Manage → Resume new work**. Read back both the hosted fleet row and
`atoll-runner --profile agent-a status`; the final state is `connected` with
active/accepting intake. Resuming can immediately claim eligible assigned work,
so do not use it as a setup probe.

One machine can store and run multiple named profiles, including profiles for
different organizations. Each runner process and macOS service is fixed to one
profile, and that profile supplies one agent identity and organization. Install
one service per profile, but enable the loopback dashboard on only one service:

```bash
atoll-runner --profile agent-a service install --ui --ui-port 4735
atoll-runner --profile agent-b service install
```

The dashboard lists machine-local process, presence, intake, and current-job
status for every configured runner profile. Detailed diagnostics and repository
actions remain scoped to the profile that hosts the dashboard. Additional
dashboards are optional and require different ports.

Do not run competing profiles for the same Atoll agent identity: the server
allows one current local runner installation per authenticated agent. A single
profile can bind several authorized repositories, each to its own absolute local
checkout. Work remains serialized to one current job per runner installation.

### Local runner presence

Authenticated agents can register and refresh one local runner installation with
`PUT /api/orgs/{id}/runners/self`, read it with `GET`, and disconnect it with
`DELETE`. The organization and agent member are derived from authentication, not
the request body. The strict body contains `instanceId`, optional `hostId`, `platform`, `arch`,
`capabilities`, `clientVersion`. Intake state is server-owned and is not accepted
from self refresh; human pause/resume uses the hosted fleet control endpoint.
Platform, architecture,
and capabilities use closed documented values; the server derives the display name.
Recent competing installations return `409`; an installation silent for 10
minutes can be replaced. Refresh is limited to 60 requests per agent per
minute. Responses expose only bounded operational metadata and computed
`presence_state` (`connected`, `stale`, or `offline`), never keys, prompts, or
local filesystem paths.

### Local runner leases

`POST /api/orgs/{id}/runner-leases/claim` atomically claims one assigned,
accessible, dependency-satisfied issue for the authenticated agent's current
runner. The body accepts `issueId` and `idempotencyKey`; `attention_resume`
first claims require an unread `attentionItemId`, `runnerHostId` (maximum 255 characters), `preservedThreadId`,
and `actionKind`. The response returns an ephemeral token; only its SHA-256
hash is stored. An untouched, unexpired, pre-intent `active` replay returns a
new token with `token_reissued: true` and invalidates the original token. During
overlapping recovery retries, the four newest prior recovery tokens remain valid for one minute or
until one is used, which promotes it. Other replays return `token: null`; terminal attention replays are acknowledgement-only, including after notification acknowledgement.
Only a proven pre-intent orphan can be replaced. Lease rows enforce the composite `(issue_id, org_id)` tenant fence. `PATCH /api/orgs/{id}/runner-leases/{leaseId}` accepts fenced
renew, progress, turn-milestone, terminal, reconciliation, and acknowledgement
transitions, including `model_completed`. Exact mutation retries are idempotent, and `uncertain_outcome`
blocks automatic replacement. Disconnected, stale, or replaced runners cannot
mutate or replay. A paused current runner may mutate or reconcile an already-held
lease but cannot acquire a new claim. These routes do not create candidates, schedules,
arbitrary commands, automation events, or action history.
Optional `progress` and `errorCode` metadata uses documented closed operational
codes; free-form values and sensitive runtime details are rejected.

### Verified workflow resume

GitHub workflow completion can resume a preserved Codex thread only when a
human owner or admin selects the explicit `resume` verification mode. The mode
is disabled by default and requires a current Codex runner for the configured
delivery agent. Atoll records one durable binding for the completed issue
lease: repository ID and name, PR number, exact head SHA, runner host, and
preserved thread. A `verification.completed` attention item is upgraded to
`resume_agent_thread` only when all of those values match the stored event and
binding. The runner sends the exact `verificationEventId` with its
`attention_resume` claim and revalidates the event, host, thread, repository,
and SHA before resuming.

Missing, ambiguous, stale, or mismatched server identity fails closed and
leaves the ordinary verification attention available for review. The runner
never creates a new thread as a fallback. A terminal replay returns
acknowledgement only and does not submit another Codex turn. A transactional
`RUNNER_LEASE_VERIFICATION_BINDING_MISMATCH` is a definite server claim
rejection: the local journal closes the attempt, the notification stays
unread, and the next heartbeat or supervisor pass can handle ordinary
verification review. A retained local worktree HEAD mismatch is a separate
`verification_worktree_sha_mismatch` failure; the runner marks the active lease
failed and leaves the unread attention for operator reconciliation.

## CLI runner

Builds that include the real headless runner provide a separate `atoll-runner`
binary. It uses an existing named Atoll profile. The server controls identity,
intake, assignment, repository authorization, and lease eligibility.

```bash
atoll-runner --profile agent-a doctor
atoll-runner --profile agent-a repositories list
atoll-runner --profile agent-a repositories bind repo-ref /path/to/checkout --issue issue-uuid
atoll-runner --profile agent-a repositories validate repo-ref
atoll-runner --profile agent-a status
atoll-runner --profile agent-a run --once --dry-run
atoll-runner --profile agent-a run
atoll-runner --profile agent-a run --ui
atoll-runner --profile agent-a ui
```

`run` uses the pinned Codex SDK and runtime `0.153.4`. Codex must be
authenticated. Each issue requires exactly one verified repository on its
project and a matching machine-local `repo_ref` binding. A local binding does
not grant server access. The runner checks the origin identity and exact base
commit, then creates an owned branch and worktree without changing the primary
checkout. Codex uses `workspace-write`, approval policy `never`, and disabled
sandbox network access. It does not use a global Codex executable as a fallback.

`--dry-run` performs a read-only dispatch check. Manage pause/resume in hosted
Atoll under Workspace Settings → Runners. Local intake is read-only; legacy
`pause` and `resume` commands return `RUNNER_INTAKE_HOSTED_ONLY`. Pausing new
intake does not cancel a held lease. The runner keeps local thread/worktree evidence
and never submits a replacement turn after an uncertain post-intent outcome.
An attention resume requires the exact retained thread and validated ownership;
there is no fallback to a new thread. Terminal branches and worktrees remain
available for inspection and are not deleted automatically.

Each ordinary lease is associated with one canonical execution before model
work. The lease UUID is the local-runner execution `external_run_id`, and the
job journal stores one bounded management outbox before each canonical write.
After a resolved canonical human-attention item, the runner claims a new lease
only when execution, item, versions, installation, host, source lease, and
retained thread match. The continuation includes only canonical IDs and the
closed resolution outcome enum. It never copies human request text, summaries,
prompts, logs, paths, credentials, or tokens.

Use `atoll-runner --profile agent-a repositories remove repo-ref` to remove an
unused local binding. This does not remove the server repository mapping or
local Git checkout.

`run --ui` enables the optional setup and diagnostics page at
`http://127.0.0.1:4735`; `--ui-port` selects another local port. `ui --port 4735`
opens diagnostics without starting work, including for a stopped runner or
malformed local config. Select the existing credential profile with `--profile`
at process start. Credentials never enter browser forms or responses.
The page lists server-authorized repositories, local bindings, Codex health,
local jobs/worktrees, uncertainty, and bounded redacted logs. Bindings use the
same runner config writer and never grant server authorization. Bind/remove
are blocked while a current job exists. Refresh, config validation, and Codex
preflight are non-destructive; there is no model retry or cleanup button.
A UI port or asset failure does not stop headless execution. Do not proxy this
loopback interface to another host. Service installation remains separate.

### macOS service and lifecycle

Install an explicit user service only when unattended operation is required:

```bash
atoll-runner --profile agent-a service install
atoll-runner --profile agent-a service install --ui --ui-port 4735
atoll-runner --profile agent-a service status
atoll-runner --profile agent-a service uninstall
```

The service is macOS-only. Install writes an atomic user-owned `0600` plist
under `~/Library/LaunchAgents/` with canonical Node and runner entry paths,
the selected profile, `run`, and optional loopback UI arguments. It contains no
environment variables, API keys, Codex or lease tokens, shell command,
checkout path, or worktree path. Unknown or changed plists fail closed.
Package installation is passive and never installs or starts the service. Use
uninstall, package upgrade, `doctor`, then install for an upgrade. Uninstall
removes only the exact owned plist and leaves journals, tokens, logs, branches,
and worktrees. Status and uninstall validate the local plist and do not require
profile credentials; install remains authenticated.

SIGINT/SIGTERM closes the process-local intake gate immediately. The current
child drains for at most 30 seconds; TERM and then KILL after 10 seconds are
sent only when the journaled PID still has the same process-start identity. A
wall-clock event-loop gap above 30 seconds is a possible wake. The child is
stopped, durable lease state is reconciled, and intake reopens only after that
pass. A wake may release a worker only to finish an already durable result;
stop never releases a worker. No hosted pause request is sent. Existing-wire
response failures are bounded as `RUNNER_PROTOCOL_MISMATCH` and keep pending
mutation journals available for replay.

### Opt-in real local smoke

This developer harness is available only from an Atoll source checkout. It is
not included in the installed npm CLI. After deterministic checks, use a clean
loopback fixture profile with no current or conflicting retained job, and run
from `packages/cli`:

Loopback remains the normal default. Repository owners may also run one bounded
production validation turn from a clean Atoll source checkout. This mode requires
an exact canonical production origin, organization, project, authenticated agent,
issue, runner host and instance, and the live project repository mapping's opaque
`repo_ref` plus repository full name. The supplied `repo_ref` is checked against
live issue routing and must never be hard-coded. The smoke derives the canonical
source root from its own script, requires a clean source checkout, rebuilds the
candidate in the invocation, and records the source root, source `HEAD`, and
worker-entry SHA-256 in bounded mode-`0600` evidence. Exact production admission
performs zero presence `PUT`/upsert operations for either connected or
disconnected targets. Registration and refresh belong to separate operator setup
outside this invocation. The invocation reads the connected runner identity
before claim and rechecks it immediately before the claim; a disconnected target
fails closed. The runner does not explicitly select a model. The Codex runtime
and local Codex configuration supply model selection. `@openai/codex` and
`@openai/codex-sdk` are pinned to package/runtime version `0.153.4`; this
version is not a model name. Use the internal AH-2088 production smoke
runbook for the owner-only command and cleanup procedure.


```bash
cd packages/cli && bun run build
ATOLL_RUNNER_MANUAL_SMOKE=1 bun run runner:manual-smoke -- \
  --profile agent-a --issue issue-uuid --repository /path/to/checkout \
  --timeout-ms 300000 --evidence /absolute/path/evidence.json
```

The smoke runs one real Codex turn through the existing runner. It creates and
retains its owned local branch and worktree while preserving the primary
checkout, and writes bounded fixture issue, host, generation, branch/worktree,
base/head SHA, thread, terminal, and time evidence outside the checkout. A
timeout is always failure; retained journal state is authoritative. It never
pushes or deletes retained state, publishes, deploys, or installs a service.
Codex Desktop visibility is a separate operator observation; deterministic tests
use a fake SDK.
