## Description:

Handles invoice creation, payment link generation, payment status tracking, and automated reminders via Stripe API. Supports multi-currency billing and recurring payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create Stripe payment links and invoices, check payment status, send reminders, manage recurring billing, and process refunds for CashClaw services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful Stripe payment authority, including invoice, subscription, payment link, and refund operations.

Mitigation: Use a restricted Stripe key and require explicit human approval before refunds or subscription changes.

Risk: Stripe credentials can be read from ~/.cashclaw/config.json if no environment variable is set.

Mitigation: Prefer short-lived environment configuration; if a config file is used, lock down file permissions and keep it out of backups and logs.

Risk: The release includes unreviewed npm installation guidance.

Mitigation: Audit and pin npm package versions before installation in production environments.

Risk: Payment and reminder events may be written to local CashClaw ledger and dashboard files.

Mitigation: Restrict access to local CashClaw data files and avoid storing unnecessary customer or payment details.

## Reference(s):

- [Cashclaw Invoicer on ClawHub](https://clawhub.ai/andreataide86/skills/cashclaw-invoicer)
- [Publisher profile](https://clawhub.ai/user/andreataide86)
- [cashclaw npm package](https://www.npmjs.com/package/cashclaw)
- [Stripe invoices API endpoint](https://api.stripe.com/v1/invoices)
- [Stripe payment links API endpoint](https://api.stripe.com/v1/payment_links)
- [Stripe refunds API endpoint](https://api.stripe.com/v1/refunds)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command or API call snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and STRIPE_SECRET_KEY for Stripe operations; may write payment events to local CashClaw ledger files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
