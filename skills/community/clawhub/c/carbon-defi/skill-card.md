## Description:

Use this skill when the user wants to create or manage on-chain maker trading strategies on Carbon DeFi across Ethereum, Sei, Celo, TAC, or COTI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashachaf](https://clawhub.ai/user/ashachaf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Carbon DeFi positions, plan maker trading strategies, retrieve quotes, and prepare unsigned on-chain transactions for user review and signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a remote Carbon DeFi MCP service and local npx execution in a financial workflow.

Mitigation: Install only when the remote service and local MCP launcher are acceptable, and pin and verify the MCP client package where possible.

Risk: The skill can produce unsigned transactions for on-chain trading and strategy management.

Mitigation: Independently verify each transaction's destination, calldata, value, token allowances, and warnings before signing.

Risk: Broad curl access can reach network endpoints during use.

Mitigation: Restrict network access to Carbon DeFi domains when deploying the skill.

## Reference(s):

- [Carbon DeFi ClawHub Skill Page](https://clawhub.ai/ashachaf/skills/carbon-defi)
- [Carbon DeFi App](https://app.carbondefi.xyz)
- [Carbon DeFi Documentation](https://docs.carbondefi.xyz)
- [AI Agents and MCP Integration](https://docs.carbondefi.xyz/ai-agents-and-mcp-integration)
- [Carbon DeFi Transaction Encoding](https://docs.carbondefi.xyz/developer-guides/carbon-defi-transaction-encoding)
- [Carbon DeFi MCP Endpoint](https://mcp.carbondefi.xyz/mcp)
- [Carbon DeFi OpenAPI Specification](https://mcp.carbondefi.xyz/openapi.json)
- [Carbon DeFi Litepaper](https://carbondefi.xyz/litepaper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations prepare unsigned transaction data for user verification, signing, and broadcast outside the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
