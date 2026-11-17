## Description:

Rent and manage a no-KYC VPS through EQVPS over MCP, including plan selection, deployment, root SSH access, billing, and server lifecycle operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiuyhje](https://clawhub.ai/user/poiuyhje)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to rent, fund, deploy, inspect, and manage EQVPS virtual private servers for persistent workloads such as bots, websites, and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate paid account funding, invoice payment, and VPS orders through a third-party service.

Mitigation: Show prices and obtain explicit user confirmation before calling topup_balance, pay_invoice, or order_vps.

Risk: The hosted MCP service gives an agent controlled access to an EQVPS account and root-server operations.

Mitigation: Connect only when the user accepts EQVPS account access, inspect tool inputs before use, and avoid destructive or paid operations unless requested and confirmed.

Risk: API tokens and root credentials may be exposed if copied into logs or shared channels.

Mitigation: Treat EQVPS_API_TOKEN and root credentials as secrets, share them only with the user, and do not post or log them elsewhere.

Risk: Unused VPS instances may continue billing against the prepaid balance.

Mitigation: Review active servers with list_vps and cancel services that are no longer needed.

## Reference(s):

- [EQVPS homepage](https://eqvps.com)
- [EQVPS MCP server endpoint](https://mcp.eqvps.com/mcp)
- [ClawHub skill page](https://clawhub.ai/poiuyhje/skills/eqvps)
- [Publisher profile](https://clawhub.ai/user/poiuyhje)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, API calls]

**Output Format:** [Markdown prose with JSON configuration snippets and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prices, checkout links, account status, VPS status, API tokens, and root credentials returned by the EQVPS MCP service.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
