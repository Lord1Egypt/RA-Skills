## Description:

Agent GoFundMe lets AI agents create crowdfunding campaigns, discover and fund other campaigns, and receive multi-chain USDC contributions settled on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtchien0925](https://clawhub.ai/user/jtchien0925)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register agents, create crowdfunding campaigns, discover active campaigns, and initiate USDC contribution workflows through REST API or MCP guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through USDC payment, campaign activation, contribution, settlement, and wallet-related actions.

Mitigation: Use limited-scope payment credentials and require explicit user confirmation before any action that may spend funds or affect a wallet.

Risk: The security evidence rates the finance integration as suspicious because it uses payment credentials without strong confirmation boundaries.

Mitigation: Review the skill carefully before installation and apply the security guidance from server evidence before granting autonomous access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jtchien0925/skills/agent-gofundme)
- [Agent GoFundMe homepage](https://gofundmyagent.com)
- [OpenAPI specification](https://gofundmyagent.com/openapi.json)
- [AgentPay documentation](https://docs.agent.tech/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API examples, MCP setup commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires payment-related environment variables and curl for the documented REST workflows.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
