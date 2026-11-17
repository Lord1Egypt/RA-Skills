# Connect tools by capability

Use existing harness tools first. The skill pack supplies procedures and portable diagnostics, not a hosted data API, signer, or wallet adapter. Consult the selected tool's current official installation documentation; setup does not silently modify harness settings.

| Capability | Concrete methods or evidence | Needed for |
|---|---|---|
| Chain connectivity | `eth_chainId`, `eth_getBlockByNumber`; correct chain and fresh timestamp | All current chain claims |
| Protocol identity/state | `eth_getCode`, ABI-decoded `eth_call` at a recorded block; official deployment/ABI provenance | Analysis, planning, monitoring |
| Historical data | Bounded `eth_getLogs`, receipts or a documented indexer with coverage/freshness checks | Fee history, cash flows, performance |
| Quotes/construction | Current official SDK or documented unsigned API; exact target, calldata, value, token bounds, expiry | Executable planning |
| Simulation | `eth_call` from actual wallet and exact transaction, gas estimation, decoded effects; sequential dependencies respected | Executable planning and execution |
| User wallet | Current trusted harness wallet tool that exposes chain/account and full transaction terms, keeps keys outside agent context and requires the user's confirmation | Execution only |
| Receipt/reconciliation | `eth_getTransactionReceipt`, finality policy, fresh ownership/balance/allowance reads, durable one-send record | Execution only |

For Uniswap, verify the chain-specific [v3 deployments](https://developers.uniswap.org/docs/protocols/v3/deployments) or [v4 deployments](https://developers.uniswap.org/docs/protocols/v4/deployments) and current SDK documentation. For Aerodrome use the [official contracts repository](https://github.com/aerodrome-finance/contracts) and verify the exact chain, factory, pool and gauge on chain. An address with bytecode is not proof that it is the intended deployment.

A practical first analysis read is: given a user-supplied Uniswap v3 pool, verify factory provenance, then read `token0`, `token1`, `fee`, `tickSpacing`, `slot0`, and `liquidity` with the verified ABI at a recorded block. Read token decimals separately. This establishes pool identity/current state, not profitability. For v4 use its PoolKey/PoolId and the current StateView interface instead of assuming a v3 pool contract.

No RPC endpoint grants signing authority. `eth_call` succeeding alone does not establish acceptable slippage, allowance policy, trusted calldata, or enough gas. If the harness lacks receipt or reconciliation capabilities, execution remains unavailable even if it can send transactions.

The diagnostic implements the [Ethereum JSON-RPC read methods and quantity encoding](https://ethereum.org/developers/docs/apis/json-rpc/), checked 2026-09-05. It does not test `eth_call`, archive access, ABI correctness, balances, quotes, or wallet readiness. Endpoint and network failures are reported without reflecting remote error text or URLs. Default freshness is 180 seconds; change it only for the selected chain's documented behavior and record the choice.
