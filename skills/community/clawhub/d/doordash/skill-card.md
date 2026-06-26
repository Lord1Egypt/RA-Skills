## Description: <br>
A CreditClaw payment and shopping wallet skill published under a DoorDash listing, with guidance for registering an agent wallet, checking spending rules, and making purchases through CreditClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent request, monitor, and spend from CreditClaw wallets for online shopping, SaaS checkout, top-ups, and payment links. It should be treated as a broad payment-wallet skill rather than a DoorDash-only meal-ordering skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing name suggests DoorDash meal ordering, while the artifact describes a broad CreditClaw payment and shopping wallet. <br>
Mitigation: Install only when the intended use is CreditClaw wallet-based shopping or payments, and verify the publisher profile and remote documentation before use. <br>
Risk: The skill requires CREDITCLAW_API_KEY, which can authorize spending from the owner's wallet. <br>
Mitigation: Store the key only in a trusted secrets manager or environment variable, never send it outside creditclaw.com, and rotate or revoke it if exposed. <br>
Risk: The skill can initiate purchases, top-up requests, payment links, and checkout flows that may spend real funds or expose shipping details. <br>
Mitigation: Keep per-purchase approval enabled, set low spending limits and merchant or category allowlists, and require explicit user approval before submitting payment or shipping data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/codejika/doordash) <br>
- [CreditClaw skill entry point](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [CreditClaw prepaid wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [CreditClaw self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
