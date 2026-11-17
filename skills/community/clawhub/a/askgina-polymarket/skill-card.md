## Description:

Fast setup for Claw bots: paste your Gina MCP token and start trading Polymarket in minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sidshekhar](https://clawhub.ai/user/sidshekhar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an MCP client to Gina for Polymarket market discovery, trading, position management, and scheduled strategy automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connection can access Polymarket account data and real-money USDC trading functions through a long-lived bearer token.

Mitigation: Keep the token out of shared files, logs, repositories, and backups; revoke it immediately if exposure is suspected.

Risk: Trading, redemption, cancellation, and automation boundaries may be unclear to a user before first use.

Mitigation: Start with read-only prompts and confirm authorization behavior before enabling trades, redemptions, cancellations, or scheduled automations.

Risk: The server evidence flags the release as suspicious because it asks users to store a 90-day bearer token for real-money trading.

Mitigation: Install only after reviewing the security guidance and confirming that the token scope and trade-confirmation workflow fit the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sidshekhar/skills/askgina-polymarket)
- [Gina documentation](https://docs.askgina.ai)
- [Predictions MCP quick start](https://docs.askgina.ai/predictions-mcp/quick-start)
- [Predictions MCP features](https://docs.askgina.ai/predictions-mcp/features)
- [Predictions MCP client setup](https://docs.askgina.ai/predictions-mcp/client-setup)
- [Predictions MCP troubleshooting](https://docs.askgina.ai/predictions-mcp/troubleshooting)
- [Privy](https://privy.io)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and natural-language prompt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide real-money USDC trading and scheduled automations through an MCP connection.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
