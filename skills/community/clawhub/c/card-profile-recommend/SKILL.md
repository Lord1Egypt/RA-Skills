---
name: card-profile-recommend
description: Analyze a multi-card portfolio, grade the current cards, and recommend 2-3 next cards with signup-bonus strategy and issuer-rule checks. Use when the user wants to know which cards to keep, drop, or add next.
---

# Card Profile Recommend

Return a graded portfolio audit plus concrete next-card recommendations.

## Input

Accept a comma-separated list of cards. Optional opening dates may appear inline or after an `opened:` note. When dates are missing, treat issuer timing rules as partially unknown and say so.

## Workflow

1. Resolve every existing card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If any card is ambiguous, stop and ask only for that clarification.
2. Follow the `card-profile-recommend` search ceiling and preferred sources in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
3. Group held cards by issuer. Research each issuer once for fees, usable credits, major earning categories, transfer access, and notable benefits; reuse those facts across that issuer's cards.
4. Identify portfolio gaps before researching candidates. In parallel, research only the two or three candidates that can fill a named gap or materially improve bonus value. Exclude cards the user already holds and apply the same shared fetch-safety rules.
5. Compute portfolio economics: gross fees, realistic credits, net annual cost, and effective cents-per-point by ecosystem. If the wallet lacks a transfer-enabling card for a currency, value that currency at `1.0 cpp`.
6. Build the earning map by category using effective value per dollar, not raw multiplier alone.
7. Grade each held card as `MVP`, `Keep`, or `Consider Dropping` using the rules below.
8. Recommend two or three personal cards only. Apply issuer rules before recommending them. Do not research a candidate merely to expand the list.
9. Sequence the applications by rule constraints, welcome-offer quality, and spend feasibility.
10. Fill the `card-profile-recommend` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml), then apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 🃏 Cards Entered`
- `## 📊 Portfolio Summary`
- `## 🏅 Card Grades`
- `## 🗺️ Earning Map`
- `## 🔻 Consider Dropping`
- `## 🕳️ Portfolio Gaps`
- `## ➕ Recommended Additions`
- `## 🎯 Signup Bonus Strategy`
- `## ⚖️ Issuer Rules Check`
- `## 🔍 Confidence Notes`

Omit `## 🔻 Consider Dropping` when no held cards belong there.

## Grading Rules

- Grade `MVP` when a card is cheap to keep or uniquely valuable in the wallet.
- Grade `Keep` when the card still has real strategic value, credit-history value, or recent-account timing value.
- Grade `Consider Dropping` only when the fee drag is real and the card does not uniquely unlock an earning lane, benefit, or transferable ecosystem.
- Never place the wallet's only transfer-enabling card for a rewards ecosystem in `Consider Dropping`.
- If the user provides opening dates, treat cards opened within the last 12 months as strong `Keep` candidates unless the downside is overwhelming.

## Issuer Rules

- Check Chase `5/24`.
- Check Amex lifetime-language risk and the five-credit-card limit.
- Check Citi `8/65` and `48-month` family timing.
- Check Capital One application spacing and two-card limits when relevant.
- Do not recommend business cards in this skill.
