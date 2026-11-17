## Description:

Gate CrossEx cross-exchange skill for trading or querying positions across Gate, Binance, OKX, and Bybit through Gate CrossEx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route Gate CrossEx account, order, position, history, transfer, convert, margin, and futures requests to documented MCP workflows across supported exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote runtime instructions could affect behavior before high-impact financial actions.

Mitigation: Verify runtime rules from a pinned or local copy before use, and do not install or update skills without explicit user confirmation.

Risk: Write-capable CrossEx actions can place trades, transfer funds, convert assets, cancel or amend orders, close positions, and change leverage.

Mitigation: Require an immediate explicit confirmation after presenting the exact action draft, parameters, and risk impact before any mutation call.

Risk: Broad account, position, and history queries may expose sensitive financial records.

Mitigation: Limit query scope to the user's stated need and avoid broad account or history requests unless the user intends to display those records.

Risk: API credentials with CrossEx write permissions can authorize high-impact account changes.

Mitigation: Use secure local MCP configuration, never ask users to paste API secrets in chat, and degrade to query-only mode when write permissions are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-crossex)
- [Gate CrossEx product page](https://www.gate.com/crossex)
- [Gate CrossEx API documentation](https://www.gate.com/docs/developers/crossex)
- [Gate API v4 documentation](https://www.gate.com/docs/developers/apiv4)
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [MCP execution specification](references/mcp.md)
- [Runtime rules](references/runtime-rules.md)
- [Trading scenarios](references/scenarios.md)
- [Spot trading workflow](references/spot-trading.md)
- [Margin trading workflow](references/margin-trading.md)
- [Futures trading workflow](references/futures-trading.md)
- [Transfer workflow](references/transfer.md)
- [Convert workflow](references/convert-trading.md)
- [Order management workflow](references/order-management.md)
- [Position query workflow](references/position-query.md)
- [History query workflow](references/history-query.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown action drafts, confirmations, query summaries, and execution results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate MCP and CrossEx API permissions for write actions; can degrade to query-only mode when write endpoints or permissions are unavailable.]

## Skill Version(s):

1.0.2 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
