## Description:

AI Content Engine connects agents to an MCP service that generates video scripts, images, videos, and social publishing workflows with public quoting, API-key brand access, and paid x402 or prepaid-token calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimitd-ai](https://clawhub.ai/user/jimitd-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brands, and developers use this skill to quote, generate, track, retrieve, and publish AI-assisted scripts, images, and videos through MCP-compatible agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wallet private key configured for x402 payments can authorize USDC transfers if the agent signs payment requests.

Mitigation: Use sandbox mode or prepaid API-key tokens when possible, and use a dedicated low-balance wallet with no unrelated assets or approvals for per-call payments.

Risk: Paid generation and publishing actions can spend funds or publish content if an agent proceeds without sufficient review.

Mitigation: Call pricing and quote tools before paid actions, require explicit review of exact payment details, and review generated content before publication.

Risk: Brand-scoped reads and token spending depend on a CONTENT_ENGINE_API_KEY.

Mitigation: Store API keys securely, scope them to the intended brand, and rotate or revoke keys that are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimitd-ai/skills/ai-content-engine)
- [Content Engine Homepage](https://content-engine-app.fly.dev)
- [MCP Endpoint](https://content-engine-x402.fly.dev/mcp)
- [MCP Server Discovery](https://content-engine-x402.fly.dev/.well-known/mcp.json)
- [x402 Protocol](https://www.x402.org/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance and MCP tool-call results, including scripts, content identifiers, status data, generated media URLs, and payment or quote details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls may require API-key prepaid tokens or explicit x402 USDC payment authorization from a dedicated low-balance agent wallet.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter lists 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
