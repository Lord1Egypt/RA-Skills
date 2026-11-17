## Description:

FIU MCP Market Data and Trading Assistant for stock quotes, K-line data, trading, positions, and market analysis across HK, US, and CN markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulnit](https://clawhub.ai/user/ulnit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure FIU MCP services, query HK, US, and CN market data, search securities, inspect account cash and positions, and initiate simulated or explicitly confirmed real trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent trading credentials may be written to local configuration files and backups.

Mitigation: Use scoped or sandbox trading credentials, verify permissions on ~/.fiu-market/config, ~/.mcp.json, and any backup files after setup, and rotate the token if it may have been exposed.

Risk: Generic router paths can call order-related MCP tools outside the documented real-trading confirmation flow.

Mitigation: Do not use mcp_router.sh for order placement, modification, cancellation, or futures trading unless an external confirmation control is in place.

Risk: Market data and order actions can affect financial decisions.

Mitigation: Confirm symbols, market status, order environment, quantity, and price before acting on trading output.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ulnit/skills/fiu-market-assistant)
- [FIU MCP Tools Reference](artifact/docs/MCP_TOOLS.md)
- [FIU MCP Server Interface Documentation](artifact/docs/mcp-interfaces_EN.md)
- [FIU MCP Server Interface Documentation (Chinese)](artifact/docs/mcp-interfaces_CN.md)
- [FIU authentication portal](https://ai.szfiu.com/auth/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-style text with JSON responses from MCP calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIU_MCP_TOKEN, curl, jq, date, and bash; trading defaults to SIMULATE mode in the documented trade flow.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
