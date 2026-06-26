# Fraud Prevention Framework — Quality Checklist

## Business Context (6 items)
- [ ] Business model and product categories clearly identified
- [ ] Average order value and monthly volume documented
- [ ] Geographic markets and sales channels specified
- [ ] Current chargeback rate and fraud loss percentage included
- [ ] Primary fraud threat types identified for the vertical
- [ ] Risk tier classification assigned with justification

## Order Screening Rules (8 items)
- [ ] Minimum 8 screening rules defined
- [ ] Each rule has specific trigger conditions (not vague descriptions)
- [ ] Risk score weights assigned to each rule with rationale
- [ ] Action thresholds defined (approve/review/decline) for each score range
- [ ] False positive risks identified for each rule with mitigation strategies
- [ ] Known exceptions documented (legitimate scenarios that trigger rules)
- [ ] Rules cover all major signal categories (payment, identity, geographic, behavioral)
- [ ] Category-specific rules included for high-risk product types

## Velocity Detection (7 items)
- [ ] Velocity rules defined for email, IP, device, shipping address, and payment method
- [ ] Time windows specified for each velocity rule (sliding, not fixed)
- [ ] Both soft thresholds (review) and hard thresholds (block) defined
- [ ] Reset conditions documented for each counter
- [ ] Bypass conditions for verified/whitelisted entities included
- [ ] Failed payment attempt velocity monitoring included
- [ ] Cross-signal velocity checks defined (e.g., same card across accounts)

## Identity Verification (6 items)
- [ ] 3DS2 configuration specified with challenge vs. frictionless triggers
- [ ] Risk-adaptive triggers defined (not blanket on/off)
- [ ] Additional verification methods recommended with trigger conditions
- [ ] Customer friction impact assessed for each verification step
- [ ] Liability shift scenarios documented for 3DS implementations
- [ ] Fallback procedures defined for verification service outages

## Chargeback Response (8 items)
- [ ] Response procedures documented for top 5 reason codes
- [ ] Card-network-specific deadlines included (Visa, Mastercard, Amex, Discover)
- [ ] Required evidence types listed for each reason code
- [ ] Compelling evidence recommendations included for win-rate improvement
- [ ] Expected win rates provided for each reason code with evidence quality
- [ ] Evidence collection automated at transaction time (not after the fact)
- [ ] Escalation procedures defined for pre-arbitration and arbitration
- [ ] Deadline tracking system recommended with alert thresholds

## Monitoring and Alerting (6 items)
- [ ] Key metrics defined with target values and alert thresholds
- [ ] Monitoring frequency specified for each metric (real-time, daily, weekly)
- [ ] Dashboard recommendations included with visualization types
- [ ] Alert escalation procedures defined for threshold breaches
- [ ] Chargeback rate tracked separately by card network
- [ ] False positive rate tracking methodology defined

## Implementation (5 items)
- [ ] Phased rollout plan with clear milestones and dependencies
- [ ] Quick wins identified for immediate chargeback rate reduction
- [ ] Tool/service recommendations included with integration requirements
- [ ] Timeline realistic for team size and technical capabilities
- [ ] Rollback procedures defined for rules that increase false positives

## Optimization (5 items)
- [ ] Review cadence established (weekly, monthly, quarterly reviews)
- [ ] False positive review process documented
- [ ] Seasonal adjustment plan included
- [ ] Benchmarking methodology defined against industry rates
- [ ] Lessons-learned documentation process for chargeback cases

## Compliance and Communication (4 items)
- [ ] PCI DSS compliance considerations addressed
- [ ] Customer communication templates included for declined orders
- [ ] Privacy policy alignment verified for data collection practices
- [ ] Payment processor terms of service requirements referenced
