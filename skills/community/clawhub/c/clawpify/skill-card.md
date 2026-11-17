## Description:

Query and manage Shopify stores via GraphQL Admin API. Use for products, orders, customers, inventory, discounts, and all Shopify data operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alhwyn](https://clawhub.ai/user/alhwyn)

### License/Terms of Use:


## Use Case:

Developers and store operators use this skill to query and manage Shopify products, orders, customers, inventory, discounts, content, webhooks, and related store data through the GraphQL Admin API. It is intended for assisted store administration where potentially destructive or financial operations require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete live Shopify store data, including products, orders, inventory, discounts, shipping, subscriptions, content, and customer-related records.

Mitigation: Use a least-privileged Shopify token, prefer read-only scopes when possible, and require fresh explicit confirmation before any write, delete, inventory, fulfillment, shipping, subscription, discount, or marketing-consent operation.

Risk: Refunds, order cancellations, gift-card balance changes, and draft-order completion can create financial or customer-impacting outcomes that may be irreversible.

Mitigation: Show the affected order, customer, items, quantities, amounts, refund method, and final impact before execution, then wait for explicit user approval.

Risk: Bulk operations and exports can expose large volumes of customer, order, product, or inventory data.

Mitigation: Minimize exports, request only necessary fields, use pagination or scoped bulk queries, and handle exported data according to the store operator's data protection requirements.

Risk: Webhook creation can persist callbacks that send store events outside the immediate session.

Mitigation: Verify webhook destinations are controlled by the store operator, limit subscribed topics and fields, and confirm persistent webhook changes before creating, updating, or deleting subscriptions.

## Reference(s):

- [Clawpify release page](https://clawhub.ai/alhwyn/skills/clawpify)
- [Shopify GraphQL Admin API skill definition](artifact/SKILL.md)
- [Products and variants management](artifact/references/products.md)
- [Order operations](artifact/references/orders.md)
- [Customer management](artifact/references/customers.md)
- [Inventory and locations](artifact/references/inventory.md)
- [Discount codes and promotions](artifact/references/discounts.md)
- [Product collections](artifact/references/collections.md)
- [Order fulfillment and shipping](artifact/references/fulfillments.md)
- [Refund processing](artifact/references/refunds.md)
- [Draft order creation](artifact/references/draft-orders.md)
- [Gift card management](artifact/references/gift-cards.md)
- [Event subscriptions](artifact/references/webhooks.md)
- [Store locations](artifact/references/locations.md)
- [Marketing activities](artifact/references/marketing.md)
- [Multi-market setup](artifact/references/markets.md)
- [Navigation menus](artifact/references/menus.md)
- [Custom data fields](artifact/references/metafields.md)
- [Store pages](artifact/references/pages.md)
- [Blog management](artifact/references/blogs.md)
- [File uploads](artifact/references/files.md)
- [Shipping configuration](artifact/references/shipping.md)
- [Store information](artifact/references/shop.md)
- [Subscription management](artifact/references/subscriptions.md)
- [Content translations](artifact/references/translations.md)
- [Customer segments](artifact/references/segments.md)
- [Bulk data operations](artifact/references/bulk-operations.md)
- [ShopifyQL segment query language reference](https://shopify.dev/docs/api/shopifyql/segment-query-language-reference)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Markdown]

**Output Format:** [Markdown with GraphQL and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Shopify GraphQL Admin API queries and mutations for execution through the shopify_graphql tool.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
