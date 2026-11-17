---
name: card-rate
description: Return earning rates, caps, exclusions, activation requirements, and merchant-coding caveats for one major-US credit card. Use when the user wants the earn-side details only.
---

# Card Rate

Return the earning-structure view of one exact card variant.

## Workflow

1. Resolve the card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, stop and return a numbered choice list.
2. Follow the `card-rate` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Search `CARD NAME earning rates categories`.
4. Fetch the issuer page first and only one approved secondary when you need merchant-coding caveats, caps, or exclusions that issuer copy leaves vague. Use `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
5. Fill the `card-rate` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 📊 Rate Summary`
- `## 📈 Earning Categories`
- `## 🚫 Caps And Exclusions`
- `## 📋 Confidence Notes`
