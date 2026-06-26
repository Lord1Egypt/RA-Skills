## Description: <br>
Gate Alpha token market skill for browsing, trading, and checking Alpha market tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to discover Gate Alpha tokens, view Alpha market data, review account and order information, and prepare quote-based buy or sell orders through Gate MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can place live Gate Alpha trades when connected to an authenticated Gate MCP setup. <br>
Mitigation: Use the narrowest available Gate authorization, do not paste API secrets into chat, and verify token, amount, slippage, quote, and sell-all confirmations before execution. <br>
Risk: The security review flags broad triggers and an external runtime dependency as requiring review before installation. <br>
Mitigation: Install only in trusted Gate MCP environments and review the linked runtime rules and security summary before granting Alpha trading access. <br>


## Reference(s): <br>
- [Gate Alpha MCP Specification](references/mcp.md) <br>
- [Token Discovery & Browsing](references/token-discovery.md) <br>
- [Market Viewing](references/market-viewing.md) <br>
- [Trading (Buy)](references/trading-buy.md) <br>
- [Trading (Sell)](references/trading-sell.md) <br>
- [Account & Holdings](references/account-holdings.md) <br>
- [Account Book (Transaction History)](references/account-book.md) <br>
- [Order Management](references/order-management.md) <br>
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with structured trade drafts, execution results, market data summaries, account summaries, and order status reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use authenticated Gate MCP tools for account, quote, order, and trading operations; trading flows require a fresh quote and explicit user confirmation before order placement.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
