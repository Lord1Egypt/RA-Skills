## Description: <br>
Gate dual investment skill for dual currency product discovery, target price settlement analysis, position and balance queries, and confirmation-gated dual order placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to browse Gate dual investment products, simulate settlement outcomes, review dual positions and balances, and prepare dual investment orders with explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Gate dual investment orders when connected to an authenticated Gate MCP server. <br>
Mitigation: Use a dedicated least-privilege API key and require explicit user confirmation after showing the full order draft before any placement. <br>
Risk: Dual investment is not principal-protected and settlement may occur in a different currency than the investment currency. <br>
Mitigation: Show settlement scenarios and product risk disclaimers, and ask the user to verify the amount, target price, APY, and settlement outcome before confirming. <br>
Risk: Minimum investment requirements or product constraints may differ from the skill output. <br>
Mitigation: Double-check minimum investment requirements and conflicting product details in the Gate app or website before placing an order. <br>


## Reference(s): <br>
- [Gate Exchange Dual Investment Skill](https://clawhub.ai/gate-exchange/gate-exchange-dual) <br>
- [Gate Skills Repository](https://github.com/gate/gate-skills) <br>
- [Gate MCP Repository](https://github.com/gate/gate-mcp) <br>
- [MCP Execution Specification](references/mcp.md) <br>
- [Product Query Reference](references/product-query.md) <br>
- [Subscription Reference](references/subscription.md) <br>
- [Settlement Assets Reference](references/settlement-assets.md) <br>
- [Gate Runtime Rules](references/gate-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with tables, order drafts, settlement summaries, and risk disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated Gate MCP read operations and confirmation-gated order placement when the user explicitly approves.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
