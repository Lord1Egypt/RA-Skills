# Gasless Swap — Execute Swaps Without SOL for Fees

Execute a token swap where Carbium covers the network fee. Output token must be SOL.

> **Note:** Gasless swaps currently use the v1 swap endpoint (`/api/v1/swap`) with the `gasless=true` flag.

## Prerequisites

```bash
npm install @solana/web3.js
export CARBIUM_RPC_KEY="your-key"
export CARBIUM_API_KEY="your-swap-api-key"
```

## Gasless Swap Flow

```typescript
import { Connection, VersionedTransaction, Keypair } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

const API_KEY = process.env.CARBIUM_API_KEY!;
const SOL_MINT = "So11111111111111111111111111111111111111112";
const USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";

async function gaslessSwap(wallet: Keypair, usdcAmount: number) {
  // Output MUST be SOL for gasless to work
  // Gasless uses v1 swap endpoint with fromMint/toMint params
  const url = new URL("https://api.carbium.io/api/v1/swap");
  url.searchParams.set("owner", wallet.publicKey.toBase58());
  url.searchParams.set("fromMint", USDC_MINT);
  url.searchParams.set("toMint", SOL_MINT);
  url.searchParams.set("amount", usdcAmount.toString());
  url.searchParams.set("slippage", "100");
  url.searchParams.set("provider", "raydium");
  url.searchParams.set("gasless", "true"); // Enable gasless

  const res = await fetch(url, {
    headers: { accept: "text/plain", "X-API-KEY": API_KEY },
  });

  if (!res.ok) throw new Error(`Gasless swap failed: ${res.status}`);

  const { transaction } = await res.json();

  const tx = VersionedTransaction.deserialize(
    Buffer.from(transaction, "base64")
  );
  tx.sign([wallet]);

  // User pays no SOL for the network fee
  const sig = await connection.sendRawTransaction(tx.serialize(), {
    maxRetries: 3,
  });

  await connection.confirmTransaction(sig, "confirmed");
  console.log("Gasless swap confirmed:", sig);
  return sig;
}

// Run:
// const wallet = Keypair.fromSecretKey(/* your key */);
// await gaslessSwap(wallet, 1_000_000); // 1 USDC (6 decimals)
```
