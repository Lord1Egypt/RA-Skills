# Merchant data connection contract

This skill does not assume that merchants use Shopify, WooCommerce, Amazon, a standalone ERP, or a certain returns system. The installation must be configured with an authorized merchant connector and have the Agent obtain data through structured tool calls. Splicing customer email fields directly into shell commands, SQL, or URLs is prohibited.

The public storefront discovery in [storefront-discovery.md](storefront-discovery.md) can automatically identify public product, campaign, and policy sources after the merchant supplies a URL. It is a supplemental, unauthenticated source. It cannot satisfy `find_customer`, `list_recent_orders`, `get_order`, private inventory, historical entitlement, or customer-specific campaign eligibility, and it never grants write authority.

For Shopify, WooCommerce, Amazon, eBay, Etsy, Walmart, BigCommerce, and Wix, first read [platform-connectors.md](platform-connectors.md). It distinguishes what the vendor API can expose from what this Skill currently implements, gives official credential links, and requires a least-privilege read-only connection. A platform's write API or a public storefront marker does not constitute connector authorization.

## Required abilities

The connector provides at least the following read-only operations; write operations must be authorized separately:

1. `find_customer`: Locate the customer by verified email, order number or platform customer ID. Marketplace connectors that do not expose a standalone customer resource may return only a verified order-associated buyer match; they must fail closed for an arbitrary email lookup.
2. `list_recent_orders`: Get the latest orders and line items by a safely resolved customer/order context, supporting the maximum number of days and quantity where the platform permits. A marketplace connector must return insufficient permission/no match rather than pretend it can search arbitrary customer history.
3. `get_order`: Get the complete order, payment, fulfillment, package, tracking, cancellation, return, refund, dispute and timeline.
4. `list_campaigns`: Get promotions, gifts, price protection, membership and pre-sale activities valid currently and on the specified date.
5. `list_policies`: Get policies and versions by region, channel, product type, order date and topic.
6. `get_product`: Get specifications, compatibility, inventory, instructions, maintenance, warranty and safety information of products and variants.

Optional write operations: `cancel_order`, `update_order`, `create_return`, `create_exchange`, `issue_refund`, `adjust_loyalty`. All are closed by default; any irreversible or monetary actions should be performed manually or confirmed twice.

## Structured return requirements

### Summary of recent orders

```json
{
  "customer_id": "cus_123",
  "matched_by": "verified_email",
  "retrieved_at": "2026-07-26T12:00:00Z",
  "orders": [
    {
      "order_id": "ord_123",
      "order_number": "#1234",
      "placed_at": "2026-07-01T03:04:05Z",
      "currency": "USD",
      "status": "paid",
      "line_items": [
        {"line_id": "li_1", "product_id": "p_1", "variant_id": "v_1", "sku": "SKU-1", "title": "Example", "variant": "Blue / M", "quantity": 1}
      ]
    }
  ]
}
```

### Complete order minimum fields

```json
{
  "order_id": "ord_123",
  "order_number": "#1234",
  "customer": {"customer_id": "cus_123", "email_verified": true},
  "channel": "online_store",
  "market": "US",
  "currency": "USD",
  "line_items": [],
  "totals": {"subtotal": 0, "discount": 0, "shipping": 0, "tax": 0, "duties": 0, "grand_total": 0},
  "payments": [],
  "fulfillments": [],
  "returns": [],
  "exchanges": [],
  "refunds": [],
  "disputes": [],
  "risk": {"status": "unknown", "customer_safe_reason": null},
  "shipping_address_masked": "***",
  "timeline": [],
  "retrieved_at": "2026-07-26T12:00:00Z"
}
```

### Activities and Policies

```json
{
  "source_url": "https://merchant.example/policies/returns",
  "title": "Return policy",
  "version": "2026-07-01",
  "retrieved_at": "2026-07-26T12:00:00Z",
  "effective_from": "2026-07-01",
  "effective_to": null,
  "markets": ["US"],
  "channels": ["online_store"],
  "product_filters": [],
  "terms": "Full source text or approved structured terms",
  "approved": true
}
```

## Data Quality Access Control

- Each response must come with source or connector name, crawl time, and stable ID.
- The amount must be returned as both a value and currency; the time uses ISO 8601 with time zone.
- Missing fields are returned as `null` or an empty array, not filled with guessed values.
- Order matching needs to return `matched_by`; high-risk actions cannot be performed based only on names or similar addresses.
- The policy should be able to read the historical version based on the order date; if there is only the current web page and the historical terms cannot be confirmed, manual processing will be performed.
- Tracking, policy and returns links visible to customers must come from approved domains.
- Automatic sending is prohibited when there is a connector error, insufficient permissions, data timeout or multi-source conflict.

## Platform selection suggestions

- Shopify, WooCommerce, BigCommerce and Wix: Use the official API path described in [platform-connectors.md](platform-connectors.md) and request only the read scopes the connector needs.
- Amazon, eBay, Etsy and Walmart: Read the marketplace's buyer-data and seller-permission limitations before configuring a connector. Do not pretend that independent-store customer or order actions apply directly.
- Self-built ERP/OMS: Provide the above six read-only interfaces and call them by fixed parameterization tools; do not allow the Agent to execute arbitrary SQL.
- When returns, subscriptions, memberships, and payments are managed by third-party systems, connect these systems as independent sources and retain their state time.
