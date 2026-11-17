# Agent guardrails — running ceph-aiops with a smaller / local model

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

- **The account you connect with.** Give it a ceph-mgr Dashboard account with a
  read-only role. A write then fails at the mgr, which is the only place the
  permission actually lives — no skill-side flag can be argued around by a
  model, but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.ceph-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | A field the Dashboard did not return comes back as `null`, never as `""`. A missing `deviceClass`, `host`, MDS `state`, or `pg_autoscale_mode` is distinguishable from an empty one in the payload. |
| "Tell me if the output was cut off" | `pg_dump_stuck` returns `{"stuck": [...], "returned": N, "limit": L, "truncated": true/false}` and `pg_summary` the same shape under `unhealthy` (plus `states`) — the list key differs, so look it up per tool rather than expecting `stuck` everywhere. Truncation is measured (one extra row is collected), not guessed. `pg_summary` also keeps `unhealthyCount` as the true total even when the list is capped. |
| "Explain what HEALTH_WARN means" | `cluster_health` already folds each active check code (`PG_DEGRADED`, `OSD_NEARFULL`, `SLOW_OPS`, `LARGE_OMAP_OBJECTS`, …) into a plain-language `cause` and `suggestedAction`. The model should quote those, not compose its own. |
| "Confirm before anything destructive" | Every destructive tool (`osd_purge`, `osd_mark_out`, `pool_delete`, `rbd_image_delete`, `rbd_snapshot_delete`, `set_pool_size`) takes `dry_run=True` for a preview and is `risk=high`, tagged `review` on its audit row. ⚠️ **The double confirmation is a CLI feature, and only `osd_purge` and `osd_mark_out` have CLI commands** — the other four are reachable only over MCP, where nothing prompts. Keep your own confirmation for those. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Ceph cluster through the ceph-aiops MCP tools, which talk to the
ceph-mgr Dashboard REST API.

TOOL USE
- Before answering any question about the current cluster, you MUST call a tool.
  Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer. A read that fails returns an "error" field rather
  than raising — treat that as "unknown", not as "healthy".

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the Dashboard did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  status strings (HEALTH_WARN, active+undersized+degraded), PG ids, or OSD ids.
- When cluster_health returns findings, quote each finding's "cause" and
  "suggestedAction" rather than composing your own explanation of the check code.

- `pool_delete`, `rbd_image_delete`, `rbd_snapshot_delete` and `set_pool_size` have no CLI
  command, so nothing will ask you to confirm them. Call them with `dry_run=True` first,
  show the operator what would change, and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, performance, or data-loss problem unless a tool
  result supports it. HEALTH_WARN is not automatically an emergency —
  PG_NOT_DEEP_SCRUBBED on a small cluster is routine.
- Do not confuse the identifier kinds: an OSD id is a number (3), a PG id is
  pool.hex ("2.1a"), a pool name is a string, and an RBD image is addressed as
  pool/name. Never pass one where another is expected.
- capacity_forecast is arithmetic extrapolation from a growth rate you supply.
  With no growth rate it reports "insufficient-data" — do not present that as a
  prediction.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — the destructive operations on a Ceph
cluster are unusually cheap to invoke and unusually expensive to undo
(`pool_delete` and `rbd_image_delete` destroy data no undo token can bring back):

```bash
# e.g. use a ceph-mgr Dashboard account with a read-only role. Then:
ceph-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export CEPH_AUDIT_APPROVED_BY="your.name@example.com"
export CEPH_AUDIT_RATIONALE="draining osd.7 for disk replacement 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `cluster_health` and
  `fleet_overview` — they do the multi-step correlation inside one call, so the
  model does not have to chain reads and keep OSD/PG ids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `limit` deliberately rather than dumping every PG in the
  cluster; `pg_summary`'s histogram is usually the right level of detail.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Ceph-AIops](https://github.com/AIops-tools/Ceph-AIops/issues)
with the model, runtime, and what went wrong.
