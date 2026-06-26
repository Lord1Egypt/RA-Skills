---
name: foodpanda-cli
description: >-
  Order food from foodpanda.ph using the foodpanda-cli command-line tool.
  Use when the user wants to search restaurants, browse menus, build a cart,
  or place a food delivery order in the Philippines.
  Requires Node.js and shell access.
compatibility: Requires Node.js 18+, npm, and shell access. Philippines only (foodpanda.ph).
metadata:
  author: johnwhoyou
  version: "0.1.0"
---

# foodpanda-cli

A command-line tool for ordering food delivery from foodpanda.ph. All commands output structured JSON to stdout. Designed for the Philippines market only.

## Prerequisites & Installation

Ensure Node.js 18+ and npm are available, then install globally:

```bash
npm install -g foodpanda-cli
```

Verify the installation:

```bash
foodpanda-cli --version
```

## Initial Setup (One-Time)

Before using any other commands, complete these two setup steps:

### 1. Set delivery location

Provide the user's delivery coordinates (latitude and longitude in the Philippines):

```bash
foodpanda-cli location <latitude> <longitude>
```

Example:

```bash
foodpanda-cli location 14.5995 120.9842
# => {"success": true, "latitude": 14.5995, "longitude": 120.9842}
```

### 2. Log in

Opens a browser window for the user to log in to their foodpanda account. The session token is captured automatically. This step requires user interaction.

```bash
foodpanda-cli login
```

An optional `--timeout <seconds>` flag controls how long to wait (default: 120s).

## Command Reference

### Search & Discovery

**Search restaurants:**

```bash
foodpanda-cli search <query> [--cuisine <type>] [--limit <n>]
```

Returns an array of matching restaurants with `id` (vendor code), `name`, `cuisine`, `rating`, `delivery_fee`, `delivery_time`, `is_open`, and optionally `chain_code`.

**List chain outlets:**

```bash
foodpanda-cli outlets <chain_code>
```

Lists all branches of a restaurant chain. Use the `chain_code` from search results.

**Get restaurant details:**

```bash
foodpanda-cli restaurant <vendor_code>
```

Returns full details: address, description, opening hours, delivery availability.

### Menu & Items

**Browse menu:**

```bash
foodpanda-cli menu <vendor_code>
```

Returns the menu organized by category. Each item includes `code`, `name`, `price`, and `description`. Use item codes for adding to cart.

**Get item details (toppings & variations):**

```bash
foodpanda-cli item <vendor_code> <product_code>
```

Returns full item details including `topping_groups` (with options, prices, and min/max quantities) and `variation` info. Always check this before adding items with customizations.

### Cart Management

**Add items to cart:**

```bash
foodpanda-cli add <vendor_code> --items '<json_array>'
```

The `--items` flag takes a JSON array. Each element:

```json
[
  {
    "item_id": "product-code",
    "quantity": 1,
    "topping_ids": ["101", "205"],
    "special_instructions": "No onions"
  }
]
```

Only `item_id` and `quantity` are required. `topping_ids` and `special_instructions` are optional.

**View cart:**

```bash
foodpanda-cli cart
```

Returns the current cart with all items, quantities, prices, fees, and total. Returns `{"message": "Cart is empty."}` if empty.

**Remove item from cart:**

```bash
foodpanda-cli remove <cart_item_id>
```

Remove an item by its `cart_item_id` (e.g., `cart-1`, `cart-2`). These IDs are shown in cart output.

### Ordering

**Preview order:**

```bash
foodpanda-cli preview
```

Returns the full order preview: cart contents, selected delivery address, available payment methods, and totals. Always run this before placing an order.

**Place order:**

```bash
foodpanda-cli order --payment <method> [--instructions <text>]
```

Places the order. Returns `order_id`, `status`, `estimated_delivery_time`, and `total`.

Currently only `payment_on_delivery` (Cash on Delivery) is supported as the payment method.

## Recommended Workflow

Follow these steps when the user wants to order food:

1. **Check setup** — Ensure location and login are configured. If the user hasn't set these up, run `location` and `login` first.
2. **Search** — Ask the user what they want to eat, then run `search` to find restaurants.
3. **Present options** — Show the user matching restaurants with names, cuisines, ratings, and delivery times.
4. **Browse menu** — Once the user picks a restaurant, run `menu` to see available items.
5. **Check item details** — If the user wants customizations, run `item` to see available toppings and variations.
6. **Build cart** — Use `add` to add items. Show the user the cart after each addition.
7. **Preview** — Run `preview` to show the final order summary with delivery address and total.
8. **Confirm and order** — ONLY after the user explicitly confirms, run `order --payment payment_on_delivery`.

## Important Rules

- **ALWAYS confirm with the user before running the `order` command.** This places a real order with real money. Never run it without explicit user approval.
- **Payment:** Only `payment_on_delivery` (Cash on Delivery) works. Do not attempt other payment methods.
- **Cart switching:** Adding items from a different restaurant clears the existing cart. Warn the user before doing this.
- **Errors:** All errors are returned as `{"error": "message"}`. If you get an authentication error, prompt the user to run `login` again.
- **Location required:** All commands except `location` and `login` require a delivery location to be set first.
- **Philippines only:** This tool only works with foodpanda.ph for delivery addresses in the Philippines.

## Common Patterns

### Filtering by cuisine

```bash
foodpanda-cli search "pizza" --cuisine "Italian" --limit 5
```

### Ordering with toppings

1. Get item details to find topping IDs:
   ```bash
   foodpanda-cli item p7nl ct-36-pd-1673
   ```
2. Add with selected toppings:
   ```bash
   foodpanda-cli add p7nl --items '[{"item_id":"ct-36-pd-1673","quantity":1,"topping_ids":["101","205"]}]'
   ```

### Finding a specific branch of a chain

1. Search returns `chain_code` for chain restaurants
2. List all branches:
   ```bash
   foodpanda-cli outlets cg0ep
   ```
3. Pick the closest/preferred branch and use its vendor code for menu and ordering
