# Fetch EVM Logs — Reference

## Skill layout

```
fetch-evm-logs/
├── SKILL.md
├── reference.md
├── examples.md
├── scripts/
│   ├── init-project.sh
│   ├── fetch-abi.mjs      # Sourcify → Etherscan ABI
│   └── list-events.mjs    # print event signatures
└── templates/             # Node.js project (s1/s2 only)
```

## Workflow

1. `init-project.sh`
2. User: `chainId` + `contractAddress` (+ optional RPC)
3. `fetch-abi.mjs` → `src/abi/abi_{address}_{chainId}.json`
4. `list-events.mjs` → ask user which events (`*` or names)
5. Edit `contract.ts` → `pnpm s1` → `pnpm s2`

## ABI discovery

JSON-RPC cannot return human ABI. Two paths:

1. **Public fetch** via `fetch-abi.mjs`: Sourcify → Etherscan API v2 (needs `ETHERSCAN_API_KEY` or `--etherscanKey`)
2. **User-provided** (always OK; **required** when public fetch fails): paste ABI JSON or local file path → write `src/abi/abi_{address}_{chainId}.json`

## contract.ts

```typescript
eventNames: '*' | string[]
rpc: string | string[]   // array → retry then failover to next URL
```

- `'*'` → `eth_getLogs` with empty topics (all logs for address)
- `['Transfer']` → topic0 = Transfer hash
- `['A', 'B']` → topic0 OR filter

## Pull behavior (`utils.pull.log.ts`)

- Paginates by `pageSize` (default 1000 blocks)
- Resumes from last `blockNumber` in existing `logs.txt`
- On RPC error: retry same endpoint (`retriesPerRpc`, default 3), then rotate to next URL
- Progress line: `[45.2%] blocks a-b / to | +n logs (total N) | eta~Xm | rpc[i]`

## Output

```
output/{address}_{chainId}/
  logs.txt
  logs.json
```

Parsed:

```typescript
{ txHash, logIndex, blockNumber, eventName, data }
```

## Dependencies (template)

```
ethers decimal.js
dev: tsx typescript @types/node
```
