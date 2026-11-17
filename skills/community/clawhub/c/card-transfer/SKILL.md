---
name: card-transfer
description: Return transfer partners, transfer ratios, timing notes, and restrictions for one major-US credit card. Use when the user wants redemption-transfer details only.
---

# Card Transfer

Return the transfer-program view of one exact card variant.

## Workflow

1. Resolve the card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, stop and return a numbered choice list.
2. Follow the `card-transfer` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Search `CARD NAME transfer partners`.
4. Fetch the issuer page first and one approved secondary only when you need current ratios, timing notes, or bonus context. Use `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
5. Fill the `card-transfer` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
6. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 🔄 Transfer Program`
- `## 🤝 Transfer Partners`
- `## ⚠️ Transfer Caveats`
- `## 📋 Confidence Notes`

Use a numbered list for partners with ratio plus one short caveat line per item.
