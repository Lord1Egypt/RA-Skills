## Description:

Gate TradFi skill for querying and trading traditional finance assets such as forex and commodities on Gate, excluding fund transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to query Gate TradFi orders, positions, market data, assets, and MT5 account information, and to prepare or execute supported trading actions when write permissions are intentionally configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README describes a read-only query helper, while the actual skill includes order placement, amendment, cancellation, position modification, and position closing workflows.

Mitigation: Treat the release as write-enabled, review confirmation prompts carefully, and install it only with credentials whose trading permissions are intentionally granted.

Risk: Using write-capable credentials for account or market queries increases exposure if the skill is invoked incorrectly.

Mitigation: Use a separate read-only API key when only query workflows are needed.

Risk: Trading actions can alter account positions or orders.

Mitigation: Require explicit user confirmation before every write action and verify the post-action parameter and result summary.

## Reference(s):

- [Gate TradFi MCP Specification](references/mcp.md)
- [Query TradFi Orders](references/query-orders.md)
- [Query TradFi Positions](references/query-positions.md)
- [Query TradFi Market Data](references/query-market.md)
- [Query TradFi User Assets and MT5 Account](references/query-assets.md)
- [Gate TradFi Place Order](references/place-order.md)
- [Gate TradFi Amend Order](references/amend-order.md)
- [Gate TradFi Cancel Order](references/cancel-order.md)
- [Gate TradFi Modify Position](references/modify-position.md)
- [Gate TradFi Close Position](references/close-position.md)
- [Gate MCP](https://github.com/gateio/gate-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown responses with tables, confirmation prompts, and parameter summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trading flows require explicit user confirmation before write actions and a post-action summary of parameters and results.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter version 2026.3.23-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
