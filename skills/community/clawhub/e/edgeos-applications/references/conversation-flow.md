# Conversation Flow (v1)

## Contract
- Keep messages short.
- Ask one question at a time.
- Confirm critical choices before submit.
- Pre-fill fields already known.
- Ask only for missing required fields.
- Do not show internal IDs unless user asks.

## Step 1 — Authenticate
1. If JWT exists and works, skip OTP.
2. Otherwise ask email.
3. Trigger OTP via `scripts/auth_request_otp.sh <email>`.
4. Ask for 6-digit code.
5. Exchange code via `scripts/auth_login.sh <email> <code>`.
6. Persist authenticated email (`SESSION_EMAIL`) for subsequent script calls.

Re-auth:
- Re-auth only after real `401`.

## Step 2 — Find accepted application
1. `GET /applications`.
2. Select accepted application.
3. Confirm target popup if multiple accepted applications exist.
4. Fetch `GET /applications/{application_id}` to resolve attendees.

## Step 3 — Product selection
1. Fetch products for popup: `GET /products?popup_city_id=<id>`.
2. Show active products in user language: name + price + relevant constraints.
3. Ask user to choose product(s) and attendee mapping.
4. Ask payment mode with wallet-awareness and discount context, using this wording:
   - "You can get a checkout link, or if you have a wallet configured I can pay directly via x402 (USDC on Base). Paying via x402 with a World ID verified agent gets you a 10% discount. Do you have a wallet set up?"

## Step 4 — Payment flow

### A) Crypto (x402)
1. Run `buy_ticket_challenge.sh --payload-file <payment-body.json>` (expect 402).
2. Parse challenge (`amount`, `payTo`, `network`, `asset`, `maxTimeoutSeconds`).
3. Tell user/agent exactly what will be signed.
4. Sign EIP-3009 TransferWithAuthorization.
5. Run `buy_ticket_submit.sh --payload-file <same-payment-body.json> --payment-signature-b64 <...>`.
6. If AgentKit challenge exists, include `--agentkit-b64 <...>` for discount.
7. Return success with settled amount + tx hash.

### B) Checkout link
1. `payment_preview.sh` and confirm total.
2. `payment_create.sh` and return checkout URL.
3. `payment_status.sh` only if user asks later.

## Error UX
- 401 → "Session expired, let's re-authenticate."
- First 402 → expected challenge, continue.
- Second 402 → "Payment verification failed" + actionable checks.
- 400 → ask user to correct only invalid input.
- 500 → explain settlement failure and offer retry.
