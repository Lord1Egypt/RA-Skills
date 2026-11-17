---
name: card-news
description: Return material news about one major-US credit card from the last 3 months, including direct card changes, relevant issuer updates, and major approved-site coverage. Use when the user wants the latest card-specific developments.
---

# Card News

Return the last-3-month news view of one exact card variant.

## Workflow

1. Resolve the card with [../card-identity/SKILL.md](../card-identity/SKILL.md). If ambiguous, stop and return a numbered choice list.
2. Apply the 3-month inclusion rules from [../card-shared/recency-rules.md](../card-shared/recency-rules.md).
3. Follow the `card-news` strategy in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
4. Search `CARD NAME news changes CURRENT_YEAR` with a 3-month freshness window.
5. Fetch the most relevant issuer newsroom or approved secondary articles needed to confirm dates and materiality, using `WebFetch` and the URL-safety rules in [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml).
6. Fill the `card-news` contract in [../card-shared/command-contracts.yaml](../card-shared/command-contracts.yaml).
7. Apply [../card-shared/confidence-rules.md](../card-shared/confidence-rules.md) and [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). Keep `sources` in hidden YAML only.

## Required Sections

- `## 📅 News Window`
- `## 📰 Recent Updates`
- `## 📝 Summary`
- `## 📋 Confidence Notes`

Exclude generic evergreen coverage. Include only direct card changes or recent issuer/news coverage that materially changes how the card should be understood.
