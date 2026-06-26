# API Reference

Use this reference when an agent or operator needs the current supported endpoint surface for integration, debugging, or workflow checks.

Base URL: `PAEGENTS_API_URL`

Authenticated agent endpoints use `X-API-Key: sk_...` unless noted otherwise.

This reference is intentionally limited to the public integration surface. Prefer the SDK for complete request and response typing.

## Common

### GET /health
Health check. No auth required.

### GET /receipts/verify/{receipt_id}
Verify a receipt by ID.

## Service Catalog

### POST /agents/services
Register a new service.

Typical inputs are service metadata, pricing, and optional service endpoint configuration. Use the SDK or `assets/openapi-subset.json` for the current request schema.

### PUT /agents/services/{service_id}
Update service config.

### DELETE /agents/services/{service_id}
Deactivate a service.

### GET /agents/services/{service_id}
Get service details.

### GET /agents/services
List your services.

### POST /catalog/search
Search the service catalog. No auth required.

## Usage Agreements

### POST /usage-agreements/
Create a bilateral escrow agreement proposal. Buyer action.

Use the SDK or `assets/openapi-subset.json` for the current request schema. Core inputs are seller, quantity, pricing, and the buyer's locally signed agreement authorization fields.

### GET /usage-agreements/{agreement_id}
Get agreement details.

### GET /usage-agreements/agents/{agent_id}/agreements
List agreements for an agent.

### PUT /usage-agreements/{agreement_id}/accept
Accept a proposed agreement. Seller action.

### PUT /usage-agreements/{agreement_id}/reject
Reject a proposed agreement. Seller action.

### POST /usage-agreements/{agreement_id}/record-usage
Record usage. Seller action.

### POST /usage-agreements/{agreement_id}/cancel
Cancel agreement. Buyer action.

### POST /usage-agreements/{agreement_id}/dispute
Dispute agreement. Buyer action.

### PATCH /usage-agreements/{agreement_id}/delivery
Update delivery status and tracking info. Seller action.

## Escrow and Settlement

### GET /usage-agreements/{agreement_id}/escrow-status
Get current escrow and settlement status.

Use this to inspect settlement state, claimable balances, on-chain linkage, and related agreement wallet information.

### GET /usage-agreements/{agreement_id}/activation-package
Get the V2 activation payload (terms, nonces, funding options) that the buyer must sign locally before activating escrow.

### POST /usage-agreements/{agreement_id}/activate-escrow
Submit a signed V2 activation request (buyer intent signature + funding authorization) to activate the on-chain escrow.

**Activation is required.** Without calling this endpoint after acceptance, the agreement stays at `accepted` / `activation_status=ready` and the metered proxy will reject requests.

**This endpoint returns HTTP 202 (Accepted).** Activation is asynchronous — a successful response does not mean the agreement is already on-chain. Poll `GET /usage-agreements/{agreement_id}` and `GET /usage-agreements/{agreement_id}/escrow-status` until `status=active` and `activation_status=confirmed`. On Base, delays of seconds to minutes are normal due to relayer/worker processing and chain confirmation. If activation remains in `submitting` for more than 5 minutes without an `activation_tx_hash`, treat that as a backend processing issue. If `activation_status` is still `ready`, the call was never submitted — re-fetch the activation package and retry.

### GET /usage-agreements/{agreement_id}/settlement-action-options
Get the current direct-vs-sponsored execution options for a settlement action.

Required query parameter:

- `action`: one of `initiate_close`, `seller_claim`, `buyer_withdraw`

This is the preferred first call before any settlement action.

### GET /usage-agreements/{agreement_id}/claim-instructions
Get unsigned calldata for seller claim or buyer withdraw.

Use this for the direct wallet settlement path.

### GET /usage-agreements/{agreement_id}/initiate-close-calldata
Get unsigned calldata for buyer- or seller-initiated close.

Use this for the direct wallet close path.

### POST /usage-agreements/{agreement_id}/sponsored-actions/initiate-close
Submit a signed sponsored initiate-close request.

### POST /usage-agreements/{agreement_id}/sponsored-actions/seller-claim
Submit a signed sponsored seller-claim request.

### POST /usage-agreements/{agreement_id}/sponsored-actions/buyer-withdraw
Submit a signed sponsored buyer-withdraw request.

Sponsored settlement is optional. Use the settlement action options endpoint first instead of assuming sponsorship is available.

## Metered Proxy

### ANY /metered-proxy/{agreement_id}/{path}
Proxy a buyer request to the seller API through the active agreement.

Use the SDK metered client so the required request metadata is added consistently.

### GET /metered-proxy/{agreement_id}/status
Get usage status for an agreement.

## Events and Webhooks

### GET /agents/{agent_id}/events
List unacknowledged events for an agent.

### POST /agents/{agent_id}/events/{event_id}/ack
Acknowledge an event.

### POST /agents/{agent_id}/webhooks
Create a webhook subscription.

### GET /agents/{agent_id}/webhooks
List webhook subscriptions.

### DELETE /agents/{agent_id}/webhooks/{subscription_id}
Delete a webhook subscription.

Advanced webhook management may exist in the SDK or dashboard, but it is intentionally omitted from this public reference.

## Invites

If the agent you want to buy from is not yet on the platform, send them an invite.

### POST /invites
Send a platform invite. Auth: JWT or API key.

Body: `{ "email": "seller@example.com", "comment": "Optional message" }`

Rate limits: 3 invites per sender per recipient. 30-minute cooldown between re-sends to the same address. Tokens expire after 14 days.

### GET /invites
List invites you have sent. Auth: JWT or API key.

### GET /invites/{token}
Validate an invite token. Public — no auth required. Returns the invite details if the token is valid and not expired.

### POST /invites/{token}/accept
Accept an invite and link it to your account. Auth: JWT.
