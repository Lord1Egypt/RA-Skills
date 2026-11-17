# BridgeNode MCP example

Call BridgeNode through its MCP server with x402 payment.

## Server

- URL: `https://bridgenode.cc/mcp` (streamable-http)
- Tool: `chat_completions` (model | mode, messages, max_tokens)
- Payment: x402 handshake per tool call (via `_meta["x402/payment"]`)

Prices are annotated in `tools/list` (`x-x402`) as an indication; the actual
amount is in the 402 response — always check it before signing.

## Option A — one-command wrapper (any MCP client)

```bash
npx -y @bridgenode/mcp@latest
```

Use this as the MCP server command in your client (Claude Code, Cursor,
Windsurf, etc.). The wrapper connects to `https://bridgenode.cc/mcp` and
handles x402 payment automatically with the agent's wallet.

Claude Code example:

```bash
claude mcp add bridgenode -- npx -y @bridgenode/mcp@latest
```

## Option B — direct streamable-http

Configure your MCP client with:

```
URL: https://bridgenode.cc/mcp
Transport: streamable-http
```

## What the agent sees

1. `tools/list` → `chat_completions` with `x-x402` price annotation.
2. `tools/call` → server returns payment required (result with
   `structuredContent` PaymentRequired object).
3. Client signs the USDC transaction, retries the call with
   `_meta["x402/payment"]`.
4. Server settles, runs inference, returns the completion with
   `_meta["x402/payment-response"]` (settlement receipt).

## Expected output (`tools/list`)

```json
{"result":{"tools":[{"name":"chat_completions","title":"Chat completions with x402 payment","description":"Send a chat completion request to any supported model. Paid tool: x402 payment (Solana USDC) is required — the first call returns 402 with the exact price; retry with _meta[\"x402/payment\"]. ...","inputSchema":{...},"x-x402":{"scheme":"exact","network":"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp","amount":"2000","asset":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","payTo":"<BridgeNode wallet>"}}]}}
```

- The `x-x402` amount is **indicative** (floor); the exact amount is in the 402 response — always check it before signing.

## Troubleshooting

- **`tools/call` returns payment required** — expected on the first call; that is the x402 challenge, not an error.
- **Client can't connect** — use the one-command wrapper (`npx -y @bridgenode/mcp@latest`) or point the client at `https://bridgenode.cc/mcp` with `streamable-http`.
- **`503 Service busy`** — retry with backoff.
- **Empty answer from reasoning models** — use `max_tokens >= 200`.

## Notes

- Solana mainnet, real USDC. Minimum charge: $0.002 per request.
- Gas sponsored by BridgeNode — the agent only needs USDC, no SOL.
- Free tools (e.g., model list) skip payment.
