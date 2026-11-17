# Lido withdrawal read recipe

Use the Ethereum queue address from official deployments and its verified ABI. Foundry commands below require `QUEUE`, `OWNER`, `RPC_URL`, numeric `BLOCK`, and a request array such as `IDS='[101,102]'` derived from the user's receipts:

```sh
cast call "$QUEUE" 'getWithdrawalRequests(address)(uint256[])' "$OWNER" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$QUEUE" 'getWithdrawalStatus(uint256[])((uint256,uint256,address,uint256,bool,bool)[])' "$IDS" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$QUEUE" 'getLastCheckpointIndex()(uint256)' --rpc-url "$RPC_URL" --block "$BLOCK"
```

The status tuple records stETH amount, shares, owner, timestamp, finalized and claimed. When checkpoints exist, find hints for finalized IDs and call `getClaimableEther`. Use the official SDK's withdrawal module if already available; inspect its installed version before assuming a method's input shape.

## Synthetic worked ledger

| Request | Observed state | Action |
| --- | --- | --- |
| 101 | 2 stETH requested, finalized, not claimed, current owner matches, claimable 1.998 ETH | Prepare claim for 1.998 ETH after simulation |
| 102 | 3 stETH requested, not finalized, not claimed | Wait; no claimable ETH or guaranteed completion date |
| 103 | Claimed, NFT no longer exists | Find prior claim receipt; do not resubmit |

A user asking to withdraw the whole 5 stETH has completed only the request stage for 101 and 102. Immediate claimable total in this synthetic record is 1.998 ETH. If 101's NFT has since moved to another account, the original requester cannot claim as owner. Read ownership at the same block as claim simulation.

## Primary sources checked 2026-09-27

- [WithdrawalQueueERC721](https://docs.lido.fi/contracts/withdrawal-queue-erc721/): queue state and call semantics.
- [Token integration guide](https://docs.lido.fi/guides/lido-tokens-integration-guide/): stETH/wstETH and request flow.
- [Lido SDK withdrawal module](https://lidofinance.github.io/lido-ethereum-sdk/modules/withdraw/)
- [Deployed contracts](https://docs.lido.fi/deployed-contracts/)

