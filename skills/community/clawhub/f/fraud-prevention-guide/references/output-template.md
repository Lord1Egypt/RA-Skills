# Fraud Prevention Framework — Output Template

Use this template to structure the fraud prevention deliverable for the seller.

## 1. Executive Summary

- **Business profile:** [Business type, product categories, AOV, monthly volume]
- **Current fraud metrics:** [Chargeback rate, fraud loss %, false positive rate if known]
- **Risk tier:** [Low / Medium / High / Critical]
- **Primary fraud threats:** [Top 3 fraud types for this business]
- **Projected impact:** [Expected chargeback rate reduction, estimated revenue recovery]

## 2. Order Screening Rules

For each rule, document:

### Rule [Number]: [Rule Name]

| Field | Value |
|---|---|
| **Trigger condition** | [Specific conditions that activate this rule] |
| **Risk score weight** | [Points added to order risk score, e.g., +15] |
| **Action at threshold** | [Approve / Manual Review / Decline] |
| **Rationale** | [Why this rule matters for this business] |
| **False positive risk** | [Low / Medium / High — with mitigation] |
| **Exceptions** | [Known legitimate scenarios that may trigger this rule] |

Repeat for each screening rule (typically 8-15 rules per framework).

## 3. Velocity Detection Rules

### Rule [Number]: [Signal Type] Velocity

| Field | Value |
|---|---|
| **Signal** | [Email / IP / Device / Shipping Address / Payment Method] |
| **Time window** | [e.g., 1 hour, 24 hours, 7 days] |
| **Soft threshold** | [Count that triggers manual review] |
| **Hard threshold** | [Count that triggers automatic block] |
| **Reset conditions** | [When the counter resets or reduces] |
| **Bypass conditions** | [Verified customers, whitelisted entities] |

## 4. Identity Verification Configuration

### 3D Secure 2.0 Settings

| Scenario | Flow Type | Trigger Conditions |
|---|---|---|
| [Scenario name] | Challenge / Frictionless / Exempt | [Specific conditions] |

### Additional Verification Methods

| Method | Trigger | Implementation |
|---|---|---|
| Email verification | [When triggered] | [How implemented] |
| Phone verification | [When triggered] | [How implemented] |
| Device fingerprinting | [When triggered] | [How implemented] |
| Document verification | [When triggered] | [How implemented] |

## 5. Chargeback Response Playbook

### Reason Code: [Code] — [Description]

| Field | Value |
|---|---|
| **Card network** | [Visa / Mastercard / Amex / Discover] |
| **Response deadline** | [Days from notification] |
| **Required evidence** | [List of required documentation] |
| **Compelling evidence** | [Additional evidence that improves win rate] |
| **Expected win rate** | [Percentage based on evidence quality] |
| **Template reference** | [Link to evidence letter template] |

## 6. Monitoring Dashboard Metrics

| Metric | Target | Alert Threshold | Frequency |
|---|---|---|---|
| Chargeback rate (Visa) | < 0.65% | > 0.75% | Daily |
| Chargeback rate (MC) | < 0.50% | > 0.60% | Daily |
| False positive rate | < 3% | > 5% | Weekly |
| Manual review queue | < 50 orders | > 100 orders | Real-time |
| Fraud loss rate | < 0.3% | > 0.5% | Weekly |
| Average review time | < 15 min | > 30 min | Daily |
| Rule trigger distribution | Balanced | Any rule > 40% of flags | Weekly |

## 7. Implementation Timeline

| Phase | Tasks | Duration | Dependencies |
|---|---|---|---|
| Phase 1: Quick wins | [Basic screening rules, AVS/CVV config] | Week 1-2 | Payment processor access |
| Phase 2: Detection | [Velocity rules, device fingerprinting] | Week 3-4 | Fraud tool integration |
| Phase 3: Verification | [3DS2 setup, identity verification] | Week 5-6 | 3DS provider account |
| Phase 4: Response | [Chargeback playbook, evidence templates] | Week 7-8 | Historical chargeback data |
| Phase 5: Optimization | [Dashboard setup, rule tuning] | Ongoing | 30+ days of data |

## 8. Review Cadence

| Review Type | Frequency | Participants | Focus Areas |
|---|---|---|---|
| Rule performance | Weekly | Fraud analyst | False positive rate, blocked order review |
| Chargeback analysis | Bi-weekly | Fraud + Finance | Win rates, new patterns, reason code trends |
| Threshold tuning | Monthly | Fraud + Product | Seasonal adjustments, category changes |
| Full framework review | Quarterly | Cross-functional | Strategy alignment, tool evaluation, ROI |
