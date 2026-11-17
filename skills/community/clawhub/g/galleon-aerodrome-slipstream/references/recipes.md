# Slipstream contract recipes

Primary sources checked 2026-09-27. Upstream main can differ from the deployed bytecode; bind an implementation commit/verified explorer source before using version-specific methods.

## Read-only calls

```sh
cast call "$MANAGER" 'ownerOf(uint256)(address)' "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$MANAGER" 'positions(uint256)(uint96,address,address,address,int24,int24,int24,uint128,uint256,uint256,uint128,uint128)' "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$VOTER" 'gauges(address)(address)' "$POOL" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$VOTER" 'isAlive(address)(bool)' "$GAUGE" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$GAUGE" 'stakedContains(address,uint256)(bool)' "$WALLET" "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$GAUGE" 'earned(address,uint256)(uint256)' "$WALLET" "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
```

For each read record block hash, RPC chain ID, target and decoded return. A revert is not a zero stake/reward. `getPool(address,address,int24)` identifies the concentrated pool. Verify gauge NFT manager rather than assuming all managers share IDs.

## Action packet

Return `{chainId, block, manager, tokenId, pool, gauge, depositor, custodian, ticks, action, recipient, expectedRewardRaw, deadline, approval, simulation, postconditions}`. Add penalty source and timestamps only where the deployed version supports them. A withdrawal packet's postconditions include NFT owner returning to depositor and gauge membership clearing. A principal removal also needs decreased liquidity and recipient token deltas.

## Primary sources

- [Aerodrome liquidity documentation](https://github.com/aerodrome-finance/docs/blob/main/content/liquidity.mdx)
- [Slipstream repository and deployments](https://github.com/aerodrome-finance/slipstream)
- [Gauge interface](https://github.com/aerodrome-finance/slipstream/blob/main/contracts/gauge/interfaces/ICLGauge.sol)
- [Gauge implementation](https://github.com/aerodrome-finance/slipstream/blob/main/contracts/gauge/CLGauge.sol)
- [Position manager interface](https://github.com/aerodrome-finance/slipstream/blob/main/contracts/periphery/interfaces/INonfungiblePositionManager.sol)
- [Factory interface](https://github.com/aerodrome-finance/slipstream/blob/main/contracts/core/interfaces/ICLFactory.sol)
