---
name: flower-fruit-basket-balloon-delivery
description: "Flower, Fruit Basket, Balloon Delivery: Search Florist One products, place flower, balloon, or fruit basket delivery orders with card messages. Use when an agent needs flower, fruit basket, balloon delivery, flower fruit basket balloon delivery, send birthday flowers with a personalized message, order sympathy arrangements for a funeral home, browse anniversary and romance collections, schedule flower delivery for a specific date, get order, orderno through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery"}}
---
# Flower, Fruit Basket, Balloon Delivery

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Now your agent can send beautiful flower arrangements, balloon bouquets, and even fruit baskets! FloristOne delivers anywhere in the US and Canada, with same-day or scheduled delivery. Browse curated collections for birthdays, anniversaries, sympathy, and special occasions. Handle corporate flower and gift delivery in seconds. Send sympathy arrangements, employee recognition gifts, client thank-yous, and more. Add a personalized message on behalf of your company and choose same-day or scheduled delivery. The easy way to manage personal and business gifting in seconds.    ***Phone app installation required to approve credit card payment*** Download from here - https://www.agentpmt.com/download-mobile-app

## Product Instructions
### Florist One Flowers

#### Overview
Search flower products by category or product code, get full pricing with delivery fees and tax, and place flower delivery orders across the US. Prices shown in search results are product prices only — a $19.99 delivery fee and applicable sales tax are added at checkout.

#### Actions

##### list_categories
Returns all available product categories grouped by type.

**Required fields:** none

**Example:**
```json
{"action": "list_categories"}
```

Returns categories grouped as: Occasions (Best Sellers, Every Day, Birthday, Anniversary, Love & Romance, Get Well, New Baby, Thank You, Funeral and Sympathy), Product Types (Centerpieces, One Sided Arrangements, Vased Arrangements, Roses, Fruit Baskets, Plants, Balloons), Funeral Product Types (Funeral Best Sellers, Funeral Table Arrangements, Funeral Baskets, Funeral Sprays, Funeral Plants, Funeral Inside Casket, Funeral Wreaths, Funeral Hearts, Funeral Crosses, Funeral Casket Sprays, Funeral Urn Arrangements), Price Ranges (Under $60, $60–$80, $80–$100, Above $100, plus funeral equivalents), Seasonal Holidays (Christmas, Easter, Valentine's Day, Mother's Day), and Other (All Products).

---

##### search_products
Search for flower products by category name or by a specific product code. Provide exactly one of `category` or `product_code` — not both.

**Required fields (one of):**
- `category` (string) — category name or alias from list_categories (e.g., "Birthday", "roses", "funeral sprays")
- `product_code` (string) — specific Florist One product code (e.g., "F1-509", "E2-4305")

**Optional fields:**
- `limit` (integer, 1–50, default 12) — max results to return
- `page` (integer, min 1, default 1) — page number for pagination
- `sort` (string) — sort order: `popularity` (default), `price_asc`, `price_desc`, `az`, `za`

**Example — search by category:**
```json
{"action": "search_products", "category": "Birthday", "limit": 6, "sort": "price_asc"}
```

**Example — search by product code:**
```json
{"action": "search_products", "product_code": "E2-4305"}
```

Each product in results includes: `code`, `name`, `price`, `dimension`, `description`, `thumbnail_url`, `image_url`. The response also includes `total_available` for the total number of matching products.

---

##### get_order_total
Get the full price breakdown (product price, delivery fee, sales tax, order total) and resolved delivery date for a specific product and recipient ZIP code. **You MUST call this before placing an order** and confirm the total and delivery date with the user.

**Required fields:**
- `product_code` (string) — the product code from search results
- `recipient_zipcode` (string) — recipient's ZIP/postal code

**Optional fields:**
- `delivery_date` (string, MM-DD-YYYY) — desired delivery date. If omitted, the soonest available date is returned.

**Example:**
```json
{"action": "get_order_total", "product_code": "E2-4305", "recipient_zipcode": "30303"}
```

