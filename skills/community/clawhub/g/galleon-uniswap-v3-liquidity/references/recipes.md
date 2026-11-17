# Uniswap v3 recipes

Checked 2026-09-27. Use the deployed version's ABI, not signatures from another protocol.

## Read-only Foundry examples

Set RPC_URL, BLOCK, MANAGER, FACTORY, POOL and TOKEN_ID from verified inputs. `cast` is optional; equivalent eth_call through an existing provider is sufficient.

```sh
cast call "$MANAGER" 'ownerOf(uint256)(address)' "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$MANAGER" 'positions(uint256)(uint96,address,address,address,uint24,int24,int24,uint128,uint256,uint256,uint128,uint128)' "$TOKEN_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$POOL" 'slot0()(uint160,int24,uint16,uint16,uint16,uint8,bool)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$POOL" 'tickSpacing()(int24)' --rpc-url "$RPC_URL" --block "$BLOCK"
```

Read `getPool(address,address,uint24)(address)` on FACTORY with position tokens and fee. Verify nonzero code and matching tokens/fee on returned pool.

## Unsigned construction fields

- `mint`: token0, token1, fee, tickLower, tickUpper, amount0Desired, amount1Desired, amount0Min, amount1Min, recipient, deadline.
- `increaseLiquidity`: tokenId, amount0Desired, amount1Desired, amount0Min, amount1Min, deadline.
- `decreaseLiquidity`: tokenId, liquidity (uint128 units, not token value), amount0Min, amount1Min, deadline.
- `collect`: tokenId, recipient, amount0Max, amount1Max (uint128). Simulate from owner; reporting maxima is not reporting expected proceeds.
- `burn(uint256)`: optional NFT cleanup, only once liquidity and owed amounts are zero.

Official SDK: `NonfungiblePositionManager.addCallParameters(position, mintOptions)` returns calldata/value; `removeCallParameters(position, removeOptions)` prepares removal. Inspect options against the installed SDK version and decode every multicall before wallet handoff. Never copy the guide's zero minimums into production.

## Primary sources

- [Deployments](https://developers.uniswap.org/deployments)
- [Minting SDK guide](https://developers.uniswap.org/docs/sdks/v3/guides/managing-liquidity/position-minting)
- [Liquidity modification](https://developers.uniswap.org/docs/sdks/v3/guides/managing-liquidity/modifying-position)
- [Fee collection](https://developers.uniswap.org/docs/protocols/v3/guides/managing-liquidity/collect-fees)
- [Position manager interface](https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol)
- [Pool state interface](https://github.com/Uniswap/v3-core/blob/main/contracts/interfaces/pool/IUniswapV3PoolState.sol)
