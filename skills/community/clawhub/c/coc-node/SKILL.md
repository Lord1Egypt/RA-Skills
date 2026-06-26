---
name: coc-node
description: Operate COC (ChainOfClaw) blockchain nodes — install, start, stop, monitor, and remove validator, fullnode, archive, gateway, and dev nodes. Use when the user wants to run a COC node, inspect the status of a running node (block height, peer count, BFT state), view node logs, edit node-config.json, or probe RPC endpoints. Also covers preparing a machine to provide ≥ 256 MiB of P2P storage to the COC network. **Smooth out-of-box experience (1.2.0+):** read-only commands (list / status / coc-rpc-query against an installed node) work immediately after `openclaw plugins install` with zero config; the activation banner reports `data dir`, `storage quota`, `tracked nodes`, and `coc repo` status so the operator sees at a glance what works now and what (if anything) needs config to unlock install/start. Data dir auto-resolves to a writable path along the same chain @chainofclaw/claw-mem and @chainofclaw/soul use (`config.dataDir → $COC_NODE_DATA_DIR → $CLAW_MEM_DATA_DIR/coc-node → $OPENCLAW_STATE_DIR/coc-node → ~/.claw-mem/coc-node`); legacy `~/.chainofclaw/nodes.json` from pre-1.2.0 installs is detected as a fallback. Fail-fast actionable EACCES at activation rather than silent breakage mid-command. Starting / installing a node additionally requires a local clone of the COC source repo (set $COC_REPO_PATH or `bootstrap.cocRepoPath`); the activation banner tells you whether one was auto-detected.
version: 1.2.0
metadata:
  openclaw:
    homepage: https://www.npmjs.com/package/@chainofclaw/node
    primaryEnv: CLAW_MEM_DATA_DIR
    requires:
      bins:
        - node
      anyBins:
        - coc-node
        - openclaw
    install:
      - kind: node
        package: "@chainofclaw/node"
        version: "1.2.0"
        bins:
          - coc-node
---

# coc-node — COC blockchain node lifecycle

