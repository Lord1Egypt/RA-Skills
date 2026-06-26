## Description: <br>
Build payment integrations, subscription management, and invoicing systems with webhook handling, tax compliance, and revenue recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement or debug payment processing, subscription lifecycle, invoicing, tax, marketplace, dispute, and revenue-recognition workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Billing snippets could be adapted to live charges, refunds, subscription changes, or payout flows. <br>
Mitigation: Use test credentials first and require explicit authorization before applying changes against live payment-provider accounts. <br>
Risk: Payment-provider credentials and webhook endpoints can create financial or account-access exposure if configured too broadly. <br>
Mitigation: Scope credentials tightly, verify webhook signatures, store event IDs for idempotency, and process raw webhook bodies for signature checks. <br>
Risk: Handling raw card or unnecessary KYC data can increase compliance and privacy obligations. <br>
Mitigation: Use tokenized payment methods, avoid storing PAN or CVV, and retain only the customer and billing data needed for the workflow. <br>
Risk: Tax, invoicing, and revenue-recognition examples may not match every jurisdiction or contract. <br>
Mitigation: Have finance, tax, or legal reviewers confirm jurisdiction-specific rules before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/billing) <br>
- [Billing Skill Definition](artifact/SKILL.md) <br>
- [Stripe Integration](artifact/stripe.md) <br>
- [Webhooks and Events](artifact/webhooks.md) <br>
- [Subscription Lifecycle](artifact/subscriptions.md) <br>
- [Invoice Generation](artifact/invoicing.md) <br>
- [Tax Compliance](artifact/tax.md) <br>
- [Usage-Based Billing](artifact/usage-billing.md) <br>
- [Chargebacks and Disputes](artifact/disputes.md) <br>
- [Marketplace Payments](artifact/marketplace.md) <br>
- [Revenue Recognition](artifact/revenue-recognition.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with code examples and implementation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only reference skill; no required binaries are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
