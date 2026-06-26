# Carbium Standard WebSocket Reference

## Endpoint

```
wss://wss-rpc.carbium.io/?apiKey=YOUR_RPC_KEY
```

Same RPC key used for HTTP JSON-RPC. Available on all tiers (Developer+ recommended for production).

## Subscription Methods

### slotSubscribe

Track new slot numbers as they are processed.

**Request:**
```json
{"jsonrpc": "2.0", "id": 1, "method": "slotSubscribe"}
```

**Notification:**
```json
{
  "jsonrpc": "2.0",
  "method": "slotNotification",
  "params": {
    "result": { "parent": 407716775, "root": 407716744, "slot": 407716776 },
    "subscription": 123456
  }
}
```

### rootSubscribe

Track new root (finalized) slots.

**Request:**
```json
{"jsonrpc": "2.0", "id": 1, "method": "rootSubscribe"}
```

### accountSubscribe

Watch account data changes (balance, data field).

**Request:**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "accountSubscribe",
  "params": [
    "ACCOUNT_ADDRESS",
    { "encoding": "base64", "commitment": "confirmed" }
  ]
}
```

**Notification:**
```json
{
  "jsonrpc": "2.0",
  "method": "accountNotification",
  "params": {
    "result": {
      "context": { "slot": 407716776 },
      "value": {
        "lamports": 366200727,
        "data": ["base64encodeddata==", "base64"],
        "owner": "11111111111111111111111111111111",
        "executable": false,
        "rentEpoch": 18446744073709551615
      }
    },
    "subscription": 123456
  }
}
```

### programSubscribe

Watch all accounts owned by a program on change.

**Request:**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "programSubscribe",
  "params": [
    "PROGRAM_ID",
    {
      "encoding": "base64",
      "commitment": "confirmed",
      "filters": [
        { "dataSize": 165 }
      ]
    }
  ]
}
```

Optional filters: `dataSize` (account size) and `memcmp` (byte comparison at offset).

**Notification:**
```json
{
  "jsonrpc": "2.0",
  "method": "programNotification",
  "params": {
    "result": {
      "context": { "slot": 407716776 },
      "value": { "pubkey": "ACCOUNT_ADDRESS", "account": { "lamports": 0, "data": [...], "owner": "PROGRAM_ID" } }
    },
    "subscription": 123456
  }
}
```

### signatureSubscribe

Watch confirmation status of a specific transaction.

**Request:**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "signatureSubscribe",
  "params": ["TX_SIGNATURE", { "commitment": "confirmed" }]
}
```

**Notification:**
```json
{
  "jsonrpc": "2.0",
  "method": "signatureNotification",
  "params": {
    "result": {
      "context": { "slot": 407716776 },
      "value": { "err": null }
    },
    "subscription": 123456
  }
}
```

Auto-unsubscribes after first notification.

### logsSubscribe

Stream transaction logs matching a filter.

**Request (all logs):**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "logsSubscribe",
  "params": ["all", { "commitment": "confirmed" }]
}
```

**Request (specific program):**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "method": "logsSubscribe",
  "params": [{ "mentions": ["PROGRAM_ID"] }, { "commitment": "confirmed" }]
}
```

Filter options: `"all"`, `"allWithVotes"`, `{ "mentions": ["PROGRAM_ID"] }`

**Notification:**
```json
{
  "jsonrpc": "2.0",
  "method": "logsNotification",
  "params": {
    "result": {
      "context": { "slot": 407716776 },
      "value": {
        "signature": "5j7s6ZFGnBMnEU4...",
        "err": null,
        "logs": [
          "Program 6EF8r... invoke [1]",
          "Program log: Instruction: Buy",
          "Program 6EF8r... success"
        ]
      }
    },
    "subscription": 123456
  }
}
```

### blockSubscribe

Stream full block data. Use for block explorers and indexers.

```json
{"jsonrpc": "2.0", "id": 1, "method": "blockSubscribe"}
```

### slotsUpdatesSubscribe

Detailed slot lifecycle events for advanced timing and validator monitoring.

```json
{"jsonrpc": "2.0", "id": 1, "method": "slotsUpdatesSubscribe"}
```

### voteSubscribe

Stream vote transactions for validator monitoring.

```json
{"jsonrpc": "2.0", "id": 1, "method": "voteSubscribe"}
```

## Unsubscribe Methods

| Subscribe | Unsubscribe | Notes |
|---|---|---|
| `slotSubscribe` | `slotUnsubscribe` | |
| `rootSubscribe` | `rootUnsubscribe` | |
| `accountSubscribe` | `accountUnsubscribe` | |
| `programSubscribe` | `programUnsubscribe` | |
| `signatureSubscribe` | `signatureUnsubscribe` | Auto after first notification |
| `logsSubscribe` | `logsUnsubscribe` | |
| `blockSubscribe` | `blockUnsubscribe` | |

**Format:**
```json
{"jsonrpc": "2.0", "id": 2, "method": "METHOD_Unsubscribe", "params": [SUBSCRIPTION_ID]}
```

## Multiple Subscriptions

Use one WebSocket connection for multiple subscriptions — do not open a connection per subscription:

```typescript
const subs = [
  { id: 1, method: "slotSubscribe", params: [] },
  { id: 2, method: "accountSubscribe", params: [WALLET, { encoding: "base64", commitment: "confirmed" }] },
  { id: 3, method: "logsSubscribe", params: [{ mentions: [PROGRAM_ID] }, { commitment: "confirmed" }] },
];
subs.forEach(sub => ws.send(JSON.stringify({ jsonrpc: "2.0", ...sub })));
```

## Error Codes

| Code | Message | Cause |
|---|---|---|
| `-32700` | Parse error | Malformed JSON or missing required params |
| `-32601` | Method not found | Typo or unsupported method |
| `-32602` | Invalid params | Wrong param types or missing fields |
| `-32603` | Internal error | Server-side — retry |

## Production Requirements

- Implement reconnection with exponential backoff (cap at 30s)
- Send ping every 30 seconds to prevent silent disconnects
- Re-subscribe to all streams after reconnect
- Use one connection for multiple subscriptions
