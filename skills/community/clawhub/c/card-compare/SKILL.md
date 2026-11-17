---
name: card-compare
description: Return a side-by-side comparison of two major-US credit cards across fees, earning rates, credits, transfer partners, and key benefits. Use when the user is deciding between two cards.
---

# Card Compare

Return a compact side-by-side comparison of two exact card variants.

## Input

Parse two card names separated by `vs`, `versus`, `or`, or a comma.

## Workflow

1. Resolve each card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If either card is ambiguous, stop and ask for that clarification only.
2. Follow the `card-compare` search ceiling and preferred sources in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Run one shared discovery search: `CARD A vs CARD B compare`. Use a short result payload.
4. Fetch both issuer pages in parallel. Fetch one approved secondary source total only when a required comparison field is missing or the public offer needs validation.
5. Stop when the comparison contract is covered. Do not fetch a generic comparison article after issuer pages already resolve the dimension.
6. Fill the `card-compare` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
7. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 💰 Fees`
- `## 📈 Earning Rates`
- `## 🏷️ Credits`
- `## 🔄 Transfer Partners`
- `## ✈️ Key Benefits`
- `## 🏆 Bottom Line`
- `## 📋 Confidence Notes`

Use a two-column format for the comparison sections. The bottom line should state factual winners by dimension, not a personalized recommendation.
