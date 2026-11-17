## Description:

Manage Shopify products, orders, customers, inventory, collections, and store operations via the Shopify Admin API with OAuth authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to manage Shopify store products, orders, customers, inventory, collections, content, webhooks, discounts, billing, and fulfillment workflows through ClawLink-authenticated Shopify Admin API tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes Shopify store operations through a third-party credentialed plugin with access to sensitive store, customer, order, webhook, refund, and billing functions.

Mitigation: Install only after verifying the ClawLink plugin source and version, reviewing Shopify OAuth scopes, and confirming how to revoke ClawLink access.

Risk: Write operations can change or delete products, customer data, webhooks, billing charges, refunds, fulfillments, and bulk store records.

Mitigation: Require explicit approval before refunds, deletions, webhook changes, bulk operations, billing charges, or other create, update, and delete actions.

Risk: Bulk delete operations cannot be undone.

Mitigation: Confirm the target resource set and intended impact before allowing any bulk delete operation.

## Reference(s):

- [Shopify Admin API](https://shopify.dev/docs/api/admin)
- [Shopify REST Admin API Reference](https://shopify.dev/docs/api/admin-rest)
- [Shopify GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql)
- [Shopify OAuth Documentation](https://shopify.dev/docs/apps/auth/oauth)
- [ClawLink](https://claw-link.dev)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/shopify-commerce)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Shopify Admin API tool calls through ClawLink after account pairing and connection.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
