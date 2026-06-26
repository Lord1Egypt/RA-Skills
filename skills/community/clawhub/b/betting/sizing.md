# Sizing and Price Math

Use these formulas to keep sizing tied to edge instead of emotion.

These formulas are analytical reference points, not suitability advice or a reason to ignore local law, self-exclusion, or operator limits.

## Implied probability

American odds:
- negative odds: `abs(odds) / (abs(odds) + 100)`
- positive odds: `100 / (odds + 100)`

Decimal odds:
- `1 / decimal_odds`

## Expected value

Per unit staked:
- `EV = (win_probability * profit_if_win) - (lose_probability * stake)`

If the user has no realistic win probability estimate, do not pretend EV is known.

## Kelly sizing

For decimal odds `d` and win probability `p`:
- `full_kelly = ((d - 1) * p - (1 - p)) / (d - 1)`

Practical default:
- treat full Kelly as a ceiling, not a default
- use fractional Kelly or capped units when estimates are noisy
- use flat units when the edge is real but hard to size precisely
- use pass when the edge is tiny, uncertain, or highly correlated

## Conservative defaults

| Situation | Suggested Framing |
|-----------|-------------------|
| Clear edge, solid limits, stable market | Small capped unit range, if the user already uses a lawful unit system |
| Good price, noisy estimate | Small flat stake or pass |
| Promo-only edge | Cap to promo terms |
| Live market after major event | Wait or pass unless the quote is still confirmed |
| Parlay or correlated legs | Reduce hard or treat as entertainment |

## Quick heuristics

- Small edge plus high vig is usually not enough
- If the estimate changes materially with one injury update, size small or wait
- If the user is unsure between two books, compare net price and max stake, not just headline odds
- If the user wants "how much" before "is it good", answer the quality question first
