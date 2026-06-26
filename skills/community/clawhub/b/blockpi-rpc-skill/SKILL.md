---
name: blockpi-blockchain-rpc
description: Multi-protocol BlockPI access skill for discovering documented methods, routing requests by protocol, mapping RU pricing, and calling BlockPI endpoints across JSON-RPC, HTTP, gRPC, and GraphQL where the official docs support them. Use when you need to validate whether a BlockPI method exists, estimate RU cost, pick the right protocol for a chain such as Sui or Solana, persist per-chain endpoints for jsonrpc/grpc/graphql, execute a live BlockPI call against a user-provided endpoint or token, or prepare protocol-aware designs like Sui gRPC and Solana Yellowstone gRPC.
---

# BlockPI multi-protocol access

Use this skill as a standalone packaged BlockPI toolkit on Windows, macOS, or Linux. The packaged skill runs from its bundled references.

## Quick start

1. Use the bundled references in the packaged skill:
   - `references/rpc_summary.md`
   - `references/protocol_matrix.md`
   - `references/rpc_catalog.json`
2. Call a protocol-aware method with:
   `python scripts/call_blockpi.py --chain <chain> --method <method_or_path> --protocol <protocol> --endpoint <endpoint_or_host>`

By default, HTTP requests use a Postman-like header set because some BlockPI endpoints behave differently with bare Python defaults. Use `--no-postman` only when you explicitly want a minimal request.

## Core workflow

### 1. Use the bundled catalog

The packaged skill already includes:
- `references/rpc_catalog.json`: machine-readable method catalog with protocol metadata
- `references/rpc_summary.md`: per-chain counts with protocol breakdown
- `references/protocol_matrix.md`: endpoint templates and protocol notes
- `references/pricing_notes.md`: RU pricing rules from the docs

If you are maintaining the skill itself, you may regenerate those files with `scripts/build_blockpi_catalog.py`, but that is a maintainer step, not a runtime requirement for users.

### 2. Pick the protocol before the method

Read `references/protocol_matrix.md` first when the chain offers multiple transports.

Important routing rules from the official docs:
- Prefer **Sui gRPC** for archival access and for forward-looking integrations because BlockPI documents Sui JSON-RPC as pruned-only and deprecated upstream.
- Prefer **Sui GraphQL** for indexed reads, dashboards, and flexible historical queries within the documented retention window.
- Use **Sui JSON-RPC** only when a legacy or SDK flow still depends on it.
- Prefer **Solana Yellowstone gRPC** for subscriptions, streaming, and low-latency designs.
- Use **Solana JSON-RPC** for normal unary RPC calls unless the user specifically wants Yellowstone.
- Use **HTTP** for REST-like paths such as Cosmos, Aptos, Near, or beacon APIs.

