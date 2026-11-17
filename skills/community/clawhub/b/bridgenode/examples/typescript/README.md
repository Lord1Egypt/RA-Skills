# BridgeNode TypeScript example

Buyer-side example: AI agent pays for and calls BridgeNode with the official
x402 TS SDKs (`@x402/fetch` + `@x402/svm`).

## Setup

```bash
npm install
cp .env.example .env
# fill SVM_PRIVATE_KEY (agent's Solana keypair, must have USDC ATA)
```

## Run

```bash
npm run start
```

## What it does

1. Registers the Solana exact payment scheme.
2. `POST /v1/chat/completions` through `wrapFetchWithPayment` — 402 handled
   automatically: sign partial TX → retry with `PAYMENT-SIGNATURE` → 200.
3. Prints the payment response (settlement receipt).

## Expected output

```
POST https://bridgenode.cc/v1/chat/completions

{
  id: '...',
  object: 'chat.completion',
  model: 'deepseek-v4-flash',
  choices: [ { index: 0, message: { role: 'assistant', content: 'Hello!' }, finish_reason: 'stop' } ],
  usage: { prompt_tokens: 10, completion_tokens: 4, total_tokens: 14 },
  header: {
    success: true,
    payer: '<your wallet address>',
    transaction: '<signature>',
    network: 'solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp',
    amount: '2000'
  }
}
```

- The exact `amount` comes from the 402 response (minimum charge: 2000 atomic units = $0.002).
- Live prices always: `GET https://bridgenode.cc/v1/models`.

## Troubleshooting

- **`SVM_PRIVATE_KEY` missing** — copy `.env.example` to `.env` and fill in the keypair.
- **`InsufficientFunds` / payment rejected** — the wallet needs a USDC ATA with balance on Solana mainnet.
- **TypeScript compile errors** — run `npm install` first; requires Node 20+.
- **`503 Service busy`** — retry with backoff.
- **Empty answer from reasoning models** — use `max_tokens >= 200`.

## Notes

- Solana mainnet, real USDC. Minimum charge: $0.002 per request.
- Gas is sponsored by BridgeNode — the agent only needs USDC, no SOL.
- The agent must have an existing USDC ATA.
