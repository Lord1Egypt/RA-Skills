## Description:

Turn any OpenClaw agent into an AI Fren with their own coin, treasury, and economy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wizsmol](https://clawhub.ai/user/wizsmol)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw agent operators use this skill to onboard an agent into AI Frens, inspect Fren token status, and run wallet-based actions such as balance checks and treasury claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signing authority and transaction commands could spend funds or waste gas if used without review.

Mitigation: Use a dedicated low-value wallet or safer external signing flow, and independently confirm transaction details before signing.

Risk: Onboarding and treasury transaction scripts include placeholder contract addresses.

Mitigation: Replace placeholder addresses with verified deployed contracts before running transaction-writing commands.

Risk: Private keys entered through shell environment variables can be exposed through shell history, logs, or process inspection.

Mitigation: Avoid pasting WALLET_PRIVATE_KEY into shell commands; prefer a secure signing flow or secret manager and clear sensitive environment variables after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wizsmol/skills/aifrens-onboard)
- [AI Frens Platform](https://aifrens.lol)
- [Create an AI Fren](https://aifrens.lol/platform/create)
- [AI Frens FAQ](https://aifrens.lol/platform/faq)
- [x402 Payment Protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require wallet and Base RPC configuration before blockchain reads or transactions.]

## Skill Version(s):

1.0.0 (source: package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
