## Description: <br>
Gate dual investment skill for answering questions about dual currency products, target price settlement, account balances, dual orders, and confirmation-gated order placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to explore Gate dual investment products, simulate settlement outcomes, review dual balances and orders, and prepare order placements through Gate MCP tools after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Earn:Write access through Gate MCP to place financial-product orders. <br>
Mitigation: Use a narrowly scoped API key when possible and require explicit user confirmation immediately before any order placement. <br>
Risk: Dual investment is not principal-protected and settlement may occur in a different currency than the user invested. <br>
Mitigation: Present settlement scenarios and the product risk disclaimer in financial-product responses; do not recommend plans or predict prices. <br>
Risk: Incorrect order details, amounts, or date ranges could lead to misleading financial guidance or unwanted subscriptions. <br>
Mitigation: Review every order draft, double-check minimum amounts and date ranges, and fetch all required order pages before drawing conclusions. <br>
Risk: API credentials and account data are sensitive. <br>
Mitigation: Rely on the configured MCP session, never ask users to paste secrets into chat, and avoid exposing raw keys, internal endpoints, or raw error traces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-exchange-dual-staging) <br>
- [Publisher profile](https://clawhub.ai/user/gaixianggeng) <br>
- [ClawHub metadata homepage](https://github.com/gate/gate-skills) <br>
- [Gate MCP dependency](https://github.com/gate/gate-mcp) <br>
- [Gate Dual Investment Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Dual Investment MCP Specification](references/mcp.md) <br>
- [Product Query](references/product-query.md) <br>
- [Subscription & Order Placement](references/subscription.md) <br>
- [Settlement & Assets](references/settlement-assets.md) <br>
- [Scenarios & Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Markdown responses with tables, settlement calculations, risk notes, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured Gate MCP tools for product discovery, balance/order queries, and confirmation-gated dual order placement.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter version: 2026.4.3-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
