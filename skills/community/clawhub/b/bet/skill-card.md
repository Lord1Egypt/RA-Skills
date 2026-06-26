## Description: <br>
Let an agent use CreditClaw payment rails for Amazon shopping, wallet spending, checkout pages, invoices, payment links, and storefront operations under owner-configured approval controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent make owner-approved purchases, monitor balances and spending rules, request top-ups, and create payment collection surfaces through CreditClaw APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real-money payment actions beyond Amazon shopping, including wallet spending, invoices, payment links, and storefront operations. <br>
Mitigation: Install only when broad CreditClaw commerce authority is intended, keep approval required for purchases, and verify merchant, domain, category, and spending limits before use. <br>
Risk: API key or card handling mistakes could expose spending authority or decrypted payment details. <br>
Mitigation: Store CREDITCLAW_API_KEY and card files in a secure secret store, send the API key only to creditclaw.com, and avoid the main-agent card-decryption fallback with real cards. <br>
Risk: Delivered checkout or decrypt scripts may handle sensitive payment data. <br>
Mitigation: Review any delivered decrypt script before execution and prefer the documented ephemeral sub-agent flow so decrypted card details do not persist in the main context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/bet) <br>
- [CreditClaw Amazon skill](https://creditclaw.com/amazon/skill.md) <br>
- [CreditClaw checkout guide](https://creditclaw.com/amazon/checkout.md) <br>
- [CreditClaw encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md) <br>
- [CreditClaw spending permissions](https://creditclaw.com/amazon/spending.md) <br>
- [CreditClaw wallet management](https://creditclaw.com/amazon/management.md) <br>
- [CreditClaw Stripe x402 wallet](https://creditclaw.com/amazon/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and external CreditClaw service access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
