# cicd-aiops — capabilities reference

28 governed MCP tools over two platforms (16 reads + 4 analyses + 6 writes +
`undo_list`/`undo_apply`). Every tool takes an optional
`target` (a name from `~/.cicd-aiops/config.yaml`); writes also take
`dry_run: bool`.

## Platforms

| Platform | API | Auth | Project addressing |
|---|---|---|---|
| `gitlab` | REST v4 (`/api/v4/...`) | `PRIVATE-TOKEN: <token>` | numeric id or URL-encoded full path (`group%2Fproject`) |
| `gitea` | API v1 (`/api/v1/...`) | `Authorization: token <token>` | `owner/repo` (two path segments) |

Self-managed/self-hosted instances only. Where Gitea lacks a surface, the
platform registry raises a teaching `KeyError` naming the resources that ARE
available: runner administration, pipeline retry/cancel, and artifact deletion
are GitLab-only in v0.1.

## Reads (16)

| Tool | What it returns | GitLab path | Gitea path |
|---|---|---|---|
| `server_version` | version + revision | `/api/v4/version` | `/api/v1/version` |
| `current_user` | token identity (scope probe) | `/api/v4/user` | `/api/v1/user` |
| `cicd_overview` | version + identity + projects + runners | (composite) | (composite) |
| `list_projects` | projects w/ storage bytes | `/api/v4/projects?statistics=true` | `/api/v1/repos/search` |
| `project_detail` | one project incl. sizes | `/api/v4/projects/{p}` | `/api/v1/repos/{owner}/{repo}` |
| `list_pipelines` | recent pipelines/runs | `/api/v4/projects/{p}/pipelines` | **unsupported** — Gitea API v1 has no run-level resource |
| `pipeline_detail` | one pipeline/run | `.../pipelines/{id}` | **unsupported** (same reason) |
| `pipeline_jobs` | jobs + failure_reason | `.../pipelines/{id}/jobs` | **unsupported**; the per-job listing is `/actions/tasks` |
| `job_trace_tail` | last N log lines | `.../jobs/{id}/trace` | `.../actions/jobs/{id}/logs` |
| `list_runners` | fleet, offline first | `/api/v4/runners/all` | — teaching error |
| `runner_detail` | contacted_at, tags, paused | `/api/v4/runners/{id}` | — teaching error |
| `list_merge_requests` | MRs / PRs | `.../merge_requests` | `.../pulls` |
| `list_branches` | branches + last-commit date | `.../repository/branches` | `.../branches` |
| `list_protected_branches` | protection rules + force-push flags | `.../protected_branches` | `.../branch_protections` |
| `list_releases` | releases newest first | `.../releases` | `.../releases` |
| `list_artifacts` | files, sizes, expiry, expired-but-kept | via `.../jobs` artifacts | `.../actions/artifacts` |

## Flagship analyses (4, read-only, thresholds are parameters)

| Tool | Flags | Key thresholds |
|---|---|---|
| `pipeline_failure_rca` | each failed job classified: test-failure / dependency-network / runner-timeout / oom / script-error, with matched evidence + action | `limit` (pipelines), `tail_lines` |
| `runner_health_rca` | offline / stale / paused runners; long-queued jobs; saturated tags | `stale_contact_min` (30), `queue_sec` (300), `saturation_ratio` (2.0) |
| `artifact_storage_bloat_analysis` | projects ranked by repo+artifact bytes; expired-but-kept; reclaimable estimate | `old_artifact_days` (30) |
| `stale_work_audit` | idle open MRs; idle branches; unprotected default branch; force-push allowed | `stale_mr_days` (14), `stale_branch_days` (90) |

All four accept injected rows for pure/offline analysis, or pull live from a
target. Classification order in `pipeline_failure_rca` is most-specific first:
OOM > timeout > network > test > script; GitLab `failure_reason` values
(`stuck_or_timeout_failure`, `runner_system_failure`, …) classify without a
trace.

## Writes (6, governed, all with `dry_run`)

| Tool | Risk | Prior state captured | Undo |
|---|---|---|---|
| `retry_pipeline` | medium | pipeline status | none (a retry is a new run) |
| `cancel_pipeline` | medium | pipeline status | none (irreversible) |
| `pause_runner` | medium | runner `paused` flag | `resume_runner` (skipped if it was already paused) |
| `resume_runner` | medium | runner `paused` flag | `pause_runner` (skipped if it was not paused) |
| `delete_artifacts` | **high** | artifact count + bytes destroyed | none (irreversible) |
| `update_branch_protection` | medium | prior protection settings (or "unprotected") | replays this tool with the prior settings |

`delete_artifacts(older_than_days=N)` deletes per-job only artifacts created
before the cutoff; `0` uses GitLab's bulk-delete of eligible artifacts.

If the artifact inventory cannot be read, `delete_artifacts` does not run blind:
the per-job form stops (it cannot tell which jobs match), and the bulk form is
refused unless `acknowledge_unknown_inventory=True`
(`--acknowledge-unknown-inventory`), in which case the inventory is recorded as
unknown (`count`/`bytes` `null`, `inventoryError` set) — never as 0 files. The
dry-run preview refuses in exactly the same cases.

## Safety plumbing

- Every substituted URL path value is percent-encoded (`quote(..., safe="")`);
  Gitea's `owner/repo` keeps its `/` but each piece is encoded and empty /
  `.` / `..` pieces are rejected (path-traversal defense).
- All server-returned text passes an injection-safe normaliser (bounded string
  length, capped nesting depth) before an agent sees it.
- Non-2xx responses become teaching errors (what failed + what to check);
  plain-text trace endpoints pass through as text.
