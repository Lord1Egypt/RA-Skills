# agent-spend-gate

**A spend-governance checkpoint for agents that pay.** Before any payment
moves, the gate evaluates the intent against your Agent Spend Policy (ASPL
v0.1) — and writes every decision to a tamper-evident, hash-chained audit
trail kept **entirely on your machine**.

**Read-only, no wallet access.** When the gate says "proceed", signing happens
in your existing wallet or payment skill (x402, MPP, Stripe, bank rails —
rail-agnostic by design).

## What it enforces

| Control | How |
|---|---|
| Monthly budgets | per-agent / per-team, month-to-date computed from your own audit stream |
| Merchant allowlists | pinned merchants, or Trust Rank floor from real on-chain settlement behaviour |
| Approval thresholds | auto-approve below X, human approval between X and Y, hard cap above Y |
| Human approvals | `--approve <eventHash>` — recorded as part of the audit trail |
| Rail permissions | which rails (x402 / MPP / stablecoin / card) each agent may use |
| Tamper evidence | every audit event links to the previous one by SHA-256; edited or deleted entries fail verification |

## Why different

- **Independent risk data.** Merchant scores come from the public PayCensus
  census (four chains of real x402 settlement history, hourly, Bitcoin-anchored
  daily) — not from a closed payment network's own records.
- **Third-party verifiable evidence.** Your local audit chain can be anchored
  externally (OpenTimestamps): show an auditor that a day's log existed and was
  never rewritten. No vendor-side "trust us" — verify it yourself.
- **Privacy by construction.** Policy and audit live in `~/.paycensus-gate/`.
  Nothing is uploaded. No account. No keys.
- **Rail-agnostic.** One policy across every wallet and payment skill your
  agents use — not one guardrail per vendor.

## Install

**ClawHub (OpenClaw):** listed as `agent-spend-gate`, or
`npx clawhub install agent-spend-gate`

**Hermes Agent:** `npx skills add https://github.com/PayCensusLabs/openclaw-skill-agent-spend-gate --skill agent-spend-gate`

**Manual:** copy this folder into `~/.openclaw/skills/` or your Hermes skills
directory.

## Quickstart

```bash
python3 scripts/gate_check.py --init        # creates ~/.paycensus-gate/policy.json — edit it
python3 scripts/gate_check.py \
  --agent agent:my-org:main \
  --amount 0.005 \
  --resource https://api.example.com/x402/data \
  --rail x402 --payto 0xABCdef...
```

Decision JSON + exit code (`0` proceed / `1` stop). `pending` means a human
must approve: `python3 scripts/gate_check.py --approve <eventHash> --approver alice`,
then re-run the evaluation.

## Spec

Policy format: [ASPL v0.1](https://gate.paycensus.com/spec/) — versioned draft,
implemented by the reference engine in `engine/`, exercised in production
dogfood since 2026-11 (public evidence: https://paycensus.com/audit.html).

## Pairs with

[`paycensus-trust-check`](https://github.com/PayCensusLabs/openclaw-skill-paycensus-trust-check)
— the read-only risk lookup your agent runs before the gate decides.

## License

MIT
