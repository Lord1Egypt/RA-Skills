## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent shop online, request wallet top-ups, create payment links, and pay through CreditClaw payment rails while following owner-set spending limits and approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real shopping, spending, top-up request, payment-link, and x402 payment abilities. <br>
Mitigation: Start with ask-for-everything approval, keep low per-transaction and daily limits, restrict merchants or categories where possible, and review payment-link, heartbeat, and x402 settings before enabling them. <br>
Risk: A leaked CREDITCLAW_API_KEY could allow unauthorized use of the connected CreditClaw account. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secrets manager, send it only to creditclaw.com API endpoints, and avoid logging request headers or bodies that may contain credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TripleHippo/card) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [Skill registration and API reference](https://creditclaw.com/creditcard/skill.md) <br>
- [General shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Amazon purchase guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [Pre-paid wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat and status guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [Machine-readable skill metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
2.3.1 (source: frontmatter and skill.json); release metadata version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
