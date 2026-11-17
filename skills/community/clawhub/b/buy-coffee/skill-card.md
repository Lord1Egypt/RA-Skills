## Description:

Buy Coffee uses Lobster Brew to help OpenClaw discover coffee roasters, compare coffees, build carts, and hand off a Shopify checkout link for owner payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abuiles](https://clawhub.ai/user/abuiles)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to discover coffee merchants, compare coffee or subscription options, prepare carts, and receive checkout links they can review and complete themselves.

### Deployment Geography for Use:

Global, subject to Lobster Brew country support and merchant availability.

## Known Risks and Mitigations:

Risk: The skill contacts Lobster Brew and merchant Shopify endpoints to look up products and prepare carts.

Mitigation: Review merchant, product, cart, and checkout details before following the returned checkout URL.

Risk: A merchant flow may not support applying a required subscription selling plan through the merchant MCP.

Mitigation: Report the flow as unsupported instead of adding the item without the required selling plan.

Risk: Product, pricing, availability, and cart details can become stale if treated as locally stored truth.

Mitigation: Use merchant MCP data as the source of truth at purchase time and avoid relying on stored product claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abuiles/skills/buy-coffee)
- [Lobster Brew homepage](https://lobsterbrew.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown summary with merchant, product, variant, purchase type, subscription details, savings, checkout URL, and resolution path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns checkout URLs for owner review and payment; does not complete payment.]

## Skill Version(s):

1.2.0 (source: server release evidence and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
