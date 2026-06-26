---
name: shopify-store
description: Manage Shopify products, orders, customers, inventory, collections, and store operations via the Shopify Admin API with OAuth authentication. Use this skill when users want to read or modify Shopify store data, manage product listings, process orders, track inventory, or automate e-commerce workflows.
---

# Shopify

Manage a Shopify store via the Shopify Admin API with OAuth authentication. List and search products, process orders, track customers and inventory, manage collections, and automate store operations.

This skill uses [ClawLink](https://claw-link.dev) for hosted connection flows and credentials so you do not need to configure Shopify API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Shopify |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Shopify |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Shopify Admin   │
│   (User Chat)   │     │   (OAuth)    │     │      API         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Shopify  │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests   │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Shopify  │
   │  File    │           │ Auth     │           │ Store    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Shopify again."

## Quick Start

```bash
# List products
clawlink_call_tool --tool "shopify_list_products" --params '{}'

# Get a specific product
clawlink_call_tool --tool "shopify_get_product" --params '{"product_id": "PRODUCT_ID"}'

# Search customers
clawlink_call_tool --tool "shopify_search_customers" --params '{"query": "customer@example.com"}'
```

## Authentication

All Shopify tool calls are authenticated automatically by ClawLink using the user's connected Shopify store OAuth token.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Shopify Admin API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=shopify and connect Shopify.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `shopify` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration shopify
```

**Response:** Returns the live tool catalog for Shopify.

### Reconnect

If Shopify tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=shopify
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration shopify`

## Security & Permissions

- Access is scoped to the Shopify store connected during OAuth setup.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (cancel order, delete product, issue refund) are marked as high-impact and must be confirmed.
- Bulk delete operations cannot be undone and must be explicitly confirmed.

## Tool Reference

### Products

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_products` | List all products in the store with pagination and filters | Read |
| `shopify_get_product` | Get a single product by ID with variants, images, and metafields | Read |
| `shopify_search_products` | Search products by title, vendor, product type, or tag | Read |
| `shopify_count_products` | Get total product count with optional filters | Read |
| `shopify_create_product` | Create a new product with variants, options, and images | Write |
| `shopify_update_product` | Update an existing product's title, description, or status | Write |
| `shopify_delete_product` | Permanently delete a product from the store | Write |
| `shopify_create_product_variant` | Add a new variant to an existing product | Write |
| `shopify_update_product_variant` | Update a product variant's price, SKU, or inventory | Write |
| `shopify_get_product_images` | List all images for a product | Read |
| `shopify_create_product_image` | Upload a new image to a product | Write |
| `shopify_create metafield` | Create a metafield on a product for custom metadata | Write |
| `shopify_bulk_create_products` | Create many products (20-50+) via bulk GraphQL mutation | Write |

### Inventory

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_inventory_levels` | List inventory levels across locations | Read |
| `shopify_adjust_inventory_level` | Increase or decrease stock at a specific location | Write |
| `shopify_connect_inventory_level` | Connect an inventory item to a location | Write |
| `shopify_list_locations` | List all warehouse and retail locations | Read |
| `shopify_count_locations` | Get the number of configured locations | Read |

### Orders

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_orders` | List orders with status and date filters | Read |
| `shopify_get_order` | Get a single order with line items and fulfillment data | Read |
| `shopify_search_orders` | Search orders by name, email, or tag | Read |
| `shopify_count_orders` | Get order count filtered by status | Read |
| `shopify_create_order` | Create a new committed order | Write |
| `shopify_update_order` | Update an order's status or metadata | Write |
| `shopify_cancel_order` | Cancel an unpaid or unfulfilled order | Write |
| `shopify_close_order` | Close an order (all items fulfilled/cancelled) | Write |
| `shopify_calculate_refund` | Preview accurate refund amounts before processing | Read |
| `shopify_create_refund` | Process a full or partial refund for an order | Write |
| `shopify_create_fulfillment` | Mark items as shipped and create fulfillment | Write |
| `shopify_cancel_fulfillment` | Cancel an existing fulfillment | Write |

### Customers

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_customers` | List all customers with pagination | Read |
| `shopify_get_customer` | Get a customer by ID with addresses and orders | Read |
| `shopify_search_customers` | Search customers by email, name, or tag | Read |
| `shopify_count_customers` | Get total customer count | Read |
| `shopify_create_customer` | Create a new customer record | Write |
| `shopify_update_customer` | Update customer information or addresses | Write |
| `shopify_delete_customer` | Delete a customer with no existing orders | Write |
| `shopify_create_customer_address` | Add a new address to a customer | Write |
| `shopify_delete_customer_address` | Remove an address from a customer | Write |
| `shopify_bulk_delete_customer_addresses` | Remove multiple addresses at once | Write |

### Collections

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_custom_collections` | List all custom (manually curated) collections | Read |
| `shopify_get_custom_collection` | Get a collection by ID | Read |
| `shopify_create_custom_collection` | Create a new custom collection | Write |
| `shopify_update_custom_collection` | Update collection title, description, or image | Write |
| `shopify_delete_custom_collection` | Delete a custom collection | Write |
| `shopify_add_product_to_custom_collection` | Add a product to a custom collection | Write |
| `shopify_remove_product_from_custom_collection` | Remove a product from a custom collection | Write |
| `shopify_count_custom_collections` | Get custom collection count | Read |
| `shopify_create_smart_collection` | Create an automated smart collection | Write |

### Fulfillment & Shipping

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_fulfillment_orders` | List fulfillment orders for an order | Read |
| `shopify_get_fulfillment_order` | Get details of a specific fulfillment order | Read |
| `shopify_apply_fulfillment_hold` | Pause a fulfillment order due to issues | Write |
| `shopify_cancel_fulfillment_order` | Cancel a fulfillment order and create a replacement | Write |
| `shopify_create_fulfillment_event` | Add a tracking event to a shipment | Write |

### Discounts & Pricing

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_create_price_rule` | Create a discount price rule (defines the discount logic) | Write |
| `shopify_list_price_rules` | List all price rules | Read |
| `shopify_create_discount_code` | Create a customer-facing discount code | Write |
| `shopify_create_discount_code_batch` | Create up to 100 discount codes at once | Write |
| `shopify_count_price_rules` | Get price rule count | Read |
| `shopify_create_coupon` | Create a discount coupon with percentage or fixed amount | Write |

### Store Content

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_articles` | List blog articles across all blogs | Read |
| `shopify_create_article` | Create a new blog article | Write |
| `shopify_update_article` | Update an existing blog article | Write |
| `shopify_delete_article` | Permanently delete a blog article | Write |
| `shopify_list_pages` | List static store pages | Read |
| `shopify_create_page` | Create a new static page | Write |
| `shopify_list_blogs` | List all blogs | Read |
| `shopify_create_blog` | Create a new blog | Write |

### Webhooks & Events

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_list_webhooks` | List all webhook subscriptions | Read |
| `shopify_create_webhook` | Subscribe to a store event via webhook | Write |
| `shopify_delete_webhook` | Remove a webhook subscription | Write |
| `shopify_count_webhooks` | Get webhook count | Read |
| `shopify_list_events` | List store activity events | Read |
| `shopify_count_events` | Get event count with filters | Read |

### Billing

| Tool | Description | Mode |
|------|-------------|------|
| `shopify_create_app_subscription` | Create a recurring billing charge | Write |
| `shopify_cancel_app_subscription` | Cancel an active app subscription | Write |
| `shopify_create_one_time_application_charge` | Create a one-time billing charge | Write |

## Code Examples

### List products

```bash
clawlink_call_tool --tool "shopify_list_products" \
  --params '{
    "limit": 10,
    "status": "active"
  }'
