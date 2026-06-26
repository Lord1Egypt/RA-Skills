## Description: <br>
Lets an agent shop online through CreditClaw wallets with owner approval, spending limits, and a required CREDITCLAW_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let an agent register with CreditClaw, check wallet status and spending permissions, and perform approved online purchases or payment-link workflows within owner-defined limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags this as suspicious because the listing understates and misbrands the financial powers it grants. <br>
Mitigation: Verify the CreditClaw and Chase branding before installing, and review the remote guide files before enabling purchases. <br>
Risk: CREDITCLAW_API_KEY functions like a payment credential and could allow spending if exposed. <br>
Mitigation: Store it only in a secure secret store or environment variable, and send it only to creditclaw.com API endpoints. <br>
Risk: The skill can support payment links, x402 payments, subscriptions, and broad online purchases. <br>
Mitigation: Keep approval required for every transaction unless intentionally changed, set low limits and blocked categories, and review activity regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jononovo/chase) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Pre-paid Wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [CreditClaw skill metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash/curl examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and can guide real-money payment actions through CreditClaw APIs.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
