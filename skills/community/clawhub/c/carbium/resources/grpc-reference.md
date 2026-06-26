# Carbium gRPC Reference

## Connection

| Method | Endpoint | Auth |
|---|---|---|
| WebSocket | `wss://grpc.carbium.io/?apiKey=KEY` | Query parameter |
| HTTP/2 (Rust) | `https://grpc.carbium.io` | Header: `x-token: KEY` |

Requires **Business tier or above** ($320/mo+).

## Protocol

JSON-RPC 2.0 over WebSocket. Messages are JSON text frames.

## Methods

### transactionSubscribe

Subscribe to real-time transaction notifications with filtering.

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "transactionSubscribe",
  "params": [
    {
      "vote": false,
      "failed": false,
      "accountInclude": ["PROGRAM_ID"],
      "accountExclude": [],
      "accountRequired": []
    },
    {
      "commitment": "confirmed",
      "encoding": "base64",
      "transactionDetails": "full",
      "showRewards": false,
      "maxSupportedTransactionVersion": 0
    }
  ]
}
```

### Filter Fields (first parameter)

| Field | Type | Description | Required |
|---|---|---|---|
| `vote` | boolean | Include validator vote transactions | Yes |
| `failed` | boolean | Include failed transactions | Yes |
| `accountInclude` | string[] | Include txs involving **any** of these accounts | At least one of Include/Required must have values |
| `accountExclude` | string[] | Exclude txs involving these accounts | No |
| `accountRequired` | string[] | Include only txs involving **all** of these accounts | At least one of Include/Required must have values |

### Subscription Options (second parameter)

| Field | Type | Values | Default |
|---|---|---|---|
| `commitment` | string | `processed`, `confirmed`, `finalized` | `confirmed` |
| `encoding` | string | `base64`, `base58`, `jsonParsed` | `base64` |
| `transactionDetails` | string | `full`, `signatures`, `none` | `full` |
| `showRewards` | boolean | Include reward information | `false` |
| `maxSupportedTransactionVersion` | number | Max tx version (0 = legacy + v0) | `0` |

### transactionUnsubscribe

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "transactionUnsubscribe",
  "params": [SUBSCRIPTION_ID]
}
```

## Response Shapes

### Subscription Confirmation

```json
{
  "jsonrpc": "2.0",
  "result": 1234567890,
  "id": 1
}
```

The `result` is the subscription ID — use it for unsubscribing.

### Transaction Notification

```json
{
  "jsonrpc": "2.0",
  "method": "transactionNotification",
  "params": {
    "result": {
      "signature": "5VERv8NMvzbJM...",
      "slot": 123456789,
      "transaction": {
        "transaction": ["base64_encoded_data", "base64"],
        "meta": {
          "err": null,
          "fee": 5000,
          "preBalances": [],
          "postBalances": [],
          "logMessages": []
        }
      }
    },
    "subscription": 1234567890
  }
}
```

## Full Blocks vs Shreds

| Metric | Value | Context |
|---|---|---|
| Solana Slot Resolution | ~400ms | Block production window |
| Competitor "Shreds" | ~9ms | Fragmented, requires client reassembly |
| Carbium Full Blocks | ~22ms | Atomic, complete, ready for use |

Carbium streams Full Blocks (Layer 2) built on the Yellowstone protocol (Layer 1). The 13ms difference is negligible within a 400ms slot window but provides:

- **Atomic integrity** — complete state update in one message
- **Parsing efficiency** — ideal for database indexing (Postgres, ClickHouse)
- **Simplicity** — no client-side shred reassembly logic

## Use Cases

| Use Case | Why gRPC |
|---|---|
| Institutional indexing / ETL | Atomic integrity prevents database corruption |
| Arbitrage / trading bots | Complete state per slot; reduces failed txs |
| MEV searchers | Ground truth for model validation |
| Real-time dashboards | Stable, complete block events for UX |
| Pump.fun sniping | Detect new token launches instantly |
| Wallet monitoring | Low-latency deposit/transfer detection |

## Yellowstone Compatibility

- **Rust clients:** Use `yellowstone-grpc-client` crate with HTTP/2 endpoint and `x-token` header
- **TypeScript/Python:** Use WebSocket JSON-RPC interface (not native protobuf)
- Filter fields and data format follow Yellowstone conventions

## Production Requirements

- Send ping every 30 seconds to prevent silent disconnects
- Implement exponential backoff reconnection (cap at 30s)
- Re-subscribe to all streams after reconnect
