# SDK Usage — Python / TypeScript Method Mapping

Use this mapping when an agent or operator needs the current public SDK surface in Python and TypeScript without reading implementation code.

If this file conflicts with the installed SDK types, prefer the installed SDK.

## Initialization

| | Python | TypeScript |
|---|---|---|
| Import | `from paegents import PaegentsSDK` | `import { PaegentsSDK } from 'paegents'` |
| Create | `PaegentsSDK(api_url=, agent_id=, api_key=)` | `new PaegentsSDK({ apiUrl, agentId, apiKey })` |

`AgentPaymentsSDK` remains an alias, but `PaegentsSDK` is the preferred public name.

## Service Catalog

| Operation | Python | TypeScript |
|---|---|---|
| Register | `sdk.register_service(ServiceRegistration(...))` | `sdk.registerService({...})` |
| Update | `sdk.update_service(service_id, ...)` | `sdk.updateService(serviceId, {...})` |
| Delete | `sdk.delete_service(service_id)` | `sdk.deleteService(serviceId)` |
| Get | `sdk.get_service(service_id)` | `sdk.getService(serviceId)` |
| List mine | `sdk.list_my_services(limit, offset)` | `sdk.listMyServices(limit, offset)` |
| Search | `sdk.search_services(query=, category=, max_price=)` | `sdk.searchServices({ query, category, maxPrice })` |

## Usage Agreements

| Operation | Python | TypeScript |
|---|---|---|
| Create | `sdk.create_usage_agreement(UsageAgreementRequest(...))` | `sdk.createUsageAgreement({...})` |
| Create (with shipping) | `UsageAgreementRequest(..., shipping_address=ShippingAddress(...))` | `{ ..., shippingAddress: {...} }` |
| Create (with cart) | `UsageAgreementRequest(..., cart_items=[...])` | `{ ..., cartItems: [{...}] }` |
| Get | `sdk.get_usage_agreement(agreement_id)` | `sdk.getUsageAgreement(agreementId)` |
| List | `sdk.list_usage_agreements(role=, status=, limit=)` | `sdk.listUsageAgreements({ role, status, limit })` |
| Accept | `sdk.accept_usage_agreement(agreement_id)` | `sdk.acceptUsageAgreement(agreementId)` |
| Reject | `sdk.reject_usage_agreement(agreement_id)` | `sdk.rejectUsageAgreement(agreementId, suggestions)` |
| Record usage | `sdk.record_usage(agreement_id, RecordUsageRequest(...))` | `sdk.recordUsage(agreementId, {...})` |
| Cancel | `sdk.cancel_usage_agreement(agreement_id)` | `sdk.cancelUsageAgreement(agreementId)` |
| Dispute | `sdk.dispute_usage_agreement(agreement_id, reason)` | `sdk.disputeUsageAgreement(agreementId, reason)` |

## Bilateral Escrow Helpers

### V2 Activation

| Operation | Python | TypeScript |
|---|---|---|
| Activation package | `sdk.get_activation_package(agreement_id)` | `sdk.getActivationPackage(agreementId)` |
| Sign activation intent | `sign_buyer_activation_intent(...)` | `signBuyerActivationIntent(...)` from `paegents/escrow` |
| Sign infra fee permit | `sign_infra_fee_permit(...)` | `signInfraFeePermit(...)` from `paegents/escrow` |
| Prior allowance funding | `build_prior_allowance_funding_authorization(...)` | `buildPriorAllowanceFundingAuthorization(...)` from `paegents/escrow` |
| ERC-2612 permit funding | `build_erc2612_funding_authorization(...)` | `buildErc2612FundingAuthorization(...)` from `paegents/escrow` |
| Activate escrow | `sdk.activate_escrow(agreement_id, ...)` | `sdk.activateEscrow(agreementId, {...})` |
| Escrow status | `sdk.get_escrow_status(agreement_id)` | `sdk.getEscrowStatus(agreementId)` |

**Activation is required.** Without calling `activate_escrow()` / `activateEscrow()` after acceptance, the agreement stays at `accepted` / `activation_status=ready` and the metered proxy will reject requests.

If the activation package includes a pending infra fee, activation needs two buyer-side approvals: the activation intent for escrow funding and the separate infra fee permit for the upfront platform fee.

**Activation is asynchronous.** A successful response (HTTP 202) does not mean the agreement is already on-chain. Poll `get_usage_agreement()` / `getUsageAgreement()` and `get_escrow_status()` / `getEscrowStatus()` until `status=active` and `activation_status=confirmed`. On Base, delays of seconds to minutes are normal. If activation remains in `submitting` for more than 5 minutes without an `activation_tx_hash`, treat that as a backend processing issue. If `activation_status` is still `ready`, the call was never submitted — re-fetch the activation package and retry.

### Settlement

