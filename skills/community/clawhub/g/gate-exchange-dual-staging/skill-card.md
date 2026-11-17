## Description:

Gate Exchange Dual Investment helps agents browse Gate dual investment products, simulate settlement outcomes, review positions and balances, and prepare confirmation-gated dual investment orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and agent developers use this skill to inspect dual investment products, understand settlement scenarios and balances, and place dual orders through a locally configured Gate MCP session after explicit confirmation. It supports informational financial workflows and confirmation-gated order execution without providing investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed dual investment orders commit funds, cannot be canceled after placement, and may settle in a different currency.

Mitigation: Show a complete order draft and require explicit immediate confirmation before calling the order placement tool.

Risk: The workflow requires Gate API credentials and Earn:Write permission.

Mitigation: Use only the locally configured Gate MCP session, never ask users to paste secrets into chat, and keep write access scoped to the documented dual investment tools.

Risk: Financial product responses could be mistaken for investment advice or guaranteed returns.

Mitigation: Present product data and settlement mechanics for reference only, include the required risk disclaimer, and avoid recommending plans or predicting prices.

Risk: Incorrect APY formatting or timestamp display can mislead users about product terms.

Mitigation: Convert raw APY and rate fields by multiplying by 100 before display, sanity-check displayed percentages, and omit timestamp fields from user-facing output.

## Reference(s):

- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate MCP Server](https://github.com/gate/gate-mcp)
- [Gate Dual Investment Runtime Rules](references/gate-runtime-rules.md)
- [Gate Dual Investment MCP Specification](references/mcp.md)
- [Product Query Workflow](references/product-query.md)
- [Subscription and Order Placement Workflow](references/subscription.md)
- [Settlement and Assets Workflow](references/settlement-assets.md)
- [Scenarios and Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown responses with comparison tables, settlement calculations, order drafts, confirmation prompts, and status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Gate MCP session with GATE_API_KEY and GATE_API_SECRET. Write operations require Earn:Write permission and explicit immediate user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog version: 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
