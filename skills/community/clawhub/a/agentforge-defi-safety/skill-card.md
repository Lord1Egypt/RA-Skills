## Description:

Provides agents with preflight checks and related risk analysis for on-chain actions across EVM networks and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acarchidi](https://clawhub.ai/user/acarchidi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building agents that interact with DeFi can use the service to review transactions, signatures, addresses, and tokens before acting, and to retrieve related market and protocol risk information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and planned transaction or signature details submitted for analysis are sent to AgentForge.

Mitigation: Start with the wallet-free MCP option, share transaction details only when acceptable, and never submit private keys or seed phrases.

Risk: Paid x402 calls can spend USDC from the configured payment wallet.

Mitigation: Check the quoted price and constrain the payment wallet with a spending limit before enabling polling or follow-up checks.

Risk: Safety verdicts may be incomplete; the deployed backend and its retention practices were not verified.

Mitigation: Treat verdicts as advice and independently review the action before execution.

## Reference(s):

- [AgentForge service](https://agentforge-taupe.vercel.app)
- [AgentForge MCP endpoint](https://agentforge-taupe.vercel.app/mcp)
- [ClawHub skill page](https://clawhub.ai/acarchidi/skills/agentforge-defi-safety)
- [x402 payment protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [Structured JSON responses with risk findings, explanations, and safety verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides proceed, caution, or avoid guidance for supported checks; findings are advisory.]

## Skill Version(s):

1.10.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
