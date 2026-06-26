## Description: <br>
Easy-to-use agentic wallets powered by Stripe for agent purchases and A2A payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give agents a CreditClaw wallet for guarded online purchases, top-ups, payment links, and x402 or agent-to-agent payments within owner controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real payment and shopping authority through CreditClaw. <br>
Mitigation: Keep ask-for-everything approval enabled or set very low limits, restrict merchants and categories, and verify purchase details before submitting requests. <br>
Risk: A leaked CREDITCLAW_API_KEY could let someone else act as the agent and spend funds. <br>
Mitigation: Store the key only in a secrets manager or protected environment variable and send it only to creditclaw.com API endpoints. <br>
Risk: The public Stripe/x402 framing does not fully describe the broader CreditClaw purchasing behavior. <br>
Mitigation: Install only when the intended use includes shopping and payment execution, and review the payment rail guides before enabling the skill. <br>
Risk: Shopping flows may expose sensitive shipping addresses, merchant details, or payment links. <br>
Mitigation: Treat shipping addresses and payment links as sensitive, and avoid sharing them outside the intended merchant or owner approval flow. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/codejika/account) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Shopping guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Pre-paid Wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [Skill metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown instructions with curl examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated wallet, spending, payment, and shopping operations.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata; artifact frontmatter states 2.3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
