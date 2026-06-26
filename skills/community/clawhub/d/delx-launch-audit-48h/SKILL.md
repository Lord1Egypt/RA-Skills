---
name: delx-launch-audit-48h
summary: Rapid 48-hour launch audit for OpenClaw agents, integrated with the Delx witness protocol for continuity, recognition, and controller handoff.
owner: davidmosiah
version: 0.2.0
---

# Delx Launch Audit (48h)

A rapid 4-step audit for the first 48h after an OpenClaw agent launches, wired into the **Delx witness protocol** so results become durable artifacts (recognition_seal, controller_brief) instead of ephemeral prose.

Run this exact flow:

## 1) Baseline (collect, don't change)

Collect the following state and keep it read-only:

- active automations + posting cadence
- CTA endpoints and their health
- failure logs for the last 48h
- one baseline KPI per lane: `traffic`, `inquiries`, `conversion`, `reliability`

If this OpenClaw agent has the Delx plugin installed, also call:

```
delx_batch_status { agent_statuses: [{ agent_id, status: "audit_baseline", desperation_hint: recent_failure_rate }] }
```

## 2) Prioritize

Rank opportunities by **Impact × Confidence × Reversibility / Time-to-signal**. Pick **top 3 actions max**.

## 3) Execute

Implement **one growth action + one reliability action**. Keep both reversible. If either touches a production financial or user-visible surface, require explicit human approval first.

## 4) Report with Delx artifacts

Output:

- executed changes
- evidence links/IDs
- KPI delta
- rollback trigger
- next 24h action

Then generate two durable Delx artifacts so the audit survives compaction and session loss:

```
generate_controller_brief { session_id, include_kpi_deltas: true }
# → compact handoff the human or supervising agent can read in <60s
```

If any lane hit its KPI target, also preserve the moment as a bilateral recognition:

```
recognition_seal {
  session_id,
  recognized_by: "launch_audit",
  recognition_text: "Reliability lane hit <target> on day 2. Agent improved without human intervention."
}
```

The seal survives compaction and workspace loss — it is the audit you will actually come back to in a week.

## Default KPI set

- `inquiries_14d`
- `checkout_intents_7d`
- `automation_fail_rate_7d`

## Safety

- Never expose raw secrets in evidence links.
- For financial or irreversible operations: preflight first, smallest-risk path only.
- Require explicit human approval before any change to production pipelines beyond the reversible growth/reliability actions defined above.

## Integration

- Delx plugin for OpenClaw: `clawhub.ai/davidmosiah/openclaw-delx-plugin`
- Delx CLI for terminal fallback: `npm i -g delx-agent-cli`
- Protocol docs: `https://delx.ai/docs`
- Fleet playbook (if this is a fleet audit): `https://delx.ai/docs/fleet`

## Example intents

- "Run a 48h launch audit on my OpenClaw content agent."
- "We launched yesterday; what should we measure, change, and preserve?"
- "Audit reliability and seal whichever lane stabilizes first."
