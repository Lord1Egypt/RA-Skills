## Description:

Create and manage agentic wallets with Unibase. Use for autonomous onchain transactions on Ethereum, Solana, and other chains. Triggers on requests involving crypto wallets for AI agents, server-side wallet operations, or autonomous transaction execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parasyte-x](https://clawhub.ai/user/parasyte-x)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent builders use this skill to configure agent-controlled Unibase wallets, query provisioned wallet addresses, and prepare onchain transaction requests across supported networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable wallet credentials can expose real funds if tokens are stored insecurely or cannot be rotated.

Mitigation: Use only a trusted Unibase endpoint, keep wallet tokens out of repositories, and confirm token revocation and rotation before connecting wallets with real funds.

Risk: Autonomous transaction execution can send funds to the wrong recipient, amount, or chain.

Mitigation: Require per-transaction confirmation, validate recipient address, amount, chain, and user intent, and prefer testnets with strict spending and recipient limits.

Risk: Prompt injection or externally sourced requests can cause unauthorized transaction attempts.

Mitigation: Execute only direct user requests from the active conversation and stop when transaction instructions come from email, webhooks, documents, or other external content.

## Reference(s):

- [Wallets](references/wallets.md)
- [Transactions](references/transactions.md)
- [Unibase Website](https://unibase.com)
- [ClawHub Skill Page](https://clawhub.ai/parasyte-x/skills/agentic-wallet-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses should preserve transaction validation, user confirmation, token handling, and endpoint configuration guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
