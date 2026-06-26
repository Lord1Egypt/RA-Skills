# EdgeOS API Flow (v1)

Base settings:
- source `{baseDir}/scripts/env.sh`
- `BASE_URL` comes from that file
- Auth header: `Authorization: Bearer $JWT`

## 1) Request OTP
Use script: `scripts/auth_request_otp.sh <email>`
(under the hood: `POST /citizens/authenticate` with `use_code=true`)

## 2) Exchange OTP for JWT
Use script: `scripts/auth_login.sh <email> <6digit>`
(under the hood: `POST /citizens/login?email=<urlencoded>&code=<6digit>`)

`auth_login.sh` persists `access_token` into script state under `scripts/.state/` keyed by email.
Other scripts auto-load token for `SESSION_EMAIL` when `JWT` env is not provided.
Do not request a new OTP unless API returns 401/unauthorized or JWT is missing.

## 3) Resolve accepted application
- `GET /applications`
- Select application with `status=accepted`
- Store `application_id` and `popup_city_id`

## 4) Resolve attendees
- `GET /applications/{application_id}`
- Extract `attendees[].id` for each purchase line

## 5) Product retrieval (accepted only)
- `GET /products?popup_city_id=<id>`
- Keep only active products (`is_active=true`)
- Support fixed-price and variable-price products (`min_price` / `max_price` + `custom_amount`)

## 6) Checkout-link flow (SimpleFi)
- Preview: `scripts/payment_preview.sh`
- Create: `scripts/payment_create.sh`
- Status: `scripts/payment_status.sh`

## 7) Crypto flow (x402 via /agent/buy-ticket)
When user chooses crypto payment:

**Step 1 — Get payment challenge:**
- Use script: `scripts/buy_ticket_challenge.sh --payload-file <payment-create-body.json>`
- (under the hood: `POST /agent/buy-ticket` with JWT + payment body, no `PAYMENT-SIGNATURE`)
- Expect 402

Parse from 402 JSON:
- `accepts[0].amount` (USDC atomic)
- `accepts[0].payTo`
- `accepts[0].network`
- `accepts[0].asset`
- `accepts[0].maxTimeoutSeconds`
- `accepts[0].extra`
- optional `extensions.agentkit` challenge/discount

**Step 2 — Sign EIP-3009:**
- Domain uses USD Coin v2 on Base (chainId 8453)
- Sign `TransferWithAuthorization(from,to,value,validAfter,validBefore,nonce)`

**Step 3 — Submit payment:**
- Use script: `scripts/buy_ticket_submit.sh --payload-file <same-body.json> --payment-signature-b64 <...> [--agentkit-b64 <...>]`
- (or pass `--payment-signature-file` / `--agentkit-file` JSON files and let the script base64-encode)
- Re-send exact same body to `POST /agent/buy-ticket`
- Include `PAYMENT-SIGNATURE` header (base64 x402 payload)
- Include `AGENTKIT` header when discount proof is available
- Success returns approved payment + transaction hash in `PAYMENT-RESPONSE`

## 8) Error handling
- `401`: re-auth and retry
- first `402`: expected challenge
- second `402`: payment verification failure (balance/signature/timing/amount)
- `400`: invalid request (wrong ids/status/body constraints)
- `500`: settlement/on-chain failure; retry after wallet/state checks
