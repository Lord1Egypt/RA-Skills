---
name: cicd-aiops
slug: cicd-aiops
displayName: "CICD AIops"
summary: "Governed self-managed GitLab + Gitea CI/CD ops: pipelines, runners, artifacts, RCA. 28 tools."
license: MIT
homepage: https://github.com/AIops-tools/CICD-AIops
tags: [aiops, mcp, governance, cicd]
description: >
  Use this skill whenever the user needs to operate a self-managed GitLab or self-hosted Gitea CI/CD server — a one-shot overview, server version and token identity, projects with storage statistics, pipelines/runs with jobs and trace tails, the runner fleet, merge/pull requests, branches, protection rules and releases, artifact inventories, four flagship RCAs (pipeline failures, runner health & queue, artifact/storage bloat, stale work), and governed writes (retry/cancel a pipeline, pause/resume a runner, delete artifacts, update branch protection).
  Always use this skill for "GitLab", "Gitea", "pipeline failed", "CI is red", "job trace", "runner offline", "jobs stuck in queue", "artifact storage full", "stale merge requests", "stale branches", "protect the default branch", "retry the pipeline", "cancel the pipeline", "delete old artifacts" when the context is a self-managed GitLab or Gitea instance.
  Do NOT use when the target is something other than a GitLab/Gitea CI/CD server (a hypervisor, storage appliance, backup product, database, network gear, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Do NOT use for Kubernetes deploy state — use k8s-aiops. GitLab.com / Gitea Cloud SaaS accounts are out of scope: this tool targets self-managed instances.
  Governed CI/CD operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers).
installer:
  kind: uv
  package: cicd-aiops
