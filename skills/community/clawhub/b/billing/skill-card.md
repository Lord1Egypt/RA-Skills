## Description:

Build payment integrations, subscription management, and invoicing systems with webhook handling, tax compliance, and revenue recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement and debug payment processing, subscription lifecycle logic, invoicing, tax handling, marketplace payments, disputes, usage billing, and revenue recognition workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable payment examples could be used directly for high-impact billing actions such as charges, refunds, invoices, subscription changes, or connected-account updates.

Mitigation: Use Stripe or Paddle test mode first and require explicit human approval before applying any payment-impacting action.

Risk: Some examples may not provide enough production guardrails for webhooks, refunds, and billing arithmetic.

Mitigation: Replace examples with durable, audited implementations that verify webhook signatures, use idempotency and transactions, and store money in integer minor units.

Risk: Billing, tax, PCI, and revenue-recognition guidance can create compliance exposure if applied without domain review.

Mitigation: Review the resulting implementation with qualified finance, tax, security, or legal owners before production use.

## Reference(s):

- [ClawHub Billing skill](https://clawhub.ai/ivangdavila/skills/billing)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [EU VIES VAT validation API](https://ec.europa.eu/taxation_customs/vies/rest-api/check-vat-number)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, tables, checklists, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory billing implementation patterns that should be reviewed before payment-impacting use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
