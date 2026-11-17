---
name: card-value
description: Estimate first-year value for one major-US credit card given an optional spending breakdown. Returns welcome bonus + estimated earn + credits minus annual fee. Use when the user wants a quick value check.
---

# Card Value

Return a compact first-year value estimate for one exact card variant.

## Input

Accept a card name plus an optional spend breakdown. If the user gives no breakdown, use a moderate default profile: `$500/mo dining`, `$200/mo travel`, `$100/mo streaming`, `$200/mo groceries`, `$2000/mo other`.

## Workflow

1. Resolve the card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, stop and return a numbered choice list.
2. Follow the `card-value` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Search `CARD NAME welcome offer annual fee value`.
4. Fetch the issuer page plus approved secondaries needed for current offer, fee, earning, and credit details, using `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
5. Compute `welcome bonus value + annual earn value + credits - annual fee`.
6. Use `1.0 cpp` as the baseline unless a justified higher redemption assumption is clearly supported; call out that assumption in confidence notes.
7. Fill the `card-value` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
8. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 💳 Spend Profile`
- `## 🎁 Welcome Bonus`
- `## 📈 Annual Earn`
- `## 🏷️ Credits`
- `## 💰 Net First-Year Value`
- `## 📋 Confidence Notes`

Show the net-value math clearly in one compact block.
