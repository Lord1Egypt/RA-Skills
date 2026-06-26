# Core Concepts

## Core Lens

- Price action is about reading the auction and the likely next path, not predicting with certainty.
- Context matters more than candle names. A setup is only useful when context, signal, and room all line up.
- Most bars in trading ranges disappoint. Most pullbacks in strong trends are attempts to rejoin the trend until proven otherwise.
- If the chart is ambiguous, treat it as a range and reduce aggression.

## Vocabulary

- `Always In`: the side that currently has control. Ask which side would be more painful to exit if you were trapped against it.
- `Trend`: repeated closes in one direction, limited overlap, and pullbacks that fail to reverse control.
- `Trading Range`: overlap, tails, failed breakouts, and disappointment in both directions.
- `Broad Channel`: a trend exists, but swings are large and two-sided enough to hurt late entries.
- `Magnet`: a price level the market is likely to test, such as a prior high/low, breakout point, EMA, open, or measured move target.
- `Breakout Mode`: compression where both sides are building pressure and either breakout could become the move.
- `Signal Bar`: the bar used for a stop-entry decision. Its body, close, and tails matter.
- `Follow-Through`: what the next bar or next few bars do after the signal bar.
- `Second Entry`: the second attempt after an initial reversal fails. Often better than the first reversal attempt.
- `Wedge`: three pushes in one direction with weakening momentum, usually near a meaningful location.
- `Final Flag`: a late trend pause that can fail and lead to a larger reversal.
- `Measured Move`: projecting a prior leg or range height to estimate a target.
- `Scalp`: a quick profit objective when context is mixed or room is limited.
- `Swing`: holding for a larger move when context, trend, and room are all favorable.

## Good Signal Bar vs Weak Signal Bar

- Good bull signal bar: closes near its high, has a meaningful body, and lacks a large top tail.
- Good bear signal bar: closes near its low, has a meaningful body, and lacks a large bottom tail.
- Weak signal bar: small body, prominent opposite tail, or poor location.
- A strong signal bar can still be a bad trade if it is in the middle of a range or directly into a magnet.

## Fast Heuristics

- If you are unsure whether it is a trend or a range, call it a range.
- Strong trends often go farther than reversal traders expect.
- Reversals usually need location, a credible signal, and often a second attempt or wedge logic.
- A setup count by itself is not enough. `High 2` in the middle of a choppy range is still low quality.
- The market often has more inertia than traders want. Do not flip bias without clear evidence.

## Stable Labels For Downstream Use

- `market_phase`: `trending`, `trading_range`, `broad_channel`, `unknown`
- `always_in`: `long`, `short`, `unknown`
- `setup_status`: `actionable`, `watch`, `none`
