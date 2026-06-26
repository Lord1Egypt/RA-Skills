# `coc-node` CLI reference

All commands live under `coc-node node`. Every subcommand prints `--help` with full flag detail.

## `node install` (alias: `node init`)

Create a new node — generates `node-config.json`, writes to the registry, does **not** start the process.

| Flag | Meaning | Default |
|---|---|---|
| `-t, --type <type>` | `validator` / `fullnode` / `archive` / `gateway` / `dev` | `dev` |
| `-n, --network <net>` | `testnet` / `mainnet` / `local` / `custom` | `local` |
| `--name <name>` | Unique node name | auto-generated |
| `--data-dir <dir>` | Override data directory | `~/.chainofclaw/nodes/<name>` |
| `--rpc-port <n>` | JSON-RPC port | 18780 (local) / 28780 (testnet) |
| `--advertised-bytes <n>` | Storage to advertise to the P2P network | 268435456 (256 MiB min) |

## `node list`

Table of every node tracked by the registry. `--json` for machine-readable output.

## `node start [name]` / `node stop [name]` / `node restart [name]`

Omit `name` to apply to all registered nodes.

## `node status [name]`

Live status. Without `name`: prints each registered node. With `--json`: structured output including:

- `running` (bool), `pid`, `dataDir`
- `blockHeight`, `peerCount`, `bftActive` (only if RPC is reachable)
- `services.{node,agent,relayer}.{running, pid}`

## `node remove <name>`

Deregister a node.

- `--yes` — skip confirmation prompt
- `--keep-data` — preserve the data directory on disk (default: delete)

## `node config show [name]`

Pretty-print the node's `node-config.json`.

## `node config edit <name>`

Open `node-config.json` in `$EDITOR`.

## `node logs <name>`

Tail / follow logs.

- `--follow` (`-f`) — continuous tail (like `tail -F`)
- `--service <svc>` — `node` (default), `agent`, or `relayer`
- `--all` — interleave all three service logs
- `--lines <n>` — how many lines when not following (default 100)

## RPC probe

A read-only RPC helper is also exported by the underlying library. If you only need to inspect a remote node:

```ts
import { rpcCall, ALLOWED_RPC_METHODS } from "@chainofclaw/node";
const height = await rpcCall("http://remote:28780", "eth_blockNumber", []);
```

`ALLOWED_RPC_METHODS` is the allowlist — anything else fails at the client side (defense-in-depth against accidental exposure of mutating methods).
