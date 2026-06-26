# gRPC Stream — Program Transaction Subscription

Subscribe to real-time program transactions via Carbium gRPC with automatic reconnection.

## Prerequisites

```bash
npm install ws
export CARBIUM_RPC_KEY="your-key"  # Business tier+
```

## Subscribe with Reconnect

```typescript
import WebSocket from "ws";

const PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"; // Pump.fun

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function connect() {
  return new Promise<void>((resolve, reject) => {
    const ws = new WebSocket(
      `wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
    );

    ws.on("open", () => {
      console.log("Connected to Carbium gRPC");

      ws.send(
        JSON.stringify({
          jsonrpc: "2.0",
          id: 1,
          method: "transactionSubscribe",
          params: [
            {
              vote: false,
              failed: false,
              accountInclude: [PROGRAM_ID],
              accountExclude: [],
              accountRequired: [],
            },
            {
              commitment: "confirmed",
              encoding: "base64",
              transactionDetails: "full",
              showRewards: false,
              maxSupportedTransactionVersion: 0,
            },
          ],
        })
      );
    });

    // Keepalive ping every 30s
    const pingInterval = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) ws.ping();
    }, 30_000);

    ws.on("message", (raw) => {
      const msg = JSON.parse(raw.toString());

      if (msg.result !== undefined) {
        console.log(`Subscribed, ID: ${msg.result}`);
        return;
      }

      if (msg.method === "transactionNotification") {
        const { signature, slot } = msg.params.result;
        console.log(`tx ${signature} in slot ${slot}`);
      }
    });

    ws.on("close", (code) => {
      clearInterval(pingInterval);
      console.warn(`Disconnected (${code})`);
      reject(new Error(`WS closed: ${code}`));
    });

    ws.on("error", (err) => {
      console.error("WS error:", err.message);
    });
  });
}

// Reconnect with exponential backoff
async function main() {
  let backoff = 1000;
  while (true) {
    try {
      await connect();
      backoff = 1000;
    } catch {
      console.log(`Reconnecting in ${backoff}ms...`);
      await delay(backoff);
      backoff = Math.min(backoff * 2, 30_000);
    }
  }
}

main();
```
