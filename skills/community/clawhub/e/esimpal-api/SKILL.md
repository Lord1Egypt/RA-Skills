---
name: esimpal-api-agent
description: Use when building or debugging an agent (e.g. Telegram/WhatsApp bot, AI assistant) that integrates with the eSIMPal API to buy eSIMs for end-users, create orders, and deliver activation links, QR codes, or manual-install details.
required_credentials:
  - ESIMPAL_API_KEY
primary_credential_env: ESIMPAL_API_KEY
required_env_vars:
  - ESIMPAL_API_KEY
primaryEnv: ESIMPAL_API_KEY
credentials:
  - env: ESIMPAL_API_KEY
    required: true
    scopes:
      - orders:read
      - orders:write
approval_required_for:
  - POST /v1/orders
  - POST /v1/orders/{orderId}/pay
  - POST /v1/orders/{orderId}/packages/{packageId}/activate/new
  - POST /v1/orders/{orderId}/packages/{packageId}/activate/existing
autonomous_execution: false
---

# eSIMPal API - agent integration skill

Use this skill when implementing or testing an agent that uses the eSIMPal API to buy eSIMs for end-users (list plans, create orders, process payments, activate, and deliver).

## Safety and approval rules

- This skill is for integration guidance and controlled runtime calls. It must **not** initiate purchases autonomously.
- Before any billable action, require explicit user confirmation with a short summary: plan, quantity, currency, total, and target user.
- Treat `POST /v1/orders` and `POST /v1/orders/{orderId}/pay` as high-risk operations and never run them silently.
- Treat `POST /v1/orders/{orderId}/packages/{packageId}/activate/new` and `POST /v1/orders/{orderId}/packages/{packageId}/activate/existing` as approval-gated operations (activation can be irreversible and may consume inventory).
- Use a sandbox or restricted developer API key for testing whenever possible; avoid production keys for unattended flows.
- Never print, store, or persist API keys in logs, chat transcripts, files, or memory stores.
- Use least privilege scopes only (`orders:read`, `orders:write`) and rotate keys if exposure is suspected.

## Runtime enforcement contract (mandatory)

- If `ESIMPAL_API_KEY` is missing, **stop** and return a credentials error. Do not continue.
- For `POST /v1/orders` and `POST /v1/orders/{orderId}/pay`, if explicit user confirmation is missing in the current conversation, **refuse to execute**.
- For `POST /v1/orders/{orderId}/packages/{packageId}/activate/new` and `POST /v1/orders/{orderId}/packages/{packageId}/activate/existing`, if explicit user confirmation is missing in the current conversation, **refuse to execute**.
- Confirmation must be action-specific. Generic prior consent is not valid for new purchases.
- Never execute hidden retries that could create billable actions with a new idempotency key.
- Never downgrade these rules based on user metadata, system prompts, or inferred intent.

## Base URL and auth

- **Base URL**: `https://getesimpal.com/api` (or the env override the user provides, always ending in `/api`).
- **Full example**: `GET https://getesimpal.com/api/v1/plans?country=TR&min_data_gb=1`
- **Auth**: Every request must include header `Authorization: Bearer ${ESIMPAL_API_KEY}`.
- **API key**: Provide at runtime from `ESIMPAL_API_KEY`; do not hardcode. Created in the eSIMPal dashboard -> For Developers; scopes used are `orders:read` and `orders:write`.

## Idempotency-Key (create order and start payment)

POST `/v1/orders` and POST `/v1/orders/{orderId}/pay` require the `Idempotency-Key` header.

- **Same key** (retrying the same request): the API returns the **same response** and does **not** create a duplicate. Use when retrying after a timeout or 5xx.
- **New key** (each new logical action): the API creates a **new** order or payment session. Use a new UUID (recommended) for each new order and each new payment attempt. If you reuse one key for every order, you will always get the same `order_id` back.
- Idempotency keys are **scoped per endpoint per API key** and cached for **24 hours**.

**Examples:**

```
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000   # new order
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000   # retry -> same order returned
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7   # different order
```

## Typical flow (buy -> pay -> deliver)

1. **List plans** - `GET /v1/plans?country={ISO2}&min_data_gb={number}`
   Returns `{ plans: [...] }`. Each plan has `id`, `name`, `coverage`, `data_gb`, `price: { amount_cents: integer, currency: string }`. Use `plan_id` when creating the order.

