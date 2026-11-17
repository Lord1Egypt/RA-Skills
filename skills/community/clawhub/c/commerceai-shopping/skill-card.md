## Description:

Search the US product catalog, compare products, and answer product questions through the CommerceAI MCP tool `shopping_agent`. Use when the user wants to find, compare, or ask about products to buy, such as "earbuds under $50" or "compare these two". Not for carts, orders, checkout, coupons, or markets other than US.

This skill is ready for commercial/non-commercial use.

## Publisher:

[commerceai](https://clawhub.ai/user/commerceai)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers can use this skill to find products in the US catalog, compare recommendations, and ask follow-up questions about products. It does not support purchasing or markets outside the US.

### Deployment Geography for Use:

United States (US)

## Known Risks and Mitigations:

Risk: Shopping requests and follow-ups are sent to CommerceAI, and completed turns consume credits.

Mitigation: Omit sensitive or unrelated personal details, keep the API key outside chat, and review credit usage.

Risk: Product prices and availability may change, and server-side data retention is not described in the supplied artifact.

Mitigation: Confirm current details on the merchant page and avoid including information you would not want shared with the service.

## Reference(s):

- [CommerceAI setup instructions](https://github.com/CommerceAI-ai/CommerceAI)
- [CommerceAI MCP server](https://commerceai.ai/mcp/)
- [CommerceAI Shopping on ClawHub](https://clawhub.ai/commerceai/skills/commerceai-shopping)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown product recommendations, comparisons, and answers with merchant purchase links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and availability can change; confirm final details on the merchant page.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
