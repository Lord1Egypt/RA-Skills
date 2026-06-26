## Description: <br>
Query and manage Shopify stores via GraphQL Admin API. Use for products, orders, customers, inventory, discounts, and all Shopify data operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Alhwyn](https://clawhub.ai/user/Alhwyn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, store operators, and support teams use this skill to query Shopify store data and prepare GraphQL Admin API operations for products, orders, customers, inventory, discounts, fulfillments, and related commerce workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Shopify Admin API access can expose customer, order, inventory, subscription, and marketing data. <br>
Mitigation: Use tightly scoped Shopify API credentials and review requested fields before running queries or exports. <br>
Risk: Write, delete, refund, fulfillment, inventory, subscription, and marketing operations can change live store state or customer communications. <br>
Mitigation: Require explicit user confirmation with a clear summary of the proposed change before execution. <br>
Risk: Bulk operations and customer-data exports can move large volumes of store data. <br>
Mitigation: Confirm the data scope, destination, and business need before starting bulk operations or exports. <br>


## Reference(s): <br>
- [Shopify Blogs & Articles](references/blogs.md) <br>
- [Shopify Bulk Operations](references/bulk-operations.md) <br>
- [Shopify Collections & Discounts](references/collections.md) <br>
- [Shopify Customers](references/customers.md) <br>
- [Shopify Discounts](references/discounts.md) <br>
- [Shopify Draft Orders](references/draft-orders.md) <br>
- [Shopify Files](references/files.md) <br>
- [Shopify Fulfillments](references/fulfillments.md) <br>
- [Shopify Gift Cards](references/gift-cards.md) <br>
- [Shopify Inventory & Locations](references/inventory.md) <br>
- [Shopify Locations](references/locations.md) <br>
- [Shopify Marketing](references/marketing.md) <br>
- [Shopify Markets](references/markets.md) <br>
- [Shopify Menus](references/menus.md) <br>
- [Shopify Metafields & Metaobjects](references/metafields.md) <br>
- [Shopify Orders](references/orders.md) <br>
- [Shopify Pages](references/pages.md) <br>
- [Shopify Products & Variants](references/products.md) <br>
- [Shopify Refunds](references/refunds.md) <br>
- [Shopify Customer Segments](references/segments.md) <br>
- [Shopify Shipping & Delivery](references/shipping.md) <br>
- [Shopify Shop](references/shop.md) <br>
- [Shopify Subscriptions](references/subscriptions.md) <br>
- [Shopify Translations](references/translations.md) <br>
- [Shopify Webhooks](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with GraphQL and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a shopify_graphql tool and appropriately scoped Shopify Admin API credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
