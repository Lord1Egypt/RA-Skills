## Description:

Enable AI agents to execute non-custodial cross-chain swaps and transfers through the deBridge protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure an agent-accessible deBridge MCP server for cross-chain crypto quotes, order creation, fee review, status checks, and supported-chain discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and persists remote code from an upstream MCP repository.

Mitigation: Review and pin an audited upstream commit, use deterministic dependency installation, and install only when the repository is trusted.

Risk: The connected MCP server can help create high-impact cryptocurrency orders.

Mitigation: Require explicit review of quotes, fees, slippage, destination chain, and wallet-level spending limits before enabling order creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aviclaw/skills/debridge-mcp)
- [Publisher profile](https://clawhub.ai/user/aviclaw)
- [deBridge MCP repository used by setup](https://github.com/debridge-finance/debridge-mcp)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup and usage guidance for an MCP server that can quote swaps, create orders, check status, and list supported chains.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
