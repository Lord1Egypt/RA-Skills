# BridgeNode Examples

Buyer-side examples: how an AI agent pays for and calls BridgeNode via x402.

All examples are **client-side only** — they use the public x402 SDKs and the
public BridgeNode endpoint (`https://bridgenode.cc/v1`). No server code.

> ⚠️ **Mainnet warning:** BridgeNode runs on Solana mainnet with real USDC.
> Use a wallet with a small balance. Minimum charge per request: $0.002 USDC.
> Check the 402 `amount` before signing.

## Contents

| Example | Stack | What it shows |
|---|---|---|
| [curl/](curl/README.md) | curl + x402curl | Manual x402 flow: request → 402 → sign → retry |
| [python/](python/README.md) | Python + `x402[svm,httpx]` | OpenAI-compatible call with automatic payment |
| [typescript/](typescript/README.md) | TypeScript + `@x402/svm` | Fetch wrapper with automatic payment |
| [mcp/](mcp/README.md) | MCP client | Paid tool call through the BridgeNode MCP server |

## Flow (x402 V2, exact scheme)

1. `POST /v1/chat/completions` without payment → server responds `402` with a
   `PAYMENT-REQUIRED` header (base64 JSON: amount, payTo, memo).
2. Client signs a partial transaction: USDC `TransferChecked` + Memo.
3. Client retries with `PAYMENT-SIGNATURE` header.
4. Server verifies, settles (gas sponsored by BridgeNode), returns `200` with a
   `PAYMENT-RESPONSE` header (settlement receipt).

Network: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` (mainnet) · Asset: USDC
`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

Models and live prices: `GET https://bridgenode.cc/v1/models` (free).
