---
name: openclaw-custom-build-validation
description: "Use when validating an OpenClaw PR, composing a custom build, or refreshing its upstream base. Manage local environments with OCM and use Crabbox for remote reproduction. Official release campaigns belong to openclaw-release-validation."
---

# OpenClaw Custom Build Validation

Produce an identifiable custom candidate, prove the requested behavior, and
leave the official installation intact unless adoption was explicitly requested.
This is an operator workflow, not an official OpenClaw release or acceptance vote.
Use one private worksheet throughout, starting from
[assets/validation-worksheet.md](assets/validation-worksheet.md). Maintain it
yourself; do not make the operator fill out an administrative form.

At an interactive run's start, follow
[references/skill-updates.md](references/skill-updates.md) for a read-only source
check. It cannot replace this skill or retarget the candidate mid-run.

## Requirements

Local validation requires OpenClaw Manager (`ocm`), Git, and the candidate's
build tools. Node.js runs the bundled helpers; authenticated GitHub CLI (`gh`)
is needed for source checks and approved comment publication. Remote proof
requires the `openclaw-crabbox` skill and an authorized provider. Resolve these
from the user's environment; the skill does not install them automatically.

## Resolve the candidate, not another release

Read the consumer repository's instructions, build scripts, current state, and
the user's selected PRs/commits. Ask only for consequential missing choices.
Record repository URLs and full immutable identities:

- baseline actually installed or previously tested, separately for app, CLI,
  Gateway, node, and relevant plugins;
- upstream base SHA, each PR head SHA and ordered local patch commit;
- final candidate SHA/tree, lockfile identity, and intended OS/architecture.

Distinguish testing a PR head from testing its integration on current main.
Do not silently replace one with the other or use GitHub's moving merge ref as
the recorded identity. Resolve a requested latest base once; keep that target
fixed until the operator asks to refresh or evidence requires a new candidate.
Verify Git remotes: `origin` may be the operator's fork, not upstream.

Use a run-owned clean checkout/worktree, preserving the user's dirty work.
Record local changes as a reviewable patch and tree identity; a dirty checkout
must not be described by HEAD alone. Stop on unresolved conflicts; do not skip
commits or drop fixes merely to get a build.

For patch stacks or a base refresh, read
[references/patch-refresh.md](references/patch-refresh.md) before composition.

Proceed when every requested component has a fixed source identity and every
patch has a disposition. Unresolved composition blocks building that candidate.

## Local environments belong to OCM

Always use OCM for local OpenClaw environment creation, state isolation, runtime
selection, service lifecycle, and environment inventory. Git worktrees isolate
source, not runtime state. Do not invent a parallel state copier, launch agent,
environment manager, or cleanup script.

Inspect the installed OCM version and command help. Resolve the selected source
and its service owner; a reachable host is not authenticated execution access.
Resolve an authentication failure at the access layer before attempting remote
service operations; preserve the candidate and report the missing access.

Use OCM's supported clone/adopt flow with a distinct environment and port.
Verify resolved writable paths for state, includes, workspaces, plugins, and
symlink targets remain inside the fixture before candidate execution. Capture
stderr as well as JSON. An escape warning blocks activation even on exit code 0.
If OCM is absent or cannot support the host/isolation, report that gap and use
the supported setup within the authorized task, or request a relevant Crabbox
target. Never substitute manual home copying or call WSL proof native Windows.

Isolation of files is not isolation from external services. Inspect copied
channel, cron, webhook, telemetry, and provider behavior without printing secrets.
Keep copied external activity inactive until its use is authorized. Never run
two consumers of the same live channel credentials. Stopping a personal source
requires that scope to be authorized, with its prior running state recorded for
restoration and verification.

OCM is not an OS security sandbox for untrusted PR code or lifecycle scripts.
Do not expose personal state or host credentials to untrusted code merely
because it has an OCM environment. Use secretless isolated reproduction first.

Proceed when OCM identifies the fixture, containment is proven, and copied
external activity has a safe, authorized owner.

## Build the actual deliverables

Determine whether the request includes CLI, Gateway, native app, node, plugins,
or a subset. Use the exact checkout's official scripts, package-manager version,
lockfile, and documented dependencies. Normal lifecycle scripts belong to an
authorized build; do not blanket-disable them and then chase missing components.
Check official sources and relevant advisories; investigate concrete warnings.

Read a build script before invoking it: build, signing, installation, relaunch,
and service replacement may be combined. Use a documented build-only/output
mode for validation. If no safe mode exists, move the build to a suitable
Crabbox target or stop with the exact limitation. Do not run a restart/sign
script against the personal installation as a build-only shortcut.

OCM runtime verification proves that runtime, not the native app. Capture
separate artifact paths, hashes, embedded version/commit, architecture, and
signature status where applicable. A version string alone is not source proof.
Keep custom candidates visibly distinguishable through supported metadata or
artifact naming; never fabricate a release version, official signature, updater
feed, or beta status. Preserve the vanilla app as the user's working base.

