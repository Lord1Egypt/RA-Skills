# Purchase Playbooks

Use this reference after discovery and route selection.

## Sale Playbook

Use for presale lots and Agentic Pass mint flows.

1. Confirm sale protocol availability (`x402` or `mpp`) on the live origin.
2. Load offers:
   - `GET /agentic/x402/offers` or
   - `GET /agentic/mpp/offers`
3. Pick `saleId` from live offers only.
4. Optional preflight quote:
   - `GET /agentic/x402/quote` or
   - `POST /agentic/mpp/quote`
5. Submit buy:
   - `POST /agentic/<protocol>/buy`
6. If fulfillment is pending, poll:
   - `GET /agentic/<protocol>/purchases/{paymentTx}`

### Sale Payload Template

```json
{
  "saleId": "<live-sale-id>",
  "quantity": 1,
  "beneficiary": "0xBeneficiaryAddress"
}
```

## Shop Playbook

Use for in-game item delivery through backend fulfillment.

1. Load shop catalog:
   - anonymous read: `GET /shop/api/shop/items`
   - personalized read: `GET /shop/api/shop/items?nickname=<player>` or `?address=<0x...>`
2. For quote and buy, include exactly one recipient field.
3. Optional preflight quote:
   - `POST /shop/<protocol>/quote`
4. Buy:
   - `POST /shop/<protocol>/buy`
5. Poll status:
   - `GET /shop/<protocol>/purchases/{paymentReference}`
   - or `GET /shop/purchase-status/{purchaseId}`

### Shop x402 Payload Template

```json
{
  "itemId": "a-units-pack:1",
  "quantity": 1,
  "nickname": "PlayerOne"
}
```

### Shop MPP Payload Template

```json
{
  "nickname": "PlayerOne",
  "items": [
    {
      "itemId": "a-units-pack:1",
      "quantity": 1
    }
  ]
}
```

## Payment Retry Rules

### x402

- First unpaid buy may return `402 payment_required`.
- Paid retry must preserve exact HTTP method and exact JSON body.
- Build paid retry from the latest payment challenge.
- Prefer canonical `PAYMENT-SIGNATURE`.

### MPP

- Prefer canonical `mppx` SDK.
- Keep unpaid and paid retry JSON body identical.
- If manual flow is required, use `Authorization: Payment`.
- For Tempo hash credentials:
  - `credential.payload.type = "hash"`
  - `credential.payload.hash = "<transfer-hash>"`

## Stop Conditions

Stop and report instead of forcing the flow when:

- protocol discovery says unavailable but OpenAPI claims payable route
- selected catalog item does not map to a valid buy endpoint
- shop recipient is missing or both recipient fields are provided
