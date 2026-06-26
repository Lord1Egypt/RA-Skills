# BlockPI RPC Skill

A BlockPI multi-protocol access skill for AI agents, designed to:

- Look up methods and interfaces **documented** in the official BlockPI docs
- Choose the appropriate access method by chain and protocol
- Use RU (Request Unit) pricing information as a reference when designing calls
- Send JSON-RPC, HTTP, GraphQL, and gRPC requests through a unified workflow
- Persist local endpoint configuration for different chains and protocols

The core purpose of this skill is not to "invent new interfaces," but to help Claude or other users access BlockPI safely in a **protocol-aware** way based on locally packaged reference materials and scripts.

## Core Capabilities

### 1. Multi-Protocol Support

The following protocol types are supported:

- `jsonrpc`
- `http`
- `graphql`
- `grpc`

All calls are unified through the following script:

```bash
python scripts/call_blockpi.py --chain <chain> --method <method_or_path> --protocol <protocol> --endpoint <endpoint_or_host>
```

### 2. Documentation-Driven Method Discovery

This skill includes local reference materials that can be used to verify whether a method is supported by the official BlockPI documentation, rather than guessing method names.

Key files:

- `references/rpc_catalog.json`: Machine-readable method catalog containing protocol, path, parameters, examples, RU hints, and more
- `references/rpc_summary.md`: Per-chain method summary
- `references/protocol_matrix.md`: Per-chain list of supported protocols, endpoint templates, and protocol notes
- `references/pricing_notes.md`: RU pricing notes

### 3. Protocol-Aware Routing

The point of this skill is not to force every chain through JSON-RPC, but to choose a more suitable protocol based on each chain's officially supported capabilities.

Typical strategy:

- **Sui**
  - Prefer `gRPC`: archive data and forward-looking integrations
  - Second choice `GraphQL`: indexed queries, dashboards, and flexible historical queries
  - Use `JSON-RPC` only for compatibility with legacy SDKs or older workflows
- **Solana**
  - Prefer `Yellowstone gRPC`: subscriptions, streaming, and low-latency scenarios
  - `JSON-RPC`: regular queries and standard unary RPC
- **Cosmos / Aptos / Near / beacon-style interfaces**
  - Prefer `HTTP` / REST-style paths

### 4. Local Endpoint Persistence

When a user provides an endpoint for a given chain and protocol for the first time, the script saves it to:

- `state/endpoints.json`
- `state/.endpoints.key` (local encryption key used to decrypt/encrypt endpoint state)

The logical endpoint mapping remains:

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

On disk, `state/endpoints.json` is stored as an encrypted envelope (`version`, `nonce`, `ciphertext`, `tag`).
Legacy plaintext endpoint state is automatically migrated to encrypted format on first load/save.

Note: `state/` contains sensitive local runtime data and should not be committed or distributed with real keys, tokens, endpoints, or key files.

## Support Overview

According to `references/rpc_summary.md`, the current index covers **48 chains**.

Most of them are primarily JSON-RPC based. Representative multi-protocol chains include:

- **Sui**: `jsonrpc` + `graphql` + `grpc`
- **Solana**: `jsonrpc` + `grpc` (Yellowstone)

Typical use cases for this skill:

- Verify whether a BlockPI method exists in the documentation
- Choose an appropriate access method on multi-protocol chains
- Estimate the rough RU cost of a call
- Make a real request using a user-provided endpoint
- Design access plans for Sui gRPC / Solana Yellowstone
## How To Use

### Step 1: Installation
You can directly use the following prompt with your AI Agents 
```
Please help me to install this skill: https://github.com/BlockPILabs/blockpi-rpc-skill#
```

Or you can clone this repo into your dirctory `.agent/skills/`

```bash
git clone https://github.com/BlockPILabs/blockpi-rpc-skill.git && mv ./blockpi-rpc-skill your_agent_skill_dirctory
```

### Step 2: Usage

