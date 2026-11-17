## Description:

Create and manage ERC20 wallets, transfer and swap tokens across supported chains, enable agent payments, and configure referrer fees for AI agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicofains1](https://clawhub.ai/user/nicofains1)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect agents to crypto wallet, transfer, swap, portfolio, and payment workflows. It is suited to agent payment scenarios such as rewards, bug bounties, automated payouts, and agent-to-agent transactions where every value-moving action is reviewed by a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet operations require raw private keys and can move real funds.

Mitigation: Use only a dedicated low-value or testnet wallet, never paste a primary wallet private key into an agent chat or shell history, and require explicit human approval before any wallet action.

Risk: The documented setup runs an external MCP server package without pinning an exact package version.

Mitigation: Pin and review the MCP server package before installation or execution.

Risk: Transfers, approvals, swaps, destinations, chains, amounts, and referrer fees can create irreversible losses or unexpected charges.

Mitigation: Require human review of every transfer, approval, swap amount, destination, chain, and fee before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicofains1/skills/crypto-agent-payments)
- [npm: @onlyswaps/mcp-server](https://www.npmjs.com/package/@onlyswaps/mcp-server)
- [OnlySwaps Docs](https://onlyswaps.fyi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for read-only quote and portfolio checks plus wallet-required transfer, swap, approval, and setup actions.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
