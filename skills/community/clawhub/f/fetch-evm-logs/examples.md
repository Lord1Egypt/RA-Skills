# Example: fetch Transfer logs

## 1. Scaffold

```bash
bash ~/.cursor/skills/fetch-evm-logs/scripts/init-project.sh my_logs
cd my_logs
```

## 2. User provides

- `chainId`: `1`
- `contractAddress`: `0xdAC17F958D2ee523a2206206994597C13D831ec7` (USDT)
- RPC: public Ethereum RPC

## 3. Fetch ABI + list events

```bash
node ~/.cursor/skills/fetch-evm-logs/scripts/fetch-abi.mjs \
  --chainId 1 \
  --address 0xdAC17F958D2ee523a2206206994597C13D831ec7 \
  --out ./src/abi

node ~/.cursor/skills/fetch-evm-logs/scripts/list-events.mjs \
  --abi ./src/abi/abi_0xdac17f958d2ee523a2206206994597c13d831ec7_1.json
```

Ask user: e.g. only `Transfer`, or `*`.

## 4. contract.ts

```typescript
export const Contracts = {
  contracts: {
    USDT: {
      address: '0xdAC17F958D2ee523a2206206994597C13D831ec7',
      chainId: 1,
      rpc: [
        'https://eth.llamarpc.com',
        'https://rpc.ankr.com/eth',
      ],
      startBlock: 18_000_000,
      endBlock: 'latest',
      eventNames: ['Transfer'],
      tokenDecimals: 6,
    },
  },
};
```

## 5. Run

```bash
pnpm s1
pnpm s2
```

Output: `output/0xdac17f958d2ee523a2206206994597c13d831ec7_1/logs.json`
