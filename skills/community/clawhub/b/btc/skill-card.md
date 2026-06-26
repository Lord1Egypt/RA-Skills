## Description: <br>
Provides payment wallets, encrypted-card checkout, checkout pages, and spending controls for agents that buy or sell online. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent register for CreditClaw, monitor wallet state, request or make controlled purchases, receive payments through checkout pages or invoices, and follow payment-rail guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad real-money spending authority. <br>
Mitigation: Use strict approval mode, low per-transaction and daily limits, merchant allowlists where possible, and require explicit human confirmation before purchases. <br>
Risk: The skill handles sensitive API keys and delivered card files. <br>
Mitigation: Store CREDITCLAW_API_KEY and card files only in approved secret storage, avoid logging them, and never send the key to domains other than creditclaw.com. <br>
Risk: The encrypted-card flow can expose decrypted payment details if run in the main agent context. <br>
Mitigation: Use the documented ephemeral sub-agent checkout flow and avoid the main-agent decryption fallback except after explicit owner approval. <br>
Risk: Payment links, invoices, fulfillment actions, and checkout flows can trigger external financial or customer-facing effects. <br>
Mitigation: Require explicit confirmation before creating or sending payment requests, invoice emails, purchase confirmations, or fulfillment actions. <br>
Risk: Local decryption-script execution can introduce execution or data-exposure risk. <br>
Mitigation: Inspect or sandbox any decrypt script before running it and remove decrypted artifacts immediately after the approved checkout completes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/codejika/btc) <br>
- [Publisher profile](https://clawhub.ai/user/codejika) <br>
- [CreditClaw shopping skill](https://creditclaw.com/shopping/skill.md) <br>
- [Encrypted card checkout guide](https://creditclaw.com/shopping/encrypted-card.md) <br>
- [Checkout, invoices, and payment links guide](https://creditclaw.com/shopping/checkout.md) <br>
- [Wallet management guide](https://creditclaw.com/shopping/management.md) <br>
- [Heartbeat and status polling guide](https://creditclaw.com/shopping/heartbeat.md) <br>
- [Crossmint wallet purchase guide](https://creditclaw.com/shopping/crossmint-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTTP examples, and JSON request and response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may guide real payment, wallet, invoice, checkout, and card-handling actions through CreditClaw APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
