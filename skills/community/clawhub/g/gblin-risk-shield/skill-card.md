## Description:

On-chain BTC/ETH market-risk check for agents on Base that reads the live Crash Shield risk regime (calm / elevated / crash) before trading or moving capital, mints a 10-minute EIP-712 Risk Attestation as machine-verifiable proof-of-diligence via x402, verifies attestations from peer agents for free, and optionally parks idle USDC in an oracle-priced index treasury.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gblinproject](https://clawhub.ai/user/gblinproject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before EVM trading, treasury movement, or portfolio rebalancing to check the live BTC/ETH risk regime, mint or verify short-lived attestations, and inspect related Base treasury operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use an unpinned npm MCP server while interacting with wallet payment tooling and ready-to-sign treasury calldata.

Mitigation: Review the MCP server package and prefer a pinned, verified version before installation or use.

Risk: The skill operates near crypto treasury workflows where unrestricted signing could move funds.

Mitigation: Keep private keys out of the skill environment and require existing wallet tooling with constrained signing permissions.

Risk: The market-risk signal is only one input and may be mistaken for financial advice.

Mitigation: Use the risk regime as part of the operator's own trading or treasury policy, and verify attestations before relying on peer claims.

## Reference(s):

- [GBLIN Agent Docs](https://gblin.digital/agents)
- [GBLIN API Surface](https://gblin.digital/llms.txt)
- [x402 Discovery](https://gblin-sentinel.vercel.app/.well-known/x402)
- [Base Risk Pulse API](https://gblin-sentinel.vercel.app/api/data/base-risk-pulse)
- [Risk Attestation API](https://gblin.digital/api/x402/attestation)
- [Live Usage Stats](https://gblin.digital/api/agent-stats)
- [GBLIN Contract on Base](https://basescan.org/address/0x36C81d7E1966310F305eA637e761Cf77F90852f0)
- [GBLIN MCP Server](https://www.npmjs.com/package/@gblin-protocol/mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and JSON API-response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to paid x402 HTTP calls, free verification endpoints, MCP tooling, and ready-to-sign treasury calldata.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
