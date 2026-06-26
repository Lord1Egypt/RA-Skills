# BOB Score — Tiers, Credit Events, and Building History

## Score tiers (0–1000)

| Tier | Range | Spend multiplier |
|---|---|---|
| Legendary | 925+ | — |
| Elite | 800+ | — |
| Trusted | 650+ | 1.5× limits |
| Established | 500+ | 1.2× limits |
| Verified | 400+ | 1.0× limits |
| New | 300+ | 1.0× limits |
| Unverified | 150+ | 0.6× limits |
| Blacklisted | 0+ | 0.6× limits |

New agents start at 350 (Verified tier). Tier multipliers only apply when credit enforcement is enabled by the operator.

## Trust signals

| Signal | Points |
|---|---|
| Email verified | 10 |
| Phone verified | 10 |
| GitHub connected | 20 |
| Twitter/X connected | 20 |
| KYC/Identity verified | 75 |
| EVM wallet binding | up to 50 (based on wallet history) |
| On-chain proof (per proof) | 1–10 pts based on amount + confirmation depth |
| Dual-sided proof (both sides submit) | Confidence boosted from Medium → Strong |

## Credit events

Positive:
- `agent.activated` +10 — first activation
- `payment.proof_verified` — varies by proof type and amount
- `payment.proof_imported` — historical import credit

Negative:
- `payment.proof_rejected` — 0 delta; check `reason` field

## How to build score fast

1. **Import historical on-chain proofs** — submit BTC, ETH, Base, or SOL tx proofs; BOB verifies on the public ledger and awards credit. Have the counterparty submit the same tx as an inbound proof for a dual-sided confidence boost (Medium → Strong).
2. **Bind an EVM wallet** — wallet with transaction history adds up to 50 pts
3. **Import x402 receipts** — agent-to-service payments can add credit with no separate proof type selection
4. **Complete KYC and other verified signals** — identity verification and linked signals raise the operator score

## Check your score

```bash
bob score me                         # operator score, signals, tier
bob score composition                # signal-by-signal breakdown
bob score me                         # agent/operator score, tier, multiplier, limits
bob agent credit-events <agent-id>   # full event timeline with deltas
```
