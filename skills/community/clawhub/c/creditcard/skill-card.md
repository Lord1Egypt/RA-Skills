## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register for a CreditClaw wallet, check spending permissions, request top-ups, create payment links, and make guarded online purchases across supported payment rails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad financial powers, including purchases, checkout requests, payment links, top-up requests, and x402 signing.

Mitigation: Install only after manual review, use a dedicated CreditClaw API key, keep human approval enabled by default, and set conservative transaction, daily, and monthly limits.

Risk: API key exposure could allow unauthorized spending through the CreditClaw account.

Mitigation: Store CREDITCLAW_API_KEY in a secure secrets manager and use it only with CreditClaw API requests.

Risk: Automated spending may occur at unintended merchants or categories if guardrails are too broad.

Mitigation: Use narrow merchant, domain, and category allowlists, block high-risk categories, and check spending permissions before purchase actions.

Risk: Successful purchase, checkout, and x402 signing calls can create real financial transactions.

Mitigation: Treat payment and signing endpoints as live financial actions, prefer preflight checks where available, and require owner approval for higher-risk or unfamiliar purchases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/creditcard)
- [Publisher Profile](https://clawhub.ai/user/jononovo)
- [CreditClaw Homepage](https://creditclaw.com)
- [CreditClaw API Base](https://creditclaw.com/api/v1)
- [CreditClaw Skill Guide](https://creditclaw.com/creditcard/skill.md)
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md)
- [Skill Metadata](https://creditclaw.com/creditcard/skill.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and uses CreditClaw API endpoints for wallet, purchase, payment-link, status, and approval workflows.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
