# Pump.fun Snipe — Full Pre-Graduation Token Sniping

Detect new pump.fun token launches via gRPC, derive the bonding curve, calculate a buy quote, and submit a buy transaction.

> **WARNING:** This is a high-risk trading strategy. Use at your own risk.

## Prerequisites

```bash
npm install @solana/web3.js ws @solana/spl-token
export CARBIUM_RPC_KEY="your-key"  # Business tier+
```

## Constants

```typescript
import {
  Connection,
  PublicKey,
  Keypair,
  TransactionInstruction,
  TransactionMessage,
  VersionedTransaction,
  LAMPORTS_PER_SOL,
} from "@solana/web3.js";
import {
  getAssociatedTokenAddressSync,
  TOKEN_PROGRAM_ID,
  ASSOCIATED_TOKEN_PROGRAM_ID,
} from "@solana/spl-token";
import { SystemProgram, SYSVAR_RENT_PUBKEY } from "@solana/web3.js";
import WebSocket from "ws";

const PUMP_PROGRAM = new PublicKey("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P");
const PUMP_GLOBAL = new PublicKey("4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf");
const PUMP_FEE_RECIPIENT = new PublicKey("CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM");
const PUMP_EVENT_AUTH = new PublicKey("Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1");
const GRADUATION_SOL = 85_000_000_000n;

const BUY_DISCRIMINATOR = Buffer.from([0x66, 0x06, 0x3d, 0x12, 0x01, 0xda, 0xeb, 0xea]);

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);
```

## Bonding Curve Helpers

```typescript
function deriveBondingCurve(mint: PublicKey): PublicKey {
  const [address] = PublicKey.findProgramAddressSync(
    [Buffer.from("bonding-curve"), mint.toBuffer()],
    PUMP_PROGRAM
  );
  return address;
}

async function fetchBondingCurve(address: PublicKey) {
  const info = await connection.getAccountInfo(address);
  if (!info) throw new Error("Bonding curve not found");
  const data = info.data;
  return {
    virtualTokenReserves: data.readBigUInt64LE(8),
    virtualSolReserves: data.readBigUInt64LE(16),
    realTokenReserves: data.readBigUInt64LE(24),
    realSolReserves: data.readBigUInt64LE(32),
    complete: data.readUInt8(72) === 1,
  };
}

function quoteBuy(
  curve: Awaited<ReturnType<typeof fetchBondingCurve>>,
  solLamports: bigint
): bigint {
  const num = curve.virtualTokenReserves * solLamports;
  const den = curve.virtualSolReserves + solLamports;
  return num / den;
}
```

## Build Buy Transaction

Buy instruction accounts (order matters, 13 total):

| # | Account | Access |
|---|---|---|
| 0 | PUMP_GLOBAL | read |
| 1 | PUMP_FEE_RECIPIENT | write |
| 2 | mint | read |
| 3 | bondingCurve | write |
| 4 | bondingCurve ATA | write |
| 5 | user ATA | write |
| 6 | user/payer | write, signer |
| 7 | SystemProgram | - |
| 8 | TokenProgram | - |
| 9 | AssociatedTokenProgram | - |
| 10 | Rent sysvar | - |
| 11 | PUMP_EVENT_AUTH | read |
| 12 | PUMP_PROGRAM | read |

```typescript
async function buildBuyTx(
  wallet: Keypair,
  mint: PublicKey,
  solAmount: bigint,
  maxSolCost: bigint
): Promise<VersionedTransaction> {
  const bondingCurve = deriveBondingCurve(mint);
  const bondingCurveAta = getAssociatedTokenAddressSync(mint, bondingCurve, true);
  const userAta = getAssociatedTokenAddressSync(mint, wallet.publicKey);

  const curve = await fetchBondingCurve(bondingCurve);
  if (curve.complete) throw new Error("Token already graduated");

  const tokensOut = quoteBuy(curve, solAmount);
  console.log(`Buying ~${Number(tokensOut) / 1e6} tokens for ${Number(solAmount) / LAMPORTS_PER_SOL} SOL`);

  const data = Buffer.alloc(8 + 8 + 8);
  BUY_DISCRIMINATOR.copy(data, 0);
  data.writeBigUInt64LE(tokensOut, 8);
  data.writeBigUInt64LE(maxSolCost, 16);

  const ix = new TransactionInstruction({
    programId: PUMP_PROGRAM,
    keys: [
      { pubkey: PUMP_GLOBAL, isSigner: false, isWritable: false },
      { pubkey: PUMP_FEE_RECIPIENT, isSigner: false, isWritable: true },
      { pubkey: mint, isSigner: false, isWritable: false },
      { pubkey: bondingCurve, isSigner: false, isWritable: true },
      { pubkey: bondingCurveAta, isSigner: false, isWritable: true },
      { pubkey: userAta, isSigner: false, isWritable: true },
      { pubkey: wallet.publicKey, isSigner: true, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
      { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      { pubkey: ASSOCIATED_TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      { pubkey: SYSVAR_RENT_PUBKEY, isSigner: false, isWritable: false },
      { pubkey: PUMP_EVENT_AUTH, isSigner: false, isWritable: false },
      { pubkey: PUMP_PROGRAM, isSigner: false, isWritable: false },
    ],
    data,
  });

  const { blockhash } = await connection.getLatestBlockhash("confirmed");
  const message = new TransactionMessage({
    payerKey: wallet.publicKey,
    recentBlockhash: blockhash,
    instructions: [ix],
  }).compileToV0Message();

  const tx = new VersionedTransaction(message);
  tx.sign([wallet]);
  return tx;
}
```

## gRPC Launch Detection

```typescript
function watchLaunches(onNewToken: (mint: string, sig: string) => void) {
  const ws = new WebSocket(
    `wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
  );

  ws.on("open", () => {
    console.log("Watching for pump.fun launches...");
    ws.send(JSON.stringify({
      jsonrpc: "2.0", id: 1,
      method: "transactionSubscribe",
      params: [
        { vote: false, failed: false, accountInclude: [PUMP_PROGRAM.toBase58()] },
        { commitment: "confirmed", encoding: "jsonParsed",
          transactionDetails: "full", showRewards: false,
          maxSupportedTransactionVersion: 0 },
      ],
    }));
  });

  setInterval(() => ws.ping(), 30_000);

  ws.on("message", (raw) => {
    const msg = JSON.parse(raw.toString());
    if (msg.method !== "transactionNotification") return;

    const { signature, transaction } = msg.params.result;
    const logs = transaction?.meta?.logMessages || [];
    for (const log of logs) {
      if (log.includes("Instruction: Create")) {
        const mint = transaction.meta.postTokenBalances?.[0]?.mint;
        if (mint) onNewToken(mint, signature);
      }
    }
  });

  ws.on("close", () => console.warn("gRPC disconnected — implement reconnect"));
}

// Run:
// watchLaunches(async (mint, sig) => {
//   console.log(`New token: ${mint} (tx: ${sig})`);
//   const wallet = Keypair.fromSecretKey(/* your key */);
//   const tx = await buildBuyTx(wallet, new PublicKey(mint), 50_000_000n, 55_000_000n);
//   const txSig = await connection.sendRawTransaction(tx.serialize(), {
//     skipPreflight: true,
//     maxRetries: 3,
//   });
//   console.log(`Buy submitted: ${txSig}`);
// });
```