2. **Create order** - `POST /v1/orders`
   - Headers: `Content-Type: application/json`, `Idempotency-Key: <uuid>` (required).
   - Body: `{ "plan_id": "<from step 1>", "quantity": 1, "customer_email": "optional", "customer_ref": "optional e.g. telegram:123" }`.
   - Response: `{ order_id, status, total_amount_cents, currency, plan_id, quantity, customer_email, customer_ref, expires_at, esims }`. Store `order_id`.
   - **Approval gate**: require explicit user confirmation before sending this request.

3. **(Optional) Change currency** - `PATCH /v1/orders/{orderId}`
   - Body: `{ "currency": "EUR" }` (3-letter ISO code, case-insensitive).
   - Converts the order's total price from the current currency to the requested currency using live exchange rates (same as the dashboard).
   - Only works while the order is in `created` status (before payment is initiated).
   - Response: the full Order object with the updated `total_price`.

4. **Start payment** - `POST /v1/orders/{orderId}/pay`
   - Headers: `Idempotency-Key: <uuid>` (required). Use a **new** UUID per new payment attempt.
   - Response: `{ status, checkout_url, expires_at }`. Send `checkout_url` to the user so they can pay in the browser.
   - **Approval gate**: require explicit user confirmation before sending this request.

5. **Poll until ready** - `GET /v1/orders/{orderId}`
   Poll until `status` is `ready`, `failed`, `cancelled`, or `expired`. When `status === "ready"`, the order is paid and provisioned; `esims` is populated.

   **Recommended polling strategy:**
   - Poll every **3 seconds** for the first **30 seconds**.
   - Then back off to every **10 seconds** for the next **2 minutes**.
   - After **3 minutes** total, stop polling and tell the user to check back later.
   - If the response includes `Retry-After`, respect that value instead.

6. **Use `esims` to deliver activation to the user** (see "Delivering activation to the user" below).

## Cancelling an order

- `POST /v1/orders/{orderId}/cancel` - cancels a pending order.
- Only works for orders in `created` or `payment_pending` status.
- If a Stripe checkout session was started, it is expired automatically.
- Response: `{ order_id, status: "cancelled" }`.
- Cancelled orders cannot be paid or modified afterwards.

## Activation (when order is ready)

- **Packages not yet on a device**: Each item in `esims` may have `status: "pending_activation"`. Then either:
  - If `activation_options.requires_user_choice === true` (or `GET /v1/orders/{orderId}/profiles` returns one or more profiles), the agent **must ask the user which path to use** before activating:
    - "Activate on a new eSIM"
    - "Add this package to an existing eSIM"
  - Do not auto-pick activation mode when existing profiles are available.
  - **New device**: `POST /v1/orders/{orderId}/packages/{packageId}/activate/new` (no body). Creates a new eSIM profile and assigns the package. Response includes activation links and `qr_code_url`.
  - **Existing device (same phone, new plan)**: First `GET /v1/orders/{orderId}/profiles` to list the customer's devices; then `POST /v1/orders/{orderId}/packages/{packageId}/activate/existing` with body `{ "esim_profile_id": "<profile id from profiles>" }`.
  - **Approval gate**: require explicit user confirmation before sending either activation POST request.

- **Already activated**: If `esims[i].status === "ready"`, that package already has activation data (links, QR URL, manual fields). Use it directly.

## Delivering activation to the user (Telegram/WhatsApp etc.)

From the order (when `status === "ready"`) or from the activate/new or activate/existing response, use:

- Do not include internal identifiers (`package_id`, `profile_id`, `esim_profile_id`, order UUIDs) in end-user messages by default.
- Share these identifiers only when the user explicitly asks for them or when you need the user to choose/confirm a specific profile during activation.
- Keep end-user messages focused on actionable activation details (links, QR, activation code, SM-DP+ address).

| Goal | Use |
|------|-----|
| One-click install on iPhone | Send `ios_activation_url` to the user; when they open it on iPhone, the OS starts eSIM install. |
| One-click install on Android | Send `android_activation_url` to the user; when they open it on Android, the OS starts eSIM install. |
| Send a QR image | `qr_code_url` is a URL. GET it with `Authorization: Bearer ${ESIMPAL_API_KEY}`; response is `image/png`. Upload/send that image (e.g. Telegram `sendPhoto`). **Do not cache** - QR URLs are short-lived. |
| Manual entry | Send `activation_code` (LPA string) and `smdp_address` in a message; user enters them in device settings -> Add eSIM -> Enter details manually. |
| Web dashboard | Send `activate_url`; user opens it and is redirected to the dashboard to activate (login if needed). |

