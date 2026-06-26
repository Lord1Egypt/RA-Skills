
name: add-tiffin-order-roty-input
description: "POST-only: Parse 'Roty input' messages and create Roty orders via HTTPS POST (no Playwright/UI automation)."

# Add Tiffin Order - Roty Input (POST-only)

## Trigger
Run when an inbound message contains the exact phrase **"Roty input"** (case-insensitive).

## Important
- **DO NOT use Playwright, browser automation, screenshots, or vision clicks.**
- This skill creates orders **only** by sending a JSON payload via **HTTPS POST** to:
`https://newdailyorderandcartcreation-818352713629.australia-southeast1.run.app`

## Execution (MANDATORY)
When triggered, you MUST call the dispatcher script and use its output.
Do NOT manually construct curl or JSON payloads.

Run:
python3 /data/.openclaw/workspace/skills/add-tiffin-order-roty-input/scripts/handle_message.py <sender_id> "<full inbound message>"

Rules:
- Always POST using the dispatcher (unless it returns Missing address/dates/product).
- Never hardcode perProductCost (never "[15]").
- Never use hardCodedPrice for perProductCost.
- perProductCost MUST come from pricing_engine.py via handle_message.py.

## Authorization (Telegram)
- Only allow Telegram users whose `from.id` is in:
`data/allowed_users.json` under `admins` or `vendors`.
- If unauthorized: reply "Not authorized."

## Behavior
1. Parse messy input into:
   - customerName
   - userAddress
   - deliveryDates (must resolve at least 1 date; otherwise ask a follow-up)
   - product selection + modifiers
   - specialRequests
2. Build payload in the exact API shape (see build_payload.py).
3. **Send POST immediately** (no "Dry-run vs Live" prompt), unless:
   - address missing, OR
   - no dates resolved, OR
   - product not matched
   In those cases, ask only for the missing piece.
4. On success: confirm with cartNo.

## Scripts
- Dispatcher: `scripts/handle_message.py`
- Parser: `scripts/parse_roty_input.py`
- Matcher: `scripts/match_product_and_modifiers.py`
- Pricing: `scripts/pricing_engine.py`
- Payload: `scripts/build_payload.py`
- POST sender (urllib): `scripts/post_order.py`
- Products registry: `data/products_roty.json`
- Allowlist: `data/allowed_users.json`
