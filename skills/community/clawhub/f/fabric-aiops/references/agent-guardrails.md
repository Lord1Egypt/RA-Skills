# Agent guardrails — running fabric-aiops with a smaller / local model

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

- **The account you connect with.** Give it a Meraki API key whose admin has
  read-only organization access (or the read-only equivalent on your
  controller). A write then fails at the controller, which is the only place the
  permission actually lives — no skill-side flag can be argued around by a model,
  but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every call is audited to `~/.fabric-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | A field the controller did not return comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | Anything with a `limit` returns `{"<items>": [...], "returned": N, "limit": L, "truncated": true/false}`, where `<items>` names what was listed — `devices`, `alerts`, `topApplications`, `worst`, `driftedNetworks` or `undos`; on ACI, `endpoints`, `faults`, `contracts` or `entries`. Read the key the tool documents rather than assuming `devices`. Truncation is measured against the full result, not guessed from a length coincidence. |
| "Preserve the ordering / tell me what's most urgent" | The ranked analyses return worst-first and carry the numbers that produced each ranking (`avgLossPct`, `score`, `alertPenalty`), so priority is in the payload rather than implied by list position. The ACI reads carry an explicit `rank` on findings and on `aci_faults_list` rows; related-fault candidates are sorted active-first but unranked. |
| "Confirm before anything destructive" | Destructive operations require a `--dry-run`-able preview + double confirmation at the CLI. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. |
| "Don't guess at an unsupported platform" | An operation a platform does not map raises a teaching `PlatformUnsupported` error naming the platform — never a silent no-op the model can mistake for success. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a network fabric through its CONTROLLER API using the fabric-aiops
MCP tools (Cisco Meraki Dashboard, Cisco Catalyst Center, Arista CloudVision
Portal, UniFi Network, or Cisco ACI, depending on the configured target).

TOOL USE
- Before answering any question about the current fabric, you MUST call a tool.
  Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.
- If a tool returns "not supported on <platform> yet", say so. Do not substitute
  a different tool and present its output as the answer to the original question.

READING RESULTS
- Read the whole result before concluding. If a result has "truncated": true,
  say so and re-run with a higher limit instead of treating the partial result
  as complete.
- A null field means the controller did not return that value. Report it as
  "not available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  status strings, severities, model names, or identifiers.
- In the ranked analyses, work worst-first and cite the measured number
  (avgLossPct, avgLatencyMs, score, alertPenalty) behind each ranking.

IDENTIFIERS — keep these straight, they are not interchangeable
- An ORGANIZATION id scopes the whole account (on Catalyst Center, CVP, and
  UniFi a site/container stands in for it).
- A NETWORK id names one site/branch inside an organization.
- A DEVICE SERIAL names one physical device. It is not a device name, not a MAC,
  and not a network id.
- An UPLINK names a WAN interface on one appliance (e.g. wan1/wan2), scoped to
  that device's serial — an uplink is never addressed on its own.
- Never pass an organization id where a network id is expected, or a device name
  where a serial is expected. If you do not have the right id, call the list
  tool that returns it (org_list, network_list, device_inventory) first.

CISCO ACI (aci_* tools)
- aci_endpoint_trace is NOT a reachability test. "staticPathResolved": true
  means the fabric is configured to carry the endpoint — never say traffic flows.
- relatedFaultCandidates are matched by DN only. Never present one as the cause
  of a problem; call them candidates. If its "faults" is null, no scan
  succeeded: say related faults are unknown, never "no faults".
- tagRelations in state "missing-target" are policy-tag lookups. They are not a
  path or attachment failure — do not report them as one.
- "recordedPathMatch": "vpc-member" is normal: APIC records a vPC-learned
  endpoint's fabricPathDn on one member leaf. It is not a move. Even
  "differs" only says two APIC records disagree — never claim the endpoint
  moved from that alone. null means it was not compared (no recorded path or
  no formed relation) — not that the paths agree.
- A section that is null with an entry in "errors" was NOT read. Say it could
  not be read; never describe it as empty or absent.
- A cleared fault keeps the description it had when raised. Judge it by
  severity and lifecycle, not by its text.
- Fault rows are records, not incidents: a "delegated": true row mirrors a
  fault on another object. Do not count the pair as two problems.
- "notFound" means the fabric has not learned the address now, or it sits in a
  tenant this account cannot see — not that the host is down.
- Anything listed in "notChecked" (vzAny, taboo, imported contracts, preferred
  groups, service graphs) was not evaluated; do not claim it allows or blocks
  traffic.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a connectivity, capacity, or availability problem unless a tool
  result supports it.
- Do not add generic advice that does not follow from the tool output.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup — the fleet-affecting operations here
(`reboot_device`, `remove_device_from_network`, `bind_network_to_template`) hit
production hardware and live networks:

```bash
# e.g. use a Meraki API key whose admin has read-only organization access. Then:
fabric-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export FABRIC_AUDIT_APPROVED_BY="your.name@example.com"
export FABRIC_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `overview` and the three
  flagship analyses (`uplink_loss_and_latency_rca`, `network_health_score`,
  `config_template_drift`) — they do the multi-step correlation inside one call,
  so the model does not have to chain reads and keep org/network/serial ids
  straight across turns.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `--limit` deliberately rather than pulling a whole org
  inventory in one go.
- **The model confuses sites with networks on Catalyst Center / CVP / UniFi.**
  On those platforms a site or container stands in for both the organization and
  the network level. Tell the model which one your target is scoped to.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Fabric-AIops](https://github.com/AIops-tools/Fabric-AIops/issues)
with the model, runtime, and what went wrong.
