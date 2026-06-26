## Description: <br>
Gate TradFi (traditional finance) skill for querying and, after explicit confirmation, trading traditional finance assets such as forex or commodities on Gate; it must not be used for fund transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Gate TradFi orders, positions, market data, assets, and MT5 account information, and to prepare confirmed TradFi trading actions. The skill routes each request to the relevant Gate MCP workflow and formats query or execution results for the current conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes write-capable TradFi actions even though the README describes the skill as read-only. <br>
Mitigation: Treat the README's read-only claim as inaccurate for this version and install only when trading actions after confirmation are intended. <br>
Risk: Write permissions can submit or change real trades through Gate TradFi MCP tools. <br>
Mitigation: Use the least-privileged Gate authorization possible, avoid Tradfi:Write for read-only use, and require explicit review of symbol, side, size, price, order, or position parameters before confirmation. <br>
Risk: Account, balance, order, position, and MT5 data may be exposed in agent responses. <br>
Mitigation: Display sensitive account data only in the current response and do not store or log credentials, balances, or account details. <br>


## Reference(s): <br>
- [Gate TradFi MCP Execution Layer](references/mcp.md) <br>
- [Gate TradFi Place Order](references/place-order.md) <br>
- [Gate TradFi Amend Order](references/amend-order.md) <br>
- [Gate TradFi Cancel Order](references/cancel-order.md) <br>
- [Gate TradFi Modify Position](references/modify-position.md) <br>
- [Gate TradFi Close Position](references/close-position.md) <br>
- [Query TradFi Orders](references/query-orders.md) <br>
- [Query TradFi Positions](references/query-positions.md) <br>
- [Query TradFi Market Data](references/query-market.md) <br>
- [Query TradFi User Assets and MT5 Account](references/query-assets.md) <br>
- [Gate MCP](https://github.com/gateio/gate-mcp) <br>
- [Gate Skills Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-tradfi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown tables and concise text summaries with MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query responses may include account, balance, position, order, market, or MT5 data in the current response; trading flows must include confirmation parameters and post-action results.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata); artifact frontmatter version 2026.3.23-1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
