# API Contract (EdgeOS Applications + Ticket Purchase)

Use this file as the canonical contract for this skill runtime.
Base URL: `https://api-citizen-portal.simplefi.tech`.

## Auth

### 1) Request OTP code
- **POST** `/citizens/authenticate`
- Body: `{"email":"user@example.com","use_code":true}`

### 2) Exchange OTP for JWT
- **POST** `/citizens/login?email=<urlencoded>&code=<6digit>`
- Success: `{"access_token":"...","token_type":"bearer"}`

Re-auth rule:
- Re-authenticate only on `401` (expired/invalid token).

## Applications + attendees

### 3) List applications
- **GET** `/applications`
- Header: `Authorization: Bearer <JWT>`
- Find the target application where `status == "accepted"`.
- Key fields: `id`, `popup_city_id`, `status`.

### 4) Get application details
- **GET** `/applications/{application_id}`
- Header: `Authorization: Bearer <JWT>`
- Use `attendees[].id` for ticket purchase.

## Products

### 5) List products
- **GET** `/products?popup_city_id=<id>`
- Header: `Authorization: Bearer <JWT>`
- Keep only `is_active == true`.
- Key fields:
  - `id`, `name`, `price`, `category`, `attendee_category`, `insurance_percentage`
  - `min_price` / `max_price` for variable-price products

## Payments (x402 via /agent/buy-ticket)

### 6) First request (expect 402 challenge)
- **POST** `/agent/buy-ticket`
- Header: `Authorization: Bearer <JWT>`
- Body:
  - `application_id`
  - `products[]` items with `product_id`, `attendee_id`, `quantity`
  - optional: `coupon_code`, `insurance`, `custom_amount` (required for variable-price products)
- No `PAYMENT-SIGNATURE` header in this first call.
- Expected: **402 Payment Required**

From `accepts[0]`, extract:
- `amount` (USDC atomic units, 6 decimals)
- `payTo`
- `network` (expected `eip155:8453`)
- `asset` (USDC on Base)
- `maxTimeoutSeconds`
- `extra` (`name`, `version`, `assetTransferMethod`)

The same payload is also present in `PAYMENT-REQUIRED` header (base64 JSON).

### 7) Sign EIP-3009 TransferWithAuthorization
Use EIP-712 typed data:
- Domain:
  - `name: "USD Coin"`
  - `version: "2"`
  - `chainId: 8453`
  - `verifyingContract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Type: `TransferWithAuthorization`
- Message:
  - `from`: user wallet
  - `to`: `payTo`
  - `value`: `amount`
  - `validAfter`: `now - 600`
  - `validBefore`: `now + maxTimeoutSeconds`
  - `nonce`: random 32-byte hex

### 8) Submit payment
- Re-send **same** `POST /agent/buy-ticket` body
- Add header `PAYMENT-SIGNATURE` with base64 JSON:
  - `x402Version`, `resource`, `accepted`, `payload.signature`, `payload.authorization`
- Optional: add `AGENTKIT` header for discount proof

Success:
- **200** with approved payment object (`source: "x402"`)
- `PAYMENT-RESPONSE` header contains base64 JSON with tx hash (`transaction`) and `network`

## AgentKit optional discount

If `extensions.agentkit` is present in 402 response:
- Build SIWE (EIP-4361) message from challenge (`domain`, `uri`, `version`, `nonce`, `issuedAt`, `resources`)
- Sign with `personal_sign` (EIP-191)
- Send `AGENTKIT` header (base64 JSON) with fields:
  - `domain`, `address`, `uri`, `version`, `chainId`, `type`, `nonce`, `issuedAt`, `signature`, `resources`

If verification succeeds and wallet is registered, discount is applied before payment verification.
Sign EIP-3009 for the discounted amount.

## Guardrails

- Never create or settle payment when application is not `accepted`.
- Keep internal IDs hidden unless user asks.
- Never expose OTP/JWT or raw private key material.
- Display USDC amounts in human units for chat (`atomic / 1_000_000`).
- For the second `/agent/buy-ticket` call, keep body identical to first call.
