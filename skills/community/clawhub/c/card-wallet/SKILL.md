---
name: card-wallet
description: Audit a multi-card wallet for overlap, gaps, and total annual cost. Given a list of cards the user holds, identifies redundant benefits, uncovered spend categories, and net fee burden. Use when the user wants to evaluate their full card lineup.
---

# Card Wallet

Return a compact wallet audit for a set of cards the user holds.

## Input

Accept a comma-separated list of cards.

## Workflow

1. Resolve every card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If any card is ambiguous, stop and ask only for that clarification.
2. Follow the `card-wallet` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Research each card for annual fee, key earning categories, credits, and notable benefits using `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
4. Build an earning map across common categories: dining, groceries, gas, travel, streaming, transit, drugstore, online shopping, rent, hotel, airline, and general spend.
5. Identify overlap, uncovered categories, redundant benefits, and total annual fee drag.
6. Fill the `card-wallet` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
7. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 💰 Annual Cost`
- `## 📈 Earning Map`
- `## 🏷️ Credits Stack`
- `## 🔁 Overlap`
- `## 🕳️ Gaps`
- `## 📋 Confidence Notes`

Only include statement credits and subscription offsets in the credits stack. Do not treat point multipliers as credits.
