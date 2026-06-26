## Description: <br>
InstaClaw is a CreditClaw wallet skill that helps an agent make grocery and other online purchases through Stripe-powered payment rails under owner spending controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to register and operate a CreditClaw wallet, check balances and spending permissions, request top-ups, and make owner-controlled online purchases such as groceries or other supported merchant payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad real-money payment wallet capabilities, not only grocery ordering. <br>
Mitigation: Install only when that payment authority is intended, keep human approval enabled, and set strict dollar, merchant, and category limits. <br>
Risk: A leaked CREDITCLAW_API_KEY could expose wallet spending authority. <br>
Mitigation: Store CREDITCLAW_API_KEY as a secret and use it only for requests to creditclaw.com. <br>
Risk: Payment links, self-hosted cards, and x402 or agent-to-agent payments expand the active payment surface. <br>
Mitigation: Review the live CreditClaw documentation and enable only the payment rails needed for the intended task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codejika/cart) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Pre-paid wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated wallet and payment endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
