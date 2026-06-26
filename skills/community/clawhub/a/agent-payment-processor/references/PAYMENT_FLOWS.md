# Payment Flows

Use this guide when an agent needs the shortest accurate public path for creating, funding, and settling a Paegents usage agreement.

This guide reflects the current bilateral escrow model. It intentionally stays at the public integration layer and does not explain internal implementation details.

## Current Standard Flow

1. Search or select the target service.
2. Create the usage agreement (no escrow signatures needed at creation).
3. Wait for the seller to accept.
4. Fetch the activation package, sign the activation intent locally, sign the separate infra fee permit if the package shows a pending fee, and then activate escrow.
5. Use the service through the metered proxy or the agreed fulfillment path.
6. Record usage until the work is complete.
7. Inspect settlement options before taking any settlement action.
8. Complete settlement through either the direct wallet path or the optional sponsored path.

## Agreement Creation

Create the agreement with basic terms. Escrow activation is a separate step after seller acceptance.

### Buyer-side Rules

- keep the buyer private key local
- use the V2 activation signing helpers, not the AP2 stablecoin payment helper
- use live SDK/API inputs instead of hardcoded network or pricing assumptions
- do not construct activation inputs locally — the activation package provides the live values that matter

### Create the Agreement

#### Python
```python
from paegents import UsageAgreementRequest

agreement = sdk.create_usage_agreement(UsageAgreementRequest(
    seller_agent_id="seller_agent_xyz",
    service_id=service_id,
    quantity=100,
    unit="image",
    price_per_unit_cents=5,
    buyer_wallet_address="0xYourWalletAddress",  # your self-custody wallet
))
```

#### TypeScript
```typescript
const agreement = await sdk.createUsageAgreement({
  sellerAgentId: 'seller_agent_xyz',
  serviceId,
  quantity: 100,
  unit: 'image',
  pricePerUnitCents: 5,
  buyerWalletAddress: '0xYourWalletAddress', // your self-custody wallet
});
```

## Activate Escrow (V2)

> **Activation is required.** Without this step, the agreement stays at `accepted` / `activation_status=ready`. The metered proxy will reject requests and no funds are deposited on-chain.

After seller acceptance, the agreement enters `accepted`. Activate the on-chain escrow:

1. `sdk.get_activation_package(agreement_id)` / `sdk.getActivationPackage(agreementId)` — fetches terms, nonces, and funding options
2. sign the buyer activation intent locally using `sign_buyer_activation_intent()` / `signBuyerActivationIntent()`
3. if the activation package shows a pending infra fee, sign the separate fee permit using `sign_infra_fee_permit()` / `signInfraFeePermit()`
4. build a funding authorization using `build_prior_allowance_funding_authorization()` or `build_erc2612_funding_authorization()`
5. `sdk.activate_escrow(agreement_id, ...)` / `sdk.activateEscrow(agreementId, {...})` — submits the signed activation

The fee permit and escrow funding authorization are separate on purpose. One authorizes the upfront platform fee. The other authorizes funding the service escrow. Treat them as distinct buyer approvals with different purposes.

**Important: Activation is asynchronous.** `activate-escrow` returns HTTP 202. A successful response does not mean the agreement is already on-chain.

**What to look for after calling `activate_escrow()`:**

- Poll `GET /usage-agreements/{agreement_id}` until `status` changes to `active`.
- Check `GET /usage-agreements/{agreement_id}/escrow-status` for `activation_status=confirmed` and a populated `activation_tx_hash`.
- On Base, delays of seconds to minutes are normal due to relayer/worker processing and chain confirmation.
- If `activation_status` remains `submitting` for more than 5 minutes without an `activation_tx_hash`, treat that as a backend processing issue.
- If `activation_status` is still `ready`, activation was never submitted — re-fetch the package, re-sign, and call `activate_escrow()` again.

Once `status=active`, the metered proxy accepts requests. See `SKILL.md` for complete code examples.

## Metered Usage

Once the agreement is active:

- use `sdk.create_metered_client()` / `sdk.createMeteredClient()` for buyer-side requests
- use `sdk.record_usage()` / `sdk.recordUsage()` when the seller is tracking usage outside the proxy
- use `sdk.get_escrow_status()` / `sdk.getEscrowStatus()` to monitor usage-linked settlement state

## Settlement Flow

Settlement now supports two public execution modes:

- direct wallet execution
- optional sponsored execution

Always check the options first.

### 1. Get settlement options

Use:

- Python: `sdk.get_settlement_action_options(agreement_id, action=...)`
- TypeScript: `sdk.getSettlementActionOptions(agreementId, { action: ... })`

Supported actions:

- `initiate_close`
- `seller_claim`
- `buyer_withdraw`

The options response tells you whether direct execution, sponsored execution, or neither is currently appropriate.

### 2. Direct wallet path

Use the direct wallet path when the signer should broadcast the transaction personally.

- close: `get_initiate_close_calldata()` / `getInitiateCloseCalldata()`
- seller claim or buyer withdraw: `get_claim_instructions()` / `getClaimInstructions()`

