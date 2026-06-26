# ClawPhunks AgentKit Action

Mint and trade ClawPhunks NFTs with Coinbase AgentKit. x402 payments are handled automatically.

## Install

```bash
npm install @coinbase/agentkit
```

## Usage

```typescript
import { AgentKit } from '@coinbase/agentkit';
import { clawphunksActions } from './clawphunks_action';

const agent = new AgentKit({
  actions: [...clawphunksActions],
  // AgentKit handles x402 USDC payments on Base automatically
});

// Mint a phunk
await agent.execute('clawphunks_mint', {
  recipient: '0x742d35Cc6634C0532925a3b844Bc9e7595f...'
});

// Check collection
await agent.execute('clawphunks_collection', {});
```

## Actions

| Action | Description |
|--------|-------------|
| `clawphunks_mint` | Mint a random phunk ($1.99 USDC on Base) |
| `clawphunks_collection` | Get mint stats and rarity info |
| `clawphunks_skills` | Get full trading scripts for L1 |

## Payment

AgentKit's x402 middleware handles USDC payments on Base automatically. Ensure your agent wallet has sufficient USDC balance.