Log in or register on the [BlockPI Dashboard](https://dashboard.blockpi.io/)

Create an endpoint for any chain you want

Copy endpoint and send it to your AI Chat. Your agents will remember your endpoint. Then, simply describe what you want to query on-chain. For example:
```
I want to get the latest raw data from BSC blockchain.
```


## Call Examples

### JSON-RPC

```bash
python scripts/call_blockpi.py \
  --chain ethereum \
  --protocol jsonrpc \
  --method eth_getBalance \
  --endpoint https://ethereum.blockpi.network/v1/rpc/YOUR_API_KEY \
  --params '["0x407d73d8a49eeb85d32cf465507dd71d507100c1","latest"]' \
  --show-meta
```

### HTTP / REST-like

```bash
python scripts/call_blockpi.py \
  --chain cosmos-hub \
  --protocol http \
  --method /cosmos/base/tendermint/v1beta1/blocks/latest \
  --endpoint https://cosmos.blockpi.network/lcd/v1/YOUR_API_KEY \
  --http-method GET
```

### GraphQL

```bash
python scripts/call_blockpi.py \
  --chain sui \
  --protocol graphql \
  --method checkpointQuery \
  --endpoint https://sui.blockpi.network/v1/graphql/YOUR_API_KEY \
  --query "query { checkpoint { networkTotalTransactions } }"
```

### gRPC

```bash
python scripts/call_blockpi.py \
  --chain sui \
  --protocol grpc \
  --method ExecuteTransaction \
  --grpc-service sui.rpc.v2.TransactionExecutionService \
  --grpc-proto /path/to/transaction_execution_service.proto \
  --grpc-token YOUR_TOKEN \
  --endpoint sui.blockpi.network:443 \
  --body-file request.json
```

## RU Pricing Notes

This skill tries to use the `ru_price` field from the catalog as a reference, but it should be treated as a **documentation-level estimate**, not the final billed amount.

Known notes include:

- Archive mode usually increases RU consumption by **30%**
- `eth_getLogs` may incur extra RU when the response is large
- Methods not listed in the RU table may be billed based on payload size
- Not all gRPC / GraphQL surfaces have complete RU tables

### gRPC Dependencies

gRPC calls are not performed through a built-in SDK. Instead, they rely on:

- A locally installed `grpcurl`
- A user-provided `.proto` file path
- Optional authentication information such as `x-token`
- A local subprocess invocation of `grpcurl` with explicit argument passing (no shell mode)

That means this skill is better suited for:

- Protocol validation
- Method discovery
- One-off call testing
- Call design preparation

Rather than full typed SDK integration.

## Usage Principles

- Before making a real call, the user must provide the endpoint or token
- Do not invent methods that do not exist in the documentation
- Prefer checking the local catalog instead of repeatedly scanning the raw documentation
- If a method does not exist, say so clearly and provide the closest available alternative
- RU information is for reference only
- For gRPC scenarios that require long-running streaming subscriptions, read the relevant design notes before deciding whether to execute directly

## Directory Structure

```text
blockpi-rpc-skill/
├── LICENSE
├── SKILL.md
├── README.md
├── references/
│   ├── pricing_notes.md
│   ├── protocol_matrix.md
│   ├── rpc_catalog.json
│   ├── rpc_summary.md
│   └── solana-yellowstone-design.md
└── scripts/
    └── call_blockpi.py
```

## Maintenance Notes

- Runtime behavior mainly depends on the generated reference materials under `references/`
- If you need to refresh the catalog data, regenerate the catalog in a maintenance workflow
- `state/` contains local state and should not include committed real configuration
- Some catalog entries may be closer to documentation page titles than strict raw RPC method names, so judge them together with the protocol and examples

## Summary

This is a Claude Code skill for BlockPI that is **multi-protocol, documentation-driven, and capable of executing real calls**.

It is especially useful for:

- Determining whether a BlockPI method is supported by the official docs
- Choosing the correct protocol on multi-protocol chains such as Sui and Solana
- Using the local catalog to quickly design calls
- Executing real requests through a unified script

A good way to think about it is as a lightweight BlockPI protocol routing and calling toolkit.
