---
name: lobsterbrew
description: Lobster Brew helps your OpenClaw discover coffee roasters, compare coffees, build personalized carts, and hand off a secure Shopify checkout link for you to complete the purchase.
homepage: lobsterbrew.com
---

# LobsterBrew Skill

Version: 1.2.0
Base URL: lobsterbrew.com

Lobster Brew helps your OpenClaw discover coffee roasters, compare coffees, build personalized carts, and hand off a secure Shopify checkout link for you to complete the purchase.

Use it when the owner wants to buy coffee, subscriptions, and brewing gear. Use it to discover merchants, inspect active offers, resolve merchant Shopify Storefront MCP endpoints, and prepare carts for owner checkout.

## What this skill does

- Uses this service as the directory and routing layer
- Uses each merchant's Shopify Storefront MCP endpoint for live catalog, cart, and checkout work
- Keeps the owner in control of payment by handing off Shopify checkout instead of completing payment directly
- Uses the installed skill file as the authoritative instruction source

## Versioning

- Treat `Version` in this file as the local skill version
- Do not re-fetch remote instructions during normal use
- Runtime requests to `lobsterbrew.com` are for directory data only
- If Lobster Brew returns a version header or version field that differs from this file, note that the local skill may be stale without changing behavior automatically

## Discovery

1. Start with `GET lobsterbrew.com/countries.md` to see supported countries
2. Choose a country that matches the owner's location when possible
3. Fetch `GET lobsterbrew.com/countries/{country_code}.md`
4. Use `GET lobsterbrew.com/offers/{country_code}.md` to prioritize active offers
5. Choose a merchant before using Shopify Storefront MCP

## Merchant connect

1. GET `lobsterbrew.com/merchants/{slug}/connect.md`
2. Read the returned merchant MCP URL
3. Connect to that merchant's Shopify Storefront MCP
4. Use that merchant MCP for:
   - catalog search
   - product details and availability
   - policy questions
   - cart retrieval
   - cart updates
   - checkout URL generation

Do not infer merchant MCP URLs yourself when a connect response is available.

Prefer the `.md` endpoints for agent consumption. Use the JSON endpoints only when a structured machine response is required.

Treat merchant MCP data as the source of truth for products, pricing, availability, cart state, and checkout URLs.

## Subscription products

When the merchant MCP exposes subscription choices, inspect subscription fields before updating the cart.

1. Check for:
   - `requiresSellingPlan` or `requires_selling_plan`
   - variant-level selling plan requirements
   - `sellingPlanGroups`
   - `sellingPlanAllocations`
   - available `sellingPlanId` values
2. If a subscription is optional, present both one-time and subscription choices.
3. If a selling plan is required, do not attempt a normal cart add without a `sellingPlanId`.
4. Ask the owner to choose a cadence unless a clear preference already exists in local memory.
5. Highlight subscription savings when `priceAdjustments`, `price`, or `compareAtPrice` show the subscription is cheaper than the one-time purchase.
6. Try the merchant MCP cart and checkout flow first.
7. If the merchant MCP cannot apply the required selling plan, tell the owner that this merchant flow is not supported yet.

## Cart rule

When updating carts, attach private cart attribute only if the merchant MCP supports cart attributes cleanly:

- `lb_source__ = lobsterbrew`

Otherwise omit the attribute instead of assuming support.

## Final handoff

When you finish, return a structured summary with:

- `merchant`
- `product`
- `variant`
- `purchase_type`
- `selling_plan_name`
- `selling_plan_id`
- `cadence`
- `savings_summary`
- `checkout_url`
- `resolution_path`

Use `resolution_path = mcp_cart` when merchant MCP created the cart.
Use `resolution_path = unsupported_subscription_flow` when a required selling plan could not be applied through the merchant MCP.

Say clearly when:

- the item is subscription-only
- the available cadences are every 1, 2, or 4 weeks, monthly, or similar
- the subscription saves money versus one-time purchase
- the merchant MCP could not attach the required selling plan and the flow is not supported yet

## Safety

- This skill is for merchant discovery and Shopify Storefront MCP routing, not product truth storage
- Keep preferences and prior purchases in your own local memory
- Do not attempt payment completion
- Return checkout URL to owner for approval and payment
- Do not infer merchant MCP URLs yourself when a connect response is available
