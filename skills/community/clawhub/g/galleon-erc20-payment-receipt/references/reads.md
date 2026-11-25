# Collect a receipt

Use the user’s existing trusted read-only EVM RPC or public explorer RPC interface. For Base USDC, confirm the deployed token using [Circle’s contract list](https://developers.circle.com/stablecoins/usdc-contract-addresses). Verify the intended payment separately. A matching ticker can refer to a different deployment.

| Read | Input | Save in evidence JSON |
| --- | --- | --- |
| `eth_chainId` | `[]` | `chainId`, the raw RPC hexadecimal quantity |
| `eth_getTransactionReceipt` | Transaction hash | `receipt`, the full result including logs, or JSON null |
| `eth_getBlockByNumber` | Receipt’s block number and `false` | `canonicalBlock` with `number` and `hash` |
| `eth_getBlockByNumber` | `"finalized"` and `false` | `finalizedBlock` with `number` and `hash`, or null if unsupported |

Stop on the wrong chain or an unavailable receipt. Read each observation from the same chain/provider in one short window. A chain reorganization or mixed provider responses can invalidate the captured header. Report RPC errors, unsupported finality tags and observation time. The meaning of a rollup provider’s finalized tag depends on its chain’s settlement model.

The [example input](../examples/synthetic.json) shows the expected payment instruction and four RPC result fields. Supply JSON-RPC result values, with no surrounding response envelopes. In `expected`, use a numeric chain ID and a decimal string for the base-unit amount. The offline helper validates block/log identity, canonical ABI padding, duplicate indices and amounts with integer arithmetic. It returns a classified JSON result for a valid observation and exits nonzero for invalid input.

For a late invoice, a different payer, split payments or multiple transaction hashes, reconcile all obligations explicitly. Never assign the same transfer log to two invoices. The verifier compares the event evidence within one transaction. `recipient-forwarded-review` means this receipt also shows same-token outflow from the recipient; determining retained value needs further accounting.

## Sources

- [ERC-20](https://eips.ethereum.org/EIPS/eip-20) specifies the indexed sender and recipient and unindexed value in the Transfer event.
- [Ethereum execution APIs](https://github.com/ethereum/execution-apis) define receipt, block and log fields. [Base finality](https://docs.base.org/base-chain/network-information/transaction-finality) describes layer-specific confirmation milestones.
- [viem receipt waiting](https://viem.sh/docs/actions/public/waitForTransactionReceipt) supports confirmation waiting and transaction replacement handling. [Etherscan receipt status](https://docs.etherscan.io/api-reference/endpoint/gettxreceiptstatus) reports execution success or failure. Compare the transfer evidence to the invoice after fetching the receipt.
