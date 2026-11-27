---
name: agent-spend-gate
description: Local policy check for agent spending (ASPL v0.1) — budgets, merchant allowlists, Trust Rank floors and approval thresholds, with a hash-linked audit log kept on the user's machine. Read-only: no wallet access, no key handling, no funds movement. Use before an agent spends on x402/MPP/stablecoin rails, or after paycensus-trust-check when a decision is needed.
---

# Agent Spend Gate

Your agent is about to spend money. Before executing any payment, evaluate the
intent against the user's **Agent Spend Policy** (ASPL v0.1). The gate decides
**proceed / ask-human / refuse** — and writes every decision to a local
hash-chained audit trail. It never touches funds: if the decision is "proceed",
the agent signs with **its own key** through whatever wallet or payment skill it
already uses.

## One-time setup

```bash
python3 scripts/gate_check.py --init
```

Creates `~/.paycensus-gate/policy.json` (a starter policy — **edit it**:
agent identity, monthly budget, pinned merchants, Trust Rank floor,
approval thresholds). Policy format: https://gate.paycensus.com/spec/

## Evaluate before EVERY payment

```bash
python3 scripts/gate_check.py \
  --agent agent:me:main \
  --amount 0.01 \
  --resource https://api.example.com/x402/data \
  --rail x402 \
  --payto 0xABCdef...
```

Output (JSON): `{"allow": true/false, "status": "...", "reason": "...",
"scopes": [...], "eventHash": "..."}` — and the event is appended to the local
hash-chained audit trail (`~/.paycensus-gate/audit.jsonl`).

Exit code: `0` = proceed allowed, `1` = do not proceed.

## Decision handling — follow exactly

| status | meaning | what you do |
|---|---|---|
| `auto-approved` | amount ≤ auto-approve threshold | proceed with payment |
| `approved` | human pre-approved this exact intent | proceed with payment |
| `pending` | between thresholds — needs a human | Pause and tell the user the reason and the `eventHash`; after they approve (see below), re-evaluate |
| `rejected` | policy violation (budget, rail, merchant, floor, hard cap) | Do not continue; tell the user the reason verbatim — re-evaluate only after the user changes the policy |

## Human approvals

A `pending` intent is approved by the user running:

```bash
python3 scripts/gate_check.py --approve <eventHash> --approver alice
```

Then the agent re-runs the same evaluation command — the decision becomes
`approved` and the approval is part of the audit trail.

## Merchant risk (honest tiering)

- **Pinned merchants** (in the policy allowlist) → allowed, no external data
- **Trust Rank floor** configured → payees are scored from real on-chain
  settlement behaviour (public census, fetched hourly, cached locally);
  payees below the floor or with no record are rejected while a floor is set
- Pair with the `paycensus-trust-check` skill to *show* the user the risk
  details; the gate enforces, the check informs

## Rules

- Run a gate evaluation for every spend intent in the session, including repeat
  merchants.
- The audit log is append-only; each entry links to the previous by SHA-256.
  Do not alter existing entries.
- The gate does not request or handle wallet keys.
- Policy and audit data remain local; nothing is uploaded. (Optional: the daily
  chain digest can be anchored for third-party verification — see
  https://gate.paycensus.com/spec/)
