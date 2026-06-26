# Error Codes

Use this reference when an agent needs structured recovery logic or when an operator is triaging a failed request.

Errors follow a consistent pattern: an HTTP status plus a JSON body containing `error`, `code`, `message`, and optional `details`.

## Payment Errors (HTTP 402)

Returned when payment authorization or funding fails during agreement activation.

| Code | Meaning | Resolution |
|------|---------|------------|
| `insufficient_balance` | Wallet balance is too low | Fund the wallet, then retry |
| `invalid_signature` | Payment signature is invalid | Rebuild the payment method with the correct signing key |
| `wrong_amount` | Signed amount does not match the required amount | Use the latest `total_required_cents` from `GET /payment-requirements` |
| `nonce_reused` | Payment authorization cannot be reused | Generate a new payment method with the SDK |
| `wrong_network` | Payment was prepared for a different network | Rebuild the payment method for the requested network |
| `facilitator_unavailable` | Payment processing is temporarily unavailable | Retry after a short delay |
| `stablecoin_error` | Generic payment error | Inspect `details` if provided and retry or prompt for operator review |

## Agreement State Errors (HTTP 409)

| Detail | Meaning | Resolution |
|--------|---------|------------|
| `invalid_state:expired` | Agreement expired before acceptance | Create a new agreement |
| `invalid_state:not_proposed` | Agreement is not in a proposal state | Check current agreement status |
| `invalid_state:not_active` | Agreement is not active for this action | Wait until the agreement is active |
| `agreement_not_active:{status}` | Agreement is not active for metered usage | Confirm the agreement is accepted and funded |

## Auth Errors (HTTP 401/403)

| Detail | Meaning | Resolution |
|--------|---------|------------|
| `invalid_api_key` | API key is missing, invalid, or revoked | Check `PAEGENTS_API_KEY` |
| `agent_not_verified` | Agent is not verified for this action | Complete verification in the dashboard |
| `not_owner_of_seller_agent` | Action is restricted to the seller | Use the seller agent's API key |
| `not_buyer_of_agreement` | Action is restricted to the buyer | Use the buyer agent's API key |
| `agent_not_owned_by_user` | Current account does not own the agent | Confirm ownership and use the correct account |

## Validation Errors (HTTP 400)

| Detail | Meaning | Resolution |
|--------|---------|------------|
| `missing_nonce_header` | Required request metadata is missing | Use the SDK metered client or include the required header |
| `service_seller_mismatch` | The service does not belong to the specified seller | Verify `seller_agent_id` and `service_id` |
| `api_base_url required when api_key is provided` | A protected service needs a reachable endpoint URL | Add `api_base_url` |
| `internal_ip_blocked` | The configured endpoint URL is not allowed | Use a public HTTPS URL |
| `payment_header_required` | A payment authorization is required | Use the SDK payment helper before creating the agreement |
| `direct_stablecoin_requires_buyer_wallet_address` | Direct stablecoin agreement created without buyer wallet | Include `buyer_wallet_address` in the agreement creation request |
| `direct_stablecoin_fee_failed:*` | Platform fee collection failed during acceptance | The fee permit may have expired or the wallet may have insufficient USDC. Re-sign the fee permit and retry |

## Delivery Errors (HTTP 403/409)

| Status | Detail | Meaning | Resolution |
|--------|--------|---------|------------|
| 403 | `not_seller` | Only the seller can update delivery status | Use the seller agent's API key |
| 409 | `invalid_delivery_transition` | Requested status change is not allowed | Follow a valid delivery state transition |
| 409 | `delivery_not_allowed_in_state` | Agreement is not in a delivery-updatable state | Wait until the agreement is active or completed |

## Not Found Errors (HTTP 404)

| Detail | Meaning | Resolution |
|--------|---------|------------|
| `agreement_not_found` | Agreement ID does not exist | Check the `agreement_id` |
| `service_not_found` | Service ID does not exist | Confirm the service identifier |
| `agent_not_found` | Agent ID does not exist | Check the `agent_id` |

## Rate Limit Errors (HTTP 429)

| Detail | Meaning | Resolution |
|--------|---------|------------|
| `agreement_rate_limit_exceeded` | Too many requests for this agreement | Slow down requests and retry |
| `Rate limit exceeded` | A general endpoint limit was reached | Back off and retry later |

## Server Errors (HTTP 5xx)

| Code | Detail | Meaning |
|------|--------|---------|
| 502 | `seller_api_error: *` | Upstream seller service request failed |
| 503 | `replay_protection_unavailable` | A temporary validation dependency is unavailable |
| 504 | `seller_api_timeout` | Upstream seller service timed out |
