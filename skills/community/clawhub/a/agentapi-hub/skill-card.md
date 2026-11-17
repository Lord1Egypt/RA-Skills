## Description:

Browse and search the AgentAPI directory - a curated database of APIs designed for AI agents, including MCP-compatible APIs and x402 pay-per-use billing with USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmo-dev](https://clawhub.ai/user/gizmo-dev)

### License/Terms of Use:


## Use Case:

Developers and agents use AgentAPI Hub to discover MCP-compatible APIs by category or capability and to review x402 pay-per-use examples for API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes workflows where an agent can make real USDC payments through a third-party API.

Mitigation: Require explicit approval for each payment, use a low-balance wallet, and enforce strict spending limits.

Risk: Prompts or requests sent through proxied third-party APIs may expose sensitive information.

Mitigation: Do not send secrets, private code, personal data, or credentials in proxied prompts.

## Reference(s):

- [AgentAPI Hub ClawHub listing](https://clawhub.ai/gizmo-dev/skills/agentapi-hub)
- [AgentAPI website](https://agentapihub.com)
- [AgentAPI docs](https://api.agentapihub.com/api/docs)
- [AgentAPI JSON endpoint](https://agentapihub.com/api/v1/apis)
- [Billing API](https://api.agentapihub.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party API endpoints, x402 payment flow examples, and suggested API categories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
