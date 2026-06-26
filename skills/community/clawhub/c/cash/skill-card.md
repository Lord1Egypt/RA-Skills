## Description: <br>
Easy-to-use agentic wallets powered by Stripe for agent purchases, A2A payments, checkout pages, top-ups, and guarded card-based spending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to give agents controlled real-money spending ability through CreditClaw wallets, encrypted-card checkout, x402-style wallet flows, payment links, invoices, and storefront operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad real-money spending, card-handling, and personal-data authority. <br>
Mitigation: Install only when the agent should have controlled spending ability; keep ask-for-everything approval enabled, set low limits, and require explicit confirmation before orders, invoices, payment links, public shop changes, or top-up requests. <br>
Risk: A leaked CreditClaw API key could allow unauthorized wallet actions. <br>
Mitigation: Use a dedicated API key stored in a secrets manager and send it only to CreditClaw API endpoints. <br>
Risk: Encrypted-card checkout can expose decrypted card details if handled in the main agent context or persisted in logs or files. <br>
Mitigation: Use the ephemeral sub-agent checkout flow, avoid main-agent card decryption, never store or log decrypted card data, and keep encrypted card files in a restricted non-synced location. <br>
Risk: Remote or delivered scripts and files may affect payment behavior. <br>
Mitigation: Inspect remotely fetched or delivered scripts before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jononovo/cash) <br>
- [CreditClaw Skill Guide](https://creditclaw.com/stripe/skill.md) <br>
- [CreditClaw Checkout Guide](https://creditclaw.com/stripe/checkout.md) <br>
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/stripe/encrypted-card.md) <br>
- [CreditClaw Management Guide](https://creditclaw.com/stripe/management.md) <br>
- [CreditClaw Spending Permissions Guide](https://creditclaw.com/stripe/spending.md) <br>
- [CreditClaw Skill Metadata](https://creditclaw.com/stripe/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, JSON payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact skill metadata reports creditclaw-stripe 2.3.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
