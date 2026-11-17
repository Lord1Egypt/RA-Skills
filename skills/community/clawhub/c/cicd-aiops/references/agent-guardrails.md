# Agent guardrails — running cicd-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the account's. The tool does
not gate it — there is no read-only switch and no approval prompt to configure.
The two right places to control read vs write:

- **The token you connect with.** Give it a GitLab/Gitea access token without
  write scope. A write then fails at the server, which is the only place the
  permission actually lives — no skill-side flag can be argued around by a
  model, but a token without the scope cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.cicd-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | A field the server did not return comes back as `null`, never as `""`. A pipeline with no `ref`, a job with no `startedAt` or `failureReason`, a runner that has never reported `contactedAt` — all stay `null`, and the key is always present. |
| "Tell me if the output was cut off" | Every listing returns `{"<items>": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is **measured** (one extra row is fetched), never guessed from a full page. `job_trace_tail` adds `charsTruncated` for the byte ceiling. |
| "Tell me if a number is unknown rather than zero" | Storage numbers a platform does not report come back as `null` with `artifactsBytesKnown: false`, and `artifact_storage_bloat_analysis` counts them in `artifactBytesUnavailable`. `cicd_overview` reports `runnersSupported`. |
| "Confirm before anything destructive" | Destructive operations require a `--dry-run`-able preview + double confirmation at the CLI. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## Platform asymmetry — a teaching error is an ANSWER, not a failure

This is the one thing worth spending prompt budget on, because it is specific
to this tool. `cicd-aiops` speaks to **two different servers** — self-managed
GitLab (REST v4) and self-hosted Gitea (API v1) — and they do not expose the
same surfaces. Where a platform has no equivalent API, the resource is
deliberately **not mapped**, and the call raises a teaching error naming the
resources that *do* exist on that platform.

That error means "wrong platform for this question". It is a correct, final
answer. A model that treats it as a transient tool failure will retry the same
call, or report "the CI/CD server is unreachable" — both wrong.

**GitLab only** (a Gitea target raises the teaching error):

| Tool | Why |
|---|---|
| `list_runners`, `runner_detail` | Gitea API v1 has no runner-administration endpoint |
| `pause_runner`, `resume_runner` | same — no runner update endpoint |
| `retry_pipeline`, `cancel_pipeline` | Gitea Actions exposes no run retry/cancel endpoint |
| `delete_artifacts` | Gitea exposes no artifact-deletion endpoint (list only) |
| `runner_health_rca` **when it pulls live** | it pulls the runner fleet, so it inherits the above. Injecting `runners=[...]` makes it pure analysis and it works anywhere |

Everything else — `server_version`, `current_user`, `cicd_overview`,
`list_projects`, `project_detail`, `list_pipelines`, `pipeline_detail`,
`pipeline_jobs`, `job_trace_tail`, `list_artifacts`, `list_merge_requests`,
`list_branches`, `list_protected_branches`, `list_releases`,
`update_branch_protection`, and the other three flagship analyses — works on
both platforms.

Check `cicd_overview`'s `platform` field first if you do not know which server
you are pointed at. When a tool is GitLab-only and the target is Gitea, do not
retry: answer from the pipeline / job / repo surface instead, and say plainly
that this platform has no runner (or retry/cancel, or artifact-deletion) API.

### Worse than a teaching error: a surface that returns *nothing* instead of refusing

A teaching error is loud. These two are quiet, and they used to be
indistinguishable from a real measurement. They are now labelled in the
payload — **read the label, do not read the number alone**:

| Where | The quiet gap | The label to read |
|---|---|---|
| `cicd_overview` on Gitea | `runnersTotal` / `runnersOnline` are `null` because the platform has no runner API — **not** because there are no runners | `runnersSupported: false`. Never report "0 runners" from this. |
| `list_projects` / `project_detail` / `artifact_storage_bloat_analysis` on Gitea | Gitea reports a repo `size` but **no artifact or total-storage statistics**, so `artifactsBytes` and `storageBytes` are `null`. A storage RCA against a Gitea target ranks projects on repo bytes alone and finds **zero** reclaimable artifact bytes — which is a gap in the data, not a clean result | `artifactsBytesKnown: false` per project, `artifactBytesUnavailable: N` on the analysis |

One more bounded read worth naming: on GitLab, `list_artifacts` has no single
artifacts endpoint, so the inventory is assembled by walking recent jobs. When
`jobScanTruncated` is `true`, older jobs' artifacts are **not** in the result —
`totalBytes` is then a lower bound, and `delete_artifacts` says so too
(`priorState.complete: false`).

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate self-managed GitLab / Gitea CI/CD servers through the cicd-aiops
MCP tools.

TOOL USE
- Before answering any question about the current CI/CD environment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.
- Some tools exist only on GitLab (runner list/detail/pause/resume, pipeline
  retry/cancel, artifact deletion). On a Gitea target they return a teaching
  error listing what IS available. That is a final answer about the platform,
  not a transient failure: do not retry it, do not call it broken. Say the
  platform has no such API and answer from another surface.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete. On the analyses "truncated" is a per-list
  object — check each entry.
- A null field means the server did not return that value. Report it as "not
  available" — never infer it, and never report it as zero. In particular:
  runnersSupported=false means "this platform has no runner API", and
  artifactsBytesKnown=false means artifact storage was not measured.
- A job trace is only the TAIL of the log. When "truncated" is true the first
  error may be above the window — raise tail_lines before naming a root cause.
- Report values exactly as returned. Do not normalise, translate, or prettify
  status strings, branch names, or IDs.
- Work RCA findings in the order returned and cite the measured number each
  finding carries ("evidence", "cause", byte counts, queue seconds).

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, storage, or reliability problem unless a tool
  result supports it.
- Do not add generic CI/CD advice that does not follow from the tool output.
- Do not confuse a project path with a pipeline id, a pipeline id with a job
  id, or a runner id with either. Job ids come from pipeline_jobs; pipeline ids
  come from list_pipelines; runner ids come from list_runners.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the token's scope
only when you trust the setup — `delete_artifacts` is irreversible, and a
mistaken pipeline retry or cancel burns runner minutes:

```bash
# e.g. use a GitLab/Gitea access token without write scope. Then:
cicd-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export CICD_AUDIT_APPROVED_BY="your.name@example.com"
export CICD_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the four RCA tools
  (`pipeline_failure_rca`, `runner_health_rca`,
  `artifact_storage_bloat_analysis`, `stale_work_audit`) — each does the
  multi-step correlation inside one call, so the model does not have to chain
  `list_pipelines` → `pipeline_jobs` → `job_trace_tail` and keep three
  different id types straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `--limit` / `tail_lines` deliberately rather than pulling
  whole inventories or long traces.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/CICD-AIops](https://github.com/AIops-tools/CICD-AIops/issues)
with the model, runtime, and what went wrong.
