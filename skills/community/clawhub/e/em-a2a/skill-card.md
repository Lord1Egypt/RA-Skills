## Description:

Agent-to-Agent payments on TRON. Use when an agent needs to pay another agent, escrow funds, check credit scores, or verify on-chain identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ypeng1620-beep](https://clawhub.ai/user/ypeng1620-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use EM-A2A to coordinate TRON-based agent payments, escrow flows, credit checks, fee previews, and on-chain identity verification between counterparties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures a third-party MCP package that receives a wallet private key.

Mitigation: Review and pin the MCP package version before installation, use testnet first, and keep mainnet keys separate from test or evaluation environments.

Risk: Payment, escrow release, and refund actions can move funds.

Mitigation: Require explicit human approval before any payment, escrow release, or refund action and avoid using high-value or primary wallets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ypeng1620-beep/skills/em-a2a)
- [npm package: @poisonpyf/a2a-mcp](https://www.npmjs.com/package/@poisonpyf/a2a-mcp)
- [TRON Shasta Faucet](https://www.trongrid.io/shasta)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown with JSON configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires A2A_NETWORK and A2A_PRIVATE_KEY environment variables for MCP tool configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
