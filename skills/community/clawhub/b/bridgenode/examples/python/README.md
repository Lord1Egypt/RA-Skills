# BridgeNode Python example

Buyer-side example: AI agent pays for and calls BridgeNode with the official
x402 Python SDK (`x402[svm,httpx]`).

## Setup

```bash
pip install "x402[svm,httpx]" "solana==0.39.0" python-dotenv
cp .env.example .env
# fill SVM_PRIVATE_KEY (agent's Solana keypair, must have USDC ATA)
```

## Run

```bash
python main.py
```

## What it does

1. `GET /v1/models` — free, lists models and prices.
2. `POST /v1/chat/completions` — x402 payment handled automatically:
   request → 402 → sign partial TX (USDC TransferChecked + Memo) →
   retry with `PAYMENT-SIGNATURE` → 200 + `PAYMENT-RESPONSE`.

## Expected output

```
Initialized SVM account: <your wallet address>
Models & prices: {"object":"list","data":[{"id":"deepseek-v4-flash","pricing":{"prompt":2e-07,"completion":4e-07},...}]}

POST https://bridgenode.cc/v1/chat/completions
Status: 200
Body: {"id":"...","object":"chat.completion","model":"deepseek-v4-flash","choices":[...],"usage":{...}}

Payment response: {
  "success": true,
  "payer": "<your wallet address>",
  "transaction": "<signature>",
  "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
  "amount": "2000"
}
```

- The exact `amount` comes from the 402 response (minimum charge: 2000 atomic units = $0.002).
- Live prices always: `GET https://bridgenode.cc/v1/models`.

## Troubleshooting

- **`SVM_PRIVATE_KEY missing`** — copy `.env.example` to `.env` and fill in the keypair.
- **`InsufficientFunds` / payment rejected** — the wallet needs a USDC ATA with balance on Solana mainnet.
- **`Invalid account`** — the agent must have an existing USDC ATA (it is derived from the wallet address automatically when funded).
- **`402` spam / timeout** — the server rate-limits 402 responses per IP; wait a moment and retry.
- **Empty answer from reasoning models** — use `max_tokens >= 200`; too-small limits can produce an empty response (service was provided, no refund).

## Notes

- Solana mainnet, real USDC. Minimum charge: $0.002 per request.
- Gas is sponsored by BridgeNode — the agent only needs USDC, no SOL.
- The agent must have an existing USDC ATA (associated token account).
- Funding: send USDC on Solana mainnet to the agent's own wallet — BridgeNode never holds balances; every request is paid individually via x402 (exact amount in the 402 response). The USDC ATA is derived from the agent's wallet address; no manual token account setup needed.
