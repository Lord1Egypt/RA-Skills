# Value Score Rubric (0–100)

The Value Score is a single weighted number that captures whether a cruise add-on package is worth buying for the user's specific situation. Output it on every response.

## Formula

```
Value_Score = (Savings_Component × 0.50) +
              (Convenience_Component × 0.20) +
              (Risk_Reduction_Component × 0.15) +
              (Pre-Cruise_Discount_Component × 0.15)
```

Each component is normalized 0–100 before weighting.

## Component 1 — Savings (50% weight)

```
Savings_% = (ACC_Total - Package_Total) / ACC_Total × 100
```

| Savings_% | Component Score |
|---|---|
| ≥ 30% savings | 100 |
| 15–29% | 80 |
| 5–14% | 60 |
| 0–4% | 40 |
| -5% to 0% (slightly more expensive) | 25 |
| < -5% (clearly more expensive) | 0 |

## Component 2 — Convenience (20% weight)

| Situation | Component Score |
|---|---|
| User explicitly hates tracking spending; long sailing (10+ nights) | 100 |
| User dislikes itemized bills; family with kids | 80 |
| Standard 7-night, indifferent to tracking | 60 |
| Short cruise (3–4 nights) where math is easy | 40 |
| User explicitly wants to control consumption | 20 |

## Component 3 — Risk Reduction (15% weight)

Captures the value of locking in pricing, avoiding sticker shock, and avoiding the "I drank too much because I already paid" trap.

| Factor | Component Score |
|---|---|
| Heavy drinker who would otherwise overspend on cocktails | 100 |
| Moderate drinker, prone to occasional binge | 70 |
| Light drinker, disciplined | 30 |
| Non-drinker (drink package only) | 0 |

For Wi-Fi: substitute "remote work need" or "must stay reachable" — if mission-critical, score 100.

## Component 4 — Pre-Cruise Discount (15% weight)

```
Pre_Cruise_Discount_% = (Onboard_Price - Pre_Cruise_Price) / Onboard_Price × 100
```

| Discount % | Component Score |
|---|---|
| ≥ 25% | 100 |
| 15–24% | 80 |
| 5–14% | 50 |
| 0–4% | 20 |
| Negative (pre-cruise more expensive — happens) | 0 |

## Verdict Mapping

| Score | Verdict |
|---|---|
| 75–100 | **BUY** — clear win |
| 60–74 | **BUY (lean)** — solid value, minor caveats |
| 45–59 | **DEPENDS** — show the user the swing factor |
| 30–44 | **SKIP (lean)** — small savings not worth the lock-in |
| 0–29 | **SKIP** — clear loss |

## Worked Example

User: 7-night Royal Caribbean, Deluxe Beverage at $89/day pre-cruise, drinks 4 cocktails/day, 1 coffee/day.

- Package_Total = $89 × 1.18 × 7 = $735
- ACC_Total = ($14 × 4 + $5 × 1) × 7 = $61 × 7 = $427
- Savings_% = (427 − 735) / 427 × 100 = **−72%** → Component 1 = **0**
- Convenience: standard 7-night, moderate consumer → **60**
- Risk Reduction: moderate drinker → **70**
- Pre-cruise discount: $89 vs onboard $109 = 18% off → Component 4 = **80**

Value_Score = (0 × 0.50) + (60 × 0.20) + (70 × 0.15) + (80 × 0.15)
            = 0 + 12 + 10.5 + 12
            = **34.5/100 → SKIP (lean)**
