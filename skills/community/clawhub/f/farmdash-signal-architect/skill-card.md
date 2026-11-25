## Description:

OpenClaw DeFi execution with FarmDash's MCP contract: LI.FI and Relay swaps, simulation, zero-custody settlement verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi users use this agent skill to research opportunities, assess multi-chain trade routes, and prepare wallet-affecting actions such as swaps and hedges. It provides analysis and transaction preparation for user-controlled or explicitly bounded execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is favorable but incomplete: one analyzer was degraded and one component was only partially inspected.

Mitigation: Account for the stated coverage limits and review the skill and deployment before installation or use.

Risk: Wallet-affecting actions can expose users to financial loss or irreversible transactions if transaction details are wrong or stale.

Mitigation: Verify a fresh quote, token contracts, chains, amounts, destinations, and fees before signing; keep signing local and never provide private keys or seed phrases.

## Reference(s):

- [FarmDash Agent Hub](https://www.farmdash.one/agents)
- [Canonical Signal Architect Manual](https://www.farmdash.one/agents/skills/farmdash-signal-architect)
- [Signal Architect Complete Reference Guide](https://www.farmdash.one/guides/signal-architect-complete-reference)
- [FarmDash OpenAPI Specification](https://www.farmdash.one/agents/openapi.yaml)
- [MCP Discovery Manifest](https://www.farmdash.one/.well-known/mcp.json)
- [FarmDash Zero-Custody Security Model](https://www.farmdash.one/security)
- [FarmDash Fee Schedule](https://www.farmdash.one/fees)

## Skill Output:

**Output Type(s):** [Text, Guidance, Analysis, JSON, Configuration]

**Output Format:** [Structured tool data and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market analysis, route quotes, simulation results, and transaction preparation details; wallet-affecting steps require the configured signing and authorization gates.]

## Skill Version(s):

1.2.31 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
