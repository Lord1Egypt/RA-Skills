# Ask: find agents with a question

`POST https://api.deside.io/api/v1/ask` finds agents from a question in plain words. It answers with a short text and up to 5 agents, only from the directory. The states are from Deside's checks, never from the AI.

Ask is free on deside.io and for users signed in with a wallet. Any other caller pays 0.01 USDC per answered question over x402 on Solana.

## Ask with the API

```bash
curl -X POST "https://api.deside.io/api/v1/ask" \
  -H "content-type: application/json" \
  -d '{"question":"an agent that checks token risk on Solana"}'
```

### Request

| Name | Type | Required | Description |
|---|---|---|---|
| `question` | string | Yes | 3 to 500 characters after trimming. |

### Response

```json
{
  "answer": "HostDeFi Token Risk API scans Solana token contracts and grades them for safety.",
  "agents": [
    {
      "id": "0d9eb666-12f1-4600-ae7f-459dd70500ed",
      "name": "HostDeFi Token Risk API",
      "category": "token_risk",
      "state": "responds",
      "connected": false,
      "lastCheckedAt": "2026-10-04T05:15:00.449Z",
      "services": [
        {
          "kind": "mcp",
          "url": "https://hostdefi.com/api/v1/mcp",
          "checked": true,
          "checkedAt": "2026-10-04T05:15:00.449Z"
        }
      ]
    }
  ],
  "claimed": [],
  "claimedTotal": 1853,
  "unmet": false,
  "intent": "token_risk",
  "measuredAt": "2026-10-04T09:40:06.737Z"
}
```

| Field | Description |
|---|---|
| `answer` | The text answer. |
| `agents[]` | Agents that fit. `state` is from Deside's checks. `connected`: the owner proved the agent is theirs. |
| `claimed[]` | Agents whose description matches but are not live in our checks. Up to 100. |
| `claimedTotal` | How many claimed agents exist. |
| `unmet` | `true` when no live agent fits the question. |
| `intent` | The category the question was read as. |
| `degraded` | `true` when the answer could not be built. `answer` is then null and lists are empty. You are not charged. |
| `measuredAt` | When the directory data was measured. |

## Ask over the MCP

Free when signed in. 10 questions a minute per account.

Tool `ask_directory`: takes `question` (3 to 500 characters). Returns the same body as the API. The MCP never pays over x402: if the account cannot use Ask free (banned, or session revoked), the tool fails with `UNKNOWN` and `status` 402.

## Pay for Ask with x402

Without a Deside session, you pay 0.01 USDC per answered question on Solana. You only need USDC: the facilitator pays the network fee, so you need no SOL.

**Ask your user before you pay.** Show the price first.

| Item | Value |
|---|---|
| Price | 0.01 USDC per answered question (`amount` `"10000"`, 6 decimals) |
| Network | Solana mainnet |
| Asset | USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`) |
| Pay to | `Bth9CibjQGiLJxm2A6CdN6URKDaefdcQLrnNdkUsd4K` |

### Flow

1. Send the question with no payment. Deside answers `402` with the offer in the body and, base64-encoded, in the `PAYMENT-REQUIRED` header.
2. Sign the payment with an x402 v2 client for Solana (such as `@x402/core` with `@x402/svm`). Send the same request again with the `PAYMENT-SIGNATURE` header. The v1 header `X-PAYMENT` is also accepted.
3. Deside verifies the payment, answers, and settles it only if the answer was built. The `200` carries the answer and the `PAYMENT-RESPONSE` header: base64 JSON with `success`, `transaction`, `network` and `payer`.

If the answer comes back with `degraded: true`, the payment is not settled and you are not charged.

One payment pays for one question. Sending the same question with the same payment again returns the saved answer.

### Get the payment offer

```bash
curl -i -X POST "https://api.deside.io/api/v1/ask" \
  -H "content-type: application/json" \
  -d '{"question":"an agent that checks token risk on Solana"}'
```

```json
{
  "x402Version": 2,
  "error": "payment required",
  "resource": {
    "url": "https://api.deside.io/api/v1/ask",
    "description": "Deside directory question: one answered question about the AI agents in the directory",
    "mimeType": "application/json"
  },
  "accepts": [{
    "scheme": "exact",
    "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
    "amount": "10000",
    "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "payTo": "Bth9CibjQGiLJxm2A6CdN6URKDaefdcQLrnNdkUsd4K",
    "maxTimeoutSeconds": 60,
    "extra": { "feePayer": "CjNFTjvBhbJJd2B5ePPMHRLx1ELZpa8dwQgGL727eKww" }
  }]
}
```

Without a payment, the `402` comes first, before the body is checked.

## Limits

| Caller | Price | Limit |
|---|---|---|
| People on deside.io/ask | Free | 10 a minute per IP, and 120 a minute for all visitors together. Over it, the answer is the `402` offer. |
| Signed in to Deside with a wallet, also over the MCP | Free | 10 a minute per account. |
| Anyone else | 0.01 USDC per answered question | 3 requests a minute per IP, with or without a new payment. A retry of a payment Deside already received has its own limit of 10 a minute per payment. |

A `429` carries `Retry-After` in seconds.

## Errors

| Status | Code | When | What to do |
|---|---|---|---|
| 400 | `INVALID_QUESTION` | Missing or bad `question`. | Send 3 to 500 characters. |
| 402 | `payment required` | No payment. | Pay and retry. |
| 402 | `invalid_payment` or `requirements_mismatch` | The payment is not valid or does not match. | Sign a new payment. |
| 409 | `PAYMENT_ALREADY_USED` | That payment paid for a different question. | Pay again. |
| 409 | `PAYMENT_IN_PROGRESS` | The same payment is being processed. | Wait and retry with the same payment. |
| 429 | `rate_limited` | Over the limit. | Wait `retryAfterSec`. |
| 503 | `FACILITATOR_UNAVAILABLE` | The facilitator does not answer. You are not charged. | Retry later. |
| 503 | `SETTLEMENT_PENDING` | The answer was built but the payment did not settle. | Retry with the same payment. Do not pay again. |
| 503 | `ASK_PAYMENTS_UNAVAILABLE` | Payments are down. You are not charged. | Retry later. |
