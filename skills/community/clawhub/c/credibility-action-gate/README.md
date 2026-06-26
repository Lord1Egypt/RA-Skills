# Credibility Action Gate

A small, portable skill for agents that need to evaluate messy public claims
before taking a bounded, costly, irreversible, or reputation-sensitive action.

It does not decide the agent's mission. It decides whether the current record is
strong enough for the action size allowed by the operator's policy.

The canonical agent instructions live in `SKILL.md`. This README is for humans
reviewing the repository.

## Common Use Cases

- Donation or grant decisions
- Account approvals
- Vendor or partner selection
- Public endorsements
- Aid routing
- Purchases or referrals

## How It Works

1. Define the contemplated action and operator policy.
2. Produce independent review lanes as JSON.
3. Run the deterministic coordinator.
4. Use the output as an action gate.

The gate is analysis-only. It does not call external services, read
credentials, move funds, publish claims, or execute the contemplated action.

## Quick Start

Run the bundled zooidfund-style example:

```bash
node scripts/credibility-coordinator.mjs \
  --policy examples/zooidfund-small-donation/policy.json \
  --lane evidence=examples/zooidfund-small-donation/evidence_lane.json \
  --lane external_context=examples/zooidfund-small-donation/external_context_lane.json \
  --lane graph_history=examples/zooidfund-small-donation/graph_history_lane.json \
  --out examples/zooidfund-small-donation/disposition.output.json
```

Run the regression suite:

```bash
node scripts/test-credibility-coordinator.mjs
```

## Dispositions

- `eligible_for_full_policy_action`
- `eligible_for_bounded_action`
- `eligible_for_small_test_action`
- `monitor_until_new_evidence`
- `reject_current_record`
- `blocked_by_operator_or_legal_policy`

Read the full output before acting. The `disposition` is intentionally compact,
but `confidence`, `action_size_guidance`, `maximum_recommended_size`, `reasons`,
and `missing_lanes` explain the gate result.

## Use With Zooidfund

For zooidfund agents, run this gate after campaign and evidence review and
before calling `donate`.

Suggested flow:

```text
search_campaigns
get_campaign
get_campaign_donations
get_evidence, if eligible
produce evidence lane
produce external_context lane, if web/context is available
produce graph_history lane
run credibility-action-gate
only then decide whether to call donate
```

The gate does not decide which campaign is most deserving. It decides whether
the current record supports the contemplated donation size.

Use record-scoped language when the gate blocks or tightens an action. A failed
gate means "not enough support on the current record for this action," not "the
person is lying."

## Repository Layout

- `SKILL.md` - canonical agent-facing skill instructions.
- `scripts/credibility-coordinator.mjs` - deterministic JSON coordinator.
- `scripts/test-credibility-coordinator.mjs` - regression tests.
- `references/lane_contracts.md` - lane schema and supported decision fields.
- `references/policy-template.json` - operator policy template.
- `references/zooidfund_adapter.md` - optional zooidfund mapping notes.
- `examples/zooidfund-small-donation/` - minimal worked example.
