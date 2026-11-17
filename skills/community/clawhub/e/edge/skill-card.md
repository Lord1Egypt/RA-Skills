## Description:

Use when user asks about crypto tokens, trading, portfolios, or price alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexomis](https://clawhub.ai/user/lexomis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to access on-chain trading data, inspect tokens and pairs, analyze wallets, manage orders, and configure price alerts through the Edge MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an externally downloaded MCP server access to an Edge API key with order or wallet authority.

Mitigation: Install only after trusting the Edge npm package and publisher, restrict the API key to minimum required permissions and limits, and use safer secret-passing controls where available.

Risk: Trading and wallet operations may affect real funds.

Mitigation: Require explicit user confirmation for every order or wallet action and review market, token, pair, and wallet data before execution.

## Reference(s):

- [Edge Agent Docs](https://edge-trade.gitbook.io/agents)
- [Edge.Trade ClawHub Skill Page](https://clawhub.ai/lexomis/skills/edge)
- [lexomis ClawHub Publisher Profile](https://clawhub.ai/user/lexomis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool, command, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose market analysis, wallet analysis, alert configuration, and order-management actions that require user review before execution.]

## Skill Version(s):

v4478.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
