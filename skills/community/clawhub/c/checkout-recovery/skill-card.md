## Description: <br>
Reduce payment failures and cart abandonment from checkout friction by auditing payment method coverage, error messaging, and retry flow design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, consultants, and growth teams use this skill to audit checkout payment coverage, error messaging, UX friction, and abandoned-checkout recovery flows, then produce a prioritized recovery roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkout audits may involve sensitive customer, payment, or funnel data. <br>
Mitigation: Use aggregated or redacted checkout metrics where possible and avoid sharing raw customer PII or payment details. <br>
Risk: Recommended PSP, checkout, SMS, email, or discount changes can affect revenue, compliance, and customer experience. <br>
Mitigation: Require human approval before applying recommended payment provider, checkout flow, messaging, or discount changes. <br>
Risk: Payment method coverage and market-share references can become outdated or vary by merchant segment. <br>
Mitigation: Verify current market data with the merchant's PSP or local payment provider before making integration decisions. <br>


## Reference(s): <br>
- [Checkout Recovery skill page](https://clawhub.ai/leooooooow/checkout-recovery) <br>
- [Output Template - Checkout Recovery Audit](references/output-template.md) <br>
- [Payment Methods by Market - Ecommerce Reference](references/payment-methods-by-market.md) <br>
- [Error Message Copy Guide - Checkout Recovery](references/error-message-copy-guide.md) <br>
- [Checkout Recovery - Audit Quality Checklist](assets/recovery-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report with tables, severity ratings, prioritized recommendations, and recovery copy templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a three-section Payment Coverage Gap Report, Friction Audit, and Recovery Roadmap; may include checkout error copy and abandoned-checkout message templates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
