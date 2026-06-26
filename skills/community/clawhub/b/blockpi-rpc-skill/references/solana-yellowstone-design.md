# Solana Yellowstone gRPC design notes

Use this file when the user wants Solana streaming, subscriptions, or low-latency event access.

## What the official docs currently show

BlockPI documents these methods:
- `ping`
- `getSlot`
- `getLatestBlockhash`
- `getVersion`
- `isBlockHashValid`
- `subscribe`
- `suix_getallbalances`

The docs reference the upstream Yellowstone `geyser.proto` release and show `grpcurl` examples with `x-token` metadata.

## Routing guidance

- Prefer Yellowstone gRPC when the user needs subscriptions, slot streams, account streams, transaction streams, or low-latency infra.
- Prefer Solana JSON-RPC for classic wallet, explorer, or one-shot RPC requests.
- If a workflow mixes both, keep separate saved endpoints for `jsonrpc` and `grpc` in `state/endpoints.json`.

## Execution model

### Supported now

- Unary gRPC calls through `grpcurl`, when `grpcurl` and a local `geyser.proto` file are available.
- Request preparation, endpoint persistence, and protocol-aware routing in `call_blockpi.py`.

### Not fully automated yet

- Rich long-lived streaming orchestration around `subscribe`
- Proto download automation
- Local code generation for typed Solana clients

Those are intentionally left out to keep the skill cross-platform and dependency-light.

## Portable command pattern

PowerShell example:

```powershell
grpcurl -proto C:\path\to\geyser.proto `
  -H "x-token: YOUR_TOKEN" `
  -d '{"slots":{},"accounts":{},"transactions":{},"blocks":{},"blocks_meta":{},"accounts_data_slice":[]}' `
  solana.blockpi.network:443 `
  geyser.Geyser/Subscribe
```

POSIX example:

```bash
grpcurl -proto /path/to/geyser.proto \
  -H 'x-token: YOUR_TOKEN' \
  -d '{"slots":{},"accounts":{},"transactions":{},"blocks":{},"blocks_meta":{},"accounts_data_slice":[]}' \
  solana.blockpi.network:443 \
  geyser.Geyser/Subscribe
```

## Recommended next step when deeper Yellowstone support is needed

If the user wants production-grade streaming, add a dedicated helper script later that:
- manages reconnects
- writes streamed events to stdout or a file
- accepts canned subscription templates
- keeps proto path and token handling explicit

Until then, treat this skill as protocol-aware discovery plus a safe `grpcurl` launcher for direct calls.
