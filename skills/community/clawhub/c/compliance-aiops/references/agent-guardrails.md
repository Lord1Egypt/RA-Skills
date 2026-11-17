# Agent guardrails — running compliance-aiops with a smaller / local model

compliance-aiops is a **meta-tool**: it reads the audit databases the other
AIops tools write, and turns them into framework-mapped evidence. That makes the
failure mode here different from an infrastructure tool. A wrong answer does not
break a cluster — it produces a **confident, false compliance claim**, which is
worse, because it looks like a finding.

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

## Authorization is not this tool's job — decide it where it belongs

Whether a bundle should be produced or signed is your decision, or the account's.
The tool does not gate it — there is no read-only switch and no approval prompt
to configure. The two right places to control it:

- **The account it runs as.** The tool only ever writes under
  `~/.compliance-aiops/`, and opens every source `audit.db` strictly read-only —
  so ordinary filesystem permissions bound what it can do. A write then fails at
  the OS, which is the only place the permission actually lives.
- **Your agent's system prompt.** If you want a query-only session, tell the
  model not to call the bundle-writing tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Never modify the audit trail" | The tool has no capability to write to any source `audit.db` — it opens them read-only. Nothing in the tool surface can alter the evidence it reports on. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |
| "Don't invent an approver or a reason" | A field the audit row did not record comes back as `null`, never as `""`. "No approver was recorded" and "the approver field was blank" stay distinguishable — which is exactly the distinction a change-approval finding turns on. |
| "Tell me if you only saw part of the trail" | Every report carries `scanLimit` and `scanTruncated`, and every capped list carries `returned` / `limit` / `truncated`. Truncation is measured — one row past the cap is fetched — never inferred from a count landing on a round number. With a `selector`, matching runs over the bounded report scan, and `truncated` is `null` when that scan hit its cap before filling the limit (more matches may exist). |
| "Check the evidence hasn't been tampered with" | `verify_source_chain` hash-chains a source's current events and reports row-id gaps; `verify_bundle` re-derives a sealed bundle's chain and reports the first broken link plus signature validity. You do not need to ask the model to reason about integrity — ask it to run the check. |
| "Be honest about what an audit log can prove" | Every control carries a `strength` and a `caveat`, and gap findings carry the design-vs-operating note. Coverage is only claimed where the trail actually contains the evidence. |
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.compliance-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate compliance-aiops, which reads the audit trails other AIops tools
produce and maps them to framework controls (HIPAA, PCI-DSS, SOC2, GDPR).

TOOL USE
- Before answering any question about compliance posture, coverage, or a
  specific control, you MUST call a tool. Never answer from memory, and never
  from your training knowledge of what a framework requires.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. An unreadable audit
  source means unknown coverage, not zero findings and not full coverage.

EVIDENCE INTEGRITY — the part that matters most here
- NEVER state or imply that an organisation "is compliant", "passes", or "is
  certified". This tool produces evidence about operations recorded in an audit
  trail. Certification is a judgement made by a qualified assessor over a much
  wider scope. Say what the evidence shows; never issue a verdict.
- If a result has scanTruncated or truncated set to true — or truncated set to
  null (completeness unknown) — the population you saw
  is a slice. Say so explicitly and do not compute or quote a coverage
  percentage, a total, or a "no violations found" statement from it.
- Quote counts and control ids exactly as returned. Never round, extrapolate,
  or fill a gap in the trail with an assumption about what probably happened.
- A null approver means no approver was recorded — report that as the finding
  it is. Do not soften it, and do not guess who approved.
- Report every control's caveat and strength alongside its coverage. A control
  marked PARTIAL is not covered; it is partly evidenced by operational logs and
  needs design/configuration evidence from a GRC system.
- An absence of evidence for a control means the trail contains nothing matching
  it. That is not proof the control failed, and not proof it passed. Say which
  one the data supports: neither.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- A hash chain is tamper-EVIDENT, not tamper-PROOF. An "intact" verdict means
  the records match a previously recorded head — it does not prove nothing was
  ever deleted before that head was taken. Row-id gaps are the signal for that,
  and they are reported separately.
- Do not confuse the source tools' identifiers with each other: a `source` is an
  AIops tool's audit database, a `skill` is the tool that logged the row, and a
  `tool` is the individual operation. They are three different columns.
```

## Recommended setup for a local model

Keep the agent query-only until you trust the setup — the tool already opens
every source trail read-only, and the only thing it can write is a bundle under
`~/.compliance-aiops/`:

```bash
compliance-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export COMPLIANCE_AUDIT_APPROVED_BY="your.name@example.com"
export COMPLIANCE_AUDIT_RATIONALE="Q3 SOC2 evidence collection"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **The model editorialises into a verdict.** This is the characteristic failure
  of smaller models on this tool. Ask for the numbers first ("what does
  coverage_summary return for soc2?") and only then for a summary, rather than
  asking "are we SOC2 compliant?" — the second phrasing invites a verdict the
  data cannot support.
- **Multi-tool workflows time out or drift.** Lead with `posture_overview` — it
  folds source availability and per-framework coverage into one call.
- **The model ignores later tool results in a long context.** Ask about one
  control at a time with `control_evidence` rather than pulling a whole
  framework's population.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Compliance-AIops](https://github.com/AIops-tools/Compliance-AIops/issues)
with the model, runtime, and what went wrong.