**Example with specific date:**
```json
{"action": "get_order_total", "product_code": "E2-4305", "recipient_zipcode": "30303", "delivery_date": "04-15-2026"}
```

Returns: `product_code`, `product_name`, `product_price`, `delivery_fee`, `tax`, `order_total`, `delivery_date`, `recipient_zipcode`. If the requested date is unavailable, the response includes `delivery_date_unavailable: true` and a list of `available_dates` — ask the user to choose one, then call get_order_total again with that date.

---

##### place_order
Place a flower delivery order. **You MUST call get_order_total first and confirm the total and delivery date with the user before calling this action.** The order will be rejected if `confirmed_total` is missing or does not match the current order total.

After calling place_order, a credit card request is sent to the user's mobile app. The order completes automatically once the user approves and enters their card details.

**Required fields:**
- `product_code` (string) — the product to order
- `confirmed_total` (number) — the `order_total` value returned by get_order_total, confirmed by the user
- `delivery_date` (string, MM-DD-YYYY) — the delivery date from get_order_total
- `recipient` (object) — delivery recipient with these fields:
  - `name` (string, required) — recipient's full name
  - `phone` (string, required) — 10-digit phone number
  - `address1` (string, required) — street address
  - `address2` (string, optional) — apt/suite/unit
  - `city` (string, required) — city
  - `state` (string, required) — 2-letter state code
  - `zipcode` (string, required) — ZIP/postal code
  - `institution` (string, optional) — hospital, funeral home, etc.
- `card_message` (string, required, max 200 characters) — message on the card

**Optional fields:**
- `special_instructions` (string, max 100 characters) — delivery instructions
- `idempotency_key` (string) — prevents duplicate orders when retrying

**Example:**
```json
{
  "action": "place_order",
  "product_code": "E2-4305",
  "confirmed_total": 84.97,
  "delivery_date": "04-15-2026",
  "recipient": {
    "name": "Jane Smith",
    "phone": "4045551234",
    "address1": "200 Peachtree St NW",
    "city": "Atlanta",
    "state": "GA",
    "zipcode": "30303"
  },
  "card_message": "Happy Birthday! Thinking of you."
}
```

---

##### get_order
Look up a completed order by its confirmation number.

**Required fields:**
- `orderno` (string) — the Florist One confirmation number returned by place_order

**Example:**
```json
{"action": "get_order", "orderno": "FO-123456"}
```

---

##### list_orders
List past orders with pagination.

**Optional fields:**
- `limit` (integer, 1–50, default 12) — max results to return
- `offset` (integer, min 0, default 0) — skip first N results

**Example:**
```json
{"action": "list_orders", "limit": 10, "offset": 0}
```

---

#### Common Workflows

##### 1. Browse and Order Flowers for a Birthday
1. `list_categories` — see available categories
2. `search_products` with `category: "Birthday"` — browse birthday arrangements
3. `get_order_total` with the chosen `product_code` and `recipient_zipcode` — get full pricing and delivery date
4. Confirm the total and delivery date with the user
5. `place_order` with the confirmed details — sends payment request to user's mobile app

##### 2. Send Sympathy Flowers to a Funeral Home
1. `search_products` with `category: "Funeral and Sympathy"` — browse funeral arrangements
2. `get_order_total` with chosen `product_code`, `recipient_zipcode`, and optionally a specific `delivery_date`
3. Confirm pricing with user
4. `place_order` including `institution` in the recipient object (e.g., the funeral home name)

##### 3. Check Order Status
1. `get_order` with the `orderno` from a previous order — view order details
2. Or `list_orders` to see all past orders

