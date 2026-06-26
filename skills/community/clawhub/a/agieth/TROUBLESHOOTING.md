# agieth Skill Troubleshooting

## RPC failure mode observed (March 2026)

### Symptom
When sending ETH payments from the skill, `send_raw_transaction` can return a transaction hash, but the hash is not found in subsequent `eth_getTransactionByHash`/receipt lookups. This appears as:

- transaction hash returned immediately
- `TransactionNotFound` or timeout waiting for receipt
- quote remains unpaid even though a hash was produced

### Why this happens
Some public RPC endpoints are good for reads (`eth_getBalance`, `eth_blockNumber`) but can be unreliable for mempool propagation/writes under load or routing issues.

### Implemented behavior
The skill now uses **RPC failover on first failure**:

1. Primary RPC (default): `https://ethereum.publicnode.com`
2. Fallback RPC (default): `https://eth.drpc.org`

If the primary path fails at any point in send flow (nonce, estimate, broadcast, receipt wait), the skill retries once via fallback.

### Return fields
Successful payment calls include:

- `rpc_used` — endpoint that succeeded
- `rpc_failover_used` — `true` when fallback handled the transaction

### Environment overrides
You can override endpoints without code edits:

```bash
ETH_RPC_PRIMARY=https://your-primary-rpc
ETH_RPC_FALLBACK=https://eth.drpc.org
```

### Recommended operators list (current)
Working well from this environment:

- `https://eth.drpc.org`
- `https://eth-mainnet.public.blastapi.io`
- `https://rpc.flashbots.net`
- `https://1rpc.io/eth`

Unreliable here:

- `https://eth.llamarpc.com` (intermittent JSON/read failures)

### Practical guidance
- Keep failover enabled.
- For production-critical writes, prefer authenticated paid RPC providers.
- Log `tx_hash`, `rpc_used`, and `rpc_failover_used` for postmortems.
