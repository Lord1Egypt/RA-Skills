## Description:

Let your agent shop tickets online with owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register for a CreditClaw wallet, check spending permissions, and initiate guarded online purchases with owner oversight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent controlled access to real-money purchasing and payment workflows.

Mitigation: Keep per-transaction and daily limits low, require owner approval for purchases unless the use case is narrow, and monitor wallet activity.

Risk: The financial scope is broader than the headline suggests because the artifact documents wallets, cards, payment links, and multiple payment rails.

Mitigation: Review enabled rails before use and disable or avoid rails that are not needed for the intended task.

Risk: Downloaded remote guide files could change after installation.

Mitigation: Review remote guides before use and do not rely on unreviewed downloaded files for payment decisions.

Risk: Exposure of CREDITCLAW_API_KEY could allow unauthorized wallet actions.

Mitigation: Store the API key in a secrets manager and only send it to CreditClaw API endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/chase)
- [CreditClaw Homepage](https://creditclaw.com)
- [CreditClaw Skill and API Reference](https://creditclaw.com/creditcard/skill.md)
- [CreditClaw Heartbeat Routine](https://creditclaw.com/creditcard/heartbeat.md)
- [CreditClaw Shopping Guide](https://creditclaw.com/creditcard/shopping.md)
- [CreditClaw Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [CreditClaw Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
