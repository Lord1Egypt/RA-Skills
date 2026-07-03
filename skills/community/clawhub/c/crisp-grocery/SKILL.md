---
name: crisp-grocery
description: Use this skill to help a user plan groceries with Crisp, inspect their user-authorized Crisp account data, compare promotions, check delivery windows and fees, fetch recipe/product images, and prepare basket changes. Use it only when the user asks for Crisp grocery planning, Crisp supermarket API inspection, meal planning from Crisp order history, promotion ranking, delivery-slot analysis, or supervised Crisp basket assistance.
---

# Crisp Grocery

This skill helps with user-authorized Crisp grocery planning and account inspection. It is read-only by default and must never place orders, change addresses, update payment details, contact support, or perform checkout.

## Safety Rules

- Treat account data as private. Do not print bearer tokens, one-time login codes, emails, phone numbers, addresses, IBAN fragments, invoice URLs, or full raw account payloads unless the user explicitly asks for that exact field.
- Do not include secrets in generated files, examples, issue reports, or ClawHub submissions.
- Use read-only endpoints by default.
- Basket mutations require explicit user confirmation naming the exact product/recipe, quantity, and intended action.
- Checkout, payment, address, phone, account deletion, support messages, and order cancellation are out of scope unless the user gives exact, action-specific confirmation.
- Do not bypass authentication, rate limits, bot checks, TLS, app controls, or server-side protections.
- Keep traffic low volume and user-driven. Cache API responses during a session instead of repeatedly fetching the same endpoint.
- Keep the app version/User-Agent configurable. If `/client` reports an `outdated` block, stop and ask the user for an updated app version.

## Configuration

Preferred environment variables:

- `CRISP_BEARER_TOKEN`: existing user-authorized bearer token.
- `CRISP_TOKEN_FILE`: path to a local token file. Use this only if `CRISP_BEARER_TOKEN` is unset.
- `CRISP_API_BASE`: default `https://crispapp.nl/v1`.
- `CRISP_USER_AGENT`: default `crisp/app/android/634`; update from the installed Android app build number when Crisp releases a newer app.
- `CRISP_OUTPUT_DIR`: default `artifacts/api`.

Token acquisition flow, when the user wants to log in:

1. Ask the user for the email address they want to use for Crisp login.
2. Generate a random 20-character alphanumeric local bearer token, or reuse a token file the user explicitly provided.
3. `POST /user/login` with `{ "email": "...", "country": "nl" }` using that bearer token.
4. Ask the user for the one-time code they received from Crisp.
5. `POST /user/login` with `{ "email": "...", "code": "...", "country": "nl" }` using the same bearer token.
6. Store the token only in a user-controlled local secret store or token file. Never include it in the skill package.

## Workflow

1. Check `/client` first for authorization and app-version status. If using Android, derive the user agent from the installed app `versionCode`/build number, for example `crisp/app/android/634`.
2. For delivery windows and fees, fetch `/basket/main`.
3. For personalization, fetch `/yourShop` and, when useful, `/order/history`.
4. For offers, fetch `/promo/current` and rank by percentage, euro savings, user history, menu relevance, and dietary fit.
5. For meal planning, use order history and `/recipe/:id` detail pages. Do not rely only on tags; inspect ingredients/allergens and reason about substitutions.
6. For images, use recipe/product blob IDs as `https://crispapp.nl/blob/<blob_id>?thumb=<size>`.
7. For any proposed basket edit, show the exact diff first and wait for confirmation.

## Common Commands

Use the helper script from this skill directory when available:

```bash
python3 scripts/crisp_api.py get /client
python3 scripts/crisp_api.py get /basket/main --save basket-main.json
python3 scripts/crisp_api.py get /promo/current --summary promos
python3 scripts/crisp_api.py get /yourShop --summary your-shop
python3 scripts/crisp_api.py get /order/history --summary orders
python3 scripts/crisp_api.py login-start user@example.com --country nl --token-file ./secrets/crisp_token.txt
python3 scripts/crisp_api.py login-code user@example.com 123456 --country nl --token-file ./secrets/crisp_token.txt
python3 scripts/crisp_api.py basket-add-product 6339 1 --from-screen YourShop --confirm "add product 6339 quantity 1"
```

## References

- Read `references/api-map.md` for endpoint behavior and payload fields.
- Read `references/planning-rules.md` for promotion ranking, meal planning, dietary handling, and basket-confirmation policy.
