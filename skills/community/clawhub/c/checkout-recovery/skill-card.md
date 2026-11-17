## Description:

Reduce payment failures and cart abandonment from checkout friction by auditing payment method coverage, error messaging, and retry flow design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, marketplace sellers, and growth teams use this skill to audit checkout payment coverage, friction points, error copy, and abandoned checkout recovery sequences. The skill produces a structured remediation plan for improving checkout completion across target markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-method market data and integration options can become stale or vary by seller geography.

Mitigation: Verify current payment-method coverage and integration options with the seller's payment provider before changing checkout configuration.

Risk: Recovery email, SMS, or push recommendations can create consent, unsubscribe, or privacy issues if applied without controls.

Mitigation: Use only necessary checkout data and confirm opt-in, unsubscribe, and retention requirements before launching recovery sequences.

## Reference(s):

- [Output Template](artifact/references/output-template.md)
- [Payment Methods by Market](artifact/references/payment-methods-by-market.md)
- [Error Message Copy Guide](artifact/references/error-message-copy-guide.md)
- [Recovery Checklist](artifact/assets/recovery-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables, prioritized recommendations, copy templates, and checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on seller-provided checkout metrics, market, platform, payment methods, and recovery-channel details.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
