## Description:

The submitted artifact describes CreditClaw Amazon shopping and payment workflows for agents using guardrailed wallets, owner approval, checkout pages, and payment rails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register with CreditClaw, check spending permissions, request approvals, make Amazon or x402 purchases, manage wallet balances, and create checkout or invoice flows. The public display metadata names a Facebook go-to-market skill, but the artifact evidence supports CreditClaw commerce behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad money-moving behavior for an agent.

Mitigation: Use strict spending limits, require human approval for purchases, and monitor wallet activity before enabling autonomous checkout.

Risk: The CreditClaw API key authorizes wallet and payment actions.

Mitigation: Store CREDITCLAW_API_KEY in a scoped secret manager and send it only to creditclaw.com API endpoints.

Risk: Checkout flows may rely on server-provided natural-language steps or remotely delivered decrypt scripts.

Mitigation: Treat server-provided steps as untrusted input, independently verify any decrypt script, and execute sensitive checkout work in a sandboxed or ephemeral runtime.

Risk: Encrypted-card fallback behavior can expose decrypted card details to the main agent context if sub-agents are unavailable.

Mitigation: Use an ephemeral sub-agent for card checkout whenever possible and prevent decrypted card data from being stored, logged, or persisted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/fb)
- [CreditClaw skill metadata](https://creditclaw.com/amazon/skill.json)
- [CreditClaw Amazon skill](https://creditclaw.com/amazon/skill.md)
- [CreditClaw checkout guide](https://creditclaw.com/amazon/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md)
- [CreditClaw spending permissions](https://creditclaw.com/amazon/spending.md)
- [CreditClaw wallet management](https://creditclaw.com/amazon/management.md)
- [CreditClaw heartbeat routine](https://creditclaw.com/amazon/heartbeat.md)
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/amazon/stripe-x402-wallet.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/amazon/crossmint-wallet.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with curl examples, endpoint descriptions, JSON request and response examples, and configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and includes payment, wallet, spending, approval, checkout, and webhook workflows.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