argument-hint: "[a project path, pipeline/runner id, or describe your CI/CD task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["cicd-aiops","uvx"]},"optional":{"env":["CICD_AIOPS_CONFIG","CICD_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/CICD-AIops","emoji":"🔁","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed CI/CD operations across self-managed GitLab (REST API v4 /api/v4/..., access token via PRIVATE-TOKEN header) and self-hosted Gitea (API v1 /api/v1/..., access token via "Authorization: token"). Each target in the config names its own platform, and a name-keyed platform registry selects the API shape, so the same tools work on both and one config can span a mixed estate; surfaces one platform lacks (e.g. runner administration on Gitea) raise a teaching error listing what is available. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.cicd-aiops/ (relocatable via CICD_AIOPS_HOME).
  Credentials: the GitLab personal/project access token or Gitea access token is stored ENCRYPTED in ~/.cicd-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'cicd-aiops init' to onboard (it asks for the platform and base URL), or 'cicd-aiops secret set <target>' to add one. The store is unlocked by a master password from CICD_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var CICD_<TARGET_NAME_UPPER>_SECRET is still honoured as a fallback with a deprecation warning (migrate with 'cicd-aiops secret migrate'). The token is presented as a PRIVATE-TOKEN header (GitLab) or an Authorization token header (Gitea) at request time and held only in memory; secrets are never logged or echoed.
  State-changing operations pass through the @governed_tool decorator (pre-check + budget guard + audit + risk-tier label). delete_artifacts is risk=high with dry_run + double confirmation and is irreversible (priorState records the destroyed count/bytes). Reversible writes (pause_runner/resume_runner as an undo pair; update_branch_protection replaying prior settings) capture the real fetched before-state and record an inverse undo descriptor; retry_pipeline/cancel_pipeline record priorState (the pipeline's prior status) only.
  Webhooks: none — no outbound network calls beyond the configured GitLab / Gitea REST API.
  SSL: verify_ssl defaults to ON; the init wizard asks before disabling it for self-signed lab certs.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: mock-validated; no recorded end-to-end run against a live server yet, and the modelled REST paths are the largest verification debt. Both GitLab CE and Gitea are free/self-hostable (each runs from a container), so a home lab is the cheapest live check. See docs/VERIFICATION.md.
---

# CICD AIops

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by GitLab Inc. or the Gitea project.** GitLab and Gitea are trademarks of their respective owners. Source at [github.com/AIops-tools/CICD-AIops](https://github.com/AIops-tools/CICD-AIops) under the MIT license.

Governed CI/CD operations — **28 MCP tools** across **self-managed GitLab** (REST
`/api/v4/...`) and **self-hosted Gitea** (API `/api/v1/...`), every one wrapped with
the bundled `@governed_tool` harness: a local unified audit log under
`~/.cicd-aiops/`, token/runaway budget guard, undo-token recording, and
descriptive risk tiers. A per-target `platform` field selects the API shape, so
the same tools work on both servers and one config can span a mixed estate. The
access token is stored **encrypted** (`~/.cicd-aiops/secrets.enc`, Fernet +
scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package
> (`cicd_aiops.governance`) — no external skill-family dependency. Both
> platforms are free/self-hostable, so a home lab is the cheapest live check;
> verification status and the checklist are in `docs/VERIFICATION.md`.

## What This Skill Does

| Group | Tools | Count | R/W |
|-------|-------|:-----:|:---:|
| **Server** | server_version, current_user, cicd_overview | 3 | read |
| **Projects** | list_projects, project_detail | 2 | read |
| **Pipelines** | list_pipelines, pipeline_detail, pipeline_jobs, job_trace_tail | 4 | read |
| **Runners** | list_runners, runner_detail | 2 | read |
| **Repo surface** | list_merge_requests, list_branches, list_protected_branches, list_releases | 4 | read |
| **Artifacts** | list_artifacts | 1 | read |
| **Flagship analyses** | pipeline_failure_rca, runner_health_rca, artifact_storage_bloat_analysis, stale_work_audit | 4 | read |
| **Writes** | retry_pipeline, cancel_pipeline, pause_runner, resume_runner, update_branch_protection | 5 | write (med) |
| **Writes** | delete_artifacts | 1 | write (**high**) |
| **Undo** | undo_list, undo_apply | 2 | read + replay |

The four flagship analyses are transparent heuristics that report their numbers,
never a black-box verdict: `pipeline_failure_rca` classifies each failed job from
its failure_reason + trace-tail markers (test-failure / dependency-network /
runner-timeout / oom / script-error) with matched evidence; `runner_health_rca`
flags offline/stale/paused runners, long-queued jobs, and per-tag saturation;
`artifact_storage_bloat_analysis` ranks projects by repo + artifact bytes and
estimates reclaimable bytes; `stale_work_audit` flags idle MRs/branches and
protection gaps.

## Quick Install

```bash
uv tool install cicd-aiops
cicd-aiops init       # wizard: pick platform (gitlab/gitea) + base URL + encrypted token
cicd-aiops doctor     # version endpoint + token-scope probe per target
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/cicd-aiops
openclaw skills info cicd-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a one-shot snapshot (`overview` / `server_version` / `current_user`)
- Answer "why is CI red?" (`rca pipelines` / `pipeline_failure_rca`) → cause +
  action per failed pipeline, with the trace evidence that drove the call
- Find wedged capacity (`rca runners` / `runner_health_rca`) → offline/stale
  runners, long-queued jobs, saturated tags
- Reclaim disk (`rca storage` / `artifact_storage_bloat_analysis`) → ranked
  projects + reclaimable bytes, feeding `delete_artifacts --dry-run`
- Repo hygiene (`rca stale` / `stale_work_audit`) → idle MRs/branches,
  unprotected default branch, force-push gaps
- Safely act: `retry_pipeline` / `cancel_pipeline`, `pause_runner` /
  `resume_runner` (undo pair), `update_branch_protection` (undo replays prior
  settings), `delete_artifacts` (risk=high, dry-run + double confirm)

**Do NOT use when** the target is not a GitLab/Gitea CI/CD server — route
hypervisor, storage, backup, database, network, or OT/industrial work to the
appropriate other AIops-tools skill.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Self-managed GitLab / Gitea CI/CD ops | **cicd-aiops** (this skill) |
| Kubernetes deploy state (what the cluster is actually running) | **k8s-aiops** |
| A non-CI/CD platform (hypervisor, storage, backup, database, network, OT edge) | the appropriate **other AIops-tools** skill |
| GitLab.com / Gitea Cloud SaaS accounts | out of scope for this tool |

## Common Workflows

Each recipe starts from one of the four RCAs and ends in a governed write.
Every CLI write accepts `--dry-run` and otherwise double-confirms. Note that
runner administration and pipeline retry/cancel are **GitLab-only** — on a
Gitea target those tools raise a teaching error listing what is available.

### 1. "The nightly pipeline has been red for three days"

1. `cicd-aiops pipelines list dev/api --status failed -n 20` → the recent
   failed pipelines, newest first.
2. `cicd-aiops rca pipelines dev/api` → each failed job classified from its
   `failure_reason` plus trace-tail markers: test-failure, dependency-network,
   runner-timeout, OOM, or script-error, with the evidence and a suggested
   action.
3. `cicd-aiops pipelines jobs dev/api <pipeline-id>` → which stage and job the
   classification came from.
4. `cicd-aiops pipelines trace dev/api <job-id> -n 120` → the actual log tail,
   so you confirm the classification instead of trusting it.
5. Fix the cause. If the RCA said the failure was transient (dependency-network
   or runner-timeout): `cicd-aiops pipelines retry dev/api <pipeline-id>
   --dry-run`, then re-run for real (double confirm).
6. `cicd-aiops rca pipelines dev/api` again to confirm the class of failure is
   gone rather than merely quieter.

**Failure branch**: if the RCA classifies the failures as **test-failure** or
**script-error**, do not retry — the code is broken and a retry burns runner
minutes to reach the same red. Retry is only honest for transient classes. If
the retry itself fails to submit on a Gitea target, that is the teaching error:
retry/cancel have no Gitea API v1 equivalent, so re-run the job from the Gitea
UI instead.

### 2. "Jobs are sitting in the queue and nothing is picking them up"

1. `cicd-aiops runners list --status offline` and `--status paused` → the
   obvious suspects first.
2. `cicd-aiops rca runners` → stale contact ages, long-queued jobs, and **which
   tag is saturated** (queued jobs versus online runners carrying that tag).
3. `cicd-aiops runners show <runner-id>` → the specific runner's tags, last
   contact and status.
4. If a needed runner was paused: `cicd-aiops runners resume <runner-id>
   --dry-run`, then for real (reversible — an inverse `pause_runner` is
   recorded).
5. If a wedged runner is grabbing jobs and failing them: `cicd-aiops runners
   pause <runner-id>` to take it out of rotation (reversible — inverse
   `resume_runner` recorded).
6. `cicd-aiops rca runners` again to confirm the queue is draining.

**Failure branch**: if the RCA shows a **saturated tag** rather than a
down runner, resuming runners will not help — no online runner carries the tag
those jobs require, so you need to add or retag capacity. And if you paused a
runner and the queue got worse, `cicd-aiops undo apply <id>` resumes exactly
the runner you paused. Runner administration is GitLab-only; a Gitea target
raises a teaching error here.

### 3. "The CI server is out of disk"

1. `cicd-aiops rca storage --old-days 30` → projects ranked by repo + artifact
   bytes with a reclaimable estimate at that age threshold.
2. `cicd-aiops artifacts list dev/api` → the actual artifact files, their sizes
   and their expiry, so you see what "reclaimable" really refers to.
3. `cicd-aiops projects --limit 50` → cross-check that the top consumer is the
   project you expect.
4. `cicd-aiops artifacts delete dev/api --older-than-days 30 --dry-run` →
   shows the scope, deletes nothing.
5. Re-run without `--dry-run`: double confirm, **high** risk. Optionally set
   `CICD_AUDIT_APPROVED_BY` + `CICD_AUDIT_RATIONALE` to annotate who/why on the
   audit row. This is **irreversible** — priorState records the destroyed count
   and bytes for the audit trail, but there is no undo.
6. `cicd-aiops rca storage` again to confirm the reclaimed bytes landed.

**Failure branch**: never run `artifacts delete` with `--older-than-days 0` as
a first move — 0 means **ALL** artifacts, including the ones a release or a
running deploy depends on. If the dry-run scope reads "ALL" and you did not
intend that, stop and set an age. Since there is no undo for this operation,
the dry-run is the only safety net you get; if the bloat is mostly **repo**
bytes rather than artifact bytes, deleting artifacts will not help at all.

### 4. "Tighten repo hygiene before the release freeze"

1. `cicd-aiops rca stale dev/api --mr-days 14 --branch-days 60` → stale open
   merge requests, idle branches, and **protection gaps** such as an
   unprotected default branch or force-push left allowed.
2. Confirm the current state via MCP `list_protected_branches` and
   `list_branches` for the project.
3. MCP `list_merge_requests` → the stale MRs the audit named, so you can close
   or revive them with their owners rather than in bulk.
4. Close the protection gap with MCP `update_branch_protection` (e.g.
   `allow_force_push=False` on the default branch) — it fetches and captures
   the prior settings and records an undo that replays them exactly.
5. `cicd-aiops undo list` → confirm the protection change is reversible.
6. `cicd-aiops rca stale dev/api` again to confirm the gap closed.

**Failure branch**: if tightening protection blocks a legitimate workflow — a
release automation that force-pushes tags, say — `cicd-aiops undo apply <id>`
restores the exact prior protection settings rather than a guessed default.
Fix the automation before re-applying, and do not disable protection
fleet-wide to unblock one job.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide
whether a write is permitted. That is your agent's judgement, or the permission
of the token you connect it with (a GitLab/Gitea access token without write
scope — writes then fail at the server). There is no read-only switch, policy
file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.cicd-aiops/audit.db` (relocatable via `CICD_AIOPS_HOME`): params, result, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `CICD_AUDIT_APPROVED_BY` / `CICD_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `CICD_RUNAWAY_MAX=0`.
- Destructive writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI. `delete_artifacts` is irreversible (priorState records the destroyed count/bytes; audit only).
- Reversible writes fetch the real before-state and record an inverse descriptor (pause_runner↔resume_runner, update_branch_protection→prior settings); irreversible ops (retry_pipeline, cancel_pipeline, delete_artifacts) record only the before-state.

## References

- `references/capabilities.md` — full tool + platform + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
- `references/agent-guardrails.md` — which guardrails the harness enforces, the
  GitLab-only vs Gitea platform asymmetry, and a ready-made system prompt for
  smaller / local models
