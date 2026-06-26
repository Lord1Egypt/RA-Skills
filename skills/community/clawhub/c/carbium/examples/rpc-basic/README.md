# RPC Basic — Balance Check & Transaction Send

Basic Carbium RPC usage: reading a wallet balance and sending SOL.

## Prerequisites

```bash
npm install @solana/web3.js
export CARBIUM_RPC_KEY="your-key"
```

## Read Balance

```typescript
import {
  Connection,
  PublicKey,
  LAMPORTS_PER_SOL,
  Keypair,
  SystemProgram,
  Transaction,
  sendAndConfirmTransaction,
} from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

async function getBalance(address: string): Promise<number> {
  const pubkey = new PublicKey(address);
  const balance = await connection.getBalance(pubkey);
  console.log(`Balance: ${balance / LAMPORTS_PER_SOL} SOL`);
  return balance;
}

const WALLET = "YOUR_WALLET_ADDRESS";
await getBalance(WALLET);
```

## Send SOL

```typescript
async function sendSol(
  from: Keypair,
  to: string,
  lamports: number
): Promise<string> {
  const transaction = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: from.publicKey,
      toPubkey: new PublicKey(to),
      lamports,
    })
  );

  const signature = await sendAndConfirmTransaction(connection, transaction, [from], {
    commitment: "confirmed",
  });

  console.log("Transaction confirmed:", signature);
  return signature;
}
```