Use official OCM runtime build/verify and upgrade-preview operations supported
by the installed version. Verify their actual semantics before execution; do
not assume an old example or inferred flag exists. Select only the candidate's
runtime for the fixture. For Gateway-dependent deliverables, check live health
plus a task-relevant CLI/API request, plugin inventory and required tools. For
CLI-only work, exercise the requested command; Gateway readiness is required
only when that command depends on it. A process PID, loaded service, HTTP shell,
or green build alone is not readiness.

## Prove behavior, locally and remotely

Offer optional diagnostics after fixture readiness; when requested or needed to
investigate a concrete failure, read
[references/diagnostics.md](references/diagnostics.md). An unavailable optional
collector does not block unrelated validation.

Write the failure and expected observable result before testing. Automate
deterministic tests and supported CLI/API paths. Let the human judge interactive
UX unless they ask for automation; keep human and automated evidence separate.
Do not gate useful automated proof on a mandatory manual campaign ritual.

For a bug fix, reproduce on the relevant baseline and test the same path on the
candidate. If baseline reproduction is unavailable, say so; green candidate
tests alone do not establish causation. For stateful bugs, include persistence
and restart/reconnect behavior when these are in scope.
For pending-completion recovery or duplicate delivery across Gateway restarts,
read [references/stateful-restart.md](references/stateful-restart.md) before
choosing the reproduction. Record its checkpoints in the existing worksheet.

Use Crabbox whenever clean-machine, remote, platform-specific, packaging,
credential-free, or independent reproduction meaningfully improves the proof.
Read the available `openclaw-crabbox` skill before using it. Preserve its resolved
provider and source-trust rules; do not select a more expensive provider silently.
Record why remote proof is needed, provider, lease/run identity, exact tested
revision, platform, command, result, and cleanup. Verify revision after sync.
When Crabbox is unavailable, report remote proof as unavailable, not passed.
Local OCM tests may continue if safe, but cannot close a required remote proof.

Use an appropriate native platform for app/service/desktop claims. Linux tests
do not prove macOS launchd/WebKit or Windows desktop integration. A remote
desktop appearing does not prove the candidate app is running. Use only approved
test data/credentials; never upload the personal Gateway home as a reproduction.

## Triage without restarting the whole exercise

Classify failures as candidate regression, pre-existing baseline problem,
OCM/tooling, build environment, access/provider, or unknown. Preserve recovered
failures and their remedies. Do not call an unknown failure an upstream bug.
Search relevant open and closed issues/PRs when a real finding exists, and inspect
the proposed fix. A closed issue or merged PR is not proof the behavior is fixed
in this candidate. Keep separate destinations for OCM, Crabbox and OpenClaw bugs.

After a failure, retry only with changed evidence or a targeted diagnostic.
Preserve the target SHA. Do not repeatedly upgrade/rebase or ask for identical
doctor/start commands. If you stop a service as part of an approved repair,
restore its intended state and verify it before reporting recovery.

Use exact evidence labels: source inspected, automated test passed, fixture
runtime passed, human confirmed, or unavailable. Never convert one into another.
Summarize candidate outcome as passed, failed, blocked, or not evaluated, and
report cleanup and promotion separately. An unresolved required test means
blocked, not passed. Passing applies only to named tested surfaces.

## Closeout

Validation leaves the personal installation unchanged. If the operator requests
adoption, read [references/adoption.md](references/adoption.md) before preparing
or executing that separate operation.

Restore any authorized source service changed by validation and verify it.
Stop task-owned remote leases. For removal, inventory exact owned environments,
runtimes and artifacts; check shared references. Use native management and
recoverable deletion consistent with the operator's cleanup authorization.
If a native removal is irreversible and not explicitly approved, retain it and
ask rather than recursively deleting directories. Report retained disk usage
when measured, never guessed.

End with the tested identity, results, unresolved findings, artifact locations,
personal-installation state, and next decision. Keep one worksheet as the ledger
and link evidence. At closeout, read
[references/reporting.md](references/reporting.md): derive the structured result
and a sanitized Markdown comment from that worksheet. Publish only approved
comments to selected PRs/issues through the native GitHub client. Custom results
remain separate from the official release campaign.

## Provenance

Workflow adapted from the inspected `openclaw-release-validation` skill and
`openclaw-crabbox`, with operator-requested custom-candidate semantics. This is
new operator-authored guidance, not an upstream mirror or replacement. The
release skill remains responsible for official release campaigns. This variant
adapts its optional local diagnostics, source-check and structured-comment
patterns; it uses a distinct report contract and public TheAngrySkills source, without
inheriting campaign dispatch, voting, or outdated telemetry package pins.
