# Risk Scoring Model Reference

Guide for building weighted risk scoring systems that balance fraud detection with false positive minimization.

## Signal Categories and Base Weights

### Payment Signals (Max 30 points)

| Signal | Condition | Points | Rationale |
|---|---|---|---|
| AVS mismatch | ZIP does not match | +8 | Strong indicator of card-not-present fraud |
| AVS partial | Street matches, ZIP does not | +4 | Common with recent address changes |
| CVV failure | CVV does not match | +12 | Very strong fraud indicator |
| CVV not provided | CVV field empty | +6 | Moderate risk, some legitimate scenarios |
| BIN country mismatch | Card BIN country ≠ IP country | +10 | High risk for cross-border fraud |
| Prepaid card | BIN identified as prepaid | +5 | Moderate risk, popular with fraudsters |
| Virtual card | BIN identified as virtual | +3 | Lower risk, growing legitimate use |

### Identity Signals (Max 25 points)

| Signal | Condition | Points | Rationale |
|---|---|---|---|
| Email age | Domain created < 30 days | +8 | Disposable email indicator |
| Email domain | Free provider (gmail, yahoo) | +2 | Weak signal but contributes to pattern |
| Email-name mismatch | Email has no correlation to billing name | +5 | Common in fraud, also common legitimately |
| Phone verification | Phone number fails verification | +7 | Strong signal when available |
| Account age | Customer account < 24 hours old | +6 | New accounts carry higher risk |
| Previous orders | No order history | +3 | New customers vs. returning |

### Geographic Signals (Max 20 points)

| Signal | Condition | Points | Rationale |
|---|---|---|---|
| IP geolocation mismatch | IP location > 500 miles from billing | +8 | Strong indicator, but travelers are common |
| Proxy/VPN detected | IP flagged as proxy or VPN | +7 | High correlation with fraud attempts |
| High-risk country | IP or shipping to high-fraud-rate country | +5 | Country-level risk adjustment |
| Billing-shipping distance | > 200 miles apart | +4 | Gift purchases create false positives |
| Shipping to freight forwarder | Known reshipping address | +10 | Very strong fraud indicator |

### Behavioral Signals (Max 15 points)

| Signal | Condition | Points | Rationale |
|---|---|---|---|
| Session duration | < 60 seconds checkout | +5 | Automated or scripted purchase |
| Page views | < 3 pages before checkout | +3 | Bypassed normal shopping flow |
| Cart composition | Only high-resale items | +4 | Targeted theft pattern |
| Copy-paste behavior | Payment fields populated by paste | +3 | Possible use of stolen card data |
| Multiple failed attempts | 2+ failed payment attempts this session | +5 | Card testing behavior |

### Velocity Signals (Max 10 points)

| Signal | Condition | Points | Rationale |
|---|---|---|---|
| Email velocity | >2 orders same email in 24h | +5 | Unusual purchasing pattern |
| IP velocity | >3 orders same IP in 1h | +7 | Likely automated fraud |
| Address velocity | >2 orders same address different cards in 48h | +8 | Strong fraud indicator |
| Device velocity | >3 orders same device fingerprint in 24h | +5 | Repeat device usage pattern |

## Action Thresholds

| Score Range | Action | Processing |
|---|---|---|
| 0–15 | Auto-approve | Process immediately, no additional friction |
| 16–30 | Low-risk review | Approve with enhanced monitoring, flag for batch review |
| 31–50 | Manual review | Hold order for analyst review within 2 hours |
| 51–70 | Enhanced verification | Require additional authentication (3DS challenge, email/phone verify) |
| 71–100 | Auto-decline | Decline transaction with generic error message |

## Threshold Calibration Process

### Initial Calibration (Month 1)

1. Set conservative thresholds (lower auto-decline threshold, e.g., 60+)
2. Route more orders to manual review to gather labeled data
3. Track all manual review decisions with detailed reason codes
4. Monitor false positive rate daily — target < 5% of flagged orders being legitimate

### Ongoing Calibration (Monthly)

1. Review all chargebacks from the past 30 days — what score did they receive?
2. Review all manually approved orders — did any result in chargebacks?
3. Review all auto-declined orders — sample 10% and assess legitimacy
4. Adjust signal weights based on predictive accuracy of each signal
5. Adjust action thresholds to maintain target false positive rate

### Seasonal Adjustments

| Season | Adjustment | Rationale |
|---|---|---|
| Holiday (Nov-Dec) | Reduce billing-shipping distance weight by 50% | Gift purchases increase |
| Back-to-school (Aug-Sep) | Reduce new account weight by 30% | New student customers |
| Flash sales | Reduce session duration weight by 70% | Legitimate rapid purchasing |
| Post-holiday (Jan-Feb) | Increase refund abuse monitoring by 50% | Return fraud spikes |

## Model Performance Metrics

| Metric | Formula | Target | Red Flag |
|---|---|---|---|
| Precision | True fraud caught / All flagged orders | > 60% | < 40% |
| Recall | True fraud caught / All actual fraud | > 85% | < 70% |
| False positive rate | Legitimate orders flagged / All legitimate orders | < 3% | > 5% |
| Review rate | Orders sent to manual review / All orders | < 5% | > 10% |
| Auto-decline rate | Auto-declined orders / All orders | < 1% | > 3% |
| Net fraud rate | Undetected fraud losses / Total revenue | < 0.3% | > 0.5% |
