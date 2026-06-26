# Migration Guide

## From Other RPC Providers

### Helius

```typescript
// Before
const connection = new Connection("https://mainnet.helius-rpc.com/?api-key=YOUR_HELIUS_KEY");

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

All standard Solana JSON-RPC methods work identically. No code changes beyond the URL.

### QuickNode

```typescript
// Before
const connection = new Connection("https://your-endpoint.quiknode.pro/YOUR_KEY");

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

### Triton

```typescript
// Before
const connection = new Connection("https://your-endpoint.triton.one/?api-key=YOUR_KEY");

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

### Alchemy

```typescript
// Before
const connection = new Connection("https://solana-mainnet.g.alchemy.com/v2/YOUR_KEY");

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

### Python (any provider)

```python
# Before
rpc = Client("https://previous-provider.com/?api-key=KEY")

# After
rpc = Client(f"https://rpc.carbium.io/?apiKey={os.environ['CARBIUM_RPC_KEY']}")
```

### Rust (any provider)

```rust
// Before
let client = RpcClient::new("https://previous-provider.com/?api-key=KEY");

// After
let url = format!("https://rpc.carbium.io/?apiKey={}", std::env::var("CARBIUM_RPC_KEY")?);
let client = RpcClient::new(url);
```

## From Triton gRPC

Same Yellowstone protocol — update endpoint only:

```typescript
// Before
const ws = new WebSocket("wss://your-triton-endpoint.triton.one/...");

// After
const ws = new WebSocket(
  `wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

For Rust (HTTP/2):

```rust
// Before
let mut client = GeyserGrpcClient::connect("https://triton-endpoint", "TRITON_TOKEN", None)?;

// After
let mut client = GeyserGrpcClient::connect("https://grpc.carbium.io", "YOUR_RPC_KEY", None)?;
```

Subscription filters and data format are identical (Yellowstone-compatible).

## From Jupiter Swap API

### Parameter Name Mapping

| Jupiter | Carbium `/quote` | Carbium `/swap` |
|---|---|---|
| `inputMint` | `src_mint` | `fromMint` |
| `outputMint` | `dst_mint` | `toMint` |
| `amount` | `amount_in` | `amount` |
| `slippageBps` | `slippage_bps` | `slippage` |

### URL and Auth

```typescript
// Jupiter (no auth required)
const jupQuote = await fetch(
  "https://quote-api.jup.ag/v6/quote?inputMint=SOL&outputMint=USDC&amount=1000000000&slippageBps=100"
);

// Carbium (API key required)
const carbQuote = await fetch(
  "https://api.carbium.io/api/v2/quote?src_mint=SOL_MINT&dst_mint=USDC_MINT&amount_in=1000000000&slippage_bps=100",
  { headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! } }
);
```

### Key Differences

- Carbium requires an API key (free to obtain)
- Carbium Quote and Swap use different parameter names (see warning in SKILL.md)
- Carbium's `/quote` with `user_account` param returns a ready-to-sign transaction
- Carbium supports `gasless` flag on `/swap` (output must be SOL)
- Carbium bundles Jito MEV protection via `/swap/bundle` endpoint
- Carbium exposes per-provider comparison via `/quote/all`

## WebSocket Migration

### From Any Solana Provider's WSS

```typescript
// Before
const connection = new Connection("https://previous-rpc.com", {
  wsEndpoint: "wss://previous-wss.com",
});

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  {
    commitment: "confirmed",
    wsEndpoint: `wss://wss-rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  }
);
```

All standard Solana pubsub methods are supported with identical behavior.
