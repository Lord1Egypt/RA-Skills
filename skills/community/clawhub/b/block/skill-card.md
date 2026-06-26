## Description: <br>
Block for OpenClaw gives agents CreditClaw payment workflows for guarded purchases, wallet management, payment requests, and owner-controlled spending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can equip an OpenClaw agent to spend from CreditClaw payment rails, request top-ups, check wallet status, follow spending rules, and create payment links or selling flows under owner controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real-money spending and seller-payment workflows beyond a narrow Amazon shopping use case. <br>
Mitigation: Install only when broad CreditClaw payment workflows are intended; keep per-purchase approval enabled and restrict merchant, domain, category, and spending permissions. <br>
Risk: CREDITCLAW_API_KEY acts like a payment credential and could enable unauthorized spending if exposed. <br>
Mitigation: Store the key in a secure secret manager, send it only to creditclaw.com API endpoints, and rotate or revoke it if exposure is suspected. <br>
Risk: Encrypted-card checkout can expose decrypted card details to the main agent if the fallback non-sub-agent flow is used. <br>
Mitigation: Use an ephemeral checkout sub-agent for card decryption and purchase completion, and never store, log, or persist decrypted card data. <br>
Risk: Delivered card files and decrypt scripts introduce sensitive local artifacts and executable handling. <br>
Mitigation: Inspect or sandbox delivered decrypt scripts and companion files before use, and keep card files in a protected location with least-privilege access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jononovo/block) <br>
- [CreditClaw Amazon skill guide](https://creditclaw.com/amazon/skill.md) <br>
- [Encrypted Card checkout guide](https://creditclaw.com/amazon/encrypted-card.md) <br>
- [Crossmint Wallet purchase guide](https://creditclaw.com/amazon/crossmint-wallet.md) <br>
- [Wallet management guide](https://creditclaw.com/amazon/management.md) <br>
- [Spending permissions guide](https://creditclaw.com/amazon/spending.md) <br>
- [Heartbeat status guide](https://creditclaw.com/amazon/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and uses CreditClaw API endpoints for payment, wallet, approval, and status workflows.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