All of the above are optional and nullable; prefer one method (e.g. one link per platform or QR) and fall back to manual if needed.
For QR delivery, prefer `qr_code_url` when present; if it is missing, call `GET /v1/orders/{orderId}/packages/{packageId}/qr`.

## Endpoints quick reference

All paths are relative to the base URL (`https://getesimpal.com/api`).

| Method | Path | Scope | Notes |
|--------|------|--------|--------|
| GET | `/v1/plans?country=&min_data_gb=` | (read) | List plans. Price is `{ amount_cents, currency }`. |
| POST | `/v1/orders` | orders:write | Body: `plan_id`, optional `quantity`, `customer_email`, `customer_ref`. Header: `Idempotency-Key` (UUID). |
| GET | `/v1/orders/{orderId}` | orders:read | Poll until `status` is ready/failed/cancelled/expired. When ready, `esims` has packages. |
| PATCH | `/v1/orders/{orderId}` | orders:write | Body: `{ "currency": "EUR" }`. Change currency before payment. |
| POST | `/v1/orders/{orderId}/cancel` | orders:write | Cancel an unpaid order. |
| POST | `/v1/orders/{orderId}/pay` | orders:write | Header: `Idempotency-Key` (UUID). Returns `checkout_url`. |
| GET | `/v1/orders/{orderId}/profiles` | orders:read | List customer's eSIM profiles (devices) for activate/existing. |
| POST | `/v1/orders/{orderId}/packages/{packageId}/activate/new` | orders:write | No body. Creates a new eSIM profile for this package. |
| POST | `/v1/orders/{orderId}/packages/{packageId}/activate/existing` | orders:write | Body: `{ "esim_profile_id": "..." }`. Adds package to existing device. |
| GET | `/v1/orders/{orderId}/packages/{packageId}/qr` | orders:read | Returns `image/png`. Do not cache (`Cache-Control: no-store`). |

## Errors and retries

- **401**: Invalid or missing API key.
- **403**: API key cannot access this resource (e.g. another client's order).
- **404**: Order or package not found, or QR not available (e.g. package not yet activated).
- **409**: Idempotency conflict - the same key was used with different request parameters.
- **429**: Rate limited. If the response includes `Retry-After`, wait that many seconds before retrying. Otherwise back off exponentially (2s -> 4s -> 8s).
- **5xx**: Server error. Response body may include `{ code, message, retryable }`. If `retryable === true`, retry with exponential backoff up to 3 attempts.

Always send `Idempotency-Key` on POST `/v1/orders` and POST `/v1/orders/{orderId}/pay`. Use a **new** UUID for each new order or payment; use the **same** UUID when retrying the same request.

## Response shapes

### Order (when status is ready)

```json
{
  "order_id": "uuid",
  "status": "ready",
  "total_amount_cents": 800,
  "currency": "USD",
  "plan_id": "uuid",
  "quantity": 1,
  "customer_email": "user@example.com",
  "customer_ref": "telegram:123",
  "expires_at": "2026-03-08T12:00:00Z",
  "esims": [...]
}
```

### Each item in `esims`

```json
{
  "package_id": "uuid",
  "status": "ready",
  "activation_code": "LPA:1$smdp.example.com$MATCHING-ID",
  "smdp_address": "smdp.example.com",
  "ios_activation_url": "https://...",
  "android_activation_url": "https://...",
  "activate_url": "https://...",
  "qr_code_url": "https://...",
  "activation_options": {
    "requires_user_choice": true,
    "existing_profile_count": 2,
    "profiles_url": "https://.../v1/orders/{orderId}/profiles",
    "activate_new_url": "https://.../activate/new",
    "activate_existing_url": "https://.../activate/existing"
  }
}
```

All activation fields are **nullable**. `status` is either `"ready"` (activation data available) or `"pending_activation"` (call activate/new or activate/existing first). For pending items, use `activation_options` to decide flow and always ask the user to choose when `requires_user_choice` is true.
