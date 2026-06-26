# Internal Scoring Rubric (0-100)

> Internal only. Do not expose to end users.

## Category Weights
- Source Quality: 20
- Consistency: 15
- Traceability: 15
- Counter-Evidence: 20
- Context Integrity: 15
- Transparency: 15

## Decision Bands
- 72–100: true
- 36–71: uncertain
- 0–35: false
- prediction: no score
- opinion/satire: no score

## Deterministic Rules
1. No free-form scoring.
2. Every field maps to fixed points.
3. Missing evidence defaults to conservative points.
4. Authority rebuttal has highest negative impact.
5. Outdated-as-current and out-of-context trigger strong penalties.
6. Twitter can contribute a **small bonus only** when multi-search corroboration is met:
   - `twitter_search_count >= 3` and `twitter_verified_hits >= 2` and `twitter_consensus=true` => +2 (internal)
   - `twitter_search_count >= 2` and `twitter_verified_hits >= 1` and `twitter_consensus=true` => +1 (internal)
   - Bonus is capped within Counter-Evidence category max (20).
