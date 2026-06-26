## Description: <br>
Provides agentic wallets powered by Stripe and CreditClaw so an agent can make online purchases, payments, and wallet checks under owner-controlled guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to equip an agent with a CreditClaw payment wallet for shopping, SaaS payments, x402 payments, balance checks, and owner approval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to spend real money through CreditClaw. <br>
Mitigation: Start with approval required for every purchase, set low spending limits, and use merchant or category allowlists before granting broader autonomy. <br>
Risk: The required CREDITCLAW_API_KEY functions like a payment credential. <br>
Mitigation: Store the key in a secure secret manager, send it only to creditclaw.com API endpoints, and rotate or revoke it if exposure is suspected. <br>
Risk: Marketplace and skill identities are inconsistent enough to require review before installation. <br>
Mitigation: Verify the ClawHub publisher profile, the release page, and the creditclaw.com domain before using the skill. <br>
Risk: Untrusted callback URLs or unnecessary shipping data can expand exposure. <br>
Mitigation: Use only trusted HTTPS callback URLs and provide shipping or personal data only when needed for the approved purchase. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/codejika/eat) <br>
- [Publisher Profile](https://clawhub.ai/user/codejika) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw API Base](https://creditclaw.com/api/v1) <br>
- [CreditClaw Skill Guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Amazon Guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [Skill Metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
