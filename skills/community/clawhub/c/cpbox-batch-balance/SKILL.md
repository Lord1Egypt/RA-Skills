---
name: batch-balance
description: Guide users on how to use the Batch EVM Address Balance Query API (/api/x402/batch-balance). Use when users ask about batch balance queries, multicall balance lookups, or how to call the x402-protected balance endpoint.
version: 1.1.0
metadata: { "openclaw": { "emoji": "💰" } }
dependencies:
  - "@springmint/x402-payment"
---

# Batch EVM Address Balance Query API

Batch query EVM address balances via Multicall3, with pay-per-use powered by x402 protocol.

> **Prerequisites**: This skill requires x402-payment. Complete the [setup steps](../README.md#prerequisites) before first use.

## Service URLs

| Role | Domain |
|------|--------|
| **API Provider** | https://www.cpbox.io |
| **Facilitator** | https://www.cppay.finance |

## Endpoint

```
POST /api/x402/batch-balance
Content-Type: application/json
```

## Payment Flow (x402 Protocol)

This endpoint uses HTTP 402 Payment Required. The three-step flow:

1. **First request** (no payment header) -> Server returns `402` with payment requirements JSON
2. **Client signs** the payment requirements using EIP-712 -> Produces a `PAYMENT-SIGNATURE`
3. **Retry** with `PAYMENT-SIGNATURE` header -> Server verifies, settles, returns result JSON

When using `@springmint/x402-payment` (Node.js) or `x402-sdk-go` (Go), all 3 steps happen **automatically**.

## Using with x402-payment

### CLI (AI Agent)

```bash
npx @springmint/x402-payment \
  --url https://www.cpbox.io/api/x402/batch-balance \
  --method POST \
  --input '{"chain":"ethereum","token":"","addresses":["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045","0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"]}'
```

### Library (Node.js)

```ts
import { createX402FetchClient } from "@springmint/x402-payment";

const client = await createX402FetchClient();
const response = await client.request(
  "https://www.cpbox.io/api/x402/batch-balance",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chain: "ethereum",
      token: "",
      addresses: [
        "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8",
      ],
    }),
  },
);
const data = await response.json();
```

- This endpoint uses EVM/ERC20 payments. See [wallet configuration](https://github.com/springmint/x402-payment#wallet-configuration) for setup options.

## Request Parameters

| Parameter   | Type     | Required | Description |
|-------------|----------|----------|-------------|
| `chain`     | string   | Yes      | Chain name: `ethereum`, `bsc`, `sepolia`, etc. |
| `token`     | string   | No       | ERC-20 contract address. Empty = native token (ETH/BNB) |
| `addresses` | []string | Yes      | Array of EVM addresses to query. Max 10,000. Must be `0x`-prefixed, 42 chars. |

## Request Body Example

```json
{
  "chain": "ethereum",
  "token": "",
  "addresses": [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8"
  ]
}
```

## Response

JSON with `data` array:

```json
{
  "data": [
    {"address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "balance": "1500000000000000000", "error": ""},
    {"address": "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8", "balance": "25000000000000000000", "error": ""}
  ]
}
```

`balance` is in smallest unit (wei). Divide by `10^decimals` for human-readable value.

## Go Example (Automatic Payment)

```go
package main

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    x402 "github.com/springmint/x402-sdk-go"
    "github.com/springmint/x402-sdk-go/mechanisms"
    "github.com/springmint/x402-sdk-go/signers"
)

func main() {
    signer := signers.NewEvmClientSigner("YOUR_PRIVATE_KEY_HEX")
    xClient := x402.NewX402Client()
    xClient.Register("eip155:*", &mechanisms.Permit402EvmClientMechanism{Signer: signer})
    xHttp := x402.NewX402HTTPClient(http.DefaultClient, xClient)

    reqBody := map[string]interface{}{
        "chain": "ethereum",
        "token": "",
        "addresses": []string{
            "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8",
        },
    }
    bodyBytes, _ := json.Marshal(reqBody)

    resp, err := xHttp.RequestWithPayment(context.Background(), "POST",
        "https://www.cpbox.io/api/x402/batch-balance",
        string(bodyBytes),
        map[string]string{"Content-Type": "application/json"},
    )
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    var result struct {
        Data []struct {
            Address string `json:"address"`
            Balance string `json:"balance"`
            Error   string `json:"error"`
        } `json:"data"`
    }
    json.NewDecoder(resp.Body).Decode(&result)
    fmt.Printf("Done! Got %d results\n", len(result.Data))
}
```

## cURL Example (Manual Two-Step)

**Step 1 - Get payment requirements:**
```bash
curl -X POST https://www.cpbox.io/api/x402/batch-balance \
  -H "Content-Type: application/json" \
  -d '{"chain":"ethereum","token":"","addresses":["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"]}'
# Returns HTTP 402 with payment requirements JSON
```

**Step 2 - Pay and get result:**
```bash
curl -X POST https://www.cpbox.io/api/x402/batch-balance \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: BASE64_ENCODED_SIGNED_PAYLOAD" \
  -d '{"chain":"ethereum","token":"","addresses":["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"]}'
```

## ERC-20 Token Example

Query USDT balances on BSC:
```bash
curl -X POST https://www.cpbox.io/api/x402/batch-balance \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: ..." \
  -d '{
    "chain": "bsc",
    "token": "0x55d398326f99059fF775485246999027B3197955",
    "addresses": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"]
  }'
```

## Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 400       | Bad request: missing addresses, no valid addresses, or >10,000 addresses |
| 402       | Payment required (first-time request, includes payment requirements) |
| 500       | Server error (RPC call failure) |

## Pricing

Each API call costs **0.0001 USDT** (paid automatically via x402 protocol, supports BSC and TRON).

## Supported Chains

Any EVM chain configured in the platform.