Operate a COC node on this machine. The skill is backed by the npm package [`@chainofclaw/node`](https://www.npmjs.com/package/@chainofclaw/node) which ships both a standalone `coc-node` CLI and an OpenClaw plugin (skill id `coc-node`).

## What this skill can do

- **Install** a new COC node of any type: `validator`, `fullnode`, `archive`, `gateway`, or `dev`
- **Start / stop / restart** nodes; follow logs across the node / agent / relayer streams
- **Report status** — block height, peer count, BFT activity, process PID, per-service health
- **Edit** a node's `node-config.json` in `$EDITOR`
- **Probe** any COC RPC endpoint safely (whitelisted methods only: `eth_blockNumber`, `eth_getBlockByNumber`, `net_peerCount`, `coc_chainStats`, `coc_getBftStatus`, `eth_syncing`, `eth_chainId`, …)

## Zero-config on install (1.2.0+)

**Everything you can do without a COC source repo works immediately after `openclaw plugins install` — no further setup.** The activation banner makes it explicit:

```
[coc-node] data dir: /home/<you>/.claw-mem/coc-node
[coc-node] storage quota: advertised=256 MiB, reserved=256 MiB, enforce=true
[coc-node] tracked nodes: 0
[coc-node] coc repo: detected at /home/<you>/COC — install/start commands enabled
[coc-node] Loaded — no nodes yet, run `openclaw coc-node node install <name>` to add one
[coc-node] CLI is mounted at `openclaw coc-node ...`. ...
```

Or, if no COC repo is on this machine:

```
[coc-node] coc repo: not detected — read-only mode (list / status / coc-rpc-query work; install / start need bootstrap.cocRepoPath or $COC_REPO_PATH pointing at a COC source clone)
```

That second line is the **only** thing you need to read to know whether `node install` / `node start` will work. Everything else (list, status, log inspection, RPC probes against an already-running node) is unconditionally available.

### Data directory

Auto-resolves to a writable path along a chain that's intentionally aligned with `@chainofclaw/claw-mem` and `@chainofclaw/soul` so the three plugins share one operator-managed root. Priority (highest first):

1. `config.dataDir` (per-instance plugin config)
2. `$COC_NODE_DATA_DIR` (coc-node-specific operator override)
3. `$CLAW_MEM_DATA_DIR/coc-node` (shared with claw-mem + soul — set this once and all three move together)
4. `$OPENCLAW_STATE_DIR/coc-node` (sandbox-managed state dir)
5. `~/.claw-mem/coc-node` (default — shared root with claw-mem + soul)
6. `~/.chainofclaw` (legacy pre-1.2.0 fallback; only picked when `nodes.json` already exists there)

Fails fast at activation with an actionable EACCES error naming each tried path, rather than silently breaking mid-command. `/tmp` is intentionally not a fallback.

### What needs setup to start a node yourself

Actually starting a node process requires the COC source repository (it spawns `node/src/index.ts` from there). Tell the skill where the repo is via **one of**:

- `COC_REPO_PATH` environment variable (simplest)
- `bootstrap.cocRepoPath` in plugin config
- Run inside (or anywhere under) the COC repo — auto-discovered via marker files
- Place a clone at `~/COC` — also auto-discovered

Plus ≥ 256 MiB free disk for the P2P storage reservation (mandatory COC network entry requirement).

The activation banner tells you whether the auto-detection succeeded. If `COC_REPO_PATH` is unset and no clone is at `~/COC`, `node install` and `node start` fail with a clear error pointing here — list / status / log / RPC commands keep working.

## Relationship with claw-mem and coc-soul

The three `@chainofclaw/*` skills are **fully decoupled** at the npm-dependency level. Each can be installed independently. They cooperate through shared on-disk conventions, not through code coupling:

| Skill | Owns | What it adds when paired |
|---|---|---|
| **coc-node** | Local node lifecycle (install / start / stop / status / RPC probe) | Independent of the other two. |
| [claw-mem2db](https://clawhub.ai/ngplateform/claw-mem2db) | Persistent agent memory (chat + tool capture, FTS5 search, hybrid recall) | Pure agent-side; doesn't touch the chain. coc-node doesn't read or write to its DB. |
| [coc-soul](https://clawhub.ai/ngplateform/coc-soul) | On-chain DID, IPFS backup, guardian recovery, carrier resurrection | Reads claw-mem's SQLite DB (when present) for semantic snapshots. Also independent of coc-node. |

**Shared dataDir convention.** All three default to writing under `~/.claw-mem` (or under `$CLAW_MEM_DATA_DIR` / `$OPENCLAW_STATE_DIR`), each in a scoped subdirectory:

- claw-mem → `~/.claw-mem/{claw-mem.db, config.json, ...}`
- coc-soul → `~/.claw-mem/keys/agent.key`
- coc-node → `~/.claw-mem/coc-node/{nodes.json, <node>/...}`

So one `CLAW_MEM_DATA_DIR=/somewhere/writable` env var moves all three. Operators in sandboxed Docker hosts (where `~/.claw-mem` is read-only) only have one knob to turn.

## How to invoke

**Inside OpenClaw (recommended — works automatically after `plugins install`):**

```bash
openclaw coc-node node install --type fullnode --network testnet
openclaw coc-node node list
openclaw coc-node node status
openclaw coc-node node logs <name> --follow --all
```

**Standalone bin (only if you ran `npm i -g @chainofclaw/node` separately):**

```bash
coc-node node install --type dev --network local --name dev-1 --rpc-port 28780
coc-node node list
```

> `openclaw plugins install` does NOT install the standalone `coc-node` binary into your PATH. Use `openclaw coc-node ...` (with the `openclaw` prefix), or install the bin globally via npm if you want the bare command.

## Typical flows

1. **Spin up a dev node against local hardhat** — `coc-node node install --type dev --network local` then `coc-node node start dev-1`.
2. **Join testnet as a fullnode** — `coc-node node install --type fullnode --network testnet --rpc-port 28780` then `coc-node node start`.
3. **Stand up a validator** — `coc-node node install --type validator --network testnet --advertised-bytes 1073741824` (1 GiB storage contribution).
4. **Diagnose a flaky node** — `coc-node node status` (snapshot) → `coc-node node logs --follow` (tail) → `coc-node node config show` (inspect config) → `coc-node node restart` if needed.
5. **Decommission a node** — `coc-node node stop NAME` then `coc-node node remove NAME --yes` (delete data) or `coc-node node remove NAME --yes --keep-data`.

## When NOT to use this skill

- Deploying COC smart contracts — that's a `contracts/` hardhat / script task, not node lifecycle.
- On-chain identity / backup / recovery — use the [coc-soul](https://clawhub.ai/ngplateform/coc-soul) skill.
- Agent memory / session capture — use the [claw-mem2db](https://clawhub.ai/ngplateform/claw-mem2db) skill.

## Reference

Detailed references live alongside this file:

- `references/cli.md` — every `coc-node` subcommand with flags and examples
- `references/config.md` — complete `~/.claw-mem/coc-node/config.json` schema
- `references/node-types.md` — validator vs fullnode vs archive vs gateway vs dev tradeoffs
- `references/troubleshooting.md` — common failure modes and fixes

Source and issue tracker: <https://github.com/NGPlateform/claw-mem/tree/main/packages/node>.
