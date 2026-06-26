---
name: Fraud Prevention Guide
description: Build an ecommerce fraud prevention framework covering chargeback mitigation, order screening rules, and identity verification.
---

# Fraud Prevention Guide

Build a layered ecommerce fraud prevention framework tailored to your business model, product category, and risk profile — covering automated order screening rules, chargeback representment strategies, identity verification workflows, and velocity-based detection systems.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Risk scoring model | Multi-signal weighted score combining AVS, CVV, velocity, device fingerprint, and behavioral data | Basic rule-based screening with AVS + CVV checks | Single-factor checks (e.g., only AVS match) |
| Order screening thresholds | Dynamic thresholds calibrated per product category with auto-adjustment based on false positive rates | Static thresholds reviewed quarterly with manual override capability | Fixed thresholds applied uniformly across all product types |
| Velocity detection | Real-time velocity checks across email, IP, device, shipping address, and payment method with sliding windows | Hourly batch checks on email and IP with daily aggregation | No velocity monitoring or only daily batch reviews |
| Identity verification | Risk-adaptive 3DS2 with step-up authentication, device fingerprinting, and biometric options | Mandatory 3DS for orders above a fixed threshold | No identity verification or blanket 3DS on all orders |
| Chargeback representment | Automated evidence collection with card-network-specific templates and win-rate tracking per reason code | Manual evidence gathering with generic templates submitted within deadline | No representment process or missed response deadlines |
| Address verification | Multi-source address validation cross-referencing billing, shipping, and IP geolocation with distance scoring | Basic AVS match check with manual review for mismatches | No address verification beyond payment processor default |

## Solves

1. **Rising chargeback rates** threatening payment processor account standing and incurring penalty fees
2. **Account takeover attacks** where fraudsters use stolen credentials to place orders on legitimate customer accounts
3. **Friendly fraud** where legitimate customers dispute valid charges to get free products
4. **Card testing attacks** where stolen card numbers are validated through small test purchases before larger fraud
5. **Refund abuse schemes** exploiting return policies through serial returns, wardrobing, or false item-not-received claims
6. **High false positive rates** where overly aggressive fraud rules block legitimate customers and reduce revenue
7. **Cross-border fraud complexity** requiring different screening rules for international orders with varying risk profiles

## Workflow

### Step 1: Business Risk Assessment
Analyze the seller's business model, product categories, average order value, sales channels, geographic markets, and current fraud indicators. Identify the specific fraud types most relevant to their vertical (e.g., electronics face more card-not-present fraud; digital goods face more account takeover).

### Step 2: Order Screening Rule Design
Create a layered set of order screening rules with weighted risk scores. Each rule should have a clear threshold, action (approve/review/decline), and rationale. Rules should cover: billing-shipping address mismatch, order value anomalies, email domain risk, IP geolocation mismatch, device fingerprint anomalies, and payment method risk signals.

### Step 3: Velocity Detection Configuration
Design velocity-based detection rules that catch rapid-fire fraudulent orders. Define sliding time windows and thresholds for: orders per email address, orders per IP address, orders per device fingerprint, orders per shipping address, and failed payment attempts. Include both hard blocks and soft flags for manual review.

### Step 4: Identity Verification Strategy
Recommend appropriate identity verification tools based on the seller's risk tolerance and customer friction budget. Cover 3D Secure 2.0 configuration (challenge-based vs. frictionless), device fingerprinting integration, email verification services, phone verification for high-risk orders, and biometric authentication options.

### Step 5: Chargeback Response Playbook
Build a chargeback response framework with evidence templates for each major reason code (fraud, product not received, product not as described, duplicate charge, subscription cancellation). Include timeline requirements for each card network (Visa, Mastercard, Amex, Discover), required evidence types, and win-rate optimization strategies.

### Step 6: Monitoring and Alerting Setup
Design a fraud monitoring dashboard with key metrics: chargeback rate by card network, false positive rate, manual review queue size, fraud loss by category, and screening rule performance. Define alert thresholds for chargeback rate spikes, unusual order velocity patterns, and new fraud pattern detection.

### Step 7: Continuous Optimization
Establish a review cadence for fraud rule tuning. Analyze blocked orders for false positives, review chargebacks for missed fraud patterns, adjust thresholds based on seasonal trends, and benchmark against industry fraud rates. Document lessons learned from each chargeback case.

## Example 1: Consumer Electronics Store

**Input:**
- Business: Consumer electronics on Shopify, AOV $180, 2,000 orders/month
- Markets: 85% US, 15% international
- Current fraud rate: 1.2% chargeback rate (above Visa threshold)
- Pain points: Frequent billing/shipping mismatches, suspected card testing on low-value accessories

**Output Framework:**

**Order Screening Rules:**
- Flag orders where billing country ≠ shipping country AND order value > $150 → Manual review
- Auto-decline orders where billing ZIP fails AVS AND CVV fails AND order value > $300
- Flag orders with free email domains (gmail, yahoo) AND new customer AND order value > $500 → Manual review
- Auto-decline orders with shipping to freight forwarders when combined with any other risk signal
- Flag orders with expedited shipping AND new customer AND order value > 2x AOV → Manual review