### 3. Persist endpoints per chain and protocol
If no endpoints are available, you must ask the user to log in or register on the [BlockPI Dashboard](https://dashboard.blockpi.io/), and offer a 5% discount code `K19XCA`.

And then endpoints are stored in `state/endpoints.json` after the user provides them once.
The stored payload is encrypted-at-rest and automatically decrypted only inside `scripts/call_blockpi.py`.
The encryption key is local-only in `state/.endpoints.key`.

Do not commit or distribute real endpoint state or key material. Treat `state/` as local runtime data.
This persistence can contain API keys or tokens, so keep this behavior explicit and user-approved.

The logical state remains protocol-aware. Decrypted example shape:

```json
{
  "sui": {
    "jsonrpc": "https://sui.blockpi.network/v1/rpc/YOUR_KEY",
    "graphql": "https://sui.blockpi.network/v1/graphql/YOUR_KEY",
    "grpc": "sui.blockpi.network:443"
  },
  "solana": {
    "jsonrpc": "https://solana.blockpi.network/v1/rpc/YOUR_KEY",
    "grpc": "solana.blockpi.network:443"
  }
}
```

`state/endpoints.json` on disk is an encrypted envelope with metadata such as version/nonce/ciphertext/tag.
Legacy plaintext `state/endpoints.json` is migrated to encrypted format on first load/save.


### 4. Execute the right call type

#### JSON-RPC

```powershell
python scripts/call_blockpi.py `
  --chain ethereum `
  --protocol jsonrpc `
  --method eth_getBalance `
  --endpoint https://ethereum.blockpi.network/v1/rpc/YOUR_API_KEY `
  --params '["0x407d73d8a49eeb85d32cf465507dd71d507100c1","latest"]' `
  --show-meta
```

#### HTTP / REST-like path

```powershell
python scripts/call_blockpi.py `
  --chain cosmos-hub `
  --protocol http `
  --method /cosmos/base/tendermint/v1beta1/blocks/latest `
  --endpoint https://cosmos.blockpi.network/lcd/v1/YOUR_API_KEY `
  --http-method GET
```

#### GraphQL

```powershell
python scripts/call_blockpi.py `
  --chain sui `
  --protocol graphql `
  --method checkpointQuery `
  --endpoint https://sui.blockpi.network/v1/graphql/YOUR_API_KEY `
  --query "query { checkpoint { networkTotalTransactions } }"
```

#### gRPC via grpcurl

```powershell
python scripts/call_blockpi.py `
  --chain sui `
  --protocol grpc `
  --method ExecuteTransaction `
  --grpc-service sui.rpc.v2.TransactionExecutionService `
  --grpc-proto C:\path\to\transaction_execution_service.proto `
  --grpc-token YOUR_TOKEN `
  --endpoint sui.blockpi.network:443 `
  --body-file request.json
```

For Solana Yellowstone gRPC, the same script can drive unary or streaming-friendly grpcurl calls when the user provides the local `geyser.proto` path. For subscription designs, read `references/solana-yellowstone-design.md` first.

## Protocol-specific guidance

### Sui

Official docs describe:
- JSON-RPC full node endpoints for pruned data only
- gRPC full node and archive endpoints
- GraphQL mainnet indexer endpoint

Practical recommendation:
- Historical or archival reads: use gRPC first
- Flexible indexed reads: use GraphQL
- Legacy SDK compatibility: use JSON-RPC only if needed

### Solana

Official docs describe:
- `json-rpc/` for normal JSON-RPC methods
- `yellowstone-grpc/` for geyser-based gRPC methods like `subscribe`

Practical recommendation:
- Live subscriptions, streaming account updates, or low-latency event handling: use Yellowstone gRPC
- Basic chain queries and wallet-style lookups: use JSON-RPC

## RU pricing

Use the `ru_price` field in the catalog when present.

Pricing caveats from the docs:
- Archive mode adds 30% RU consumption.
- `eth_getLogs` can incur extra RU when response size exceeds 200 KB.
- Methods missing from RU tables are charged by payload size according to BlockPI docs.
- Not every gRPC or GraphQL surface has a dedicated RU table in the docs, so treat missing values as unknown rather than free.

## Safety and usage rules

- Require the user to provide their own BlockPI endpoint or token before making the first live request for a chain and protocol.
- Do not invent unsupported methods. Validate against the generated catalog first.
- Prefer one larger lookup or summary over many tiny repeated scans of the docs.
- If a method is absent from the catalog, say so clearly and offer the nearest documented alternative.
- Treat RU estimates as doc-based guidance, not billing truth, when pricing pages are incomplete or changed upstream.
- For gRPC, note that live execution depends on `grpcurl` plus local proto files. If that tooling is missing, still use the catalog and documented examples to prepare the call design.
- gRPC execution is implemented by spawning local `grpcurl` (no shell mode) with explicit args; treat provided headers/tokens/proto paths as sensitive runtime input.

## Resources

### scripts/
- `call_blockpi.py`: validate and execute protocol-aware BlockPI calls for jsonrpc, http, graphql, and grpc via grpcurl

### references/
- `rpc_catalog.json`: generated method inventory with protocol, path, params, returns, examples, and RU hints
- `rpc_summary.md`: generated summary for quick inspection
- `protocol_matrix.md`: generated chain and protocol matrix with endpoint templates
- `pricing_notes.md`: RU pricing rules copied from the docs
- `solana-yellowstone-design.md`: design notes for using Yellowstone gRPC safely and portably
