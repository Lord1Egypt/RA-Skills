# Agent guardrails — running endpoint-aiops with a smaller / local model

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

- **The account you connect with.** Give it a management-console account or API
  token scoped to a read-only role. A write then fails at the server, which is
  the only place the permission actually lives — no skill-side flag can be
  argued around by a model, but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.endpoint-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | A field the management server did not return comes back as `null`, never as `""`. An endpoint with no reported `patchLevel` is distinguishable from one reporting a blank level, and the key is always present. |
| "Tell me if the output was cut off" | Every capped list is `{"items": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is measured against the full result, not guessed from the row count matching the limit. |
| "Give me the real totals, not just what you can see" | Counts are computed over the whole fleet, never over the capped list: `driftedCount`, `behindCount`, `nonCompliantCount`, `stormCount`, and the health-score `summary` are all uncapped. `complianceRatePct` is likewise a whole-fleet figure. |
| "Explain why something was flagged" | Every flag carries its number: each health-score deduction is cited in that endpoint's `reasons`, each drift row states `expected` vs `actual`, and `login_storm_analysis` returns the `thresholds` it used. |
| "Confirm before anything destructive" | `endpoint assign-profile` and `endpoint reboot` require `--dry-run`-able preview + double confirmation at the CLI. |
| "Remember the previous profile so we can roll back" | `endpoint_assign_profile` reads the endpoint's current profile *before* changing it and records an inverse undo token — the before-state is captured, never guessed. (A reboot has no safe inverse and honestly declares none.) |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a managed-endpoint fleet (thin clients / VDI / managed devices)
through the endpoint-aiops MCP tools.

TOOL USE
- Before answering any question about the current fleet, you MUST call a tool.
  Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. A list arrives as
  {"items": [...], "returned": N, "limit": L, "truncated": bool}; when
  "truncated" is true, say so and re-run with a higher limit instead of
  treating the partial list as the whole fleet.
- Use the uncapped counts (driftedCount, behindCount, nonCompliantCount,
  stormCount, summary) for "how many", and the items list only for "which ones".
- A null field means the management server did not report that value. Report it
  as "not available" — never infer a patch level, agent version, or hostname.
- Report values exactly as returned. Do not normalise, translate, or prettify
  patch levels, agent versions, profile ids, or hostnames.
- A health score is advisory: it is 100 minus the deductions listed in that
  endpoint's "reasons". Quote the reasons rather than restating the score alone.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a login-storm, drift, or patch-compliance problem unless a tool
  result supports it — a storm is only a storm when an episode was returned.
- A drift finding is an exact string mismatch against a baseline, and that
  baseline may be the fleet majority rather than a declared gold image. Say
  which (the payload tells you: baselineSource / targetSource).
- Do not confuse an endpoint id with a hostname, or a profile id with either.
- Do not add generic advice that does not follow from the tool output.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — a mistaken `endpoint_reboot` across a
fleet is cheap to invoke and has no safe inverse:

```bash
# e.g. use a management-console account or API token with a read-only role. Then:
endpoint-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export ENDPOINT_AUDIT_APPROVED_BY="your.name@example.com"
export ENDPOINT_AUDIT_RATIONALE="scheduled patch window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the analysis tools —
  `overview`, `login_storm_analysis`, `drift_report`, `endpoint_health_score`
  each do the multi-step correlation inside one call, so the model does not have
  to chain reads and keep endpoint ids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `--limit` deliberately rather than pulling a whole fleet
  inventory into the context window.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Endpoint-AIops](https://github.com/AIops-tools/Endpoint-AIops/issues)
with the model, runtime, and what went wrong.
