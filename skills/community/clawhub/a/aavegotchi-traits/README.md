# Aavegotchi Traits Skill

Fetch Aavegotchi NFT stats on Base by gotchi ID or name.

## Features

- ID lookup via on-chain contract call
- Name lookup via subgraph first, with on-chain fallback
- Trait/BRS/Kinship/XP/level output
- Equipped wearable IDs and names
- Human output + JSON output

## Quick Start

```bash
cd scripts
npm install

# By ID
node get-gotchi.js 9638

# By name
node get-gotchi.js aaigotchi
```

## Environment Variables

- `AAVEGOTCHI_RPC_URL`
  - Optional Base RPC override
  - Default: `https://mainnet.base.org`
- `AAVEGOTCHI_SUBGRAPH_URL`
  - Optional subgraph override
  - Default: public Goldsky Base subgraph
  - Set to empty string to disable subgraph and force on-chain name scan
- `AAVEGOTCHI_SEARCH_BATCH_SIZE`
  - On-chain name scan batch size (default `25`)
- `AAVEGOTCHI_RPC_RETRIES`
  - Retry attempts for rate-limited RPC calls (default `4`)
- `AAVEGOTCHI_RPC_RETRY_DELAY_MS`
  - Base retry delay in ms (default `250`, exponential backoff)

## Notes

- Base chain only (`8453`)
- Name search is case-insensitive
- Partial names via subgraph may return closest match when exact match is unavailable