#### Important Notes
- **Pricing:** Search result prices are product-only. The $19.99 delivery fee and sales tax are only shown via get_order_total.
- **Order flow is mandatory:** Always call get_order_total before place_order. Always confirm the total and delivery date with the user. The order is rejected if confirmed_total does not match (tolerance: $0.01).
- **Payment:** place_order does not complete the order immediately. It sends a credit card request to the user's mobile app. The order is fulfilled automatically after the user approves.
- **Same-day delivery cutoff:** Same-day deliveries can only be processed if payment is approved by 12:00 PM in the recipient's time zone. If approved later, delivery is automatically moved to the next available date.
- **Date format:** Always use MM-DD-YYYY format for delivery_date.
- **Idempotency:** Use `idempotency_key` when retrying to prevent duplicate orders. If a matching pending or completed order exists, the existing order is returned instead of creating a new one.
- **Category matching:** Categories accept names, aliases, and codes (e.g., "Birthday", "bday", "bd" all work). Use list_categories if unsure.
- **Card message limit:** Maximum 200 characters for the card message, 100 characters for special instructions.
- **Phone numbers:** Must include at least 10 digits. Country codes are stripped automatically.
- **US delivery only:** ZIP codes must be valid US 5-digit codes (9-digit codes are truncated to 5). Canadian postal codes are also accepted.

## When To Use
- Use this skill for `Flower, Fruit Basket, Balloon Delivery` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: flower, fruit basket, balloon delivery, flower fruit basket balloon delivery, send birthday flowers with a personalized message, order sympathy arrangements for a funeral home, browse anniversary and romance collections, schedule flower delivery for a specific date, get order, orderno.
- Supported action names: `get_order`, `get_order_total`, `list_categories`, `list_orders`, `place_order`, `search_products`.

## Use Cases
- Send birthday flowers with a personalized message
- order sympathy arrangements for a funeral home
- browse anniversary and romance collections
- schedule flower delivery for a specific date
- thank a client with a fruit basket
- recognize an employee with a surprise delivery
- send get-well wishes to a hospital
- congratulate someone with a balloon bouquet

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `6`.
x402 availability: not enabled for this product.

- `get_order` (action slug: `get-order`): Look up a completed order by its Florist One confirmation number. Price: `0` credits. Parameters: `orderno`.
- `get_order_total` (action slug: `get-order-total`): Get the full price breakdown (product price, delivery fee, tax, order total) and resolved delivery date for a product and recipient ZIP code. Must be called before place_order. Price: `0` credits. Parameters: `delivery_date`, `product_code`, `recipient_zipcode`.
- `list_categories` (action slug: `list-categories`): Returns all available product categories grouped by type (Occasions, Product Types, Funeral, Price Ranges, Seasonal, Other). Price: `0` credits. Parameters: none.
- `list_orders` (action slug: `list-orders`): List past flower delivery orders with pagination. Price: `0` credits. Parameters: `limit`, `offset`.
- `place_order` (action slug: `place-order`): Place a flower delivery order. Requires calling get_order_total first and confirming the total with the user. A credit card request is sent to the user's mobile app after calling this action. Price: `0` credits. Parameters: `card_message`, `confirmed_total`, `delivery_date`, `idempotency_key`, `product_code`, `recipient`, `special_instructions`.
- `search_products` (action slug: `search-products`): Search for flower products by category name/alias or by a specific product code. Provide exactly one of category or product_code. Price: `0` credits. Parameters: `category`, `limit`, `page`, `product_code`, `sort`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "flower-fruit-basket-balloon-delivery"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "flower-fruit-basket-balloon-delivery"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "flower-fruit-basket-balloon-delivery"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "flower-fruit-basket-balloon-delivery"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "flower-fruit-basket-balloon-delivery"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "flower-fruit-basket-balloon-delivery"
  }
}
```

## Call This Tool
Product slug: `flower-fruit-basket-balloon-delivery`

Marketplace page: https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Flower-Fruit-Basket-Balloon-Delivery",
    "arguments": {
      "action": "get_order",
      "orderno": "example orderno"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "flower-fruit-basket-balloon-delivery",
  "parameters": {
    "action": "get_order",
    "orderno": "example orderno"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_order` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/flower-fruit-basket-balloon-delivery
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
