# Agent guardrails — running ai-guardian with a smaller / local model

There is a pleasing recursion here: ai-guardian governs local LLMs, and this page
is about driving ai-guardian *with* one. The same weaknesses this tool exists to
observe — a model that answers confidently without checking, that cannot tell
"unknown" from "none", that reports a truncated view as complete — are the ones
you will hit while operating it.

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

- **The host and account you run under.** Point the tool at a runtime the account
  cannot administer — an Ollama daemon whose model store the user can't modify —
  so a `remove_model` or `pull_model` fails at the runtime, the only place the
  permission actually lives. A revoked permission cannot be argued around by a
  model; a skill-side flag can.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`), or hand
  it only the scan/observe tools.

Content governance is different, and it stays: `guarded_generate` still scans and
gates each prompt against the allow/deny model policy and the block threshold
before the model runs. That is a product control over *what a model is asked to
do*, not an authorization gate over *which tools an agent may call*.

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.ai-guardian/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. Observed local-LLM usage lives in a separate `~/.ai-guardian/usage.db`. |
| "Don't invent a digest / version / license" | A field the runtime cannot report comes back as `null`, never as `""`. This is load-bearing: Ollama and llama.cpp expose a pinnable identity, while LM Studio and vLLM expose only a model id. |
| "Don't call it tampering when you just can't tell" | `model_provenance` reports a pinned model with no obtainable digest as `unverifiable`, never as `DRIFT`. Only a digest that is present **and** different is drift. |
| "Tell me if the output was cut off" | `usage_events` returns `{"events": [...], "count": N, "returned": N, "limit": L, "truncated": true/false}`. Truncation is measured (one extra row is fetched), not guessed. An under-reported usage log otherwise looks exactly like an absence of risky prompts. |
| "Never log the prompt text itself" | The route-through path stores only the prompt's length, its risk band, and the redacted findings. The raw prompt is never written to the usage log. |
| "Redact secrets before showing me" | The scanner's findings are already redacted; matched secrets and PII are reported by type and location, not by value. |
| "Confirm before anything destructive" | `remove_model` is high-risk, requires a `--dry-run`-able preview + double confirmation at the CLI, and captures the model manifest for an undo (re-pull). |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate ai-guardian, which observes and governs local LLM runtimes (Ollama,
llama.cpp, LM Studio, vLLM) on this machine.

TOOL USE
- Before answering any question about which models are installed, running,
  sanctioned, or what has been observed, you MUST call a tool. Never answer from
  memory — you are not a reliable witness to the machine you are running on.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. An unreachable runtime
  means unknown state, not "no models installed".

REPORTING WHAT CAN AND CANNOT BE KNOWN
- A null digest means the runtime cannot identify the weights. Report that as
  "unverifiable" — never as clean, and never as drift.
- A null version or license means the API does not expose it, not that the model
  has none.
- If usage_events returns truncated: true, say so. Never conclude "no risky
  prompts were observed" from a truncated log.
- A shadow model is a model present but not sanctioned by policy. That is a
  policy finding, not evidence of malice. Report what the policy says, not what
  you infer about intent.
- scan_prompt results are heuristic. A "none" risk band means no pattern matched,
  which is not the same as "this prompt is safe". Say which one you mean.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not recommend removing a model on the basis of it being unsanctioned alone —
  surface it and let a human decide. remove_model deletes local weights.
- Do not confuse the identifier kinds: a model name (llama3:8b) carries a tag, a
  base name (llama3) does not, and a digest identifies the weights. A pinned
  digest belongs to an exact model name.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — `remove_model` deletes local model
weights, and re-pulling them is a large download rather than a quick undo:

```bash
# e.g. point ai-guardian at a runtime/account that can't administer the model
# store, or hand the agent only the scan/observe tools. Then:
ai-guardian doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export AI_GUARDIAN_AUDIT_APPROVED_BY="your.name@example.com"
export AI_GUARDIAN_AUDIT_RATIONALE="removing unsanctioned model per policy review"
```

Content governance is independent of all this: `guarded_generate` / `observe_chat`
scan each prompt, gate it against the allow/deny model policy and the block
threshold, record it to the usage log, and only then call the model. That is what
keeps secrets and jailbreaks out of a local model regardless of how read vs write
is controlled.

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **The model reports "no drift" for an unverifiable runtime.** Ask it to quote
  the `status` field per model rather than summarising; `unverifiable` and `ok`
  are visually similar in a rollup but mean opposite things about confidence.
- **Multi-tool workflows time out or drift.** Lead with `posture_overview` or
  `anomaly_report` — they fold inventory, policy verdicts, and usage stats into
  one call.
- **The model ignores later tool results in a long context.** Ask about one model
  at a time with `model_details` rather than dumping the whole inventory.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/AI-Guardian](https://github.com/AIops-tools/AI-Guardian/issues)
with the model, runtime, and what went wrong.
