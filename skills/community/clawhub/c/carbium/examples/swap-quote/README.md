# Swap Quote — Quote + Execute in One Call (v2/Q1)

Full swap flow using Carbium's Q1 engine: get a quote with executable transaction, sign it, and submit via RPC. Single API call — no separate swap endpoint needed.

## Prerequisites

```bash
npm install @solana/web3.js
export CARBIUM_RPC_KEY="your-key"
export CARBIUM_API_KEY="your-swap-api-key"
```

## Full Flow

```typescript
import { Connection, VersionedTransaction, Keypair } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

const API_KEY = process.env.CARBIUM_API_KEY!;
const SOL_MINT = "So11111111111111111111111111111111111111112";
const USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";

// Step 1: Get quote with executable transaction
async function getQuoteWithTx(walletAddress: string, amountLamports: number) {
  const url = new URL("https://api.carbium.io/api/v2/quote");
  url.searchParams.set("src_mint", SOL_MINT);
  url.searchParams.set("dst_mint", USDC_MINT);
  url.searchParams.set("amount_in", amountLamports.toString());
  url.searchParams.set("slippage_bps", "100");
  url.searchParams.set("user_account", walletAddress); // triggers txn in response

  const res = await fetch(url, {
    headers: { "X-API-KEY": API_KEY },
  });

  if (!res.ok) throw new Error(`Quote failed: ${res.status}`);
  return res.json();
}

// Step 2: Sign and submit
async function executeSwap(wallet: Keypair, amountLamports: number) {
  const quote = await getQuoteWithTx(
    wallet.publicKey.toBase58(),
    amountLamports
  );
  console.log("Quote:", {
    in: quote.srcAmountIn,
    out: quote.destAmountOut,
    minOut: quote.destAmountOutMin,
    route: quote.routePlan,
  });

  if (!quote.txn) {
    throw new Error("No executable transaction — ensure user_account is set");
  }

  const tx = VersionedTransaction.deserialize(
    Buffer.from(quote.txn, "base64")
  );
  tx.sign([wallet]);

  const sig = await connection.sendRawTransaction(tx.serialize(), {
    maxRetries: 3,
  });

  await connection.confirmTransaction(sig, "confirmed");
  console.log("Swap confirmed:", sig);
  return sig;
}

// Run:
// const wallet = Keypair.fromSecretKey(/* your key */);
// await executeSwap(wallet, 100_000_000); // 0.1 SOL
```
