## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users authorize agents to make online purchases and payments through CreditClaw wallets with spending limits, owner approvals, and order tracking. The skill guides agents through registration, wallet status checks, purchasing flows, payment signing, and top-up or tracking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real-money purchasing authority across wallet, card, payment-link, and x402 payment flows. <br>
Mitigation: Install only when that authority is intended; start with ask-for-everything approval, low spending limits, and merchant or domain allowlists. <br>
Risk: Broad autonomous spending and payment signing can create financial loss if limits, approvals, or allowed merchants are too permissive. <br>
Mitigation: Review guardrails before use, avoid enabling payment links, self-hosted cards, Sub-Agent Cards, or x402 unless needed, and monitor owner-visible activity. <br>
Risk: API keys, webhook secrets, shipping data, tracking data, or X-PAYMENT headers may expose financial authority or sensitive personal information if leaked. <br>
Mitigation: Store secrets in a secure secret manager, send the CreditClaw API key only to creditclaw.com endpoints, and keep sensitive values out of prompts and logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TripleHippo/apple) <br>
- [Publisher profile](https://clawhub.ai/user/TripleHippo) <br>
- [CreditClaw skill documentation](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [CreditClaw Amazon purchase guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [CreditClaw pre-paid wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [CreditClaw self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [CreditClaw skill metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