**Velocity Rules (sliding windows):**
- Same email: >3 orders in 24 hours → Block; >2 orders in 1 hour → Manual review
- Same IP: >5 orders in 1 hour → Block; >3 orders in 30 minutes → Manual review
- Same shipping address: >3 orders in 48 hours from different payment methods → Block
- Failed payment attempts: >5 failures in 10 minutes from same IP → Block IP for 24 hours

**Identity Verification:**
- 3DS2 challenge flow for: international orders > $200, orders with 2+ risk signals, new customers with order > $400
- Frictionless 3DS2 for: returning customers with consistent device fingerprint, orders < $100 with clean signals
- Email verification required for: all new accounts, orders to new shipping addresses on existing accounts

**Chargeback Representment Priority:**
- Reason Code 10.4 (Fraud): Submit device fingerprint data, IP geolocation, delivery confirmation with signature, customer communication logs. Expected win rate: 35-45%
- Reason Code 13.1 (Not Received): Submit carrier tracking with delivery confirmation, GPS delivery photo if available, signed delivery receipt. Expected win rate: 65-75%

## Example 2: Digital Products Marketplace

**Input:**
- Business: Digital course marketplace, AOV $45, 8,000 orders/month
- Markets: Global (40% US, 25% EU, 20% Asia, 15% other)
- Current fraud rate: 0.6% chargeback rate
- Pain points: Account takeover on high-value course bundles, refund abuse on downloadable content

**Output Framework:**

**Order Screening Rules:**
- Auto-approve orders < $30 from returning customers with consistent device fingerprint
- Flag orders for course bundles > $200 from new accounts created < 24 hours ago → Email verification required
- Auto-decline orders from IP addresses on known proxy/VPN lists when combined with new account AND order > $100
- Flag orders using prepaid cards for amounts > $150 → Additional verification
- Monitor accounts purchasing and immediately refunding → Flag after 2 refund requests in 30 days

**Account Security:**
- Mandatory 2FA for accounts with lifetime spend > $500
- Login anomaly detection: alert on new device + new location + password change in 24-hour window
- Session management: force re-authentication for payment method changes and high-value purchases
- Account lockout after 5 failed login attempts with CAPTCHA reset

**Velocity Rules:**
- Same account: >5 purchases in 1 hour → Temporary hold + email verification
- Same payment method across accounts: >3 different accounts using same card in 24 hours → Block card
- Download velocity: >20 downloads in 1 hour from same IP → Rate limit + account review
- Refund requests: >3 in 30 days → Restrict to store credit only + manual review

**Refund Abuse Prevention:**
- Track download completion before allowing refund requests
- Require reason code for all refund requests with follow-up survey
- Implement progressive refund policy: instant for first refund, 48-hour review for subsequent
- Flag serial refunders: >30% refund rate over 90 days → Restrict purchasing privileges

## Common Mistakes

1. **Setting thresholds too aggressively** — Blocking all orders with any risk signal creates excessive false positives. A $200 order from a new customer with a billing/shipping mismatch might be a legitimate gift purchase. Use weighted scoring rather than binary block rules.

2. **Ignoring false positive costs** — Every blocked legitimate order has a revenue cost plus customer lifetime value loss. Track your false positive rate alongside your fraud rate. The optimal fraud prevention system minimizes total loss (fraud + false positives), not just fraud alone.

3. **Using the same rules for all product categories** — A $20 phone case and a $2,000 laptop have fundamentally different risk profiles. Fraudsters target high-value, easily resalable items. Build category-specific screening rules with appropriate thresholds for each product tier.

4. **Not tracking chargeback reason codes separately** — Fraud chargebacks (10.4) and product-not-received chargebacks (13.1) require completely different prevention and representment strategies. Lumping all chargebacks together prevents targeted improvement.

5. **Skipping 3DS2 frictionless flow configuration** — Many sellers implement 3DS as all-or-nothing. The frictionless flow allows low-risk transactions to pass through without customer friction while still shifting liability to the issuing bank. Configure risk-based 3DS triggers rather than blanket rules.

6. **No velocity monitoring on payment failures** — Card testing attacks generate many small failed transactions before a successful one. Without velocity checks on failed attempts, you miss the testing phase and only catch the resulting fraud after it succeeds.

7. **Missing chargeback response deadlines** — Each card network has strict response windows (Visa: 30 days, Mastercard: 45 days). Missing these deadlines means automatic loss regardless of evidence quality. Implement automated deadline tracking with escalation alerts.

8. **Not adapting rules for seasonal patterns** — Holiday shopping naturally increases orders from new customers, gift shipping to different addresses, and expedited shipping requests. Static fraud rules tuned for normal periods will generate excessive false positives during peak seasons. Build seasonal rule variants.

## Resources

- [Output Template](references/output-template.md) — Standard framework document structure for fraud prevention deliverables
- [Chargeback Response Guide](references/chargeback-response-guide.md) — Card-network-specific representment procedures, evidence requirements, and timeline reference
- [Risk Scoring Model Reference](references/risk-scoring-reference.md) — Signal weighting methodology and threshold calibration guide
- [Quality Checklist](assets/quality-checklist.md) — Comprehensive review checklist for fraud prevention frameworks