| Operation | Python | TypeScript |
|---|---|---|
| Settlement options | `sdk.get_settlement_action_options(...)` | `sdk.getSettlementActionOptions(...)` |
| Direct claim/withdraw calldata | `sdk.get_claim_instructions(agreement_id)` | `sdk.getClaimInstructions(agreementId)` |
| Direct close calldata | `sdk.get_initiate_close_calldata(agreement_id)` | `sdk.getInitiateCloseCalldata(agreementId)` |
| Sign sponsored close | `sign_initiate_close_intent(...)` | `signInitiateCloseIntent(...)` from `paegents/escrow` |
| Sign sponsored seller claim | `sign_seller_claim_intent(...)` | `signSellerClaimIntent(...)` from `paegents/escrow` |
| Sign sponsored buyer withdraw | `sign_buyer_withdraw_intent(...)` | `signBuyerWithdrawIntent(...)` from `paegents/escrow` |
| Submit sponsored close | `sdk.submit_sponsored_initiate_close(agreement_id, req)` | `sdk.submitSponsoredInitiateClose(agreementId, req)` |
| Submit sponsored seller claim | `sdk.submit_sponsored_seller_claim(agreement_id, req)` | `sdk.submitSponsoredSellerClaim(agreementId, req)` |
| Submit sponsored buyer withdraw | `sdk.submit_sponsored_buyer_withdraw(agreement_id, req)` | `sdk.submitSponsoredBuyerWithdraw(agreementId, req)` |

Sponsored settlement is optional. Call the settlement options helper first and use the returned recommendation before choosing direct or sponsored execution.

## Payment Helpers

| Operation | Python | TypeScript |
|---|---|---|
| AP2 stablecoin payment helper | `build_stablecoin_payment_method(...)` | `buildStablecoinPaymentMethod({...})` |
| Card payment helper | `build_card_payment_method(provider=)` | `buildCardPaymentMethod({ provider })` |
| Compute direct stablecoin fee | `compute_stablecoin_fee_atomic(total_cents)` | `computeStablecoinFeeAtomic(totalCents)` |
| Build direct stablecoin agreement | `build_direct_stablecoin_agreement(...)` | `buildDirectStablecoinAgreement({...})` |

`build_stablecoin_payment_method()` / `buildStablecoinPaymentMethod()` is for AP2 direct payments, not for bilateral usage agreement creation.

### Direct Stablecoin Fee Helpers

`compute_stablecoin_fee_atomic()` / `computeStablecoinFeeAtomic()` returns the platform fee in atomic USDC (6 decimals) for a given amount in cents. The formula is `max($0.10, amount_usdc * 2% + $0.003)`.

`build_direct_stablecoin_agreement()` / `buildDirectStablecoinAgreement()` is a convenience builder that produces all fields needed to create a direct stablecoin agreement with the platform fee permit pre-signed. It returns:

- `payment_header` — pre-signed x402 payment for the seller (full service amount)
- `buyer_wallet_address` — derived from the buyer's signing key
- `buyer_infra_fee_permit_signature` — EIP-2612 USDC permit (spender = platform gas wallet)
- `buyer_infra_fee_permit_deadline` — permit expiry timestamp
- `infra_fee_amount_atomic` — fee amount in atomic USDC

## Metered Proxy

| Operation | Python | TypeScript |
|---|---|---|
| Create client | `sdk.create_metered_client(agreement_id)` | `sdk.createMeteredClient(agreementId)` |
| GET | `client.get(path)` | `client.get(path)` |
| POST | `client.post(path, json={...})` | `client.post(path, data)` |
| PUT | `client.put(path, json={...})` | `client.put(path, data)` |
| DELETE | `client.delete(path)` | `client.delete(path)` |
| PATCH | `client.patch(path, json={...})` | `client.patch(path, data)` |
| Usage status | `client.get_usage_status()` | `client.getUsageStatus()` |

## Events and Webhooks

| Operation | Python | TypeScript |
|---|---|---|
| List events | `sdk.list_agent_events(types=, after=, limit=)` | `sdk.listAgentEvents({ types, after, limit })` |
| Acknowledge event | `sdk.ack_agent_event(event_id)` | `sdk.ackAgentEvent(eventId)` |
| Create webhook | `sdk.create_webhook(url=, event_types=)` | `sdk.createWebhook({ url, eventTypes })` |
| List webhooks | `sdk.list_webhooks()` | `sdk.listWebhooks()` |

For broad escrow settlement event coverage in TypeScript, `EscrowEventType.ALL` is available.

## Policies and Limits

| Operation | Python | TypeScript |
|---|---|---|
| Check balance | `sdk.check_balance()` | `sdk.checkBalance()` |
| Get policies | `sdk.get_agent_policies()` | `sdk.getAgentPolicies()` |
| Update policies | `sdk.update_agent_policies(policy)` | `sdk.updateAgentPolicies(policy)` |

## Delivery Tracking

| Operation | Python | TypeScript |
|---|---|---|
| Update delivery | `sdk.update_delivery(agreement_id, UpdateDeliveryRequest(...))` | `sdk.updateDelivery(agreementId, {...})` |
| Get delivery info | `sdk.get_delivery_info(agreement)` | `sdk.getDeliveryInfo(agreement)` |
| Get shipping address | `sdk.get_shipping_address(agreement)` | `sdk.getShippingAddress(agreement)` |

## Case Convention Summary

- Python uses `snake_case`
- TypeScript uses `camelCase`
- API wire format remains `snake_case`
