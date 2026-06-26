# Metrics Reference (v4)

## Scope

This skill outputs a **heuristic BTC risk-state snapshot** from public APIs. It is designed for transparency and fast situational awareness, not exact replication of institutional dashboards.

## Core Metrics

- **ATM IV (front expiry)**: average of call/put mark IV nearest to 50-delta.
  - Higher = richer short-dated fear / event premium.
- **RR(25d)**: IV(call 25d) - IV(put 25d).
  - More negative = stronger downside skew.
- **RR(15d)**: IV(call 15d) - IV(put 15d).
  - More negative = faster panic sensitivity.
- **Put/Call OI ratio**: front-expiry put OI / call OI.
  - Higher = more downside open-interest concentration.
- **Put buy share proxy**: put option 24h USD volume / total (put+call) USD volume.
  - Proxy only; not signed aggressor flow.
- **Deribit funding/basis**: perpetual carry + perp/index dislocation.
  - Negative funding is generally more bearish.
- **Cross-exchange spot dispersion (bp)**: max-min spot spread across available venues.
  - Higher = more dislocation / weaker liquidity.
- **Funding regime**: aggregated sign ratio across Deribit/OKX/Bybit funding snapshots.
  - `bearish` / `mixed` / `bullish_or_neutral`.

## Heuristic Threshold Logic

Thresholds are intentionally simple and reviewable. They are designed for alerting and state-labeling, not precision forecasting.

### Normal mode
- RED: score >= 6
- AMBER: score 3-5
- GREEN: score <= 2

Typical contributor thresholds:
- RR15 < -8
- RR25 < -5
- ATM IV > 55
- Put volume proxy > 58%
- Spot dispersion > 20bp
- Funding regime = bearish

### High-alert mode (event-sensitive)
Use during macro/event windows when you want earlier warning at the cost of more false positives.

- RED: score >= 5
- AMBER: score 2-4
- GREEN: score <= 1

Typical contributor thresholds:
- RR15 < -7
- RR25 < -4.5
- ATM IV > 52
- Put volume proxy > 56%
- Spot dispersion > 15bp
- Funding regime = bearish

## 72h Validation Matrix

Track 5 checks for the next 72h:
1. Options skew panic
2. Vol regime hot
3. Flow put dominance
4. Funding bearish confirm
5. Liquidity stress

Action map:
- fired >= 4: DEFENSIVE
- fired 2-3: CAUTIOUS
- fired <= 1: PROBING

Interpretation:
- `DEFENSIVE`: tail-risk pricing is broad and aligned.
- `CAUTIOUS`: enough stress exists to justify smaller size / tighter risk.
- `PROBING`: conditions are less stressed; tactical re-risking can be explored.

## Action Triggers

- `de_risk_triggers`: conditions that suggest reducing risk / hedging
- `re_risk_triggers`: conditions that suggest gradual re-risking

These are heuristic prompts, not automatic instructions.

## Audience Modes

- `pro`: terse, trading-oriented output
- `beginner`: plain-language explanation of each key metric and what it means

## Confidence

Confidence score (0-100) is based on:
- Data availability (options + cross-venue sources)
- Signal agreement (how many bearish signals align)

If venue coverage is incomplete, confidence should fall and the output should expose the gap via:
- `availability`
- `data_gaps`
- `degraded_mode`

## Limitations

- This is a risk-state framework, not trading advice.
- RR metrics are front-expiry delta-nearest approximations.
- Put-flow is a volume-share proxy, not aggressor-side flow.
- Some venue endpoints may be regionally blocked or intermittently unavailable.
