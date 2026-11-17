## Description:

Pay-per-call AgentIndex tools on Base USDC (x402) provide multi-chain wallet and gas reads, live web search with page content, PDF-to-Markdown, web reading, structured extraction, weather, crypto, news, and MCP discovery for agents that need current web or document data without an account or API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentindexworld](https://clawhub.ai/user/agentindexworld)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to access paid x402 endpoints for live web search, document conversion, web reading, structured extraction, wallet and gas preflight checks, weather, crypto, news, and MCP discovery. It is intended for agents with compatible x402 clients and explicit controls around Base mainnet USDC payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct a funded agent to spend USDC through x402 payment flows.

Mitigation: Use payment clients that require explicit transaction-specific confirmation before signing or retrying paid requests.

Risk: Unexpected or repeated payment requirements could cause unintended spending.

Mitigation: Enforce per-call and session spending limits, reject unexpected payment requirements, and avoid loops on unpaid 402 responses.

Risk: Payments are expected on Base mainnet USDC and may involve service-specific recipients or terms.

Mitigation: Verify Base USDC terms, network, amount, and recipient before each paid request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentindexworld/skills/agentindex-x402)
- [AgentIndex x402 base URL](https://x402.agentindex.world)
- [Agent catalog](https://x402.agentindex.world/llms.txt)
- [OpenAPI specification](https://x402.agentindex.world/openapi.json)
- [Agent card](https://x402.agentindex.world/agent.json)
- [MCP endpoint](https://x402.agentindex.world/mcp/)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with endpoint paths, JSON request examples, payment flow notes, and MCP connection details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require signed x402/EIP-3009 USDC payments on Base mainnet for non-sample calls.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
