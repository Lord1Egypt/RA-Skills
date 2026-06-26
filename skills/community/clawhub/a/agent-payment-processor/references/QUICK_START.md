# Quick Start

Use this guide when an agent needs to start transacting quickly as a seller or buyer with the current Paegents bilateral escrow flow.

These walkthroughs are written for agent execution, but they are also useful to a human operator supervising wallet state, approval policy, and settlement progress.

## What You Will Complete

- register a service for sale
- create a bilateral escrow agreement as a buyer
- route usage through the metered proxy
- monitor escrow and settlement
- choose the correct settlement path when the agreement is ready

## Before You Start

If you have not completed onboarding yet (account, agent, verification, wallet), follow the **Getting Started** section in `SKILL.md` first.

Confirm that:

- the correct API URL, API key, agent ID, and wallet credentials are available
- the SDK is installed in the runtime you plan to use
- the agent is verified and allowed to transact
- the buyer wallet is a self-custody wallet (not an exchange wallet) with enough USDC on Base
- if direct settlement may be needed, the signer wallet has ETH on Base for gas
- the operator has confirmed the correct account, wallet, and approval policy settings

## Install and Verify

```bash
# Python
pip install paegents

# OR TypeScript
npm install paegents

curl -s "$PAEGENTS_API_URL/health"
```

Set these environment variables:

```bash
export PAEGENTS_API_URL=https://app.paegents.com/api
export PAEGENTS_API_KEY=sk_your_key
export PAEGENTS_AGENT_ID=your_agent_id
# Buyer wallet credentials (address + signing key) are managed separately.
# See your wallet provider or keystore for secure key management.
```

## Seller Walkthrough

### 1. Register the service

#### Python
```python
import os
from paegents import PaegentsSDK, ServiceRegistration

sdk = PaegentsSDK(
    api_url=os.environ["PAEGENTS_API_URL"],
    agent_id=os.environ["PAEGENTS_AGENT_ID"],
    api_key=os.environ["PAEGENTS_API_KEY"],
)

service = sdk.register_service(ServiceRegistration(
    service_name="text-summarizer",
    description="Summarize long documents into concise paragraphs",
    category="ai",
    price_model="per_unit",
    base_price_cents=2,
    unit="document",
    api_base_url="https://your-api.example.com",
    api_key="your-secret-api-key",
))
```

#### TypeScript
```typescript
import { PaegentsSDK } from 'paegents';

const sdk = new PaegentsSDK({
  apiUrl: process.env.PAEGENTS_API_URL!,
  agentId: process.env.PAEGENTS_AGENT_ID!,
  apiKey: process.env.PAEGENTS_API_KEY!,
});

const service = await sdk.registerService({
  serviceName: 'text-summarizer',
  description: 'Summarize long documents into concise paragraphs',
  category: 'ai',
  priceModel: 'per_unit',
  basePriceCents: 2,
  unit: 'document',
  apiBaseUrl: 'https://your-api.example.com',
  apiKey: 'your-secret-api-key',
});
```

### 2. Monitor agreements and usage

- if auto-accept is enabled, the platform may advance the agreement automatically
- otherwise, accept proposals explicitly with `accept_usage_agreement()` / `acceptUsageAgreement()`
- monitor active agreements with `list_usage_agreements()` / `listUsageAgreements()`
- if you are not using the metered proxy, record usage with `record_usage()` / `recordUsage()`

## Buyer Walkthrough

### 1. Search for services

#### Python
```python
results = sdk.search_services(query="summarize", category="ai")
```

#### TypeScript
```typescript
const results = await sdk.searchServices({ query: 'summarize', category: 'ai' });
```

### 2. Create the bilateral agreement

Create the agreement with basic terms. Escrow activation happens after the seller accepts.

Do not use `build_stablecoin_payment_method()` or `build_bilateral_agreement_signatures()` — those are V1 patterns.

#### Python
```python
from paegents import UsageAgreementRequest

agreement = sdk.create_usage_agreement(UsageAgreementRequest(
    seller_agent_id="seller_agent_id",
    service_id=service_id,
    quantity=100,
    unit="document",
    price_per_unit_cents=2,
    buyer_wallet_address="0xYourWalletAddress",  # your self-custody wallet
))
```

#### TypeScript
```typescript
const agreement = await sdk.createUsageAgreement({
  sellerAgentId: 'seller_agent_id',
  serviceId,
  quantity: 100,
  unit: 'document',
  pricePerUnitCents: 2,
  buyerWalletAddress: '0xYourWalletAddress', // your self-custody wallet
});
```

### 3. Activate escrow after seller accepts (V2)

> **Activation is required.** Without this step, the agreement stays at `accepted` / `activation_status=ready`. The metered proxy will reject requests and no funds are deposited on-chain.

After the seller accepts, activate the on-chain escrow:

1. Call `get_activation_package(agreement_id)` / `getActivationPackage(agreementId)` to fetch terms, nonces, and funding options.
2. Sign the buyer activation intent locally using `sign_buyer_activation_intent()` / `signBuyerActivationIntent()`.
3. If the activation package shows a pending infra fee, sign the separate fee permit with `sign_infra_fee_permit()` / `signInfraFeePermit()`.
4. Build a funding authorization with `build_prior_allowance_funding_authorization()` or `build_erc2612_funding_authorization()`.
5. Call `activate_escrow(agreement_id, ...)` / `activateEscrow(agreementId, {...})` to submit.

This split exists because the platform fee and the service escrow solve different problems. The fee permit covers the upfront platform charge. The funding authorization covers locking service funds into escrow.

**Important: Activation is asynchronous.** `activate-escrow` returns HTTP 202. A successful response does not mean the agreement is already on-chain.

**What to look for after calling `activate_escrow()`:**

- Poll `GET /usage-agreements/{agreement_id}` until `status` changes from `accepted` to `active`.
- Also check `GET /usage-agreements/{agreement_id}/escrow-status` — look for `activation_status=confirmed` and a populated `activation_tx_hash`.
- On Base, delays of seconds to minutes are normal due to relayer/worker processing and chain confirmation.
- If `activation_status` remains `submitting` for more than 5 minutes without an `activation_tx_hash`, treat that as a backend processing issue — contact support or retry the activation call.
- If you see `activation_status=ready`, activation was never submitted. Re-fetch the activation package, re-sign, and call `activate_escrow()` again.

Once `status=active` and `activation_status=confirmed`, the agreement is live and the metered proxy accepts requests. See `SKILL.md` for complete code examples.

### 4. Use the metered proxy

#### Python
```python
client = sdk.create_metered_client(agreement.agreement_id)
result = client.post("/summarize", json={"text": "Long document text here..."})
status = client.get_usage_status()
```

#### TypeScript
```typescript
const client = sdk.createMeteredClient(agreement.agreementId);
const result = await client.post('/summarize', {
  text: 'Long document text here...',
});
const status = await client.getUsageStatus();
```

## Settlement Quick Path

When usage is complete:

1. inspect `get_escrow_status()` / `getEscrowStatus()`
2. call `get_settlement_action_options()` / `getSettlementActionOptions()`
3. if direct is recommended, use direct calldata helpers and broadcast from the signer wallet
4. if sponsored is recommended, sign locally and submit through the matching sponsored SDK wrapper

Settlement actions:

- `initiate_close`
- `seller_claim`
- `buyer_withdraw`

## Physical Goods Note

Shipping address and cart item support remain available during agreement creation. Delivery tracking still uses `update_delivery()` / `updateDelivery()` after acceptance.
