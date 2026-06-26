# Trading Bot Architecture with Carbium

## Recommended Architecture

Split your bot into three isolated services:

1. **Reader** — pulls RPC state or listens on gRPC/WebSocket
2. **Decision layer** — evaluates whether signals are actionable
3. **Execution service** — requests quote, signs, submits, confirms

Keep keys and signing inside backend services you control. Do not let one loop both discover opportunities and blindly hammer retries.

```
Market state → Bot reader → Decision layer → Quote request → Signed tx → RPC submit → Confirmation
                   ↑                                                           ↑
              gRPC/WSS listener                                        Status check before retry
```

## Which Carbium Surface for Each Job

| Bot job | Best surface | Why |
|---|---|---|
| Read balances, blockhashes, status | RPC | Standard JSON-RPC, any SDK |
| Request executable swap route | Swap API (`/quote` with `user_account`) | Returns ready-to-sign transaction |
| Submit signed transaction | RPC | Standard Solana submission path |
| Compare routes across DEXes | Swap API (`/quote/all`) | See all provider quotes at once |
| Watch transaction-heavy flows | gRPC | Better than constant RPC polling |
| Monitor specific accounts | Standard WebSocket | Lower tier requirement than gRPC |
| MEV-protected execution | Swap API (`/swap/bundle`) | Jito bundling built in |

## Minimal Bot: Quote on API, Execute on RPC

```typescript
import { Connection, VersionedTransaction, Keypair } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

async function executeArb(wallet: Keypair, fromMint: string, toMint: string, amount: number) {
  // 1. Get executable quote
  const url = new URL("https://api.carbium.io/api/v2/quote");
  url.searchParams.set("src_mint", fromMint);
  url.searchParams.set("dst_mint", toMint);
  url.searchParams.set("amount_in", amount.toString());
  url.searchParams.set("slippage_bps", "10");
  url.searchParams.set("user_account", wallet.publicKey.toBase58());

  const quote = await fetch(url, {
    headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! },
  }).then(r => r.json());

  if (!quote.txn) {
    console.log("No route found");
    return;
  }

  // 2. Sign
  const tx = VersionedTransaction.deserialize(Buffer.from(quote.txn, "base64"));
  tx.sign([wallet]);

  // 3. Submit
  const sig = await connection.sendRawTransaction(tx.serialize(), {
    skipPreflight: true,
    maxRetries: 3,
  });

  // 4. Confirm — check status before retrying
  const status = await connection.getSignatureStatus(sig);
  console.log(`Submitted: ${sig}`, status.value);
}
```

## Rate Limit Strategy for Bots

429 errors are architecture signals:

- **Separate keys** for dev, staging, and production
- **Never retry `sendTransaction`** before checking `getSignatureStatus`
- **Isolate retry paths** from decision logic — a retry that triggers another quote doubles your request count
- **Track credits** via the RPC dashboard to avoid hitting monthly limits

## Adding gRPC for Real-Time Feeds

Add gRPC when polling becomes too slow or expensive. Typical trigger points:

- You are polling every 400ms or faster
- You need to react to transactions within a single slot
- Your RPC credit consumption is dominated by polling

```typescript
// Reader service with gRPC
import WebSocket from "ws";

const ws = new WebSocket(`wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`);

ws.on("open", () => {
  ws.send(JSON.stringify({
    jsonrpc: "2.0", id: 1,
    method: "transactionSubscribe",
    params: [
      { vote: false, failed: false, accountInclude: ["TARGET_PROGRAM"] },
      { commitment: "confirmed", encoding: "base64", transactionDetails: "full",
        showRewards: false, maxSupportedTransactionVersion: 0 },
    ],
  }));
});

// Feed signals to decision layer
ws.on("message", (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.method === "transactionNotification") {
    decisionLayer.evaluate(msg.params.result);
  }
});
```

## Security Checklist for Bots

- API keys in environment variables only — never in code
- Signing happens on a trusted backend, never exposed to external services
- RPC endpoint restricted by IP in the dashboard
- Separate API keys per environment (dev/staging/prod)
- Rate limit monitoring to avoid unexpected 429s
- Transaction status checked before any retry
