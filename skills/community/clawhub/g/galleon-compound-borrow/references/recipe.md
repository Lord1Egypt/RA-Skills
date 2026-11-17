# Compound III read recipe

With verified deployment inputs and Foundry:

```sh
cast call "$COMET" 'baseToken()(address)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$COMET" 'baseBorrowMin()(uint256)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$COMET" 'balanceOf(address)(uint256)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$COMET" 'borrowBalanceOf(address)(uint256)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$COMET" 'isBorrowCollateralized(address)(bool)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$COMET" 'isLiquidatable(address)(bool)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
```

Verify base token decimals before displaying `baseBorrowMin`; the value is raw base units. AssetInfo collateral factors use 1e18 scale. Query the deployed ABI for structs rather than guessing field layouts from Compound V2 examples.

## Synthetic worked record

A user has 400 base units supplied, no debt and 2,000 common-base collateral value. Borrow factor is 70%, liquidation factor is 80%, and minimum borrow is 1,000 base units. Requested base withdrawal is 1,000: projected debt is 600, below the minimum. Return a blocked plan, not a request to approve 1,400. If the user later requests withdrawing 1,400, debt becomes 1,000, borrow capacity is 1,400 and liquidation capacity is 1,600 before accrual. Under a 30% collateral-price decline, liquidation capacity is 1,120; that narrow margin still needs the user's risk floor, rate horizon and a simulation.

Troubleshooting: `isLiquidatable=false` and `isBorrowCollateralized=false` can both be correct. The position can sit between the two factors; reject a new borrow even though liquidation has not begun.

## Primary sources checked 2026-09-27

- [Collateral and borrowing](https://docs.compound.finance/collateral-and-borrowing/)
- [Helper functions](https://docs.compound.finance/helper-functions/)
- [Comet specification](https://github.com/compound-finance/comet/blob/main/SPEC.md)
- [Deployment configurations](https://github.com/compound-finance/comet/tree/main/deployments)

