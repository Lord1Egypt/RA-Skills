## Description:

Guides an agent through 1688 product research workflows using the Dianleida MCP connector, including product search, bestseller ranking, product analysis, category browsing, account balance checks, parameter selection, and visual result presentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b18797245781-commits](https://clawhub.ai/user/b18797245781-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sourcing agents use this skill to search 1688 products, inspect rankings, analyze individual product trends, browse categories, and turn returned data into product cards, tables, Markdown, or HTML summaries for sourcing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make Dianleida MCP calls that consume account credits, including the initial connector and balance check.

Mitigation: Ask for consent before credit-consuming calls, explain that each call may consume one point, and check or report the remaining balance when failures suggest insufficient credits.

Risk: Business sourcing queries and product-research intent are routed through the required third-party Dianleida MCP service.

Mitigation: Tell users what data is being sent to Dianleida, avoid sending sensitive sourcing strategy unless the user approves, and allow the user to decline or choose another provider where available.

## Reference(s):

- [1688 Product Selection MCP API Reference](references/api_reference.md)
- [1688 Product Selection Domain Knowledge](references/domain_knowledge.md)
- [Dianleida MCP Service](https://www.dianleida.net/mcp)
- [Dianleida MCP Configuration Documentation](https://www.dianleida.net/mcp/docs/)
- [ClawHub Skill Release Page](https://clawhub.ai/b18797245781-commits/skills/dld-skills)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance, analysis]

**Output Format:** [Markdown or rendered HTML with product images, links, tables, cards, and concise sourcing analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Dianleida MCP tools that consume account credits and return third-party 1688 product data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
