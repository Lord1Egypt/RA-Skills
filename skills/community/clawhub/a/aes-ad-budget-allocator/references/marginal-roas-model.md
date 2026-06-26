# Modeling Marginal ROAS

The single most important concept in budget allocation: average ROAS is not marginal ROAS. A channel with 4x average ROAS can deliver less than 2x on incremental dollars if it is past saturation. Allocate against the curve, not the headline.

## Why the curve matters

Each ad channel has a diminishing-returns curve. At low spend, every dollar reaches high-intent audiences cheaply. As spend grows, you reach lower-intent audiences and pay higher CPMs to outbid yourself. Eventually each marginal dollar produces less revenue than the last.

If you keep adding budget to a channel past its saturation point, blended ROAS falls even though the channel's headline ROAS still looks acceptable. The fix is to measure marginal ROAS — the ROAS of the most recent slice of spend — and stop adding budget when it crosses the blended floor.

## Fitting a simple curve

You don't need a statistician. You need 8-12 weeks of weekly data and a basic model.

1. Plot weekly spend vs weekly revenue per channel.
2. Look for the shape:
   - Straight line through origin = channel still in linear range; more budget is fine.
   - Concave curve flattening as spend rises = approaching saturation.
   - Flat tail = saturated; incremental dollars near zero return.
3. Fit a log curve (revenue ≈ a + b·log(spend)) or a square-root curve (revenue ≈ a + b·sqrt(spend)). Both are reasonable approximations.
4. Compute marginal ROAS at current spend level: take the slope of the fitted curve at that point.

## Interpreting the result

| Marginal ROAS | Action |
|---|---|
| > 1.3x blended floor | Add budget aggressively, up to the next test increment |
| 1.0x – 1.3x blended floor | Hold flat; this channel is at its sweet spot |
| 0.7x – 1.0x blended floor | Reduce budget by 10-20% next cycle |
| < 0.7x blended floor | Reduce by 30%+ and reinvest elsewhere |

## Caveats

- Curves shift over time. Refit at least quarterly.
- Curves shift with creative. A breakthrough ad can reset the curve upward.
- Curves shift with auction dynamics. Competitor entry can flatten your curve in weeks.
- Channels with small samples (under 6 weeks of data, or under $5k/week) have unreliable curves; use channel benchmarks as a sanity check.
- Last-click attribution understates upper-funnel channels' marginal contribution. If you have MMM or incrementality tests, weight those higher.

## Quick sanity check

When in doubt, run a single iso-budget reallocation: pull 10% from your assumed-saturated channel for 4 weeks. If blended revenue is flat or up, the channel was saturated. If blended revenue drops more than 10%, it wasn't. This is cheaper than building a model.
