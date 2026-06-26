# WebSocket Monitor — Account + Slot + Logs Monitoring

Monitor wallet balances, slot progression, and program logs using Carbium Standard WebSocket via `@solana/web3.js`.

## Prerequisites

```bash
npm install @solana/web3.js
export CARBIUM_RPC_KEY="your-key"
```

## Monitor Multiple Subscriptions

```typescript
import { Connection, PublicKey } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  {
    commitment: "confirmed",
    wsEndpoint: `wss://wss-rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  }
);

const WALLET = new PublicKey("YOUR_WALLET_ADDRESS");
const PROGRAM_ID = new PublicKey("YOUR_PROGRAM_ID");

// Watch wallet balance
const accountSubId = connection.onAccountChange(
  WALLET,
  (accountInfo, context) => {
    console.log(
      `[Account] Balance: ${accountInfo.lamports / 1e9} SOL at slot ${context.slot}`
    );
  },
  "confirmed"
);

// Watch slot progression
const slotSubId = connection.onSlotChange((slotInfo) => {
  console.log(`[Slot] ${slotInfo.slot} (parent: ${slotInfo.parent})`);
});

// Watch program logs
const logsSubId = connection.onLogs(
  PROGRAM_ID,
  (logs, context) => {
    console.log(`[Logs] Tx: ${logs.signature}`);
    if (logs.err) {
      console.log(`  Error: ${JSON.stringify(logs.err)}`);
    }
    logs.logs.forEach((log) => console.log(`  ${log}`));
  },
  "confirmed"
);

// Confirm a specific transaction
async function confirmTx(signature: string): Promise<boolean> {
  return new Promise((resolve) => {
    connection.onSignature(
      signature,
      (result) => {
        if (result.err) {
          console.log(`Tx failed: ${JSON.stringify(result.err)}`);
          resolve(false);
        } else {
          console.log("Tx confirmed!");
          resolve(true);
        }
      },
      "confirmed"
    );
  });
}

console.log("Monitoring started. Press Ctrl+C to exit.");

// Cleanup on exit:
// connection.removeAccountChangeListener(accountSubId);
// connection.removeSlotChangeListener(slotSubId);
// connection.removeOnLogsListener(logsSubId);
```