Then submit the returned unsigned transaction from the signer wallet.

### 3. Sponsored path

Use the sponsored path only when the settlement options helper recommends it and the path is available.

Supported public pattern:

1. call the settlement options helper
2. sign the matching action locally with the escrow helper
3. submit through the matching sponsored SDK wrapper

Helper mapping:

| Action | Signing helper | Submit helper |
|---|---|---|
| initiate close | `sign_initiate_close_intent()` / `signInitiateCloseIntent()` | `submit_sponsored_initiate_close()` / `submitSponsoredInitiateClose()` |
| seller claim | `sign_seller_claim_intent()` / `signSellerClaimIntent()` | `submit_sponsored_seller_claim()` / `submitSponsoredSellerClaim()` |
| buyer withdraw | `sign_buyer_withdraw_intent()` / `signBuyerWithdrawIntent()` | `submit_sponsored_buyer_withdraw()` / `submitSponsoredBuyerWithdraw()` |

Guidance:

- use the live nonce, deadline, and signer context from the settlement options call
- keep the signature local until submission
- if sponsored is unavailable, use the direct path if possible or wait for state to change

## Direct Stablecoin Purchase Flow

For one-off stablecoin payments without bilateral escrow, use the direct stablecoin flow. The platform fee is collected via an EIP-2612 USDC permit **before** the x402 payment executes.

### Fee Structure

- 2% + $0.003 flat, minimum $0.10
- Fee is in atomic USDC (6 decimals). Use `compute_stablecoin_fee_atomic()` / `computeStablecoinFeeAtomic()` to calculate.

### Flow

1. Buyer calls `GET /payment-requirements?amount_cents=...&rail=stablecoin` to get fee details, gas wallet address, and chain ID.
2. Buyer uses `build_direct_stablecoin_agreement()` / `buildDirectStablecoinAgreement()` to sign the x402 payment header and the fee permit in one step.
3. Buyer creates the agreement with `settlement_model: "direct_payment"`, `payment_header`, `buyer_wallet_address`, `buyer_infra_fee_permit_signature`, and `buyer_infra_fee_permit_deadline`.
4. Seller accepts the agreement.
5. On acceptance, the platform collects the fee via the EIP-2612 permit, then executes the x402 payment to the seller.
6. If fee collection fails, the acceptance is rejected and the x402 payment does not execute.

### Python
```python
from paegents import build_direct_stablecoin_agreement, UsageAgreementRequest

# Load your private key from a secure local source (keystore, HSM, or env).
# The key is used for local signing only — it is never sent to the platform.
buyer_private_key = load_private_key()  # your implementation

pkg = build_direct_stablecoin_agreement(
    buyer_private_key=buyer_private_key,
    seller_wallet="0xSellerWallet...",
    amount_cents=500,
    resource_id="svc_abc123",
    gas_wallet_address="0xGasWallet...",
    chain_id=84532,
    usdc_permit_nonce=0,
    permit_deadline=int(time.time()) + 600,
)

agreement = sdk.create_usage_agreement(UsageAgreementRequest(
    seller_agent_id="seller_agent_xyz",
    service_id="svc_abc123",
    quantity=1,
    unit="purchase",
    price_per_unit_cents=500,
    settlement_model="direct_payment",
    buyer_wallet_address=pkg["buyer_wallet_address"],
    payment_header=pkg["payment_header"],
))
```

### TypeScript
```typescript
import { buildDirectStablecoinAgreement } from 'paegents';

// Load your private key from a secure local source (keystore, HSM, or env).
// The key is used for local signing only — it is never sent to the platform.
const buyerPrivateKey = loadPrivateKey(); // your implementation

const pkg = await buildDirectStablecoinAgreement({
  buyerPrivateKey,
  sellerWallet: '0xSellerWallet...',
  amountCents: 500,
  resourceId: 'svc_abc123',
  gasWalletAddress: '0xGasWallet...',
  chainId: 84532,
  usdcPermitNonce: 0n,
  permitDeadline: BigInt(Math.floor(Date.now() / 1000) + 600),
});

const agreement = await sdk.createUsageAgreement({
  sellerAgentId: 'seller_agent_xyz',
  serviceId: 'svc_abc123',
  quantity: 1,
  unit: 'purchase',
  pricePerUnitCents: 500,
  settlementModel: 'direct_payment',
  buyerWalletAddress: pkg.buyerWalletAddress,
  paymentHeader: pkg.paymentHeader,
});
```

### Key Differences from Bilateral Escrow

- No activation step — payment happens when the seller accepts.
- No metered proxy — the buyer receives the service directly.
- Fee is collected via EIP-2612 permit, not via escrow deposit.
- Settlement is instant — the seller receives the full service amount via x402.

## Notes

- Keep private keys in your own environment.
- Prefer SDK helpers over hand-built request payloads.
- Use live agreement state instead of hardcoded timing assumptions.
- Treat settlement choice as a runtime decision, not a compile-time assumption.
