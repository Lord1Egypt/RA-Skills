---
name: card-credits
description: Return statement credits and cash-like credits for one major-US credit card, including trigger rules, cadence, enrollment requirements, restrictions, and practical usage notes. Use when the user wants the credits picture only.
---

# Card Credits

Return the credits view of one exact card variant.

## Credit Boundary

Count only statement credits, cash-back rebates, and complimentary subscriptions with a concrete dollar value. Exclude bonus multipliers, elevated earn rates, and anniversary-point perks.

## Workflow

1. Resolve the card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, stop and return a numbered choice list.
2. Follow the `card-credits` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Search `CARD NAME credits benefits`.
4. Fetch the issuer page first and one approved secondary only when you need trigger rules, cadence detail, or enrollment nuance. Use `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
5. Fill the `card-credits` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 💳 Credits Overview`
- `## 🏷️ Credit Details`
- `## 📏 Usage Rules`
- `## 📋 Confidence Notes`

Use one compact numbered line per credit with amount, cadence, trigger, and main restriction.
