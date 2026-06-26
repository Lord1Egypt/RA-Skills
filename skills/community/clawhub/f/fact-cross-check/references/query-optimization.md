# Query Optimization

## Operators

- `"exact phrase"` — quote specific terms
- `site:domain.com` — target authoritative sources
- `2025 OR 2026` — date filter for current info
- `-demo -template` — exclude noise
- `("term1" OR "term2")` — expand when exact term unknown

## Multi-Stage Strategy

1. Official: `"[subject]" site:[authoritative-domain]`
2. Analytical: `"[subject]" site:[relevant-analysis-tool]`
3. General: `"[subject]" [claim] 2025 OR 2026`

Stop at first stage that returns confident result.

## Rules

- Add date filters for time-sensitive topics (tech, market data, company status)
- Skip date filters for definitions and historical facts
