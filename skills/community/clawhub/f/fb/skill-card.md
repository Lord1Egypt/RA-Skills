## Description: <br>
The submitted artifact describes a CreditClaw Amazon shopping and payments skill that lets an agent use guardrailed wallets, owner approval, payment rails, checkout pages, and wallet management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to let an agent register with CreditClaw, check wallet status and spending rules, request owner-approved purchases, and manage checkout, wallet, and sales workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad real-money commerce capabilities, including purchases, payment links, invoices, and storefront workflows. <br>
Mitigation: Keep per-purchase approval enabled, use low spending limits, use a dedicated payment method, and review buyer, shipping, and payment details before enabling purchases or sales. <br>
Risk: The CREDITCLAW_API_KEY can authorize spending actions if exposed or sent to an untrusted domain. <br>
Mitigation: Store the key in protected secret storage and use it only for requests to creditclaw.com API endpoints. <br>
Risk: Encrypted card flows can expose decrypted card details to the main agent context when the sub-agent isolation pattern is unavailable. <br>
Mitigation: Use an ephemeral checkout sub-agent whenever possible, and never store, log, or persist decrypted card details. <br>
Risk: The server title describes a Facebook go-to-market skill, while the artifact content describes CreditClaw Amazon shopping and payments. <br>
Mitigation: Confirm that the release metadata and artifact content refer to the intended skill before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jononovo/fb) <br>
- [CreditClaw Amazon Skill Guide](https://creditclaw.com/amazon/skill.md) <br>
- [CreditClaw Skill Metadata](https://creditclaw.com/amazon/skill.json) <br>
- [Encrypted Card Checkout Guide](https://creditclaw.com/amazon/encrypted-card.md) <br>
- [Stripe x402 Wallet Guide](https://creditclaw.com/amazon/stripe-x402-wallet.md) <br>
- [Spending Permissions Guide](https://creditclaw.com/amazon/spending.md) <br>
- [Wallet Management Guide](https://creditclaw.com/amazon/management.md) <br>
- [Checkout and Sales Guide](https://creditclaw.com/amazon/checkout.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request and response examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may guide payment, wallet, checkout, approval, and sales operations.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact skill.json states 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