```

### Get a specific order

```bash
clawlink_call_tool --tool "shopify_get_order" \
  --params '{
    "order_id": "ORDER_ID"
  }'
```

### Create a new customer

```bash
clawlink_call_tool --tool "shopify_create_customer" \
  --params '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "phone": "+15551234567"
  }'
```

### Search customers by email

```bash
clawlink_call_tool --tool "shopify_search_customers" \
  --params '{
    "query": "jane.doe@example.com"
  }'
```

### Adjust inventory level

```bash
clawlink_call_tool --tool "shopify_adjust_inventory_level" \
  --params '{
    "inventory_item_id": "INVENTORY_ITEM_ID",
    "location_id": "LOCATION_ID",
    "available_adjustment": -5
  }'
```

### Create a price rule and discount code

```bash
clawlink_call_tool --tool "shopify_create_price_rule" \
  --params '{
    "title": "SUMMER_SALE",
    "value_type": "percentage",
    "value": "-20",
    "customer_selection": "all"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Shopify is connected.
2. Call `clawlink_list_tools --integration shopify` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `shopify`.
5. If no Shopify tools appear, direct the user to https://claw-link.dev/dashboard?add=shopify.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → count → call                         │
│                                                             │
│  Example: List products → Get product details → Show result │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview refund → User approves → Process refund    │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Products with many variants may require multiple API calls to fetch full variant data.
- Order cancellation is only possible for orders that are not already paid or fulfilled.
- Refunds require calculating first (`shopify_calculate_refund`) to get accurate transaction data.
- Bulk operations (bulk product creation, bulk metafield deletion) run asynchronously and return a job ID.
- Webhook subscriptions require a publicly accessible callback URL.
- Metafield operations require knowing the namespace and key for the target resource.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration shopify`. |
| Missing connection | Shopify is not connected. Direct the user to https://claw-link.dev/dashboard?add=shopify. |
| `product_not_found` | The product ID does not exist or has been deleted. |
| `order_not_found` | The order ID does not exist or has been deleted. |
| `customer_not_found` | The customer ID does not exist. |
| `not_authorised` | The connected account lacks permission for this operation. |
| ` fulfillment_not_cancellable` | The fulfillment has already been completed or cannot be cancelled. |
| `order_already_cancelled` | The order has already been cancelled. |
| `RefundAmountMismatch` | Calculated refund amounts don't match expected values. Re-calculate first. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `shopify`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.
4. Confirm the target resource exists before attempting updates or deletions.

## Resources

- [Shopify Admin API](https://shopify.dev/docs/api/admin)
- [Shopify REST Admin API Reference](https://shopify.dev/docs/api/admin-rest)
- [Shopify GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql)
- [Shopify OAuth Documentation](https://shopify.dev/docs/apps/auth/oauth)
- ClawLink: https://claw-link.dev
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)