# Morpho evidence worksheet

## Read recipe

Use the ABI matching the deployed Morpho core. These Foundry reads require verified `MORPHO`, `MARKET_ID`, `ACCOUNT`, `RPC_URL`, and numeric `BLOCK` inputs:

```sh
cast call "$MORPHO" 'idToMarketParams(bytes32)(address,address,address,address,uint256)' "$MARKET_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$MORPHO" 'market(bytes32)(uint128,uint128,uint128,uint128,uint128,uint128)' "$MARKET_ID" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$MORPHO" 'position(bytes32,address)(uint256,uint128,uint128)' "$MARKET_ID" "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
```

The position result is supplyShares, borrowShares, collateral. Market totals include lastUpdate and fee. Use maintained Morpho SDK math for accrued conversion; record SDK version. Use indexed APIs for discovery and retain response timestamps; verify the selected position onchain before a write.

For legacy MetaMorpho V1 only, inspect `withdrawQueueLength()` and `withdrawQueue(i)`, then evaluate each returned market. Missing V2 adapter documentation blocks V2 exit preparation, not a read-only summary.

## Synthetic worked record

Market M lends USDC against token C with LLTV 86%. A verified decimal-aware conversion gives collateral value 20,000 USDC and accrued debt 14,000 USDC. LTV is 70%; after a 20% collateral-value decline it is 87.5%, above LLTV. The advertised 4% incentive does not change this liquidation condition. Raw market assets show 1,000,000 supplied and 990,000 borrowed: roughly 10,000 loan units are available before new accrual/actions. A proposed vault exit of 25,000 cannot be promised from that market alone.

Decision record: `M | chain | five parameters | block | oracle composition | debt conversion version | current LTV 70% | stressed LTV 87.5% | exit coverage incomplete`. Next read is remaining allocations/idle balance and vault-specific exit limits, not a deposit approval.

## Primary sources checked 2026-09-27

- [Core contracts and deployments](https://docs.morpho.org/developers/contracts/)
- [Core source and accounting](https://github.com/morpho-org/morpho-blue)
- [Liquidation](https://docs.morpho.org/learn/concepts/liquidation/)
- [Legacy vault queues](https://docs.morpho.org/curate/tutorials-v1/manage-markets/)
- [MetaMorpho source](https://github.com/morpho-org/metamorpho)
- [Maintained API coverage](https://docs.morpho.org/developers/api/morpho/)

