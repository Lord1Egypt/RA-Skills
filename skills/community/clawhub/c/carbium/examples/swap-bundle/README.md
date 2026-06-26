# Swap Bundle — MEV-Protected Execution via Jito Bundle

Execute a swap with Jito MEV protection using the Carbium Swap API. No separate Jito SDK required.

> **Note:** Bundle submission currently uses the v1 endpoints (`/api/v1/swap` with `mevSafe=true` + `/api/v1/swap/bundle`).

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

// Step 1: Get swap transaction with MEV safety (v1 endpoint)
async function getSwapTx(
  owner: string,
  fromMint: string,
  toMint: string,
  amount: number,
  slippage: number,
  provider: string
) {
  const url = new URL("https://api.carbium.io/api/v1/swap");
  url.searchParams.set("owner", owner);
  url.searchParams.set("fromMint", fromMint);
  url.searchParams.set("toMint", toMint);
  url.searchParams.set("amount", amount.toString());
  url.searchParams.set("slippage", slippage.toString());
  url.searchParams.set("provider", provider);
  url.searchParams.set("mevSafe", "true"); // Adds Jito tip instruction

  const res = await fetch(url, {
    headers: { accept: "text/plain", "X-API-KEY": API_KEY },
  });

  if (!res.ok) throw new Error(`Swap failed: ${res.status}`);
  return res.json();
}

// Step 2: Sign transaction
function signTransaction(base64Tx: string, wallet: Keypair): string {
  const tx = VersionedTransaction.deserialize(
    Buffer.from(base64Tx, "base64")
  );
  tx.sign([wallet]);
  return Buffer.from(tx.serialize()).toString("base64");
}

// Step 3: Submit via Jito bundle (v1 endpoint)
async function submitBundle(signedBase64: string) {
  const url = new URL("https://api.carbium.io/api/v1/swap/bundle");
  url.searchParams.set("signedTransaction", signedBase64);

  const res = await fetch(url, {
    headers: { accept: "application/json", "X-API-KEY": API_KEY },
  });

  if (!res.ok) throw new Error(`Bundle submission failed: ${res.status}`);
  return res.json();
}

// Full MEV-protected swap
async function mevProtectedSwap(wallet: Keypair) {
  const SOL = "So11111111111111111111111111111111111111112";
  const USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v";

  const { transaction } = await getSwapTx(
    wallet.publicKey.toBase58(),
    SOL, USDC,
    100_000_000, // 0.1 SOL
    100,          // 1% slippage
    "raydium"
  );

  const signed = signTransaction(transaction, wallet);
  const result = await submitBundle(signed);
  console.log("Bundle submitted:", result);
  return result;
}

// Run:
// const wallet = Keypair.fromSecretKey(/* your key */);
// await mevProtectedSwap(wallet);
```
