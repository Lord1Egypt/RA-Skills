# x402 Payment Flow on Hedera

## Overview

x402 is an HTTP-based payment protocol. When a server requires payment, it returns HTTP 402 with payment requirements. The client signs a transaction and retries.

## Flow

```
Agent → MCP Server: callTool("hedera_token_lookup", {tokenId: "0.0.429274"})
Agent ← MCP Server: 402 Payment Required
                     { accepts: [{ scheme: "exact", network: "hedera-testnet",
                       maxAmountRequired: "10000", payTo: "0x...", asset: "0x..." }] }

Agent → ClawPay SDK: createPaymentHeader(signer, requirements)
Agent ← ClawPay SDK: X-PAYMENT token (base64 partially-signed tx)

Agent → MCP Server: callTool(..., { _meta: { "x402/payment": token } })
MCP Server → Blocky402 Facilitator: verify(payment, requirements)
Blocky402 → Hedera: submit TransferTransaction (USDC)
MCP Server ← Blocky402: { isValid: true }
MCP Server: execute tool
MCP Server → Blocky402: settle(payment, requirements)
Agent ← MCP Server: { content: [...], _meta: { "x402/payment-response": { success: true, tx: "0.0.xxx@..." } } }

ClawPay HCS Hook → Hedera: TopicMessageSubmitTransaction (audit log)
```

## Hedera-Specific Details

- Uses HTS (Hedera Token Service) for USDC transfers
- USDC testnet token: `0.0.429274` (6 decimals)
- Facilitator: Blocky402 (`api.testnet.blocky402.com`)
- Payments settle in ~3-5 seconds
- Every payment logged to HCS topic (immutable audit trail)

## Payment Assets

| Asset | Testnet ID | Mainnet ID | Decimals |
|-------|-----------|------------|----------|
| USDC  | 0.0.429274 | 0.0.456858 | 6 |
| HBAR  | native    | native     | 8 |
