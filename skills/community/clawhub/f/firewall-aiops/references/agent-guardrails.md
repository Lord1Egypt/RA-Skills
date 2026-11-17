# Agent guardrails — running firewall-aiops with a smaller / local model

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

- **The account you connect with.** Give the OPNsense/pfSense API user a
  read-only role. A write then fails at the server, which is the only place the
  permission actually lives — no skill-side flag can be argued around by a model,
  but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool now enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Never restart the web GUI / lock yourself out" | **Already enforced.** `restart_service` refuses the daemon serving this appliance's own API (`nginx`, `lighttpd`, `configd`, `webgui`, ...), and `apply_changes` / `reconfigure` refuse a staged rule set that would provably cut management access. Both are exact and fail open — see `capabilities.md`. Do not spend prompt budget on it. |
| "Don't invent a value when a field is missing" | OPNsense and pfSense populate different keys for the same concept. A field neither platform returned comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | `firewall_log`, `states_table` and `top_talkers` all return `{"<items>": [...], "returned": N, "limit": L, "truncated": true/false}` — the list key is `entries`, `states` and `topTalkers` respectively. Truncation is measured, not guessed from a length coincidence. |
| "Make it show the number it judged on" | Gateway and blocked-source entries carry the numbers they were judged on — `lossPercent` and `rttMs` for a gateway (`lossPct`/`latencyMs` are the *thresholds* they were compared against, reported separately under `thresholds`), `hits`, `distinctPorts` and `topPort` for a blocked source — so those claims can be checked against a figure. `blocked_traffic_rca` orders `topSources` by `hits`, which is in the payload. Rule findings are qualitative: they carry `uuid`, `description`, `interface`, `shadowedBy`/`duplicateOf` and no count, because the hit counter they would be judged on is not always available — `hitCountersUnavailable` says whether it was. |
| "Confirm before anything destructive" | Every write takes `dry_run=True` for a preview that runs the same guards as the real call. ⚠️ **The double confirmation is a CLI feature, and only `toggle_rule` and `undo apply` have CLI commands** — `apply_changes`, `reconfigure`, `reboot`, `restart_service`, `kill_states`, `add_alias_entry` and `remove_alias_entry` are reachable only over MCP, where nothing prompts. Keep your own confirmation for those. |
| "Log what you did" | Every governed call is audited to `~/.firewall-aiops/audit.db` regardless of what the model says it did. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.

⚠️ **Only one of the three orderings can be checked from the output.** `blocked_traffic_rca`
sorts `topSources` by `hits`, and `hits` is returned — that order is verifiable.
`gateway_health_rca` sorts on an internal score that is dropped before the payload is
returned, so its order cannot be rechecked; and `rule_hit_and_shadow_analysis` does not order
its output at all. No entry from these three carries a `rank` or a `severity`.

Recommended setup for a local model (adapt it to your agent client):

```text
You operate an OPNsense or pfSense firewall through the firewall-aiops MCP tools.

TOOL USE
- Before answering any question about the current firewall, you MUST call a
  tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- Of the three RCAs, only `blocked_traffic_rca`'s order is checkable (by `hits`). Do not read
  priority off the position of a gateway finding, and do not look for a number on a rule
  finding — there is none; read `hitCountersUnavailable` to see whether "never hit" was even
  measurable.
- A null field means neither platform returned that value. Report it as "not
  available" — never infer it. In particular, a rule with a null "interface" is
  not a rule on an interface named "none".
- Report values exactly as returned. Do not normalise, translate, or prettify
  rule actions, gateway statuses, or interface names.
- A gateway whose status is "none" is unmonitored, not down. A gateway with no
  status field at all is unknown — say so rather than calling it healthy.

- Only `toggle_rule` has a CLI command. `apply_changes`, `reconfigure`, `reboot`,
  `restart_service`, `kill_states` and the alias writes are MCP-only and nothing will ask
  you to confirm them: call with `dry_run=True` first and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert that traffic is being blocked by a specific rule unless a log
  entry or the shadow analysis actually names that rule.
- Do not add generic firewall advice that does not follow from the tool output.
- Do not confuse a rule UUID with an alias name, an interface name (wan, lan,
  opt1) with its description, or a gateway name with its monitor IP.
- OPNsense and pfSense are different platforms with different API shapes. Do not
  suggest an OPNsense-only action on a pfSense target; the target's platform is
  reported in the overview.

CHANGES ARE TWO-STEP
- On OPNsense, editing a rule stages it; nothing takes effect until
  apply_changes is called. Never report a change as live before that.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup. A read-only role is a sensible default
for a firewall specifically: a mistaken `toggle_rule` or `reboot` on the box that
carries your management session locks you out of the thing you were trying to fix.

```bash
# Give the OPNsense/pfSense API user a read-only role, then:
firewall-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export FIREWALL_AUDIT_APPROVED_BY="your.name@example.com"
export FIREWALL_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the RCA tools
  (`gateway_health_rca`, `blocked_traffic_rca`,
  `rule_hit_and_shadow_analysis`) — they do the multi-step correlation inside
  one call, so the model does not have to chain reads and keep rule UUIDs
  straight.
- **The model ignores later tool results in a long context.** The firewall log
  and state table are the two big payloads here; ask narrower questions and use
  `--limit` / `top` deliberately rather than pulling the whole state table.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Firewall-AIops](https://github.com/AIops-tools/Firewall-AIops/issues)
with the model, runtime, and what went wrong.
