# BridgeNode curl example

Manual x402 flow with curl. This shows the protocol steps; for automatic
payment handling use [x402curl](https://github.com/second-state/x402-skill)
(drop-in curl replacement) or the SDK examples.

> ⚠️ Mainnet warning: Solana mainnet, real USDC. Minimum charge: $0.002.
> Check the 402 `amount` before signing.

## Step 1 — Request, get 402

```bash
curl -sS -D - -o /dev/null https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hello"}],"max_tokens":100}'
```

Expected: `HTTP/1.1 402 Payment Required` with a `PAYMENT-REQUIRED` header
(base64 JSON: scheme, network, amount, asset, payTo, memo, feePayer).

## Step 2 — Sign the partial transaction

Decode the `PAYMENT-REQUIRED` header and sign a partial transaction:
USDC `TransferChecked` (amount from the 402) + Memo instruction, signed with
the agent's Solana keypair. The fee payer is NOT signed by the agent —
BridgeNode sponsors gas.

Use any x402-capable signer: `x402curl`, the official SDKs (`x402[svm,httpx]`,
`@x402/svm`), or the Solana `pay` CLI. This produces a base64 JSON payload
(`x402Version`, `resource`, `accepted`, `payload.transaction`).

## Step 3 — Retry with PAYMENT-SIGNATURE

```bash
PAYLOAD="<base64 JSON from step 2>"
curl -sS https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: $PAYLOAD" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hello"}],"max_tokens":100}'
```

Expected: `200 OK` with the completion and a `PAYMENT-RESPONSE` header
(settlement receipt).

## Automatic alternative — x402curl

```bash
# install: https://github.com/second-state/x402-skill
# config: X402_PRIVATE_KEY=... (agent's Solana keypair)
x402curl -sS https://bridgenode.cc/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"hello"}],"max_tokens":100}'
```

x402curl detects the 402, signs the payment, and retries automatically.

## Expected output (Step 1)

```
HTTP/2 402
payment-required: <base64 JSON — scheme, network, amount, asset, payTo, memo, feePayer, recentBlockhash>
{"x402Version":2,"error":"PAYMENT-SIGNATURE header is required","resource":{...},"accepts":[{"scheme":"exact","network":"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp","asset":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","amount":"2000","payTo":"<BridgeNode wallet>","maxTimeoutSeconds":30,"extra":{...}}]}
```

## Expected output (Step 3, after signing)

```
HTTP/2 200
payment-response: <base64 JSON — SettlementResponse: success, payer, transaction, network, amount>
{"id":"...","object":"chat.completion","model":"deepseek-v4-flash","choices":[...],"usage":{...}}
```

- The exact `amount` comes from the 402 response (minimum charge: 2000 atomic units = $0.002).
- Live prices always: `GET https://bridgenode.cc/v1/models`.

## Troubleshooting

- **`402` instead of `200`** — expected on the first request; that is the payment challenge, not an error.
- **`400 Bad request`** — unknown model, invalid body, or `max_tokens` above the non-stream cap (use `stream: true` for long generations).
- **`503 Service busy`** — retry with backoff.
- **Signing fails** — use `x402curl`, the official SDKs (`x402[svm,httpx]`, `@x402/svm`), or the Solana `pay` CLI; the fee payer is NOT signed by the agent.
- **Empty answer from reasoning models** — use `max_tokens >= 200`.

## Notes

- Network: `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` (mainnet)
- Asset: USDC `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- The agent needs a USDC ATA, but no SOL (gas sponsored).
- Free: `GET https://bridgenode.cc/v1/models` (models + prices).
