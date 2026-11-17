---
name: fetch-evm-logs
description:
  Scaffold and fetch event logs from any EVM smart contract via RPC (eth_getLogs + ABI parse).
  Works on any EVM-compatible chain/contract (Ethereum, L2s, custom chains) given chainId +
  address + RPC. Trigger when the user asks to get, pull, fetch, sync, or download contract
  event logs / 合约日志 / 事件日志 / eth_getLogs — e.g.「帮我获取某个 EVM 合约的日志」
  「帮我拉取智能合约的日志」「fetch logs for this contract」「get Transfer events from 0x…」.
  Also when they give chainId + contractAddress and want on-chain events. Discovers ABI from
  public sources or accepts user-provided ABI, lists events, asks which to fetch, then runs
  s1/s2. Pull + parse only — not for stats/analytics (use evm-log-stats).
---

# Fetch EVM Logs

Pull event logs from **any EVM contract** on any EVM-compatible chain (Ethereum mainnet/testnets, L2s, sidechains, custom chains) — not limited to a specific protocol or event type. You only need `chainId`, `contractAddress`, an RPC, and an ABI (auto-fetched or user-provided).

Self-contained skill: **scaffold → chainId + address → get ABI → pick events → pull + parse**.

```
init-project.sh
  → ask chainId + contractAddress (+ rpc)
  → ABI: public fetch OR user-provided
  → list events → user picks → contract.ts → pnpm s1 → pnpm s2
```

Templates: this skill's `templates/` (no external repo).

## When to use (triggers)

**Scope:** any EVM contract / any chain that speaks JSON-RPC `eth_getLogs` — ERC-20, NFT, distributor, DEX, custom contracts, etc.

**Use this skill** when the user wants raw/on-chain **event logs** from an EVM smart contract. Typical asks:

| User says (examples) | Action |
|----------------------|--------|
| 「帮我获取某个 EVM 合约的日志」 | Start this skill |
| 「帮我获取 / 拉取智能合约的日志」 | Start this skill |
| 「帮我拉一下这个合约的 event / Transfer / Claim 日志」 | Start this skill |
| 「fetch / pull / sync logs for contract `0x…`」 | Start this skill |
| 「用 eth_getLogs 拉这个地址的事件」 | Start this skill |
| Gives `chainId` + `contractAddress` and wants events | Start this skill |

If they only have a vague ask (「帮我获取智能合约的日志」) without address/chainId, **still start this skill**, then ask for `chainId` + `contractAddress` in Step 1.

**Do not use** for:

- Aggregating / stats / CSV claim rates → **evm-log-stats**
- Deploying contracts, writing Solidity, or general chain Q&A without wanting logs

## Step 0 — Initialize project

If no project yet:

```bash
bash ~/.cursor/skills/fetch-evm-logs/scripts/init-project.sh [target_dir]
```

Default: `./fetch_evm_logs`. Then continue below.

## Step 1 — Ask for chainId + contractAddress

**Required from user:**

| Item | Required | Example |
|------|----------|---------|
| `chainId` | yes | `1`, `41443` |
| `contractAddress` | yes | `0x4CcDb...` |
| RPC URL | optional | public RPC for that chain if user has none |
| `startBlock` / `endBlock` | optional | default `0` / `'latest'` |
| `tokenDecimals` | optional | `18` for amount fields |

Ask clearly, e.g.:

> 请提供 `chainId` 和合约地址 `contractAddress`。如有专用 RPC 也可一并提供。

## Step 2 — Get ABI (public fetch or user-provided)

ABI **cannot** be read from JSON-RPC bytecode alone. Two valid ways to obtain it:

### A. Try public verified-contract sources first

```bash
node ~/.cursor/skills/fetch-evm-logs/scripts/fetch-abi.mjs \
  --chainId <id> --address <0x...> --out <project>/src/abi
```

1. **Sourcify** (no API key)
2. **Etherscan-compatible API** if `ETHERSCAN_API_KEY` is set (or user provides a key)

### B. User-provided ABI (always allowed; required if A fails)

If public fetch fails, the contract is unverified, or the user already has the ABI — **ask the user to provide it**:

> 公开源未能找到该合约 ABI。请粘贴完整合约 ABI JSON（或至少包含目标 event 的 fragment），也可提供本地 ABI 文件路径。

Accept:

- Paste JSON in chat
- Point to a local file

Then write it to:

```
src/abi/abi_{address}_{chainId}.json
```

(`address` lowercase). Do **not** invent or guess ABI.

### List events and confirm

```bash
node ~/.cursor/skills/fetch-evm-logs/scripts/list-events.mjs \
  --abi <project>/src/abi/abi_{address}_{chainId}.json
```

**Show the event list to the user** and ask which to fetch:

> 该合约 ABI 中有以下 event：…  
> 需要拉取哪些？可选：全部 / 指定若干个 event 名称。

Do **not** skip this confirmation when multiple events exist (unless they already said “全部”).

## Step 3 — Configure

### ABI path

```
src/abi/abi_{address}_{chainId}.json
```

(`address` lowercase)

### `src/contract.ts`

```typescript
export const Contracts = {
  contracts: {
    MyContract: {
      address: '0x...',
      chainId: 41443,
      // string OK; array = ordered failover on RPC errors
      rpc: ['https://primary-rpc.example', 'https://backup-rpc.example'],
      startBlock: 0,
      endBlock: 'latest',
      // '*' = all ABI events; or string[] of event names
      eventNames: ['Transfer', 'Approval'],
      tokenDecimals: 18,
    },
  },
};
```

- `rpc: string | string[]` — on failure, retries then rotates to the next URL
- `eventNames: '*'` → pull all logs from the contract (no topic filter)
- `eventNames: ['Foo', 'Bar']` → topic0 OR filter for those events
- ABI loaded automatically via `address` + `chainId`

## Step 4 — Run

```bash
cd <target_dir>
pnpm s1    # → output/{address}_{chainId}/logs.txt
pnpm s2    # → output/{address}_{chainId}/logs.json
```

Stop after s2.

## Output layout

```
output/{address}_{chainId}/
  ├── logs.txt
  └── logs.json
```

Parsed log:

```typescript
{
  txHash: string;
  logIndex: number;
  blockNumber: number;
  eventName: string;
  data: Record<string, string | boolean>;
}
```

## Checklist

```
- [ ] Project scaffolded (if needed)
- [ ] User gave chainId + contractAddress
- [ ] ABI obtained (public fetch **or** user-provided) → abi_{address}_{chainId}.json
- [ ] Events listed; user chose which to fetch
- [ ] contract.ts configured
- [ ] pnpm s1 && pnpm s2
```

## Pitfalls

- Unverified / private-chain contracts → public fetch fails; **ask user for ABI** (do not block)
- Prefer multiple RPCs in `rpc: [...]` so failover can recover from rate limits / outages
- Large block ranges → lower `pageSize` in s1 (default 1000)
- ABI filename must be `abi_{address}_{chainId}.json` (lowercase address)

## Additional Resources

- [scripts/init-project.sh](scripts/init-project.sh)
- [scripts/fetch-abi.mjs](scripts/fetch-abi.mjs)
- [scripts/list-events.mjs](scripts/list-events.mjs)
- [reference.md](reference.md)
- [examples.md](examples.md)
