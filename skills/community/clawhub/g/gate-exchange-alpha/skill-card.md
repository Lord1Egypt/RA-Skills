## Description:

Gate Exchange Alpha helps agents browse Gate Alpha tokens, view market and account data, and prepare quote-based buy or sell orders with explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse Gate Alpha markets, inspect holdings and order history, and run quote-confirmed Alpha token trading workflows through Gate MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access account data and help place Alpha token trades.

Mitigation: Use least-privilege credentials, prefer read-only access for market or history tasks, and enable write access only when trading is intended.

Risk: Trading actions can execute real buy, sell, or sell-all orders.

Mitigation: Require a fresh quote and explicit immediate confirmation before every order placement, including each token in a batch sell flow.

Risk: Quotes are time-sensitive and market prices can change quickly.

Mitigation: Re-quote when confirmation is delayed or quote/order details no longer match.

Risk: Evidence reports reliance on mutable or unpinned external instructions and installers.

Mitigation: Verify installer provenance manually before deployment and review the skill before enabling account or trading permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-alpha)
- [Gate Alpha MCP Specification](references/mcp.md)
- [Token Discovery & Browsing](references/token-discovery.md)
- [Market Viewing](references/market-viewing.md)
- [Trading (Buy)](references/trading-buy.md)
- [Trading (Sell)](references/trading-sell.md)
- [Account & Holdings](references/account-holdings.md)
- [Account Book (Transaction History)](references/account-book.md)
- [Order Management](references/order-management.md)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown tables, confirmation prompts, and structured trade or order summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write workflows require Gate MCP access, a fresh quote, and explicit user confirmation before order placement.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
