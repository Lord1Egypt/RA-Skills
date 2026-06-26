## Description: <br>
Gate CrossEx cross-exchange skill for trading, transfers, order management, and position or history queries across Gate, Binance, OKX, and Bybit through Gate MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query CrossEx accounts and manage cross-exchange spot, margin, futures, transfer, convert, order, position, and history workflows through Gate MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad CrossEx trading authority can place, amend, cancel, transfer, convert, close positions, or change leverage using real funds. <br>
Mitigation: Use least-privilege API keys where possible, start with a small funded test amount, and require explicit confirmation of exchange, symbol, amount, order ID, transfer route, and leverage before every mutation. <br>
Risk: Margin, futures, leverage, and cross-exchange execution can create liquidation, slippage, or fast price-movement exposure. <br>
Mitigation: Run account, balance, symbol, fee, risk-limit, and leverage pre-checks; surface risk details in the action draft; and verify resulting state with read endpoints after execution. <br>
Risk: External runtime or update instructions may change after installation. <br>
Mitigation: Review the installed skill version and change details before accepting updates, and stop or stay query-only when required MCP read or write endpoints are unavailable. <br>
Risk: API credentials could be mishandled during setup. <br>
Mitigation: Never paste API secrets into chat; configure credentials through secure local MCP configuration and rotate leaked keys immediately. <br>


## Reference(s): <br>
- [Gate CrossEx Product Page](https://www.gate.com/crossex) <br>
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage) <br>
- [MCP Execution Specification](references/mcp.md) <br>
- [Runtime Rules](references/runtime-rules.md) <br>
- [Spot Trading](references/spot-trading.md) <br>
- [Margin Trading](references/margin-trading.md) <br>
- [Futures Trading](references/futures-trading.md) <br>
- [Cross-Exchange Transfer](references/transfer.md) <br>
- [Convert Trading](references/convert-trading.md) <br>
- [Order Management](references/order-management.md) <br>
- [Position Query](references/position-query.md) <br>
- [History Query](references/history-query.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown action drafts, confirmation prompts, result summaries, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gate MCP, CrossEx API permissions, pre-checks before mutations, explicit user confirmation, and read-back verification after writes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
